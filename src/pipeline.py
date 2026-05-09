import sys
import logging
from pathlib import Path
from typing import List, Optional

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from config.settings import (
    ALL_CATEGORIES, DB_PATH, RAW_DIR,
    MAX_ARTICLES_PER_CATEGORY, LOG_DIR, LOG_FORMAT, LOG_LEVEL,
)
from src.scrapers import ScraperFactory
from src.storage import DataStorage

logger = logging.getLogger(__name__)


def setup_logging():
    LOG_DIR.mkdir(parents=True, exist_ok=True)
    log_file = LOG_DIR / "pipeline.log"
    logging.basicConfig(
        level=getattr(logging, LOG_LEVEL),
        format=LOG_FORMAT,
        handlers=[
            logging.StreamHandler(),
            logging.FileHandler(log_file, encoding="utf-8"),
        ],
    )


def run_pipeline(sources=None, max_articles=MAX_ARTICLES_PER_CATEGORY, save_csv=True):
    """Chay pipeline scraping cho cac nguon va danh muc duoc chi dinh"""
    storage = DataStorage(db_path=DB_PATH, raw_dir=RAW_DIR)
    all_articles = []

    active_sources = sources or list(ALL_CATEGORIES.keys())

    for source in active_sources:
        if source not in ALL_CATEGORIES:
            logger.warning(f"Nguon khong ho tro: {source}")
            continue

        scraper = ScraperFactory.get_scraper(source)
        categories = ALL_CATEGORIES[source]

        for cat_name, cat_url in categories.items():
            logger.info(f"Dang scrape: [{source}] {cat_name}")

            articles = scraper.scrape_category(
                category_url=cat_url,
                max_articles=max_articles,
                category_name=cat_name,
            )
            logger.info(f"Duoc {len(articles)} bai tu {cat_name}")
            all_articles.extend(articles)

    if not all_articles:
        logger.warning("Khong scrape duoc bai nao!")
        return []

    # bo trung theo URL
    seen = set()
    unique = []
    for a in all_articles:
        if a["url"] not in seen:
            seen.add(a["url"])
            unique.append(a)
    logger.info(f"Tong bai (sau khi bo trung): {len(unique)}/{len(all_articles)}")

    # luu database
    storage.save_to_sqlite(unique)

    # luu CSV
    if save_csv and unique:
        storage.save_to_csv(unique)

    # in thong ke
    stats = storage.get_stats()
    print(f"\nThong ke database:")
    print(f"  Tong bai:   {stats['total_articles']}")
    print(f"  Tac gia:    {stats['total_authors']}")
    print(f"  Theo nguon: {stats['by_source']}")

    return unique
