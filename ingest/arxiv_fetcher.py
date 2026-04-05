import requests
import xml.etree.ElementTree as ET

def fetch_arxiv():
    # Fetch latest 10 papers from cs.AI OR cs.LG
    url = 'http://export.arxiv.org/api/query?search_query=cat:cs.AI+OR+cat:cs.LG&sortBy=submittedDate&sortOrder=descending&max_results=10'
    response = requests.get(url)
    if response.status_code != 200:
        print(f"Failed to fetch arXiv API: {response.status_code}")
        return []

    articles = []
    root = ET.fromstring(response.content)
    
    # namespaces in arxiv XML
    ns = {'atom': 'http://www.w3.org/2005/Atom'}
    
    for entry in root.findall('atom:entry', ns):
        title = entry.find('atom:title', ns).text.strip() if entry.find('atom:title', ns) is not None else ''
        summary = entry.find('atom:summary', ns).text.strip() if entry.find('atom:summary', ns) is not None else ''
        link = entry.find('atom:id', ns).text.strip() if entry.find('atom:id', ns) is not None else ''
        published_at = entry.find('atom:published', ns).text.strip() if entry.find('atom:published', ns) is not None else ''
        
        authors = []
        for author in entry.findall('atom:author', ns):
            name = author.find('atom:name', ns).text if author.find('atom:name', ns) is not None else ''
            if name:
                authors.append(name)
        
        # We can either combine summary and authors, or just have authors as string
        authors_str = ", ".join(authors)
        combined_summary = f"Authors: {authors_str}\n\nAbstract: {summary}"

        articles.append({
            'title': title,
            'source': 'arXiv',
            'link': link,
            'summary': combined_summary,
            'published_at': published_at
        })
        
    return articles

if __name__ == "__main__":
    print(fetch_arxiv())
