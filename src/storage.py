import csv
import sqlite3
import logging
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Optional

import pandas as pd

logger = logging.getLogger(__name__)

CREATE_TABLE_SQL = """
CREATE TABLE IF NOT EXISTS articles (
    id            INTEGER PRIMARY KEY AUTOINCREMENT,
    title         TEXT NOT NULL,
    url           TEXT UNIQUE NOT NULL,
    content       TEXT,
    published_date TEXT,
    author        TEXT,
    image_url     TEXT,
    source        TEXT,
    category      TEXT,
    scraped_at    TEXT,
    word_count    INTEGER
);
"""

FIELDNAMES = [
    "title", "url", "content", "published_date",
    "author", "image_url", "source", "category", "scraped_at", "word_count",
]


class DataStorage:
    def __init__(self, db_path, raw_dir):
        self.db_path = Path(db_path)
        self.raw_dir = Path(raw_dir)
        self.raw_dir.mkdir(parents=True, exist_ok=True)
        self._init_db()

    def _init_db(self):
        with sqlite3.connect(self.db_path) as conn:
            conn.execute(CREATE_TABLE_SQL)
            conn.commit()

    def _enrich(self, article):
        """Them metadata truoc khi luu"""
        a = dict(article)
        a.setdefault("scraped_at", datetime.now().isoformat(timespec="seconds"))
        a["word_count"] = len(a.get("content", "").split())
        return a

    def save_to_sqlite(self, articles):
        """Luu vao SQLite, bo qua URL trung. Tra ve so bai them moi."""
        if not articles:
            return 0
        inserted = 0
        sql = """
            INSERT OR IGNORE INTO articles
                (title, url, content, published_date, author, image_url,
                 source, category, scraped_at, word_count)
            VALUES
                (:title, :url, :content, :published_date, :author, :image_url,
                 :source, :category, :scraped_at, :word_count)
        """
        with sqlite3.connect(self.db_path) as conn:
            for a in articles:
                row = self._enrich(a)
                cursor = conn.execute(sql, row)
                inserted += cursor.rowcount
            conn.commit()
        logger.info(f"SQLite: them {inserted}/{len(articles)} bai moi")
        return inserted

    def load_from_sqlite(self, where=""):
        """Doc du lieu tu database, tra ve DataFrame"""
        query = "SELECT * FROM articles"
        if where:
            query += f" WHERE {where}"
        query += " ORDER BY scraped_at DESC"
        with sqlite3.connect(self.db_path) as conn:
            df = pd.read_sql_query(query, conn)
        return df

    def get_stats(self):
        """Tra ve thong ke tong hop"""
        with sqlite3.connect(self.db_path) as conn:
            total = conn.execute("SELECT COUNT(*) FROM articles").fetchone()[0]
            sources = conn.execute("SELECT source, COUNT(*) FROM articles GROUP BY source").fetchall()
            cats = conn.execute("SELECT category, COUNT(*) FROM articles GROUP BY category").fetchall()
            authors = conn.execute("SELECT COUNT(DISTINCT author) FROM articles").fetchone()[0]
        return {
            "total_articles": total,
            "total_authors": authors,
            "by_source": dict(sources),
            "by_category": dict(cats),
        }

    def save_to_csv(self, articles, filename=None):
        """Luu ra file CSV"""
        if not filename:
            ts = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"articles_{ts}.csv"
        path = self.raw_dir / filename
        enriched = [self._enrich(a) for a in articles]
        with open(path, "w", newline="", encoding="utf-8-sig") as f:
            writer = csv.DictWriter(f, fieldnames=FIELDNAMES, extrasaction="ignore")
            writer.writeheader()
            writer.writerows(enriched)
        logger.info(f"CSV: da luu {len(enriched)} bai -> {path}")
        return path
