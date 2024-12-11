# backend/app/config.py
import os
from dotenv import load_dotenv
from functools import lru_cache

load_dotenv()

class Settings:
    # ParseHub Configuration
    PARSEHUB_API_KEY: str = os.getenv('PARSEHUB_API_KEY', '')
    
    # OpenAI Configuration
    OPENAI_API_KEY: str = os.getenv('OPENAI_API_KEY', '')
    
    # News Sources Configuration
    NEWS_SOURCES = [
        {
            'name': 'Deutsche Welle',
            'url': 'https://www.dw.com',
            'language': 'en',
            'parsehub_token': os.getenv('DW_PARSEHUB_TOKEN', '')
        },
        {
            'name': 'The Hindu',
            'url': 'https://www.thehindu.com',
            'language': 'en',
            'parsehub_token': os.getenv('HINDU_PARSEHUB_TOKEN', '')
        },
        # Add other news sources here
    ]
    
    # Logging Configuration
    LOG_LEVEL: str = os.getenv('LOG_LEVEL', 'INFO')
    
    # Caching Configuration
    CACHE_EXPIRATION: int = int(os.getenv('CACHE_EXPIRATION', 3600))  # 1 hour

@lru_cache()
def get_settings():
    return Settings()

settings = get_settings()
