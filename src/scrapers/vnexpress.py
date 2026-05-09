import logging
from typing import Optional, Dict, List
from .base import BaseScraper

logger = logging.getLogger(__name__)


class VnExpressScraper(BaseScraper):
    BASE_URL = "https://vnexpress.net"

    def scrape_category(self, category_url: str, max_articles=20, category_name=""):
        """Lay danh sach bai viet tu trang chuyen muc"""
        soup = self.fetch_page(category_url)
        if not soup:
            return []

        articles = []
        seen_urls = set()

        # thu nhieu selector vi vnexpress co nhieu layout khac nhau
        for sel in ["article.item-news h3.title-news a", "h3.title-news a"]:
            links = soup.select(sel)
            if links:
                break
        else:
            links = []

        logger.info(f"VnExpress [{category_name}]: tim thay {len(links)} links")

        for link in links[:max_articles]:
            url = link.get("href", "")
            if not url.startswith("http"):
                url = self.BASE_URL + url
            if url in seen_urls:
                continue
            seen_urls.add(url)

            article = self.scrape_article(url)
            if article:
                article["category"] = category_name
                article["source"] = "vnexpress"
                articles.append(article)
                logger.info(f"  OK: {article['title'][:60]}")

        return articles

    def scrape_article(self, url: str) -> Optional[Dict[str, str]]:
        """Scrape noi dung mot bai viet VnExpress"""
        soup = self.fetch_page(url)
        if not soup:
            return None

        try:
            # tieu de
            title_el = soup.select_one("h1.title-detail")
            title = title_el.get_text(strip=True) if title_el else None
            if not title:
                return None

            # ngay dang
            date_el = soup.select_one("span.date")
            published_date = date_el.get_text(strip=True) if date_el else ""

            # noi dung
            content_el = soup.select_one("article.fck_detail")
            if content_el:
                paragraphs = content_el.select("p.Normal")
                content = "\n\n".join(
                    p.get_text(strip=True) for p in paragraphs if p.get_text(strip=True)
                )
            else:
                content = None
            if not content:
                return None

            # tac gia
            author_el = soup.select_one("article.fck_detail p.Normal strong")
            author = author_el.get_text(strip=True) if author_el else "Khong ro"

            # anh dai dien
            img_el = soup.select_one("article.fck_detail img[itemprop='contentUrl']")
            if img_el:
                image_url = img_el.get("src") or img_el.get("data-src") or ""
            else:
                og = soup.select_one("meta[property='og:image']")
                image_url = og.get("content") if og else ""

            return {
                "title": title,
                "url": url,
                "content": content,
                "published_date": published_date,
                "author": author,
                "image_url": image_url or "",
            }

        except Exception as e:
            logger.error(f"Loi parse bai {url}: {e}")
            return None
