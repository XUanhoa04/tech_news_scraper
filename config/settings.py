import os
from pathlib import Path

# thu muc goc du an
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
RAW_DIR = DATA_DIR / "raw"
LOG_DIR = BASE_DIR / "logs"
DB_PATH = DATA_DIR / "tech_news.db"

# tao thu muc neu chua co
for d in [DATA_DIR, RAW_DIR, LOG_DIR]:
    d.mkdir(parents=True, exist_ok=True)

# so bai toi da moi danh muc
MAX_ARTICLES_PER_CATEGORY = 20
REQUEST_TIMEOUT = 10
REQUEST_DELAY = 0.5

# danh muc VnExpress
VNEXPRESS_CATEGORIES = {
    "khoa-hoc": "https://vnexpress.net/khoa-hoc",
    "so-hoa": "https://vnexpress.net/so-hoa",
    "kinh-doanh": "https://vnexpress.net/kinh-doanh",
    "the-gioi": "https://vnexpress.net/the-gioi",
}

# danh muc Tuoi Tre
TUOITRE_CATEGORIES = {
    "cong-nghe": "https://tuoitre.vn/khoa-hoc-cong-nghe.htm",
    "kinh-te": "https://tuoitre.vn/kinh-te.htm",
    "the-gioi": "https://tuoitre.vn/the-gioi.htm",
    "nhip-song-so": "https://tuoitre.vn/nhip-song-so.htm",
}

ALL_CATEGORIES = {
    "vnexpress": VNEXPRESS_CATEGORIES,
    "tuoitre": TUOITRE_CATEGORIES,
}

# logging
LOG_FORMAT = "%(asctime)s | %(levelname)-8s | %(name)s | %(message)s"
LOG_LEVEL = "INFO"
