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
    c.execute('''
        CREATE TABLE IF NOT EXISTS brief_scores (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            high_count INTEGER NOT NULL,
            medium_count INTEGER NOT NULL,
            filtered_count INTEGER NOT NULL,
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

def delete_old_articles(days=30):
    conn = get_connection()
    c = conn.cursor()
    c.execute(f"DELETE FROM articles WHERE datetime(created_at) < datetime('now', '-{days} days')")
    conn.commit()
    conn.close()

def save_brief_score(high_count, medium_count, filtered_count):
    conn = get_connection()
    c = conn.cursor()
    c.execute('''
        INSERT INTO brief_scores (high_count, medium_count, filtered_count, created_at)
        VALUES (?, ?, ?, ?)
    ''', (high_count, medium_count, filtered_count, datetime.now().isoformat()))
    conn.commit()
    conn.close()

def get_avg_scores():
    conn = get_connection()
    c = conn.cursor()
    c.execute('SELECT AVG(high_count), AVG(medium_count), AVG(filtered_count) FROM brief_scores')
    row = c.fetchone()
    conn.close()
    if row and row[0] is not None:
        return {'high': round(row[0], 1), 'medium': round(row[1], 1), 'filtered': round(row[2], 1)}
    return {'high': 0, 'medium': 0, 'filtered': 0}

def get_recent_macro_trends(days=7):
    conn = get_connection()
    c = conn.cursor()
    c.execute(f"SELECT trend, created_at FROM macro_trends WHERE datetime(created_at) >= datetime('now', '-{days} days') ORDER BY created_at DESC")
    rows = c.fetchall()
    conn.close()
    return [{"trend": row[0], "created_at": row[1]} for row in rows]
