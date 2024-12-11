# backend/app/services/summarization.py
import openai
from typing import List, Dict
from app.models.news_article import TopicCluster
from app.config import settings
import logging

class NewsSummarizer:
    def __init__(self):
        openai.api_key = settings.OPENAI_API_KEY
        self.logger = logging.getLogger(__name__)
    
    def generate_global_perspective(self, topic_cluster: TopicCluster) -> Dict:
        """Generate a balanced, multi-perspective summary of a topic cluster"""
        try:
            # Prepare context from multiple articles
            context = " ".join([article.content for article in topic_cluster.articles])
            
            # Prompt for multi-perspective analysis
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo-16k",
                messages=[
                    {
                        "role": "system", 
                        "content": "You are an impartial global news analyst. Provide a balanced, nuanced summary of the topic from multiple perspectives."
                    },
                    {
                        "role": "user", 
                        "content": f"""Analyze these news articles about '{topic_cluster.title}' from multiple international perspectives.
                        
                        Context: {context}
                        
                        Please provide:
                        1. A balanced summary of the topic
                        2. Key perspectives from different regions or news sources
                        3. Background context
                        4. Potential implications
                        5. Areas of agreement and disagreement
                        
                        Maintain objectivity and represent diverse viewpoints."""
                    }
                ],
                max_tokens=1000,
                temperature=0.7
            )
            
            global_perspective = response.choices[0].message.content
            
            return {
                "title": topic_cluster.title,
                "summary": global_perspective,
                "sources": [article.source for article in topic_cluster.articles],
                "keywords": topic_cluster.related_keywords
            }
        
        except Exception as e:
            self.logger.error(f"Error generating summary for {topic_cluster.title}: {e}")
            return {
                "title": topic_cluster.title,
                "summary": "Unable to generate summary due to technical difficulties.",
                "sources": [],
                "keywords": []
            }
