from .scrappers.reddit_scraper import coletar_reddit
from .scrappers.news_scraper import coletar_noticias
from .scrappers.youtube_scraper import coletar_youtube
from .scrappers.apify_scraper import coletar_apify

__all__ = ["coletar_reddit", "coletar_noticias", "coletar_youtube", "coletar_apify"]