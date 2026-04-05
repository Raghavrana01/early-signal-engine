import sqlite3
import os
from datetime import datetime

DB_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'signals.db')

def get_connection():
    return sqlite3.connect(DB_PATH)

def init_db():
    conn = get_connection()
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS articles (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            source TEXT NOT NULL,
            link TEXT NOT NULL UNIQUE,
            summary TEXT,
            published_at TEXT,
            created_at TEXT NOT NULL
        )
    ''')
    c.execute('''
        CREATE TABLE IF NOT EXISTS macro_trends (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            trend TEXT NOT NULL,
            created_at TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

def insert_article(title, source, link, summary, published_at):
    conn = get_connection()
    c = conn.cursor()
    try:
        c.execute('''
            INSERT INTO articles (title, source, link, summary, published_at, created_at)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (title, source, link, summary, published_at, datetime.now().isoformat()))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        # Deduplication based on UNIQUE link constraint
        return False
    finally:
        conn.close()

def get_all_articles_grouped_by_source():
    conn = get_connection()
    c = conn.cursor()
    c.execute('SELECT source, title, link, summary, published_at FROM articles ORDER BY source')
    rows = c.fetchall()
    conn.close()
    
    grouped = {}
    for row in rows:
        source, title, link, summary, published_at = row
        if source not in grouped:
            grouped[source] = []
        grouped[source].append({
            'title': title,
            'link': link,
            'summary': summary,
            'published_at': published_at
        })
    return grouped

def get_recent_articles(limit=20):
    conn = get_connection()
    c = conn.cursor()
    c.execute('SELECT source, title, link, summary, published_at FROM articles ORDER BY created_at DESC LIMIT ?', (limit,))
    rows = c.fetchall()
    conn.close()
    
    articles = []
    for row in rows:
        source, title, link, summary, published_at = row
        articles.append({
            'source': source,
            'title': title,
            'link': link,
            'summary': summary,
            'published_at': published_at
        })
    return articles

def save_macro_trend(trend_text):
    if not trend_text:
        return
    conn = get_connection()
    c = conn.cursor()
    c.execute('''
        INSERT INTO macro_trends (trend, created_at)
        VALUES (?, ?)
    ''', (trend_text, datetime.now().isoformat()))
    conn.commit()
    conn.close()

def get_last_macro_trend():
    conn = get_connection()
    c = conn.cursor()
    c.execute('SELECT trend FROM macro_trends ORDER BY created_at DESC LIMIT 1')
    row = c.fetchone()
    conn.close()
    return row[0] if row else None
