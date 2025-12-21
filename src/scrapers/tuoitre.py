from base import BaseScraper
from typing import Optional, Dict
import logging

logger = logging.getLogger(__name__)

class TuoiTreScraper(BaseScraper):
    BARE_URL = 'https://tuoitre.vn'
    def scrape_article(self, url: str) -> Optional[Dict[str,str]]:
        soup = self.fetch_page(url)
        if not soup:
            return None
        try:
            # Extract title
            title_element = soup.select_one('h1.detail-title.article-title')
            title = title_element.get_text(strip = True) if title_element else None
            if not title:
                logger.warning('no title found')
            
            # Extract date
            date_element = soup.select_one('div.detail-time div[data-role="publishdate"]')
            published_date = date_element.get_text(strip = True) if date_element else None
            if not published_date:
                logger.warning('no date found')

            #Extract content
            content_element = soup.select_one('div.detail-content.afcbc-body')
            paragraphs = content_element.select('p:not(:has(img))')
            content = "\n\n".join(
                p.get_text(strip=True)
                for p in paragraphs
                if p.get_text(strip=True)
            )
            if not content:
                logger.warning(f'no content found at {url}')
                return None

            #Extract author
            author_element = soup.select_one('div.detail-author-bot a.name')
            author = author_element.get_text(strip = True) if author_element else None
            if not author:
                logger.warning(f'no author found at {url}')
                return None
            
            img = soup.select_one('a[data-fancybox="content"] img')
            image_url = img.get('data-original') if img else None
            if not image_url:
                logger.warning(f'no author found at {url}')

            return{
                'title': title,
                'url': url,
                'content': content,
                'published_date': published_date,
                'author': author,
                'image_url': image_url,
            }
        except Exception as e:
            logger.error(f'Error parsing article {url}: {e}')   
            return None
if __name__ == "__main__":
    scraper = TuoiTreScraper()
    test_url = 'https://tuoitre.vn/trung-quoc-co-chip-ai-nhanh-gap-100-lan-chip-manh-nhat-cua-nvidia-202512201438017.htm'
    article = scraper.scrape_article(test_url)
    
    if article:
        print("✅ Tuổi Trẻ scraper works")
        print(f"Title: {article['title']}")