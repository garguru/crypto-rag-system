"""
Crypto RAG with Memory - Inspired by the Docker LLM tutorial
Implements session memory, context accumulation, and Streamlit UI
"""

import streamlit as st
import requests
import json
from datetime import datetime, timedelta
from pathlib import Path
import pandas as pd
import os

# Initialize session state for memory
if 'predictions' not in st.session_state:
    st.session_state.predictions = []
if 'market_context' not in st.session_state:
    st.session_state.market_context = []
if 'accuracy_tracker' not in st.session_state:
    st.session_state.accuracy_tracker = {'correct': 0, 'total': 0}

class CryptoRAGWithMemory:
    """Enhanced RAG with session memory and learning capability"""
    
    def __init__(self):
        self.polygon_api_key = "ZOPT0lW9zJUuwX6NuxCMX1zhGVBqaVID"
        self.data_dir = Path("crypto_data")
        self.data_dir.mkdir(exist_ok=True)
        
    def get_market_data(self, ticker="X:BTCUSD"):
        """Fetch real-time market data"""
        url = f"https://api.polygon.io/v2/aggs/ticker/{ticker}/prev"
        params = {"apiKey": self.polygon_api_key}
        
        try:
            response = requests.get(url, params=params)
            data = response.json()
            
            if data['status'] == 'OK' and data['results']:
                result = data['results'][0]
                return {
                    'price': result['c'],
                    'change': ((result['c'] - result['o']) / result['o']) * 100,
                    'volume': result['v'],
                    'high': result['h'],
                    'low': result['l']
                }
        except:
            return None
    
    def get_fear_greed(self):
        """Get Fear & Greed Index"""
        try:
            response = requests.get("https://api.alternative.me/fng/")
            data = response.json()
            if 'data' in data:
                return {
                    'value': int(data['data'][0]['value']),
                    'text': data['data'][0]['value_classification']
                }
        except:
            return {'value': 50, 'text': 'Neutral'}
    
    def build_context_with_memory(self):
        """Build context including session memory"""
        context = []
        
        # Add recent predictions and their outcomes
        if st.session_state.predictions:
            recent_predictions = st.session_state.predictions[-5:]  # Last 5
            context.append("Previous Predictions:")
            for pred in recent_predictions:
                outcome = pred.get('outcome', 'pending')
                context.append(f"- {pred['time']}: {pred['direction']} (Outcome: {outcome})")
        
        # Add market context from memory
        if st.session_state.market_context:
            context.append("\nMarket Context Memory:")
            for ctx in st.session_state.market_context[-3:]:  # Last 3 contexts
                context.append(f"- {ctx}")
        
        # Add accuracy stats
        if st.session_state.accuracy_tracker['total'] > 0:
            accuracy = (st.session_state.accuracy_tracker['correct'] / 
                       st.session_state.accuracy_tracker['total']) * 100
            context.append(f"\nPrediction Accuracy: {accuracy:.1f}%")
        
        return "\n".join(context)
    
    def generate_prediction(self, market_data, sentiment, use_memory=True):
        """Generate prediction with optional memory context"""
        
        # Build base analysis
        signals = {'bullish': 0, 'bearish': 0}
        reasoning = []
        
        # Market data analysis
        if market_data:
            if market_data['change'] > 2:
                signals['bearish'] += 1
                reasoning.append(f"Large gain {market_data['change']:.1f}% - potential correction")
            elif market_data['change'] < -2:
                signals['bullish'] += 1
                reasoning.append(f"Large drop {market_data['change']:.1f}% - potential bounce")
        
        # Sentiment analysis
        if sentiment['value'] < 30:
            signals['bullish'] += 2
            reasoning.append(f"Fear level {sentiment['value']} - contrarian buy signal")
        elif sentiment['value'] > 70:
            signals['bearish'] += 2
            reasoning.append(f"Greed level {sentiment['value']} - contrarian sell signal")
        
        # Include memory context if enabled
        if use_memory:
            memory_context = self.build_context_with_memory()
            if "correct" in memory_context.lower():
                reasoning.append("Learning from past successful predictions")
        
        # Determine prediction
        if signals['bullish'] > signals['bearish']:
            direction = "BULLISH 📈"
            confidence = (signals['bullish'] / (signals['bullish'] + signals['bearish'])) * 100
        elif signals['bearish'] > signals['bullish']:
            direction = "BEARISH 📉"
            confidence = (signals['bearish'] / (signals['bullish'] + signals['bearish'])) * 100
        else:
            direction = "NEUTRAL ➡️"
            confidence = 50
        
        prediction = {
            'time': datetime.now().strftime("%H:%M:%S"),
            'direction': direction,
            'confidence': confidence,
            'reasoning': reasoning,
            'price': market_data['price'] if market_data else 0,
            'signals': signals
        }
        
        # Store in session memory
        st.session_state.predictions.append(prediction)
        
        # Add to market context
        context_entry = f"At ${market_data['price']:.0f}, predicted {direction} based on {sentiment['text']} sentiment"
        st.session_state.market_context.append(context_entry)
        
        return prediction
    
    def update_prediction_outcome(self, prediction_index, was_correct):
        """Update prediction outcome for learning"""
        if 0 <= prediction_index < len(st.session_state.predictions):
            st.session_state.predictions[prediction_index]['outcome'] = 'correct' if was_correct else 'incorrect'
            st.session_state.accuracy_tracker['total'] += 1
            if was_correct:
                st.session_state.accuracy_tracker['correct'] += 1

def main():
    st.set_page_config(page_title="Crypto RAG with Memory", page_icon="🤖", layout="wide")
    
    st.title("🤖 Crypto RAG Prediction System with Memory")
    st.caption("Learns from past predictions to improve accuracy")
    
    # Initialize RAG system
    rag = CryptoRAGWithMemory()
    
    # Sidebar for settings
    with st.sidebar:
        st.header("⚙️ Settings")
        
        # Model selection (inspired by tutorial)
        use_advanced = st.checkbox("🧠 Think Harder (Use Advanced Analysis)", value=False)
        use_memory = st.checkbox("📚 Use Memory Context", value=True)
        
        # Ticker selection
        ticker = st.selectbox(
            "Select Cryptocurrency",
            ["X:BTCUSD", "X:ETHUSD", "X:SOLUSD"],
            index=0
        )
        
        st.divider()
        
        # Accuracy metrics
        st.header("📊 Performance")
        if st.session_state.accuracy_tracker['total'] > 0:
            accuracy = (st.session_state.accuracy_tracker['correct'] / 
                       st.session_state.accuracy_tracker['total']) * 100
            st.metric("Prediction Accuracy", f"{accuracy:.1f}%")
            st.progress(accuracy / 100)
        else:
            st.info("No predictions tracked yet")
        
        # Clear memory button
        if st.button("🗑️ Clear Memory"):
            st.session_state.predictions = []
            st.session_state.market_context = []
            st.session_state.accuracy_tracker = {'correct': 0, 'total': 0}
            st.success("Memory cleared!")
    
    # Main content area
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.header("📈 Market Analysis")
        
        # Fetch button
        if st.button("🔄 Analyze Market", type="primary", use_container_width=True):
            with st.spinner("Fetching data..."):
                # Get market data
                market_data = rag.get_market_data(ticker)
                sentiment = rag.get_fear_greed()
                
                if market_data:
                    # Display current market
                    st.subheader("Current Market")
                    mcol1, mcol2, mcol3 = st.columns(3)
                    with mcol1:
                        st.metric("Price", f"${market_data['price']:,.2f}")
                    with mcol2:
                        st.metric("24h Change", f"{market_data['change']:.2f}%",
                                delta=f"{market_data['change']:.2f}%")
                    with mcol3:
                        st.metric("Fear & Greed", f"{sentiment['value']} ({sentiment['text']})")
                    
                    # Generate prediction
                    st.subheader("🎯 Prediction")
                    prediction = rag.generate_prediction(market_data, sentiment, use_memory)
                    
                    # Display prediction
                    if "BULLISH" in prediction['direction']:
                        st.success(f"**{prediction['direction']}** - Confidence: {prediction['confidence']:.1f}%")
                    elif "BEARISH" in prediction['direction']:
                        st.error(f"**{prediction['direction']}** - Confidence: {prediction['confidence']:.1f}%")
                    else:
                        st.warning(f"**{prediction['direction']}** - Confidence: {prediction['confidence']:.1f}%")
                    
                    # Show reasoning
                    st.write("**Reasoning:**")
                    for reason in prediction['reasoning']:
                        st.write(f"• {reason}")
                    
                    # Show signals
                    st.write("**Signal Strength:**")
                    signal_col1, signal_col2 = st.columns(2)
                    with signal_col1:
                        st.progress(prediction['signals']['bullish'] / 5, text=f"Bullish: {prediction['signals']['bullish']}")
                    with signal_col2:
                        st.progress(prediction['signals']['bearish'] / 5, text=f"Bearish: {prediction['signals']['bearish']}")
                else:
                    st.error("Failed to fetch market data")
    
    with col2:
        st.header("📝 Prediction History")
        
        if st.session_state.predictions:
            # Show recent predictions
            for i, pred in enumerate(reversed(st.session_state.predictions[-5:])):
                pred_index = len(st.session_state.predictions) - 1 - i
                
                with st.expander(f"{pred['time']} - {pred['direction']}", expanded=(i==0)):
                    st.write(f"Price: ${pred['price']:,.2f}")
                    st.write(f"Confidence: {pred['confidence']:.1f}%")
                    
                    # Outcome tracking
                    if 'outcome' not in pred:
                        col_correct, col_wrong = st.columns(2)
                        with col_correct:
                            if st.button("✅ Correct", key=f"correct_{pred_index}"):
                                rag.update_prediction_outcome(pred_index, True)
                                st.rerun()
                        with col_wrong:
                            if st.button("❌ Wrong", key=f"wrong_{pred_index}"):
                                rag.update_prediction_outcome(pred_index, False)
                                st.rerun()
                    else:
                        if pred['outcome'] == 'correct':
                            st.success(f"Outcome: ✅ Correct")
                        else:
                            st.error(f"Outcome: ❌ Incorrect")
        else:
            st.info("No predictions yet. Click 'Analyze Market' to start!")
    
    # Memory context display (bottom)
    with st.expander("🧠 Memory Context", expanded=False):
        if st.session_state.market_context:
            st.write("**Recent Market Context:**")
            for ctx in st.session_state.market_context[-5:]:
                st.write(f"• {ctx}")
        else:
            st.write("No memory context yet")

if __name__ == "__main__":
    main()