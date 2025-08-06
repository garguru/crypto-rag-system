"""
Enhanced Crypto RAG System with Real Data
Uses Polygon.io API for real market data
"""

import os
import json
import requests
from datetime import datetime, timedelta
from pathlib import Path
import time

class EnhancedCryptoRAG:
    """Enhanced RAG system with real market data"""
    
    def __init__(self):
        self.project_dir = Path(__file__).parent
        self.data_dir = self.project_dir / "crypto_data"
        self.data_dir.mkdir(exist_ok=True)
        
        # Polygon API setup
        self.polygon_api_key = "ZOPT0lW9zJUuwX6NuxCMX1zhGVBqaVID"
        self.polygon_base = "https://api.polygon.io"
        
        # Data storage
        self.predictions_dir = self.data_dir / "predictions"
        self.predictions_dir.mkdir(exist_ok=True)
        
        # Knowledge base for RAG
        self.knowledge_base = {
            'market_data': {},
            'technical_indicators': {},
            'news': [],
            'predictions': []
        }
        
        print(">>> Enhanced Crypto RAG System Initialized")
        print(">>> Using Polygon.io for real market data")
    
    def get_real_crypto_price(self, ticker="X:BTCUSD"):
        """Get real crypto price from Polygon"""
        print(f"\n[POLYGON] Fetching real {ticker} data...")
        
        # Get previous day's data
        url = f"{self.polygon_base}/v2/aggs/ticker/{ticker}/prev"
        params = {"apiKey": self.polygon_api_key}
        
        try:
            response = requests.get(url, params=params)
            data = response.json()
            
            if data['status'] == 'OK' and data['results']:
                result = data['results'][0]
                market_data = {
                    'ticker': ticker,
                    'timestamp': datetime.now().isoformat(),
                    'close': result['c'],
                    'open': result['o'],
                    'high': result['h'],
                    'low': result['l'],
                    'volume': result['v'],
                    'vwap': result.get('vw', 0),
                    'change_percent': ((result['c'] - result['o']) / result['o']) * 100
                }
                
                self.knowledge_base['market_data'] = market_data
                
                print(f"   Price: ${market_data['close']:,.2f}")
                print(f"   24h Change: {market_data['change_percent']:.2f}%")
                print(f"   Volume: ${market_data['volume']:,.0f}")
                
                return market_data
            else:
                print(f"   Error: {data.get('status', 'Unknown error')}")
                return None
                
        except Exception as e:
            print(f"   Error fetching data: {e}")
            return None
    
    def get_crypto_aggregates(self, ticker="X:BTCUSD", timespan="hour", limit=24):
        """Get historical aggregates for technical analysis"""
        print(f"\n[TECHNICALS] Fetching {limit} {timespan} bars...")
        
        # Calculate date range
        end = datetime.now()
        start = end - timedelta(days=7)
        
        url = f"{self.polygon_base}/v2/aggs/ticker/{ticker}/range/1/{timespan}/{start.strftime('%Y-%m-%d')}/{end.strftime('%Y-%m-%d')}"
        params = {
            "apiKey": self.polygon_api_key,
            "limit": limit,
            "sort": "desc"
        }
        
        try:
            response = requests.get(url, params=params)
            data = response.json()
            
            if data['status'] == 'OK' and 'results' in data:
                prices = [bar['c'] for bar in data['results']]
                
                # Calculate technical indicators
                if len(prices) >= 14:
                    rsi = self.calculate_rsi(prices[:14])
                else:
                    rsi = 50  # Default neutral
                
                # Simple moving averages
                sma_short = sum(prices[:10]) / min(10, len(prices)) if prices else 0
                sma_long = sum(prices[:20]) / min(20, len(prices)) if prices else 0
                
                current_price = prices[0] if prices else 0
                
                technicals = {
                    'rsi': rsi,
                    'sma_10': sma_short,
                    'sma_20': sma_long,
                    'current_price': current_price,
                    'trend': 'bullish' if current_price > sma_short > sma_long else 'bearish',
                    'momentum': 'strong' if rsi > 50 else 'weak'
                }
                
                self.knowledge_base['technical_indicators'] = technicals
                
                print(f"   RSI: {rsi:.2f}")
                print(f"   Trend: {technicals['trend']}")
                print(f"   Momentum: {technicals['momentum']}")
                
                return technicals
            else:
                print(f"   No data available")
                return None
                
        except Exception as e:
            print(f"   Error: {e}")
            return None
    
    def calculate_rsi(self, prices, period=14):
        """Calculate RSI indicator"""
        if len(prices) < period:
            return 50  # Default neutral
        
        gains = []
        losses = []
        
        for i in range(1, period):
            change = prices[i-1] - prices[i]  # Reversed because prices are desc
            if change > 0:
                gains.append(change)
                losses.append(0)
            else:
                gains.append(0)
                losses.append(abs(change))
        
        avg_gain = sum(gains) / period
        avg_loss = sum(losses) / period
        
        if avg_loss == 0:
            return 100
        
        rs = avg_gain / avg_loss
        rsi = 100 - (100 / (1 + rs))
        
        return rsi
    
    def get_fear_greed_index(self):
        """Get Fear & Greed Index from Alternative.me"""
        print("\n[SENTIMENT] Fetching Fear & Greed Index...")
        
        url = "https://api.alternative.me/fng/"
        
        try:
            response = requests.get(url)
            data = response.json()
            
            if 'data' in data and data['data']:
                fng = data['data'][0]
                sentiment = {
                    'value': int(fng['value']),
                    'classification': fng['value_classification'],
                    'timestamp': fng['timestamp']
                }
                
                print(f"   Index: {sentiment['value']} ({sentiment['classification']})")
                
                # Interpret for prediction
                if sentiment['value'] < 25:
                    sentiment['signal'] = 'extreme_fear_buy'
                elif sentiment['value'] > 75:
                    sentiment['signal'] = 'extreme_greed_sell'
                else:
                    sentiment['signal'] = 'neutral'
                
                return sentiment
            
        except Exception as e:
            print(f"   Error: {e}")
            return {'value': 50, 'classification': 'Neutral', 'signal': 'neutral'}
    
    def get_crypto_news(self):
        """Get latest crypto news from CryptoCompare"""
        print("\n[NEWS] Fetching latest crypto news...")
        
        url = "https://min-api.cryptocompare.com/data/v2/news/?lang=EN"
        
        try:
            response = requests.get(url)
            data = response.json()
            
            if 'Data' in data:
                news_items = data['Data'][:5]  # Get top 5 news
                
                processed_news = []
                for item in news_items:
                    news = {
                        'title': item['title'],
                        'source': item['source_info']['name'],
                        'published': datetime.fromtimestamp(item['published_on']).isoformat(),
                        'categories': item.get('categories', ''),
                        'sentiment': self.analyze_headline_sentiment(item['title'])
                    }
                    processed_news.append(news)
                    print(f"   • {news['title'][:60]}... ({news['sentiment']})")
                
                self.knowledge_base['news'] = processed_news
                return processed_news
            
        except Exception as e:
            print(f"   Error: {e}")
            return []
    
    def analyze_headline_sentiment(self, headline):
        """Simple sentiment analysis for headlines"""
        headline_lower = headline.lower()
        
        positive_words = ['surge', 'rally', 'gain', 'bull', 'adopt', 'approve', 'partner', 'launch', 'high', 'breakthrough']
        negative_words = ['crash', 'drop', 'fall', 'bear', 'ban', 'hack', 'scam', 'sell', 'low', 'concern']
        
        pos_count = sum(1 for word in positive_words if word in headline_lower)
        neg_count = sum(1 for word in negative_words if word in headline_lower)
        
        if pos_count > neg_count:
            return 'positive'
        elif neg_count > pos_count:
            return 'negative'
        else:
            return 'neutral'
    
    def generate_rag_prediction(self):
        """Generate prediction using all collected data"""
        print("\n[RAG PREDICTION] Analyzing all sources...")
        
        # Aggregate signals
        signals = {
            'bullish': 0,
            'bearish': 0,
            'neutral': 0
        }
        
        reasoning = []
        
        # 1. Technical Analysis
        if self.knowledge_base.get('technical_indicators'):
            tech = self.knowledge_base['technical_indicators']
            
            if tech['trend'] == 'bullish':
                signals['bullish'] += 2
                reasoning.append(f"Technical: Bullish trend detected")
            else:
                signals['bearish'] += 2
                reasoning.append(f"Technical: Bearish trend detected")
            
            if tech['rsi'] > 70:
                signals['bearish'] += 1
                reasoning.append(f"RSI {tech['rsi']:.0f}: Overbought")
            elif tech['rsi'] < 30:
                signals['bullish'] += 1
                reasoning.append(f"RSI {tech['rsi']:.0f}: Oversold")
        
        # 2. Market Data
        if self.knowledge_base.get('market_data'):
            market = self.knowledge_base['market_data']
            
            if market['change_percent'] > 3:
                signals['bearish'] += 1  # Potential correction
                reasoning.append(f"Large move {market['change_percent']:.1f}%: Correction possible")
            elif market['change_percent'] < -3:
                signals['bullish'] += 1  # Potential bounce
                reasoning.append(f"Large drop {market['change_percent']:.1f}%: Bounce possible")
        
        # 3. Sentiment Analysis
        fng = self.get_fear_greed_index()
        if fng['value'] < 25:
            signals['bullish'] += 2
            reasoning.append(f"Fear & Greed {fng['value']}: Extreme fear (contrarian buy)")
        elif fng['value'] > 75:
            signals['bearish'] += 2
            reasoning.append(f"Fear & Greed {fng['value']}: Extreme greed (contrarian sell)")
        
        # 4. News Sentiment
        if self.knowledge_base.get('news'):
            news_sentiment = {'positive': 0, 'negative': 0, 'neutral': 0}
            for news in self.knowledge_base['news']:
                news_sentiment[news['sentiment']] += 1
            
            if news_sentiment['positive'] > news_sentiment['negative']:
                signals['bullish'] += 1
                reasoning.append(f"News: {news_sentiment['positive']} positive articles")
            elif news_sentiment['negative'] > news_sentiment['positive']:
                signals['bearish'] += 1
                reasoning.append(f"News: {news_sentiment['negative']} negative articles")
        
        # Calculate final prediction
        total_signals = sum(signals.values())
        if total_signals == 0:
            prediction = 'NEUTRAL'
            confidence = 0
        else:
            if signals['bullish'] > signals['bearish']:
                prediction = 'BULLISH'
                confidence = (signals['bullish'] / total_signals) * 100
            elif signals['bearish'] > signals['bullish']:
                prediction = 'BEARISH'
                confidence = (signals['bearish'] / total_signals) * 100
            else:
                prediction = 'NEUTRAL'
                confidence = 50
        
        # Create prediction object
        prediction_obj = {
            'timestamp': datetime.now().isoformat(),
            'prediction': prediction,
            'confidence': f"{confidence:.1f}%",
            'signals': signals,
            'reasoning': reasoning,
            'data_sources': {
                'market_data': bool(self.knowledge_base.get('market_data')),
                'technical': bool(self.knowledge_base.get('technical_indicators')),
                'news': len(self.knowledge_base.get('news', [])),
                'sentiment': fng['classification']
            }
        }
        
        # Save prediction
        filename = self.predictions_dir / f"prediction_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(filename, 'w') as f:
            json.dump(prediction_obj, f, indent=2)
        
        print(f"\n{'='*50}")
        print(f"PREDICTION: {prediction}")
        print(f"Confidence: {confidence:.1f}%")
        print(f"{'='*50}")
        print("\nReasoning:")
        for r in reasoning:
            print(f"  • {r}")
        print(f"\nPrediction saved to: {filename.name}")
        
        return prediction_obj
    
    def run_complete_analysis(self, ticker="X:BTCUSD"):
        """Run complete analysis pipeline"""
        print(f"\n[COMPLETE ANALYSIS] Starting for {ticker}...")
        print("="*50)
        
        # Collect all data
        self.get_real_crypto_price(ticker)
        time.sleep(0.5)  # Rate limiting
        
        self.get_crypto_aggregates(ticker)
        time.sleep(0.5)
        
        self.get_crypto_news()
        time.sleep(0.5)
        
        # Generate prediction
        prediction = self.generate_rag_prediction()
        
        return prediction

def main():
    """Main program"""
    print("""
========================================
   Enhanced Crypto RAG System
   Real Data from Polygon.io
========================================
    """)
    
    rag = EnhancedCryptoRAG()
    
    while True:
        print("\n" + "="*50)
        print("MENU")
        print("="*50)
        print("1. Get real BTC price")
        print("2. Get technical indicators")
        print("3. Get latest news")
        print("4. Get Fear & Greed Index")
        print("5. Generate RAG prediction")
        print("6. Run complete analysis")
        print("0. Exit")
        print("-"*50)
        
        choice = input("Choose (0-6): ").strip()
        
        if choice == "1":
            rag.get_real_crypto_price()
        
        elif choice == "2":
            rag.get_crypto_aggregates()
        
        elif choice == "3":
            rag.get_crypto_news()
        
        elif choice == "4":
            rag.get_fear_greed_index()
        
        elif choice == "5":
            rag.generate_rag_prediction()
        
        elif choice == "6":
            ticker = input("Enter ticker (default X:BTCUSD): ").strip() or "X:BTCUSD"
            rag.run_complete_analysis(ticker)
        
        elif choice == "0":
            print("\nGoodbye!")
            break
        
        else:
            print("Invalid choice")

if __name__ == "__main__":
    main()