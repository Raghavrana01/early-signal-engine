from dotenv import load_dotenv
import os
load_dotenv()
DISCORD_WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK_URL")


from storage.db import init_db, insert_article, get_all_articles_grouped_by_source, get_recent_articles, save_macro_trend, delete_old_articles, save_brief_score
from ingest.rss_fetcher import fetch_rss
from ingest.arxiv_fetcher import fetch_arxiv
from ingest.reddit_fetcher import fetch_reddit
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime
import time
import json
from notify.discord_notifier import send_test_message, send_brief
from analysis.summarizer import run_summarizer

WATCHLIST = ["AGI", "ASI", "Anthropic", "acquisition", "raises", "jailbreak", "agent", "shutdown", "leaked", "regulation", "breach", "open weights", "fine-tune"]

def run_pipeline():
    print(f"\n[{datetime.now().isoformat()}] Starting pipeline run...")
    print("Initializing database...")
    init_db()
    
    print("Cleaning up old articles...")
    delete_old_articles(days=30)
    
    print("Fetching from RSS feeds...")
    rss_articles = fetch_rss()
    new_articles = []
    
    for article in rss_articles:
        if insert_article(article['title'], article['source'], article['link'], article['summary'], article['published_at']):
            new_articles.append(article)
    
    print(f"Inserted {len(new_articles)} new RSS articles.")
    
    print("Fetching from arXiv...")
    arxiv_articles = fetch_arxiv()
    arxiv_inserted = 0
    for article in arxiv_articles:
        if insert_article(article['title'], article['source'], article['link'], article['summary'], article['published_at']):
            new_articles.append(article)
            arxiv_inserted += 1
            
    print(f"Inserted {arxiv_inserted} new arXiv articles.")
    
    print("Fetching from Reddit...")
    reddit_articles = fetch_reddit()
    reddit_inserted = 0
    for article in reddit_articles:
        if insert_article(article['title'], article['source'], article['link'], article['summary'], article['published_at']):
            new_articles.append(article)
            reddit_inserted += 1
            
    print(f"Inserted {reddit_inserted} new Reddit articles.")
    
    keyword_stats = {}
    for keyword in WATCHLIST:
        keyword_stats[keyword] = {'article_count': 0, 'sources': set()}
        
    alert_lines = []
    for article in new_articles:
        title = article['title']
        source = article['source']
        title_lower = title.lower()
        matched_keywords = []
        for keyword in WATCHLIST:
            if keyword.lower() in title_lower:
                matched_keywords.append(keyword)
                keyword_stats[keyword]['article_count'] += 1
                keyword_stats[keyword]['sources'].add(source)
                
        if matched_keywords:
            alert_lines.append(f'🔑 {json.dumps(matched_keywords)} — {title}')
            
    trending_lines = []
    for keyword, stats in keyword_stats.items():
        if stats['article_count'] >= 3 and len(stats['sources']) >= 2:
            trending_lines.append(f'🔥 "{keyword}" — mentioned in {stats["article_count"]} articles across {len(stats["sources"])} sources')
                
    if alert_lines:
        print("Sending WATCHLIST alerts to Discord...")
        alert_msg = "🚨 WATCHLIST ALERTS\n\n" + "\n".join(alert_lines)
        send_brief(DISCORD_WEBHOOK_URL, alert_msg)
        
    recent_articles = get_recent_articles(limit=20)
    if recent_articles:
        print("Running AI logic pipeline on the last 20 articles...")
        brief, macro_trend, counts = run_summarizer(recent_articles)
        if brief:
            if trending_lines:
                trend_header = "🔥 TRENDING ACROSS SOURCES\n\n" + "\n".join(trending_lines) + "\n\n"
                brief = trend_header + brief
                
            print("Sending AI brief to Discord...")
            send_brief(DISCORD_WEBHOOK_URL, brief)
            if macro_trend:
                save_macro_trend(macro_trend)
                print("Saved macro trend.")
            if counts:
                save_brief_score(counts['high'], counts['medium'], counts['filtered'])
                print("Saved brief scoring breakdown.")
        else:
            print("Summarizer returned empty. Not sending brief.")
            
    print(f"[{datetime.now().isoformat()}] Pipeline run complete.\n")

def main():
    print("Starting Early Signal Engine Scheduler...")
    
    # Send test message
    send_test_message(DISCORD_WEBHOOK_URL)
    
    # Run once immediately on startup
    run_pipeline()
    
    # Setup background scheduler
    scheduler = BackgroundScheduler()
    scheduler.add_job(run_pipeline, 'interval', hours=3)
    
    try:
        from notify.email_digest import send_weekly_digest
        scheduler.add_job(send_weekly_digest, 'cron', day_of_week='sun', hour=9)
    except Exception as e:
        print(f"Failed to setup weekly email digest job: {e}")
        
    print(f"\n[{datetime.now().isoformat()}] Scheduler started. Pipeline will run every 3 hours. Press Ctrl+C to exit.")
    scheduler.start()
    
    try:
        while True:
            time.sleep(1)
    except (KeyboardInterrupt, SystemExit):
        scheduler.shutdown()
        print("\nScheduler stopped.")

if __name__ == "__main__":
    main()
