from vnexpress import VnExpressScraper
from tuoitre import TuoiTreScraper


class ScraperFactory:
    _scrapers = {
        'vnexpress': VnExpressScraper,
        'tuoitre': TuoiTreScraper,
    }
    
    @classmethod
    def get_scraper(cls, source: str):
        scraper_class = cls._scrapers.get(source.lower())
        if not scraper_class:
            raise ValueError(f"Unsupported source: {source}")
        return scraper_class()
    
    @classmethod
    def get_all_sources(cls):
        return list(cls._scrapers.keys())

# Test
if __name__ == "__main__":
    print("Available sources:", ScraperFactory.get_all_sources())
    vne_scraper = ScraperFactory.get_scraper('vnexpress')
    print(f"Created: {type(vne_scraper).__name__}")