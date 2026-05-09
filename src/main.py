import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.pipeline import setup_logging, run_pipeline
from src.storage import DataStorage
from config.settings import DB_PATH, RAW_DIR


def cmd_scrape(args):
    print(f"Bat dau scrape: nguon={args.sources}, max={args.max}")
    articles = run_pipeline(
        sources=args.sources,
        max_articles=args.max,
        save_csv=not args.no_csv,
    )
    print(f"Hoan thanh! Scrape duoc {len(articles)} bai.")


def cmd_stats(args):
    storage = DataStorage(db_path=DB_PATH, raw_dir=RAW_DIR)
    stats = storage.get_stats()
    print(f"\nThong ke database:")
    print(f"  Tong bai viet: {stats['total_articles']}")
    print(f"  Tong tac gia:  {stats['total_authors']}")
    print(f"  Theo nguon:")
    for src, cnt in stats["by_source"].items():
        print(f"    {src}: {cnt} bai")
    print(f"  Theo danh muc:")
    for cat, cnt in sorted(stats["by_category"].items(), key=lambda x: -x[1]):
        print(f"    {cat}: {cnt} bai")


def main():
    parser = argparse.ArgumentParser(description="Tech News Scraper CLI")
    subparsers = parser.add_subparsers(dest="command")
    subparsers.required = True

    # scrape command
    p_scrape = subparsers.add_parser("scrape", help="Thu thap bai viet")
    p_scrape.add_argument("--sources", nargs="+", default=["vnexpress", "tuoitre"],
                          choices=["vnexpress", "tuoitre"])
    p_scrape.add_argument("--max", type=int, default=20,
                          help="So bai toi da moi danh muc")
    p_scrape.add_argument("--no-csv", action="store_true")
    p_scrape.set_defaults(func=cmd_scrape)

    # stats command
    p_stats = subparsers.add_parser("stats", help="Xem thong ke database")
    p_stats.set_defaults(func=cmd_stats)

    args = parser.parse_args()
    setup_logging()
    args.func(args)


if __name__ == "__main__":
    main()
