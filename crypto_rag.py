"""
Crypto RAG System - Financial Predictions with Context
Combines multiple data sources for informed crypto predictions
"""

import os
import json
from datetime import datetime, timedelta
from pathlib import Path
import requests

class CryptoRAG:
    """RAG system specialized for crypto market analysis"""
    
    def __init__(self):
        self.project_dir = Path(__file__).parent
        self.data_dir = self.project_dir / "crypto_data"
        self.data_dir.mkdir(exist_ok=True)
        
        # Different data sources
        self.news_dir = self.data_dir / "news"
        self.analysis_dir = self.data_dir / "analysis"
        self.metrics_dir = self.data_dir / "metrics"
        self.predictions_dir = self.data_dir / "predictions"
        
        for d in [self.news_dir, self.analysis_dir, self.metrics_dir, self.predictions_dir]:
            d.mkdir(exist_ok=True)
        
        # Knowledge base
        self.knowledge_base = {
            'news': [],
            'technical_analysis': [],
            'on_chain_metrics': [],
            'social_sentiment': [],
            'historical_patterns': []
        }
        
        print(">>> Crypto RAG System Initialized")
        print(f">>> Data directory: {self.data_dir}")
    
    def collect_market_data(self, symbol="BTC"):
        """Collect current market data"""
        print(f"\n[COLLECT] Gathering {symbol} market data...")
        
        # Simulated data collection (replace with real APIs)
        market_data = {
            'symbol': symbol,
            'timestamp': datetime.now().isoformat(),
            'price': 43250.00,  # Simulated
            'volume_24h': 28500000000,
            '24h_change': 2.3,
            'market_cap': 847000000000,
            'fear_greed_index': 65,  # 0-100
            'rsi': 58,  # Relative Strength Index
            'moving_avg_50': 42800,
            'moving_avg_200': 38500
        }
        
        # Save market data
        filename = self.metrics_dir / f"{symbol}_{datetime.now().strftime('%Y%m%d_%H%M')}.json"
        with open(filename, 'w') as f:
            json.dump(market_data, f, indent=2)
        
        print(f"   Price: ${market_data['price']:,.2f}")
        print(f"   24h Change: {market_data['24h_change']}%")
        print(f"   Fear/Greed: {market_data['fear_greed_index']}")
        
        return market_data
    
    def analyze_news_sentiment(self):
        """Analyze crypto news for sentiment"""
        print("\n[NEWS] Analyzing news sentiment...")
        
        # Simulated news analysis
        news_items = [
            {
                'headline': 'Major Institution Announces Bitcoin Purchase',
                'sentiment': 'positive',
                'impact': 'high',
                'source': 'CoinDesk'
            },
            {
                'headline': 'Regulatory Clarity Expected Next Month',
                'sentiment': 'positive', 
                'impact': 'medium',
                'source': 'Bloomberg'
            },
            {
                'headline': 'Network Hashrate Reaches All-Time High',
                'sentiment': 'positive',
                'impact': 'medium',
                'source': 'Bitcoin Magazine'
            }
        ]
        
        # Calculate overall sentiment
        sentiment_scores = {'positive': 0, 'negative': 0, 'neutral': 0}
        for news in news_items:
            sentiment_scores[news['sentiment']] += 1
        
        self.knowledge_base['news'] = news_items
        
        print(f"   Analyzed {len(news_items)} news items")
        print(f"   Sentiment: {sentiment_scores}")
        
        return sentiment_scores
    
    def technical_analysis(self, market_data):
        """Perform technical analysis"""
        print("\n[TECHNICAL] Running technical analysis...")
        
        analysis = {
            'trend': 'bullish' if market_data['price'] > market_data['moving_avg_50'] else 'bearish',
            'momentum': 'strong' if market_data['rsi'] > 50 else 'weak',
            'support_level': market_data['moving_avg_200'],
            'resistance_level': market_data['price'] * 1.05,
            'volatility': 'moderate',
            'volume_trend': 'increasing'
        }
        
        # Signal generation
        signals = []
        if analysis['trend'] == 'bullish' and market_data['rsi'] < 70:
            signals.append('BUY signal: Bullish trend with room to grow')
        if market_data['rsi'] > 70:
            signals.append('CAUTION: Overbought territory')
        if market_data['price'] < market_data['moving_avg_200']:
            signals.append('WARNING: Price below 200 MA')
        
        self.knowledge_base['technical_analysis'] = [analysis]
        
        print(f"   Trend: {analysis['trend']}")
        print(f"   Momentum: {analysis['momentum']}")
        for signal in signals:
            print(f"   Signal: {signal}")
        
        return analysis, signals
    
    def on_chain_analysis(self):
        """Analyze on-chain metrics"""
        print("\n[ON-CHAIN] Analyzing blockchain metrics...")
        
        # Simulated on-chain data
        on_chain = {
            'active_addresses': 950000,
            'exchange_inflow': 'decreasing',  # Bullish
            'exchange_outflow': 'increasing',  # Bullish
            'long_term_holder_supply': 'increasing',
            'miner_revenue': 'stable',
            'network_difficulty': 'increasing'
        }
        
        # Interpret metrics
        interpretations = []
        if on_chain['exchange_outflow'] == 'increasing':
            interpretations.append('Bullish: Coins moving to cold storage')
        if on_chain['long_term_holder_supply'] == 'increasing':
            interpretations.append('Bullish: HODLers accumulating')
        
        self.knowledge_base['on_chain_metrics'] = [on_chain]
        
        print(f"   Active addresses: {on_chain['active_addresses']:,}")
        print(f"   Exchange flow: {on_chain['exchange_inflow']}/{on_chain['exchange_outflow']}")
        
        return on_chain, interpretations
    
    def generate_prediction(self, timeframe="24h"):
        """Generate prediction based on all data sources"""
        print(f"\n[PREDICT] Generating {timeframe} prediction...")
        
        # Aggregate all signals
        bullish_signals = 0
        bearish_signals = 0
        
        # Check technical analysis
        if self.knowledge_base['technical_analysis']:
            ta = self.knowledge_base['technical_analysis'][0]
            if ta['trend'] == 'bullish':
                bullish_signals += 2
            else:
                bearish_signals += 2
        
        # Check news sentiment
        if self.knowledge_base['news']:
            positive_news = sum(1 for n in self.knowledge_base['news'] if n['sentiment'] == 'positive')
            negative_news = sum(1 for n in self.knowledge_base['news'] if n['sentiment'] == 'negative')
            bullish_signals += positive_news
            bearish_signals += negative_news
        
        # Check on-chain metrics
        if self.knowledge_base['on_chain_metrics']:
            on_chain = self.knowledge_base['on_chain_metrics'][0]
            if on_chain['exchange_outflow'] == 'increasing':
                bullish_signals += 1
            if on_chain['long_term_holder_supply'] == 'increasing':
                bullish_signals += 1
        
        # Generate prediction
        total_signals = bullish_signals + bearish_signals
        if total_signals == 0:
            confidence = 0
            direction = "neutral"
        else:
            bullish_ratio = bullish_signals / total_signals
            confidence = abs(bullish_ratio - 0.5) * 200  # 0-100%
            direction = "bullish" if bullish_ratio > 0.5 else "bearish"
        
        prediction = {
            'timestamp': datetime.now().isoformat(),
            'timeframe': timeframe,
            'direction': direction,
            'confidence': f"{confidence:.1f}%",
            'bullish_signals': bullish_signals,
            'bearish_signals': bearish_signals,
            'reasoning': self._generate_reasoning()
        }
        
        # Save prediction
        filename = self.predictions_dir / f"prediction_{datetime.now().strftime('%Y%m%d_%H%M')}.json"
        with open(filename, 'w') as f:
            json.dump(prediction, f, indent=2)
        
        return prediction
    
    def _generate_reasoning(self):
        """Generate explanation for prediction"""
        reasoning = []
        
        if self.knowledge_base['technical_analysis']:
            ta = self.knowledge_base['technical_analysis'][0]
            reasoning.append(f"Technical: {ta['trend']} trend with {ta['momentum']} momentum")
        
        if self.knowledge_base['news']:
            news_count = len(self.knowledge_base['news'])
            reasoning.append(f"News: Analyzed {news_count} recent articles")
        
        if self.knowledge_base['on_chain_metrics']:
            reasoning.append("On-chain: Exchange outflows suggest accumulation")
        
        return reasoning
    
    def ask_question(self, question):
        """Answer questions about crypto market"""
        print(f"\n[QUERY] {question}")
        
        # Simple keyword-based responses
        question_lower = question.lower()
        
        if "predict" in question_lower or "forecast" in question_lower:
            prediction = self.generate_prediction()
            return f"""
Based on current analysis:
- Direction: {prediction['direction'].upper()}
- Confidence: {prediction['confidence']}
- Bullish signals: {prediction['bullish_signals']}
- Bearish signals: {prediction['bearish_signals']}

Reasoning:
{chr(10).join(f'• {r}' for r in prediction['reasoning'])}
"""
        
        elif "news" in question_lower:
            if self.knowledge_base['news']:
                news_summary = "\n".join([f"• {n['headline']} ({n['sentiment']})" 
                                         for n in self.knowledge_base['news'][:3]])
                return f"Recent news:\n{news_summary}"
            return "No recent news loaded. Run news analysis first."
        
        elif "technical" in question_lower:
            if self.knowledge_base['technical_analysis']:
                ta = self.knowledge_base['technical_analysis'][0]
                return f"""
Technical Analysis:
- Trend: {ta['trend']}
- Momentum: {ta['momentum']}
- Support: ${ta['support_level']:,.0f}
- Resistance: ${ta['resistance_level']:,.0f}
"""
            return "No technical analysis available. Run analysis first."
        
        else:
            return "Please ask about predictions, news, or technical analysis."

def main():
    """Main interactive loop"""
    print("""
========================================
   Crypto RAG Prediction System       
   Multi-Source Market Analysis       
========================================
    """)
    
    rag = CryptoRAG()
    
    # Menu
    while True:
        print("\n" + "="*50)
        print("CRYPTO ANALYSIS MENU")
        print("="*50)
        print("1. Collect market data (BTC)")
        print("2. Analyze news sentiment")
        print("3. Run technical analysis")
        print("4. Analyze on-chain metrics")
        print("5. Generate prediction")
        print("6. Ask question")
        print("7. Run full analysis (all above)")
        print("0. Exit")
        print("-"*50)
        
        choice = input("Choose (0-7): ").strip()
        
        if choice == "1":
            symbol = input("Enter symbol (default BTC): ").strip() or "BTC"
            market_data = rag.collect_market_data(symbol)
        
        elif choice == "2":
            rag.analyze_news_sentiment()
        
        elif choice == "3":
            # Need market data first
            market_data = rag.collect_market_data()
            rag.technical_analysis(market_data)
        
        elif choice == "4":
            rag.on_chain_analysis()
        
        elif choice == "5":
            timeframe = input("Timeframe (24h/7d/30d): ").strip() or "24h"
            prediction = rag.generate_prediction(timeframe)
            print(f"\n{'='*50}")
            print(f"PREDICTION: {prediction['direction'].upper()}")
            print(f"Confidence: {prediction['confidence']}")
            print(f"{'='*50}")
            print("Reasoning:")
            for reason in prediction['reasoning']:
                print(f"  • {reason}")
        
        elif choice == "6":
            question = input("\nAsk your question: ").strip()
            if question:
                answer = rag.ask_question(question)
                print(answer)
        
        elif choice == "7":
            print("\n[RUNNING FULL ANALYSIS]")
            market_data = rag.collect_market_data()
            rag.analyze_news_sentiment()
            rag.technical_analysis(market_data)
            rag.on_chain_analysis()
            prediction = rag.generate_prediction()
            print(f"\n{'='*50}")
            print(f"FINAL PREDICTION: {prediction['direction'].upper()}")
            print(f"Confidence: {prediction['confidence']}")
            print(f"{'='*50}")
        
        elif choice == "0":
            print("\nGoodbye!")
            break

if __name__ == "__main__":
    main()