from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime

class NewsArticle(BaseModel):
    id: str = Field(default_factory=lambda: str(datetime.now().timestamp()))
    title: str
    source: str
    url: str
    content: str
    language: str
    published_at: datetime = Field(default_factory=datetime.now)
    keywords: List[str] = []
    sentiment: Optional[float] = None

class TopicCluster(BaseModel):
    id: str = Field(default_factory=lambda: str(datetime.now().timestamp()))
    title: str
    articles: List[NewsArticle]
    related_keywords: List[str]
    similarity_score: float
    global_perspectives: List[dict]
