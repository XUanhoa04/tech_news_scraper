import time
import logging
import requests
from bs4 import BeautifulSoup
from typing import Optional

logger = logging.getLogger(__name__)


class BaseScraper:
    def __init__(self, timeout=10, delay=0.5):
        self.timeout = timeout
        self.delay = delay
        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        })

    def fetch_page(self, url: str) -> Optional[BeautifulSoup]:
        """Tai va parse HTML cua mot trang web"""
        try:
            time.sleep(self.delay)  # tranh bi block
            response = self.session.get(url, timeout=self.timeout)
            response.raise_for_status()
            return BeautifulSoup(response.content, "html.parser")
        except requests.Timeout:
            logger.warning(f"Timeout khi tai: {url}")
            return None
        except requests.HTTPError as e:
            logger.warning(f"HTTP error {e.response.status_code}: {url}")
            return None
        except requests.RequestException as e:
            logger.warning(f"Request error: {url} - {e}")
            return None
