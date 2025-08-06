"""
Test Script for Phase 1: Data Foundation
Let's see our data pipeline in action!
"""

import asyncio
import json
from datetime import datetime
from phase1_data_foundation.data_pipeline import CryptoDataPipeline
from phase1_data_foundation.config import Config

async def test_data_pipeline():
    """Test the data pipeline with real data"""
    
    print("\n" + "="*60)
    print(">>> PHASE 1 TEST: Data Foundation")
    print("="*60)
    
    # Validate configuration
    print("\n[CONFIG] Checking configuration...")
    if Config.validate():
        print("[OK] Configuration valid")
    else:
        print("[ERROR] Configuration issues found")
        return
    
    # Initialize pipeline
    print("\n[INIT] Initializing data pipeline...")
    pipeline = CryptoDataPipeline(Config.to_dict())
    print("[OK] Pipeline initialized")
    
    # Health check
    print("\n[HEALTH] Running health check...")
    health = await pipeline.health_check()
    print("Health Status:")
    for source, status in health['sources'].items():
        emoji = "[OK]" if status == "healthy" else "[FAIL]"
        print(f"  {emoji} {source}: {status}")
    
    # Collect data for test symbols
    test_symbols = ['BTC', 'ETH']
    print(f"\n[DATA] Collecting data for {test_symbols}...")
    
    combined_signals = await pipeline.collect_all_data(test_symbols)
    
    # Display results
    print("\n" + "="*60)
    print("RESULTS")
    print("="*60)
    
    for symbol, signal in combined_signals.items():
        print(f"\n[COIN] {symbol}")
        print("-" * 40)
        
        # Market Data
        if signal.market_data:
            print(f"Price: ${signal.market_data.price:,.2f}")
            print(f"24h Change: {signal.market_data.change_24h:+.2f}%")
            print(f"Volume: ${signal.market_data.volume_24h:,.0f}")
        
        # News
        if signal.news_items:
            print(f"\nLatest News ({len(signal.news_items)} articles):")
            for news in signal.news_items[:3]:
                sentiment_emoji = "[+]" if news.sentiment_score > 0 else "[-]" if news.sentiment_score < 0 else "[=]"
                print(f"  {sentiment_emoji} {news.headline[:60]}...")
        
        # Sentiment
        if signal.sentiment:
            print(f"\nFear & Greed: {signal.sentiment.fear_greed_index} ({signal.sentiment.fear_greed_label})")
            print(f"   {signal.sentiment.get_market_mood()}")
        
        # Combined Signal
        print(f"\n[SIGNAL] {signal.overall_signal.name}")
        print(f"Confidence: {signal.confidence:.1%}")
        print(f"Risk Level: {signal.risk_level}")
        
        # Reasoning
        if signal.reasoning:
            print("\nReasoning:")
            for reason in signal.reasoning:
                print(f"  - {reason}")
        
        # Warnings & Opportunities
        if signal.warnings:
            print("\n[WARNING] Warnings:")
            for warning in signal.warnings:
                print(f"  - {warning}")
        
        if signal.opportunities:
            print("\n[OPPORTUNITY] Opportunities:")
            for opp in signal.opportunities:
                print(f"  - {opp}")
    
    # Save results to file
    print("\n[SAVE] Saving results...")
    output = {
        'timestamp': datetime.now().isoformat(),
        'signals': {}
    }
    
    for symbol, signal in combined_signals.items():
        output['signals'][symbol] = {
            'signal': signal.overall_signal.name,
            'confidence': signal.confidence,
            'risk_level': signal.risk_level,
            'reasoning': signal.reasoning
        }
    
    with open('phase1_test_results.json', 'w') as f:
        json.dump(output, f, indent=2)
    
    print("[OK] Results saved to phase1_test_results.json")
    
    print("\n" + "="*60)
    print("PHASE 1 TEST COMPLETE!")
    print("="*60)

def main():
    """Main entry point"""
    try:
        # Run the async test
        asyncio.run(test_data_pipeline())
    except KeyboardInterrupt:
        print("\n\nTest interrupted by user")
    except Exception as e:
        print(f"\n[ERROR] Test failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()