from .vnexpress import VnExpressScraper
from .tuoitre import TuoiTreScraper


class ScraperFactory:
    _scrapers = {
        "vnexpress": VnExpressScraper,
        "tuoitre": TuoiTreScraper,
    }

    @classmethod
    def get_scraper(cls, source: str):
        scraper_class = cls._scrapers.get(source.lower())
        if not scraper_class:
            raise ValueError(f"Nguon khong ho tro: {source}")
        return scraper_class()

    @classmethod
    def get_all_sources(cls):
        return list(cls._scrapers.keys())