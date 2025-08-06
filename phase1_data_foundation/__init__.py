"""
Phase 1: Data Foundation
The bedrock of our crypto prediction system
"""

from .data_pipeline import CryptoDataPipeline
from .data_models import MarketData, NewsItem, MarketSentiment, CombinedSignal
# from .vector_store import VectorStoreManager  # Coming soon
# from .cache_layer import CacheManager  # Coming soon
# from .orchestrator import PipelineOrchestrator  # Coming soon

__version__ = "1.0.0"
__all__ = [
    'CryptoDataPipeline',
    'MarketData',
    'NewsItem', 
    'MarketSentiment',
    'CombinedSignal',
    'VectorStoreManager',
    'CacheManager',
    'PipelineOrchestrator'
]