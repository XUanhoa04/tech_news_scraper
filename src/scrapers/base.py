import requests
from bs4 import BeautifulSoup
from typing import Optional
import logging

class BaseScraper:
    def __init__(self, timeout: int = 10):
        self.timeout = timeout
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }

    def fetch_page(self, url: str) -> Optional[BeautifulSoup]:
        try:
            response = requests.get(url,headers= self.headers, timeout=self.timeout)
            if response.status_code != 200:
                print(f'Failed to fetch {url}, status code : {response.status_code}')
                return None
            soup = BeautifulSoup(response.content, 'html.parser')
            return soup
        except requests.Timeout:
            logging.warning(f'timeout when fetching {url}')
            return None
        except requests.RequestException as e:
            logging.warning(f'error when fetching {url}: {e}')
            return None
        except Exception as e:
            logging.warning(f'error when fetching {url}: {e}')
            return None

if __name__ == "__main__":
    scraper = BaseScraper()
    soup = scraper.fetch_page('https://vnexpress.net/khoa-hoc')
    
    if(soup):
        print("fetch successfull")
        print(f"Title tag: {soup.title.text if soup.title else 'No title'}")
    else:
        print("Fetch failed")
    


    
