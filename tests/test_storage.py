import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from src.storage import DataStorage

SAMPLE_ARTICLES = [
    {
        "title": "AI thay doi cong nghiep 2025",
        "url": "https://vnexpress.net/ai-2025",
        "content": "Tri tue nhan tao dang thay doi nhieu nganh cong nghiep.",
        "published_date": "01/04/2026",
        "author": "Nguyen Van A",
        "image_url": "",
        "source": "vnexpress",
        "category": "khoa-hoc",
    },
    {
        "title": "Blockchain trong tai chinh",
        "url": "https://tuoitre.vn/blockchain",
        "content": "Cong nghe blockchain dang duoc ap dung trong linh vuc tai chinh.",
        "published_date": "02/04/2026",
        "author": "Tran Thi B",
        "image_url": "",
        "source": "tuoitre",
        "category": "cong-nghe",
    },
]


def make_storage():
    tmp_db = tempfile.NamedTemporaryFile(suffix=".db", delete=False)
    tmp_dir = Path(tempfile.mkdtemp())
    return DataStorage(db_path=tmp_db.name, raw_dir=tmp_dir)


class TestDataStorage:
    def test_save_and_load(self):
        storage = make_storage()
        inserted = storage.save_to_sqlite(SAMPLE_ARTICLES)
        assert inserted == 2
        df = storage.load_from_sqlite()
        assert len(df) == 2

    def test_dedup_url(self):
        storage = make_storage()
        storage.save_to_sqlite(SAMPLE_ARTICLES)
        again = storage.save_to_sqlite(SAMPLE_ARTICLES)
        assert again == 0  # khong them trung
        df = storage.load_from_sqlite()
        assert len(df) == 2

    def test_word_count(self):
        storage = make_storage()
        storage.save_to_sqlite(SAMPLE_ARTICLES[:1])
        df = storage.load_from_sqlite()
        assert df["word_count"].iloc[0] > 0

    def test_csv(self):
        storage = make_storage()
        path = storage.save_to_csv(SAMPLE_ARTICLES, filename="test.csv")
        assert path.exists()

    def test_stats(self):
        storage = make_storage()
        storage.save_to_sqlite(SAMPLE_ARTICLES)
        stats = storage.get_stats()
        assert stats["total_articles"] == 2

    def test_empty_stats(self):
        storage = make_storage()
        stats = storage.get_stats()
        assert stats["total_articles"] == 0
