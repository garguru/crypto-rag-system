"""
Configuration for the Crypto RAG System
Central place for all settings and API keys
"""

import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
env_path = Path(__file__).parent.parent / '.env'
load_dotenv(env_path)

class Config:
    """System configuration"""
    
    # API Keys
    POLYGON_API_KEY = os.getenv('POLYGON_API_KEY', 'ZOPT0lW9zJUuwX6NuxCMX1zhGVBqaVID')
    NEWSAPI_KEY = os.getenv('NEWSAPI_KEY', '')
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY', '')
    OPENROUTER_KEY = os.getenv('OPENROUTER_KEY', '')
    
    # Data Sources
    DEFAULT_SYMBOLS = ['BTC', 'ETH', 'SOL']
    DATA_UPDATE_INTERVAL = 300  # 5 minutes
    
    # Vector Database
    CHROMA_PERSIST_DIR = Path(__file__).parent.parent / 'vector_db'
    CHROMA_COLLECTION_NAME = 'crypto_rag'
    
    # Cache Settings
    REDIS_HOST = os.getenv('REDIS_HOST', 'localhost')
    REDIS_PORT = int(os.getenv('REDIS_PORT', 6379))
    REDIS_DB = int(os.getenv('REDIS_DB', 0))
    CACHE_TTL = 300  # 5 minutes default
    
    # Model Settings
    EMBEDDING_MODEL = 'text-embedding-ada-002'
    LLM_MODEL = 'gpt-3.5-turbo'
    MAX_TOKENS = 2000
    TEMPERATURE = 0.7
    
    # System Settings
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
    DEBUG_MODE = os.getenv('DEBUG_MODE', 'False').lower() == 'true'
    MAX_RETRIES = 3
    TIMEOUT = 30  # seconds
    
    # Trading Settings
    MIN_CONFIDENCE = 0.7  # Minimum confidence for trading signal
    MAX_RISK_LEVEL = 'high'  # Don't trade on 'extreme' risk
    PAPER_TRADING = True  # Always start with paper trading!
    
    # Performance Settings
    MAX_CONCURRENT_REQUESTS = 10
    BATCH_SIZE = 100
    
    @classmethod
    def to_dict(cls) -> dict:
        """Convert config to dictionary"""
        return {
            'polygon_api_key': cls.POLYGON_API_KEY,
            'newsapi_key': cls.NEWSAPI_KEY,
            'openai_api_key': cls.OPENAI_API_KEY,
            'default_symbols': cls.DEFAULT_SYMBOLS,
            'data_update_interval': cls.DATA_UPDATE_INTERVAL,
            'cache_ttl': cls.CACHE_TTL,
            'min_confidence': cls.MIN_CONFIDENCE,
            'paper_trading': cls.PAPER_TRADING,
            'debug_mode': cls.DEBUG_MODE
        }
    
    @classmethod
    def validate(cls) -> bool:
        """Validate configuration"""
        issues = []
        
        if not cls.POLYGON_API_KEY:
            issues.append("Missing POLYGON_API_KEY")
        
        if not cls.CHROMA_PERSIST_DIR.exists():
            cls.CHROMA_PERSIST_DIR.mkdir(parents=True, exist_ok=True)
        
        if cls.MIN_CONFIDENCE < 0 or cls.MIN_CONFIDENCE > 1:
            issues.append("MIN_CONFIDENCE must be between 0 and 1")
        
        if issues:
            print("Configuration issues found:")
            for issue in issues:
                print(f"  - {issue}")
            return False
        
        return True

# Create singleton instance
config = Config()