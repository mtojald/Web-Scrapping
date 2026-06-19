from .scrappers.reddit_scraper import RedditScraper, coletar_reddit
from .scrappers.news_scraper import NewsScraper, coletar_noticias
from .scrappers.youtube_scraper import YoutubeScraper, coletar_youtube
from .scrappers.apify_scraper import ApifyScraper, ReclameAquiScraper, coletar_apify
from .models import Feedback, FeedbackCollection, Sentimento

__all__ = [
    "RedditScraper", "NewsScraper", "YoutubeScraper", "ApifyScraper", "ReclameAquiScraper",
    "coletar_reddit", "coletar_noticias", "coletar_youtube", "coletar_apify",
    "Feedback", "FeedbackCollection", "Sentimento",
]
