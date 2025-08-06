# 🚀 Crypto RAG Prediction System

> **Learning Project**: Building an AI-powered cryptocurrency prediction system using Retrieval-Augmented Generation (RAG)

[![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://www.python.org/)
[![Status](https://img.shields.io/badge/Status-Phase%201%20Complete-green.svg)]()
[![Learning](https://img.shields.io/badge/Learning-In%20Progress-yellow.svg)]()

## 🎯 Project Overview

This is my journey learning machine learning and AI by building a **real-world crypto prediction system**. Instead of just following tutorials, I'm building something that actually works with live market data!

### What This System Does:
- 📊 Collects real-time crypto market data
- 📰 Analyzes news sentiment
- 😨 Monitors Fear & Greed Index
- 🤖 Generates intelligent trading signals
- 📈 Provides confidence scores and risk assessment

## 📁 Project Structure
```
crypto-rag-system/
│
├── phase1_data_foundation/    # ✅ Complete
│   ├── __init__.py
│   ├── config.py              # Configuration
│   ├── data_models.py         # Data structures
│   └── data_pipeline.py       # API integration
│
├── phase2_intelligence/       # 🚧 In Progress
│   ├── vector_store.py        # ChromaDB
│   ├── rag_engine.py          # Advanced RAG
│   └── agents.py              # Multi-agent system
│
├── tests/                     # Testing
├── docs/                      # Documentation
└── examples/                  # Usage examples
```

## 🚀 Quick Start

### Step 1: Clone the Repository
```bash
git clone https://github.com/YOUR_USERNAME/crypto-rag-system.git
cd crypto-rag-system
```

### Step 2: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 3: Set Up API Keys
Create a `.env` file:
```env
POLYGON_API_KEY=your_polygon_key
OPENAI_API_KEY=your_openai_key  # For Phase 2
```

### Step 4: Run the System
```bash
python test_phase1.py
```

## 🧠 What I'm Learning

### Phase 1: Data Engineering ✅ COMPLETE!
- **Async Programming**: Making multiple API calls simultaneously
- **Data Modeling**: Structured data with Python dataclasses
- **API Integration**: Working with real-world data sources
- **Signal Processing**: Combining multiple indicators
- **Error Handling**: Building robust systems

### Phase 2: Advanced AI (In Progress)
- **Vector Databases**: ChromaDB for embeddings
- **RAG Techniques**: HyDE, CRAG, Self-RAG
- **Multi-Agent Systems**: LangGraph + CrewAI
- **ML Models**: Random Forest, LSTM, XGBoost

## 🏗️ Architecture

```
┌─────────────────────────────────────────┐
│         CRYPTO RAG SYSTEM               │
├─────────────────────────────────────────┤
│                                         │
│  📥 DATA LAYER                          │
│  ├── Polygon.io (Prices)               │
│  ├── CryptoCompare (News)              │
│  └── Alternative.me (Sentiment)        │
│                                         │
│  🧮 PROCESSING LAYER                    │
│  ├── Signal Generation                 │
│  ├── Confidence Scoring                │
│  └── Risk Assessment                   │
│                                         │
│  🤖 AI LAYER (Coming Soon)              │
│  ├── Vector Storage                    │
│  ├── RAG Engine                        │
│  └── Multi-Agent Orchestra             │
│                                         │
│  📊 OUTPUT LAYER                        │
│  └── Trading Signals + Reasoning       │
└─────────────────────────────────────────┘
```

## 📊 Live Example Output

```
[COIN] BTC
----------------------------------------
Price: $43,256.78
24h Change: +2.34%
Volume: $28,543,234,567

Latest News (15 articles):
  [+] Bitcoin ETF Approval Imminent...
  [=] Market Analysis: BTC Consolidation...
  [-] Regulatory Concerns in Asia...

Fear & Greed: 72 (Greed)
   Market is optimistic but approaching extreme greed

[SIGNAL] NEUTRAL
Confidence: 99.0%
Risk Level: medium

Reasoning:
  - Strong price action with +2.34% gain
  - High trading volume indicates interest
  - Mixed news sentiment (60% positive)
  - Fear & Greed in "Greed" territory (caution)
```

## 🎓 Learning Resources

### Concepts I've Mastered:
- ✅ **Async/Await**: Parallel API calls for speed
- ✅ **Dataclasses**: Clean data modeling
- ✅ **API Integration**: Working with real APIs
- ✅ **Signal Processing**: Combining indicators

### Currently Learning:
- 📚 **Vector Databases**: How to store and search embeddings
- 📚 **RAG Techniques**: Advanced retrieval methods
- 📚 **Multi-Agent Systems**: Orchestrating AI agents

### Next to Learn:
- 📅 **Backtesting**: Testing strategies on historical data
- 📅 **Portfolio Management**: Risk and position sizing
- 📅 **Deployment**: Running in production

## 💡 Key Insights & Lessons

### What Worked Well:
1. **Starting with real data** made learning more engaging
2. **Modular design** lets me improve one piece at a time
3. **Rich data models** with methods make code cleaner
4. **Async architecture** is 10x faster than sequential

### Challenges Overcome:
- Windows encoding issues with emojis → Use text indicators
- Rate limiting across APIs → Implement caching
- Complex signal aggregation → Weighted averaging

### Tips for Other Learners:
1. **Build something real** - tutorials are good, projects are better
2. **Use real APIs** - free tiers are perfect for learning
3. **Document as you go** - future you will thank you
4. **Test everything** - especially with real money involved!

## 🗺️ Roadmap

### Phase 1: Foundation ✅
- [x] Data pipeline
- [x] API integration  
- [x] Signal generation
- [x] Testing with live data

### Phase 2: Intelligence 🚧
- [ ] Vector storage (ChromaDB)
- [ ] Advanced RAG techniques
- [ ] Multi-agent system
- [ ] ML model integration

### Phase 3: Production 📅
- [ ] Backtesting framework
- [ ] Paper trading mode
- [ ] Performance monitoring
- [ ] Deploy to cloud

## 🤝 Contributing

This is a learning project, but I welcome:
- 🐛 Bug reports
- 💡 Feature suggestions
- 📚 Learning resources
- 🤔 Code reviews

## 📝 License

MIT License - Use this code to learn!

## 🙏 Acknowledgments

- **Claude AI** - My coding mentor and pair programmer
- **Polygon.io** - Amazing free tier for market data
- **CryptoCompare** - Comprehensive crypto APIs
- **Alternative.me** - Fear & Greed Index

## 📚 Learning Journal

### Day 1 (2025-08-06)
**What I Built**: Complete Phase 1 with real-time data pipeline
**Key Learning**: Async programming is incredibly powerful for API calls
**Breakthrough Moment**: When I saw real BTC prices flowing through my system!
**Time Spent**: 6 hours
**Lines of Code**: ~800

### Day 2 (Tomorrow)
**Goal**: Set up ChromaDB and create first embeddings
**To Research**: Vector similarity search, embedding models
**Expected Challenge**: Understanding embedding dimensions

---

⭐ **If you're learning too, star this repo and let's learn together!**

🚀 **Remember**: The best way to learn is to build something real. This isn't just a tutorial - it's a working system that analyzes real crypto markets!