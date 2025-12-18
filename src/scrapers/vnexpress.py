from base import BaseScraper
from typing import Optional, Dict
import logging

logger = logging.getLogger(__name__)

class VnExpressScraper(BaseScraper):
    BARE_URL = 'https://vnexpress.net'
    def scrape_article(self, url: str) -> Optional[Dict[str, str]]:
        soup = self.fetch_page(url)
        if not soup:
            return None
        try:
            # Extract title
            title_element = soup.select_one('h1.title-detail')
            title = title_element.get_text(strip=True) if title_element else None
            if not title:
                logger.warning(f"No title found for {url}")
                return None
            
            #Extract date
            date_element =  soup.select_one('span.date')
            published_date = date_element.get_text(strip = True) if date_element else None
            if not published_date:
                logger.warning(f'no date found at {url}')
                return None
            
            #Extract content
            content_element = soup.select_one('article.fck_detail ')
            paragraphs = content_element.select('p.Normal')
            content = "\n\n".join(
                p.get_text(strip=True)
                for p in paragraphs
                if p.get_text(strip=True)
            )
            if not content:
                logger.warning(f'no content found at {url}')
                return None
            
            #Extract author
            author_element = soup.select_one('article.fck_detail p.Normal strong')
            author = author_element.get_text(strip = True) if author_element else None
            if not author:
                logger.warning(f'no author found at {url}')
                return None
            
            imgUrl_element = soup.select_one('article.fck_detail img[itemprop="contentUrl"]')
            image_url = imgUrl_element.get_text(strip = True) if imgUrl_element else None
            if not author:
                logger.warning(f'no img url found at {url}')
                return None
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
    scraper = VnExpressScraper()
    test_url = 'https://vnexpress.net/xu-huong-chuyen-dich-moi-cua-internet-viet-nam-4994867.html'
    article = scraper.scrape_article(test_url)
    if article:
        print("Scrape successful")
        print(f"Title: {article['title'][:50]}...")
        print(f"Content length: {len(article['content'])} chars")
    else:
        print("Scrape failed")

            


