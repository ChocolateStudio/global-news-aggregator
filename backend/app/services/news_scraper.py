# backend/app/services/news_scraper.py
import asyncio
import aiohttp
from typing import List
import requests
from app.models.news_article import NewsArticle
from app.config import settings
from app.utils.text_preprocessor import preprocess_text
import logging

class NewsScraper:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
    
    async def scrape_source(self, source: dict) -> List[NewsArticle]:
        """Asynchronously scrape news from a specific source"""
        try:
            # ParseHub API call
            response = requests.get(
                f"https://www.parsehub.com/api/v2/projects/{source['parsehub_token']}/last_ready_run/data",
                params={"api_key": settings.PARSEHUB_API_KEY}
            )
            response.raise_for_status()
            articles_data = response.json()
            
            # Process articles
            articles = []
            for article_data in articles_data:
                try:
                    processed_content = preprocess_text(article_data.get('content', ''))
                    
                    article = NewsArticle(
                        title=article_data.get('title', ''),
                        source=source['name'],
                        url=article_data.get('url', ''),
                        content=processed_content,
                        language=source['language']
                    )
                    articles.append(article)
                except Exception as e:
                    self.logger.error(f"Error processing article from {source['name']}: {e}")
            
            return articles
        
        except Exception as e:
            self.logger.error(f"Error scraping {source['name']}: {e}")
            return []
    
    async def aggregate_news(self) -> List[NewsArticle]:
        """Aggregate news from all sources concurrently"""
        tasks = [self.scrape_source(source) for source in settings.NEWS_SOURCES]
        results = await asyncio.gather(*tasks)
        
        # Flatten results
        return [article for sublist in results for article in sublist]
