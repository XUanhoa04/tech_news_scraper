import sys
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from src.scrapers.vnexpress import VnExpressScraper
from src.scrapers.tuoitre import TuoiTreScraper
from bs4 import BeautifulSoup


# HTML mau de test, khong can internet
VNEXPRESS_HTML = """
<html>
<body>
  <h1 class="title-detail">Tri tue nhan tao thay doi the gioi</h1>
  <span class="date">Thu Hai, 1/4/2026, 08:00</span>
  <article class="fck_detail">
    <p class="Normal">Noi dung doan 1 ve AI.</p>
    <p class="Normal">Noi dung doan 2 ve ung dung.</p>
    <p class="Normal"><strong>Nguyen Van A</strong></p>
  </article>
  <meta property="og:image" content="https://example.com/img.jpg"/>
</body>
</html>
"""

TUOITRE_HTML = """
<html>
<body>
  <h1 class="detail-title">Cong nghe blockchain tai Viet Nam</h1>
  <div class="detail-time">
    <span data-role="publishdate">01/04/2026 09:00</span>
  </div>
  <div class="detail-content afcbc-body">
    <p>Noi dung chinh cua bai viet.</p>
    <p>Doan 2 chi tiet hon.</p>
  </div>
  <div class="detail-author-bot">
    <a class="name">Tran Thi B</a>
  </div>
</body>
</html>
"""


def make_soup(html):
    return BeautifulSoup(html, "html.parser")


class TestVnExpressScraper:
    def setup_method(self):
        self.scraper = VnExpressScraper()

    def test_scrape_article_ok(self):
        soup = make_soup(VNEXPRESS_HTML)
        with patch.object(self.scraper, "fetch_page", return_value=soup):
            result = self.scraper.scrape_article("https://vnexpress.net/test")
        assert result is not None
        assert result["title"] == "Tri tue nhan tao thay doi the gioi"
        assert "AI" in result["content"]

    def test_scrape_article_no_content(self):
        html = "<html><body><h1 class='title-detail'>Tieu de</h1></body></html>"
        with patch.object(self.scraper, "fetch_page", return_value=make_soup(html)):
            result = self.scraper.scrape_article("https://vnexpress.net/test")
        assert result is None

    def test_scrape_article_fetch_fail(self):
        with patch.object(self.scraper, "fetch_page", return_value=None):
            result = self.scraper.scrape_article("https://vnexpress.net/test")
        assert result is None

    def test_scrape_category_empty(self):
        with patch.object(self.scraper, "fetch_page", return_value=None):
            result = self.scraper.scrape_category("https://vnexpress.net/khoa-hoc")
        assert result == []


class TestTuoiTreScraper:
    def setup_method(self):
        self.scraper = TuoiTreScraper()

    def test_scrape_article_ok(self):
        soup = make_soup(TUOITRE_HTML)
        with patch.object(self.scraper, "fetch_page", return_value=soup):
            result = self.scraper.scrape_article("https://tuoitre.vn/test")
        assert result is not None
        assert result["title"] == "Cong nghe blockchain tai Viet Nam"
        assert result["author"] == "Tran Thi B"

    def test_scrape_article_no_title(self):
        html = "<html><body><p>khong co tieu de</p></body></html>"
        with patch.object(self.scraper, "fetch_page", return_value=make_soup(html)):
            result = self.scraper.scrape_article("https://tuoitre.vn/test")
        assert result is None

    def test_scrape_article_fetch_fail(self):
        with patch.object(self.scraper, "fetch_page", return_value=None):
            result = self.scraper.scrape_article("https://tuoitre.vn/test")
        assert result is None
