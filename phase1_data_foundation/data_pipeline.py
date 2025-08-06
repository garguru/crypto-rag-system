"""
Crypto Data Pipeline - The Heart of Our System
Collects, processes, and routes all data streams
"""

import asyncio
import aiohttp
from typing import List, Dict, Optional, Any
from datetime import datetime, timedelta
import json
import logging
from concurrent.futures import ThreadPoolExecutor
import requests
from dataclasses import asdict

from .data_models import (
    MarketData, NewsItem, MarketSentiment, 
    TechnicalIndicators, CombinedSignal, DataQuality
)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class CryptoDataPipeline:
    """Main data collection and processing pipeline"""
    
    def __init__(self, config: Dict[str, Any]):
        """Initialize the pipeline with configuration"""
        self.config = config
        self.polygon_key = config.get('polygon_api_key')
        self.coingecko_base = "https://api.coingecko.com/api/v3"
        self.newsapi_key = config.get('newsapi_key')
        self.alternative_base = "https://api.alternative.me"
        
        # Rate limiting
        self.rate_limits = {
            'polygon': {'calls': 0, 'max': 5, 'window': 60},  # 5 per minute
            'coingecko': {'calls': 0, 'max': 10, 'window': 60},  # 10 per minute
            'newsapi': {'calls': 0, 'max': 100, 'window': 86400},  # 100 per day
            'alternative': {'calls': 0, 'max': 30, 'window': 60}  # 30 per minute
        }
        
        # Cache for recent data
        self.cache = {
            'market_data': {},
            'news': {},
            'sentiment': {},
            'last_update': {}
        }
        
        # Thread pool for parallel processing
        self.executor = ThreadPoolExecutor(max_workers=4)
        
        logger.info("CryptoDataPipeline initialized")
    
    async def collect_all_data(self, symbols: List[str]) -> Dict[str, CombinedSignal]:
        """Collect data from all sources for given symbols"""
        logger.info(f"Starting data collection for {symbols}")
        
        combined_signals = {}
        
        for symbol in symbols:
            try:
                # Collect data in parallel
                tasks = [
                    self._collect_market_data(symbol),
                    self._collect_news(symbol),
                    self._collect_sentiment(),
                    self._calculate_technicals(symbol)
                ]
                
                results = await asyncio.gather(*tasks, return_exceptions=True)
                
                # Unpack results
                market_data = results[0] if not isinstance(results[0], Exception) else None
                news_items = results[1] if not isinstance(results[1], Exception) else []
                sentiment = results[2] if not isinstance(results[2], Exception) else None
                technicals = results[3] if not isinstance(results[3], Exception) else None
                
                # Create combined signal
                combined = CombinedSignal(
                    symbol=symbol,
                    timestamp=datetime.now(),
                    market_data=market_data,
                    news_items=news_items,
                    sentiment=sentiment,
                    technicals=technicals
                )
                
                # Calculate aggregated signals
                combined.calculate_combined_signal()
                
                combined_signals[symbol] = combined
                
                logger.info(f"Collected data for {symbol}: Signal={combined.overall_signal.name}, Confidence={combined.confidence:.2%}")
                
            except Exception as e:
                logger.error(f"Error collecting data for {symbol}: {e}")
                continue
        
        return combined_signals
    
    async def _collect_market_data(self, symbol: str) -> Optional[MarketData]:
        """Collect market data from multiple sources"""
        try:
            # Try Polygon first
            if self.polygon_key and self._check_rate_limit('polygon'):
                data = await self._fetch_polygon_data(symbol)
                if data:
                    return data
            
            # Fallback to CoinGecko
            if self._check_rate_limit('coingecko'):
                data = await self._fetch_coingecko_data(symbol)
                if data:
                    return data
            
            # Check cache
            cache_key = f"market_{symbol}"
            if cache_key in self.cache['market_data']:
                cached = self.cache['market_data'][cache_key]
                if (datetime.now() - cached['timestamp']).seconds < 300:  # 5 min cache
                    logger.info(f"Using cached market data for {symbol}")
                    return cached['data']
            
            logger.warning(f"No market data available for {symbol}")
            return None
            
        except Exception as e:
            logger.error(f"Error collecting market data for {symbol}: {e}")
            return None
    
    async def _fetch_polygon_data(self, symbol: str) -> Optional[MarketData]:
        """Fetch data from Polygon.io"""
        try:
            # Convert symbol format (BTC -> X:BTCUSD)
            polygon_symbol = f"X:{symbol}USD" if not symbol.startswith("X:") else symbol
            
            url = f"https://api.polygon.io/v2/aggs/ticker/{polygon_symbol}/prev"
            params = {"apiKey": self.polygon_key}
            
            async with aiohttp.ClientSession() as session:
                async with session.get(url, params=params) as response:
                    if response.status == 200:
                        data = await response.json()
                        
                        if data.get('status') == 'OK' and data.get('results'):
                            result = data['results'][0]
                            
                            market_data = MarketData(
                                symbol=symbol,
                                timestamp=datetime.now(),
                                price=result['c'],
                                volume_24h=result['v'],
                                market_cap=0,  # Polygon doesn't provide market cap
                                open=result['o'],
                                high=result['h'],
                                low=result['l'],
                                close=result['c'],
                                change_24h=((result['c'] - result['o']) / result['o']) * 100,
                                source='polygon',
                                quality=DataQuality.VERIFIED
                            )
                            
                            # Update cache
                            self._update_cache('market_data', f"market_{symbol}", market_data)
                            self._increment_rate_limit('polygon')
                            
                            return market_data
            
            return None
            
        except Exception as e:
            logger.error(f"Polygon API error: {e}")
            return None
    
    async def _fetch_coingecko_data(self, symbol: str) -> Optional[MarketData]:
        """Fetch data from CoinGecko"""
        try:
            # Map symbol to CoinGecko ID
            symbol_map = {
                'BTC': 'bitcoin',
                'ETH': 'ethereum',
                'SOL': 'solana',
                'BNB': 'binancecoin',
                'XRP': 'ripple',
                'ADA': 'cardano',
                'DOGE': 'dogecoin'
            }
            
            coin_id = symbol_map.get(symbol.upper(), symbol.lower())
            
            url = f"{self.coingecko_base}/coins/markets"
            params = {
                'vs_currency': 'usd',
                'ids': coin_id,
                'order': 'market_cap_desc',
                'sparkline': 'false'
            }
            
            async with aiohttp.ClientSession() as session:
                async with session.get(url, params=params) as response:
                    if response.status == 200:
                        data = await response.json()
                        
                        if data and len(data) > 0:
                            coin = data[0]
                            
                            market_data = MarketData(
                                symbol=symbol,
                                timestamp=datetime.now(),
                                price=coin['current_price'],
                                volume_24h=coin['total_volume'],
                                market_cap=coin['market_cap'],
                                open=coin['current_price'],  # CoinGecko doesn't provide OHLC in this endpoint
                                high=coin['high_24h'],
                                low=coin['low_24h'],
                                close=coin['current_price'],
                                change_24h=coin['price_change_percentage_24h'],
                                change_7d=coin.get('price_change_percentage_7d'),
                                circulating_supply=coin.get('circulating_supply'),
                                total_supply=coin.get('total_supply'),
                                source='coingecko',
                                quality=DataQuality.RELIABLE
                            )
                            
                            # Update cache
                            self._update_cache('market_data', f"market_{symbol}", market_data)
                            self._increment_rate_limit('coingecko')
                            
                            return market_data
            
            return None
            
        except Exception as e:
            logger.error(f"CoinGecko API error: {e}")
            return None
    
    async def _collect_news(self, symbol: str) -> List[NewsItem]:
        """Collect news from various sources"""
        news_items = []
        
        try:
            # Check cache first
            cache_key = f"news_{symbol}"
            if cache_key in self.cache['news']:
                cached = self.cache['news'][cache_key]
                if (datetime.now() - cached['timestamp']).seconds < 1800:  # 30 min cache
                    logger.info(f"Using cached news for {symbol}")
                    return cached['data']
            
            # CryptoCompare News API (free tier)
            url = "https://min-api.cryptocompare.com/data/v2/news/"
            params = {'lang': 'EN', 'categories': symbol}
            
            async with aiohttp.ClientSession() as session:
                async with session.get(url, params=params) as response:
                    if response.status == 200:
                        data = await response.json()
                        
                        if data.get('Data'):
                            for article in data['Data'][:10]:  # Get top 10 news
                                news_item = NewsItem(
                                    headline=article['title'],
                                    source=article.get('source_info', {}).get('name', 'Unknown'),
                                    published_at=datetime.fromtimestamp(article['published_on']),
                                    url=article.get('url', ''),
                                    content=article.get('body', '')[:500],  # First 500 chars
                                    categories=article.get('categories', '').split('|'),
                                    sentiment_score=self._analyze_sentiment(article['title']),
                                    relevance_score=0.8 if symbol.upper() in article['title'].upper() else 0.5,
                                    mentioned_coins=[symbol],
                                    impact_level=self._assess_impact(article['title']),
                                    quality=DataQuality.RELIABLE
                                )
                                news_items.append(news_item)
            
            # Update cache
            self._update_cache('news', cache_key, news_items)
            
        except Exception as e:
            logger.error(f"Error collecting news for {symbol}: {e}")
        
        return news_items
    
    async def _collect_sentiment(self) -> Optional[MarketSentiment]:
        """Collect market sentiment data"""
        try:
            # Check cache
            cache_key = "sentiment_global"
            if cache_key in self.cache['sentiment']:
                cached = self.cache['sentiment'][cache_key]
                if (datetime.now() - cached['timestamp']).seconds < 3600:  # 1 hour cache
                    logger.info("Using cached sentiment data")
                    return cached['data']
            
            # Fear & Greed Index
            url = f"{self.alternative_base}/fng/"
            
            async with aiohttp.ClientSession() as session:
                async with session.get(url) as response:
                    if response.status == 200:
                        data = await response.json()
                        
                        if data.get('data'):
                            fng = data['data'][0]
                            
                            sentiment = MarketSentiment(
                                timestamp=datetime.now(),
                                fear_greed_index=int(fng['value']),
                                fear_greed_label=fng['value_classification'],
                                source='alternative.me',
                                quality=DataQuality.RELIABLE
                            )
                            
                            # Update cache
                            self._update_cache('sentiment', cache_key, sentiment)
                            self._increment_rate_limit('alternative')
                            
                            return sentiment
            
            return None
            
        except Exception as e:
            logger.error(f"Error collecting sentiment: {e}")
            return None
    
    async def _calculate_technicals(self, symbol: str) -> Optional[TechnicalIndicators]:
        """Calculate technical indicators from historical data"""
        # This would typically use historical price data
        # For now, returning mock technicals
        # In production, you'd calculate these from OHLCV data
        
        try:
            # Fetch historical data (simplified for demo)
            # In reality, you'd get last 200 days of data
            
            technicals = TechnicalIndicators(
                symbol=symbol,
                timestamp=datetime.now(),
                rsi_14=50.0,  # Would be calculated from price data
                sma_50=0.0,   # Would be calculated
                sma_200=0.0,  # Would be calculated
            )
            
            return technicals
            
        except Exception as e:
            logger.error(f"Error calculating technicals for {symbol}: {e}")
            return None
    
    def _analyze_sentiment(self, text: str) -> float:
        """Simple sentiment analysis (would use NLP in production)"""
        positive_words = ['bullish', 'surge', 'rally', 'gain', 'rise', 'up', 'high', 
                         'positive', 'growth', 'increase', 'soar', 'moon', 'breakthrough']
        negative_words = ['bearish', 'crash', 'fall', 'drop', 'down', 'low', 'negative',
                         'decline', 'decrease', 'plunge', 'dump', 'correction', 'fear']
        
        text_lower = text.lower()
        pos_count = sum(1 for word in positive_words if word in text_lower)
        neg_count = sum(1 for word in negative_words if word in text_lower)
        
        if pos_count + neg_count == 0:
            return 0.0
        
        return (pos_count - neg_count) / (pos_count + neg_count)
    
    def _assess_impact(self, headline: str) -> str:
        """Assess the impact level of news"""
        high_impact_words = ['regulation', 'sec', 'government', 'ban', 'legal', 'hack',
                            'bankruptcy', 'collapse', 'etf', 'institutional', 'billion']
        
        headline_lower = headline.lower()
        
        if any(word in headline_lower for word in high_impact_words):
            return "high"
        elif any(word in headline_lower for word in ['million', 'partnership', 'upgrade']):
            return "medium"
        return "low"
    
    def _check_rate_limit(self, service: str) -> bool:
        """Check if we can make another API call"""
        limit = self.rate_limits.get(service)
        if not limit:
            return True
        
        return limit['calls'] < limit['max']
    
    def _increment_rate_limit(self, service: str) -> None:
        """Increment rate limit counter"""
        if service in self.rate_limits:
            self.rate_limits[service]['calls'] += 1
    
    def _update_cache(self, category: str, key: str, data: Any) -> None:
        """Update cache with new data"""
        self.cache[category][key] = {
            'data': data,
            'timestamp': datetime.now()
        }
    
    def reset_rate_limits(self) -> None:
        """Reset rate limit counters (call this periodically)"""
        for service in self.rate_limits:
            self.rate_limits[service]['calls'] = 0
        logger.info("Rate limits reset")
    
    async def health_check(self) -> Dict[str, Any]:
        """Check health of all data sources"""
        health = {
            'timestamp': datetime.now().isoformat(),
            'sources': {}
        }
        
        # Test each data source
        for source in ['polygon', 'coingecko', 'alternative']:
            try:
                if source == 'polygon' and self.polygon_key:
                    # Test Polygon
                    test_data = await self._fetch_polygon_data('BTC')
                    health['sources']['polygon'] = 'healthy' if test_data else 'unhealthy'
                elif source == 'coingecko':
                    # Test CoinGecko
                    test_data = await self._fetch_coingecko_data('BTC')
                    health['sources']['coingecko'] = 'healthy' if test_data else 'unhealthy'
                elif source == 'alternative':
                    # Test Alternative.me
                    test_data = await self._collect_sentiment()
                    health['sources']['alternative'] = 'healthy' if test_data else 'unhealthy'
            except:
                health['sources'][source] = 'error'
        
        # Check cache status
        health['cache'] = {
            'market_data': len(self.cache['market_data']),
            'news': len(self.cache['news']),
            'sentiment': len(self.cache['sentiment'])
        }
        
        # Check rate limits
        health['rate_limits'] = self.rate_limits
        
        return health