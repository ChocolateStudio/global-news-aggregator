# backend/app/models/news_article.py
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

# backend/app/models/topic_model.py
from typing import List, Dict
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

class TopicModeler:
    def __init__(self, articles: List[NewsArticle]):
        self.articles = articles
        self.vectorizer = TfidfVectorizer(stop_words='english')
    
    def cluster_topics(self, similarity_threshold: float = 0.3) -> List[TopicCluster]:
        # Extract content for vectorization
        contents = [article.content for article in self.articles]
        
        # Create TF-IDF matrix
        tfidf_matrix = self.vectorizer.fit_transform(contents)
        
        # Compute cosine similarity
        similarity_matrix = cosine_similarity(tfidf_matrix)
        
        # Clustering logic
        clusters = []
        used_articles = set()
        
        for i, article in enumerate(self.articles):
            if i in used_articles:
                continue
            
            cluster_articles = [article]
            used_articles.add(i)
            
            for j, other_article in enumerate(self.articles):
                if j in used_articles:
                    continue
                
                if similarity_matrix[i][j] > similarity_threshold:
                    cluster_articles.append(other_article)
                    used_articles.add(j)
            
            # Create topic cluster
            cluster = TopicCluster(
                title=self._generate_cluster_title(cluster_articles),
                articles=cluster_articles,
                related_keywords=self._extract_keywords(cluster_articles),
                similarity_score=np.mean([similarity_matrix[i][self.articles.index(a)] for a in cluster_articles]),
                global_perspectives=[]
            )
            
            clusters.append(cluster)
        
        return clusters
    
    def _generate_cluster_title(self, articles: List[NewsArticle]) -> str:
        # Use TF-IDF to generate cluster title
        contents = [article.content for article in articles]
        tfidf = self.vectorizer.transform(contents)
        feature_names = self.vectorizer.get_feature_names_out()
        
        # Get top keywords
        keywords = []
        for idx in tfidf.toarray().mean(axis=0).argsort()[-3:][::-1]:
            keywords.append(feature_names[idx])
        
        return f"Global Topic: {' '.join(keywords)}"
    
    def _extract_keywords(self, articles: List[NewsArticle]) -> List[str]:
        # Extract and rank keywords
        contents = [article.content for article in articles]
        tfidf = self.vectorizer.transform(contents)
        feature_names = self.vectorizer.get_feature_names_out()
        
        # Get top 10 keywords
        keyword_scores = tfidf.toarray().mean(axis=0)
        top_keyword_indices = keyword_scores.argsort()[-10:][::-1]
        
        return [feature_names[idx] for idx in top_keyword_indices]
