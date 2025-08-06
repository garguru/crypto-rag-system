"""
Data Models for Crypto RAG System
These are the building blocks of our intelligence
"""

from dataclasses import dataclass, field
from typing import Optional, Dict, List, Any
from datetime import datetime
from enum import Enum
import json
import hashlib

class SignalStrength(Enum):
    """Signal strength for predictions"""
    STRONG_BUY = 5
    BUY = 4
    NEUTRAL = 3
    SELL = 2
    STRONG_SELL = 1

class DataQuality(Enum):
    """Quality rating for data points"""
    VERIFIED = "verified"
    RELIABLE = "reliable"
    UNCERTAIN = "uncertain"
    UNRELIABLE = "unreliable"

@dataclass
class MarketData:
    """Real-time market data structure"""
    symbol: str
    timestamp: datetime
    price: float
    volume_24h: float
    market_cap: float
    open: float
    high: float
    low: float
    close: float
    change_24h: float
    change_7d: Optional[float] = None
    circulating_supply: Optional[float] = None
    total_supply: Optional[float] = None
    source: str = "unknown"
    quality: DataQuality = DataQuality.RELIABLE
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def to_vector_metadata(self) -> Dict:
        """Convert to metadata for vector storage"""
        return {
            'symbol': self.symbol,
            'timestamp': self.timestamp.isoformat(),
            'price': self.price,
            'volume_24h': self.volume_24h,
            'change_24h': self.change_24h,
            'source': self.source,
            'quality': self.quality.value,
            'data_type': 'market_data'
        }
    
    def to_embedding_text(self) -> str:
        """Generate text for embedding creation"""
        return (
            f"Cryptocurrency {self.symbol} trading at ${self.price:.2f} "
            f"with 24h volume of ${self.volume_24h:,.0f} "
            f"and 24h change of {self.change_24h:.2f}%. "
            f"Market cap: ${self.market_cap:,.0f}. "
            f"Daily range: ${self.low:.2f} - ${self.high:.2f}"
        )
    
    def get_signal_strength(self) -> SignalStrength:
        """Calculate signal strength based on price movement"""
        if self.change_24h > 10:
            return SignalStrength.STRONG_BUY
        elif self.change_24h > 3:
            return SignalStrength.BUY
        elif self.change_24h < -10:
            return SignalStrength.STRONG_SELL
        elif self.change_24h < -3:
            return SignalStrength.SELL
        return SignalStrength.NEUTRAL

@dataclass
class NewsItem:
    """News article data structure"""
    headline: str
    source: str
    published_at: datetime
    url: str
    content: Optional[str] = None
    author: Optional[str] = None
    sentiment_score: float = 0.0  # -1 to 1
    relevance_score: float = 0.0  # 0 to 1
    mentioned_coins: List[str] = field(default_factory=list)
    categories: List[str] = field(default_factory=list)
    impact_level: str = "low"  # low, medium, high, critical
    quality: DataQuality = DataQuality.RELIABLE
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def to_vector_metadata(self) -> Dict:
        """Convert to metadata for vector storage"""
        return {
            'headline': self.headline[:100],
            'source': self.source,
            'published_at': self.published_at.isoformat(),
            'sentiment_score': self.sentiment_score,
            'relevance_score': self.relevance_score,
            'impact_level': self.impact_level,
            'mentioned_coins': ','.join(self.mentioned_coins),
            'data_type': 'news'
        }
    
    def to_embedding_text(self) -> str:
        """Generate text for embedding creation"""
        coins_text = f"Mentions: {', '.join(self.mentioned_coins)}" if self.mentioned_coins else ""
        return (
            f"{self.headline}. "
            f"Published by {self.source}. "
            f"Sentiment: {'positive' if self.sentiment_score > 0 else 'negative' if self.sentiment_score < 0 else 'neutral'}. "
            f"Impact: {self.impact_level}. "
            f"{coins_text}"
        )
    
    def get_signal_from_sentiment(self) -> SignalStrength:
        """Convert sentiment to trading signal"""
        if self.sentiment_score > 0.5 and self.impact_level in ["high", "critical"]:
            return SignalStrength.STRONG_BUY
        elif self.sentiment_score > 0.2:
            return SignalStrength.BUY
        elif self.sentiment_score < -0.5 and self.impact_level in ["high", "critical"]:
            return SignalStrength.STRONG_SELL
        elif self.sentiment_score < -0.2:
            return SignalStrength.SELL
        return SignalStrength.NEUTRAL

@dataclass
class MarketSentiment:
    """Market sentiment indicators"""
    timestamp: datetime
    fear_greed_index: int  # 0-100
    fear_greed_label: str  # Extreme Fear, Fear, Neutral, Greed, Extreme Greed
    social_volume: Optional[int] = None
    social_sentiment: Optional[float] = None  # -1 to 1
    google_trends: Optional[int] = None  # 0-100
    reddit_mentions: Optional[int] = None
    twitter_mentions: Optional[int] = None
    source: str = "aggregate"
    quality: DataQuality = DataQuality.RELIABLE
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def to_vector_metadata(self) -> Dict:
        """Convert to metadata for vector storage"""
        return {
            'timestamp': self.timestamp.isoformat(),
            'fear_greed_index': self.fear_greed_index,
            'fear_greed_label': self.fear_greed_label,
            'social_volume': self.social_volume or 0,
            'social_sentiment': self.social_sentiment or 0,
            'data_type': 'sentiment'
        }
    
    def to_embedding_text(self) -> str:
        """Generate text for embedding creation"""
        social_text = ""
        if self.social_volume:
            social_text = f"Social volume: {self.social_volume} mentions. "
        return (
            f"Market sentiment shows {self.fear_greed_label} "
            f"with Fear & Greed Index at {self.fear_greed_index}. "
            f"{social_text}"
            f"Overall market mood: {self.get_market_mood()}"
        )
    
    def get_market_mood(self) -> str:
        """Interpret overall market mood"""
        if self.fear_greed_index < 20:
            return "Extreme panic - potential buying opportunity"
        elif self.fear_greed_index < 40:
            return "Fear dominant - market cautious"
        elif self.fear_greed_index < 60:
            return "Neutral sentiment - market balanced"
        elif self.fear_greed_index < 80:
            return "Greed increasing - potential overheating"
        else:
            return "Extreme greed - high risk of correction"
    
    def get_contrarian_signal(self) -> SignalStrength:
        """Contrarian signal based on extreme sentiment"""
        if self.fear_greed_index < 20:  # Extreme fear = buy opportunity
            return SignalStrength.STRONG_BUY
        elif self.fear_greed_index > 80:  # Extreme greed = sell signal
            return SignalStrength.STRONG_SELL
        elif self.fear_greed_index < 35:
            return SignalStrength.BUY
        elif self.fear_greed_index > 65:
            return SignalStrength.SELL
        return SignalStrength.NEUTRAL

@dataclass
class TechnicalIndicators:
    """Technical analysis indicators"""
    symbol: str
    timestamp: datetime
    rsi_14: Optional[float] = None  # Relative Strength Index
    macd: Optional[float] = None  # MACD line
    macd_signal: Optional[float] = None  # MACD signal line
    bollinger_upper: Optional[float] = None
    bollinger_middle: Optional[float] = None
    bollinger_lower: Optional[float] = None
    sma_50: Optional[float] = None  # 50-day Simple Moving Average
    sma_200: Optional[float] = None  # 200-day SMA
    ema_12: Optional[float] = None  # 12-day Exponential MA
    ema_26: Optional[float] = None  # 26-day EMA
    volume_sma_20: Optional[float] = None  # 20-day volume average
    atr_14: Optional[float] = None  # Average True Range (volatility)
    support_level: Optional[float] = None
    resistance_level: Optional[float] = None
    
    def get_rsi_signal(self) -> SignalStrength:
        """Get signal from RSI"""
        if not self.rsi_14:
            return SignalStrength.NEUTRAL
        if self.rsi_14 < 30:
            return SignalStrength.STRONG_BUY  # Oversold
        elif self.rsi_14 < 40:
            return SignalStrength.BUY
        elif self.rsi_14 > 70:
            return SignalStrength.STRONG_SELL  # Overbought
        elif self.rsi_14 > 60:
            return SignalStrength.SELL
        return SignalStrength.NEUTRAL
    
    def get_ma_signal(self, current_price: float) -> SignalStrength:
        """Get signal from moving averages"""
        if not self.sma_50 or not self.sma_200:
            return SignalStrength.NEUTRAL
        
        # Golden cross / Death cross
        if self.sma_50 > self.sma_200 and current_price > self.sma_50:
            return SignalStrength.STRONG_BUY
        elif self.sma_50 < self.sma_200 and current_price < self.sma_50:
            return SignalStrength.STRONG_SELL
        elif current_price > self.sma_50:
            return SignalStrength.BUY
        elif current_price < self.sma_50:
            return SignalStrength.SELL
        return SignalStrength.NEUTRAL

@dataclass
class CombinedSignal:
    """Aggregated signal from all data sources"""
    symbol: str
    timestamp: datetime
    market_data: Optional[MarketData] = None
    news_items: List[NewsItem] = field(default_factory=list)
    sentiment: Optional[MarketSentiment] = None
    technicals: Optional[TechnicalIndicators] = None
    
    # Aggregated scores
    overall_signal: SignalStrength = SignalStrength.NEUTRAL
    confidence: float = 0.0  # 0 to 1
    risk_level: str = "medium"  # low, medium, high, extreme
    
    # Component signals
    price_signal: SignalStrength = SignalStrength.NEUTRAL
    news_signal: SignalStrength = SignalStrength.NEUTRAL
    sentiment_signal: SignalStrength = SignalStrength.NEUTRAL
    technical_signal: SignalStrength = SignalStrength.NEUTRAL
    
    # Reasoning
    reasoning: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)
    opportunities: List[str] = field(default_factory=list)
    
    def calculate_combined_signal(self) -> None:
        """Calculate overall signal from all components"""
        signals = []
        weights = []
        
        # Market data signal
        if self.market_data:
            self.price_signal = self.market_data.get_signal_strength()
            signals.append(self.price_signal.value)
            weights.append(0.25)
            
            if abs(self.market_data.change_24h) > 10:
                self.warnings.append(f"High volatility: {self.market_data.change_24h:.1f}% 24h change")
        
        # News sentiment signal
        if self.news_items:
            news_scores = [item.get_signal_from_sentiment().value for item in self.news_items[:5]]
            if news_scores:
                avg_news_signal = sum(news_scores) / len(news_scores)
                self.news_signal = SignalStrength(round(avg_news_signal))
                signals.append(avg_news_signal)
                weights.append(0.3)
                
                # Check for high-impact news
                critical_news = [n for n in self.news_items if n.impact_level == "critical"]
                if critical_news:
                    self.warnings.append(f"Critical news: {critical_news[0].headline[:50]}...")
        
        # Market sentiment signal
        if self.sentiment:
            self.sentiment_signal = self.sentiment.get_contrarian_signal()
            signals.append(self.sentiment_signal.value)
            weights.append(0.2)
            
            if self.sentiment.fear_greed_index < 20 or self.sentiment.fear_greed_index > 80:
                self.opportunities.append(f"Extreme sentiment: {self.sentiment.fear_greed_label}")
        
        # Technical indicators signal
        if self.technicals:
            tech_signals = []
            if self.technicals.rsi_14:
                tech_signals.append(self.technicals.get_rsi_signal().value)
            if self.market_data and self.technicals.sma_50:
                tech_signals.append(self.technicals.get_ma_signal(self.market_data.price).value)
            
            if tech_signals:
                avg_tech_signal = sum(tech_signals) / len(tech_signals)
                self.technical_signal = SignalStrength(round(avg_tech_signal))
                signals.append(avg_tech_signal)
                weights.append(0.25)
        
        # Calculate weighted average
        if signals and weights:
            weighted_sum = sum(s * w for s, w in zip(signals, weights))
            total_weight = sum(weights)
            avg_signal = weighted_sum / total_weight
            
            self.overall_signal = SignalStrength(round(avg_signal))
            
            # Calculate confidence based on agreement
            signal_variance = sum((s - avg_signal) ** 2 for s in signals) / len(signals)
            self.confidence = max(0, min(1, 1 - (signal_variance / 4)))  # Normalize to 0-1
            
            # Determine risk level
            if self.confidence < 0.3:
                self.risk_level = "extreme"
            elif self.confidence < 0.5:
                self.risk_level = "high"
            elif self.confidence < 0.7:
                self.risk_level = "medium"
            else:
                self.risk_level = "low"
        
        # Generate reasoning
        self._generate_reasoning()
    
    def _generate_reasoning(self) -> None:
        """Generate human-readable reasoning"""
        self.reasoning = []
        
        if self.overall_signal in [SignalStrength.STRONG_BUY, SignalStrength.BUY]:
            self.reasoning.append(f"Bullish signal with {self.confidence:.1%} confidence")
        elif self.overall_signal in [SignalStrength.STRONG_SELL, SignalStrength.SELL]:
            self.reasoning.append(f"Bearish signal with {self.confidence:.1%} confidence")
        else:
            self.reasoning.append("Neutral market conditions")
        
        # Add component reasoning
        if self.market_data:
            self.reasoning.append(f"Price action: {self.market_data.change_24h:+.1f}% in 24h")
        
        if self.sentiment:
            self.reasoning.append(f"Market sentiment: {self.sentiment.fear_greed_label}")
        
        if self.news_items:
            self.reasoning.append(f"News sentiment: {len(self.news_items)} articles analyzed")
        
        if self.technicals and self.technicals.rsi_14:
            self.reasoning.append(f"RSI: {self.technicals.rsi_14:.1f}")
    
    def to_json(self) -> str:
        """Convert to JSON for storage"""
        return json.dumps({
            'symbol': self.symbol,
            'timestamp': self.timestamp.isoformat(),
            'overall_signal': self.overall_signal.name,
            'confidence': self.confidence,
            'risk_level': self.risk_level,
            'reasoning': self.reasoning,
            'warnings': self.warnings,
            'opportunities': self.opportunities
        }, indent=2)
    
    def get_unique_id(self) -> str:
        """Generate unique ID for this signal"""
        content = f"{self.symbol}{self.timestamp.isoformat()}"
        return hashlib.sha256(content.encode()).hexdigest()[:16]