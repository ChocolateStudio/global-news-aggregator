# backend/app/main.py
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Dict
import logging

from app.services.news_scraper import NewsScraper
from app.models.topic_model import TopicModeler
from app.services.summarization import NewsSummarizer
from app.config import settings

# Configure logging
logging.basicConfig(
    level=getattr(logging, settings.LOG_LEVEL),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Global News Aggregator",
    description="Aggregates and analyzes international news from multiple sources"
)

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

@app.get("/news/aggregate")
async def aggregate_news():
    """Aggregate and analyze news from multiple international sources"""
    try:
        # Scrape news from sources
        scraper = NewsScraper()
        articles = await scraper.aggregate_news()
        
        # Cluster similar topics
        topic_modeler = TopicModeler(articles)
        topic_clusters = topic_modeler.cluster_topics()
        
        # Generate summaries
        summarizer = NewsSummarizer()
        global_perspectives = [
            summarizer.generate_global_perspective(cluster) 
            for cluster in topic_clusters
        ]
        
        return {
            "total_articles": len(articles),
            "topic_clusters": len(topic_clusters),
            "global_perspectives": global_perspectives
        }
    
    except Exception as e:
        logger.error(f"Error in news aggregation: {e}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
