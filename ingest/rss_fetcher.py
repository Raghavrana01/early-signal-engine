import feedparser

FEEDS = [
    {"name": "TechCrunch AI", "url": "https://techcrunch.com/category/artificial-intelligence/feed/"},
    {"name": "MIT Tech Review AI", "url": "https://www.technologyreview.com/feed/"},
    {"name": "The Verge AI", "url": "https://www.theverge.com/ai-artificial-intelligence/rss/index.xml"},
    {"name": "Ars Technica AI", "url": "https://feeds.arstechnica.com/arstechnica/technology-lab"}
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
