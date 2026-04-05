import feedparser
import requests

FEEDS = [
    {"name": "r/artificial", "url": "https://www.reddit.com/r/artificial/.rss?limit=10"},
    {"name": "r/MachineLearning", "url": "https://www.reddit.com/r/MachineLearning/.rss?limit=10"},
    {"name": "r/singularity", "url": "https://www.reddit.com/r/singularity/.rss?limit=10"}
]

def fetch_reddit():
    articles = []
    
    headers = {
        'User-Agent': 'EarlySignalEngine/1.0 (Python RSS Fetcher)'
    }
    
    for feed_info in FEEDS:
        # We use requests here to pass a custom User-Agent because reddit blocks default urllib agents.
        try:
            response = requests.get(feed_info["url"], headers=headers, timeout=10)
            response.raise_for_status()
            feed = feedparser.parse(response.content)
            
            for entry in feed.entries:
                title = entry.get('title', '')
                link = entry.get('link', '')
                published_at = entry.get('updated', entry.get('published', ''))
                summary = ""
                
                articles.append({
                    'title': title,
                    'source': feed_info['name'],
                    'link': link,
                    'summary': summary,
                    'published_at': published_at
                })
        except requests.exceptions.RequestException as e:
            print(f"Failed to fetch {feed_info['name']}: {e}")
            
    return articles
