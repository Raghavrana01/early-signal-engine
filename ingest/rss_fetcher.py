import feedparser

FEEDS = [
    {"name": "TechCrunch AI", "url": "https://techcrunch.com/category/artificial-intelligence/feed/"},
    {"name": "MIT Tech Review AI", "url": "https://www.technologyreview.com/feed/"},
    {"name": "The Verge AI", "url": "https://www.theverge.com/ai-artificial-intelligence/rss/index.xml"},
    {"name": "Ars Technica AI", "url": "https://feeds.arstechnica.com/arstechnica/technology-lab"},
    {"name": "Wired AI", "url": "https://www.wired.com/feed/tag/ai/latest/rss"},
    {"name": "VentureBeat AI", "url": "https://venturebeat.com/category/ai/feed/"},
    {"name": "Hacker News", "url": "https://news.ycombinator.com/rss"},
    {"name": "r/LocalLLaMA", "url": "https://www.reddit.com/r/LocalLLaMA/.rss"},
    {"name": "Import AI", "url": "https://jack-clark.net/feed"},
    {"name": "The Batch", "url": "https://www.deeplearning.ai/the-batch/rss"},
    {"name": "LessWrong", "url": "https://www.lesswrong.com/feed.xml"},
    {"name": "Bloomberg Technology", "url": "https://feeds.bloomberg.com/technology/news.rss"},
    {"name": "Reuters Technology", "url": "https://feeds.reuters.com/reuters/technologyNews"},
    {"name": "r/investing", "url": "https://www.reddit.com/r/investing/.rss"},
    {"name": "r/stocks", "url": "https://www.reddit.com/r/stocks/.rss"},
    {"name": "GitHub Trending", "url": "https://mshibanami.github.io/GitHubTrendingRSS/daily/all.xml"}
]

def fetch_rss():
    articles = []
    for feed_info in FEEDS:
        feed = feedparser.parse(feed_info["url"])
        for entry in feed.entries:
            title = entry.get('title', '')
            link = entry.get('link', '')
            published_at = entry.get('published', '')
            # Optional: handle different time formats if needed, using raw string for now
            
            summary = entry.get('summary', '')
            
            articles.append({
                'title': title,
                'source': feed_info['name'],
                'link': link,
                'summary': summary,
                'published_at': published_at
            })
    return articles
