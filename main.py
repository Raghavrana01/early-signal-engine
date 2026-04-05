from dotenv import load_dotenv
import os
load_dotenv()
DISCORD_WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK_URL")


from storage.db import init_db, insert_article, get_all_articles_grouped_by_source
from ingest.rss_fetcher import fetch_rss
from ingest.arxiv_fetcher import fetch_arxiv
from ingest.reddit_fetcher import fetch_reddit
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime
import time
from notify.discord_notifier import send_digest, send_test_message

def run_pipeline():
    print(f"\n[{datetime.now().isoformat()}] Starting pipeline run...")
    print("Initializing database...")
    init_db()
    
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
    
    if new_articles:
        print("Sending digest to Discord...")
        send_digest(DISCORD_WEBHOOK_URL, new_articles)
    
    print("\n================== ALL SIGNALS ==================\n")
    grouped = get_all_articles_grouped_by_source()
    for source, articles in grouped.items():
        print(f"=== {source} ({len(articles)} articles) ===")
        for article in articles:
            print(f"- {article['title']}")
            print(f"  Link: {article['link']}")
            if article['published_at']:
                print(f"  Published: {article['published_at']}")
            print()
        print("-" * 50)
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
