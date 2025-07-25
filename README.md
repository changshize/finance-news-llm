# 🚀 Cryptocurrency Trading Alert System

A real-time cryptocurrency trading alert system that monitors news sources and uses AI to identify potential arbitrage opportunities and market-moving events.

## 🌟 Features

### 📡 Real-time News Monitoring
- **RSS Feeds**: CoinDesk, CoinTelegraph, CryptoNews, Decrypt, Bitcoinist
- **News API**: Mainstream financial news with crypto filtering
- **Social Media**: Reddit monitoring (Twitter/X support planned)
- **Government/Regulatory**: SEC, CFTC announcements
- **Exchange News**: Major exchange announcements

### 🤖 AI Analysis Engine
- **Multiple LLM Support**: OpenRouter (free tier), DeepSeek, fallback sentiment analysis
- **Smart Analysis**: Sentiment classification, importance scoring (1-10)
- **Trading Signals**: Specific actionable recommendations
- **Crypto Detection**: Automatic identification of affected cryptocurrencies
- **Time Horizon**: Immediate, short-term, or long-term impact assessment

### 🚨 Alert System
- **Configurable Thresholds**: Set minimum importance scores for alerts
- **Multiple Channels**: Console, file logging, Discord/Slack webhooks
- **Rich Formatting**: Color-coded alerts with emojis and structured data
- **Alert History**: Persistent storage and statistics tracking
- **Deduplication**: Prevents spam from duplicate news

### 🏗️ Technical Features
- **Modular Architecture**: Easy to add new news sources and LLM providers
- **Async Processing**: High-performance concurrent news fetching
- **Rate Limiting**: Respects API limits and prevents blocking
- **Error Handling**: Robust error recovery and fallback mechanisms
- **Environment Configuration**: Simple setup with just API keys

## 🚀 Quick Start

### 1. Installation

```bash
# Clone the repository
git clone https://github.com/changshize/finance-news-llm.git
cd finance-news-llm

# Run the setup script
python setup.py
```

### 2. Configuration

Edit the `.env` file with your API keys:

```bash
# LLM API (choose one)
OPENROUTER_API_KEY=your_openrouter_api_key_here
# OR
DEEPSEEK_API_KEY=your_deepseek_api_key_here

# Optional: News API for broader coverage
NEWS_API_KEY=your_newsapi_key_here

# Optional: Webhook for notifications
WEBHOOK_URL=your_discord_or_slack_webhook_url

# Alert configuration
ALERT_THRESHOLD=7  # Minimum importance (1-10)
CHECK_INTERVAL_MINUTES=5
```

### 3. Run the System

```bash
python main.py
```

## 🔑 API Keys Setup

### OpenRouter (Recommended - Free Tier Available)
1. Visit [OpenRouter.ai](https://openrouter.ai/)
2. Sign up for a free account
3. Get your API key from the dashboard
4. Add to `.env`: `OPENROUTER_API_KEY=your_key_here`

### DeepSeek (Alternative - Very Affordable)
1. Visit [DeepSeek Platform](https://platform.deepseek.com/)
2. Create an account
3. Get your API key
4. Add to `.env`: `DEEPSEEK_API_KEY=your_key_here`

### NewsAPI (Optional - Free Tier: 1000 requests/day)
1. Visit [NewsAPI.org](https://newsapi.org/)
2. Sign up for a free account
3. Get your API key
4. Add to `.env`: `NEWS_API_KEY=your_key_here`

## 📊 Sample Output

```
🚀 Initializing Crypto Trading Alert System...
✅ RSS monitoring enabled for 5 feeds
🎯 Alert threshold set to 7/10
⏱️  Check interval: 5 minutes

🔍 Starting monitoring cycle...
📰 Found 12 relevant RSS news items

🚨 CRYPTO ALERT 🚀
Importance: 8/10 | Sentiment: BULLISH
Source: coindesk
Title: SEC Approves Bitcoin ETF Applications from Major Firms

💡 Summary: Major regulatory approval could drive significant institutional adoption
🔗 URL: https://example.com/news
⏰ Detected at: 2024-01-15 14:30:25 UTC
```

## 🏗️ Architecture

```
├── main.py                 # Main application entry point
├── config.py              # Configuration management
├── requirements.txt       # Python dependencies
├── .env.example          # Environment template
├── setup.py              # Setup script
└── src/
    ├── news_sources/     # News source implementations
    │   ├── base.py       # Base classes
    │   ├── rss_feeds.py  # RSS feed monitoring
    │   └── news_api.py   # NewsAPI integration
    ├── ai_analysis/      # AI analysis engine
    │   └── llm_client.py # LLM API client
    ├── alerts/           # Alert management
    │   └── alert_manager.py
    └── utils/            # Utility functions
        ├── logger.py     # Logging setup
        └── helpers.py    # Helper functions
```

## ⚙️ Configuration Options

| Variable | Description | Default |
|----------|-------------|---------|
| `ALERT_THRESHOLD` | Minimum importance score (1-10) | 7 |
| `CHECK_INTERVAL_MINUTES` | News check frequency | 5 |
| `MAX_NEWS_AGE_HOURS` | Maximum age of news to process | 24 |
| `ENABLE_RSS_MONITORING` | Enable RSS feed monitoring | true |
| `ENABLE_NEWS_API` | Enable NewsAPI monitoring | true |
| `LOG_LEVEL` | Logging level (DEBUG/INFO/WARNING/ERROR) | INFO |

## 🎯 Trading Signal Examples

The system generates specific trading recommendations:

- **"Consider long BTC position"** - Strong bullish news detected
- **"Watch for volatility in ETH"** - Uncertain but potentially impactful news
- **"Consider short positions"** - Bearish regulatory news
- **"Monitor DeFi tokens"** - Sector-specific developments
- **"No immediate action"** - Neutral or low-impact news

## 📈 Monitoring Sources

### RSS Feeds (Always Active)
- CoinDesk - Leading crypto news
- CoinTelegraph - Crypto and blockchain news
- CryptoNews - Market analysis and updates
- Decrypt - Web3 and crypto culture
- Bitcoinist - Bitcoin and altcoin news

### News API Sources (Optional)
- Bloomberg, Reuters, CNBC crypto sections
- Financial Times, Wall Street Journal
- TechCrunch, Ars Technica blockchain coverage

### Social Media (Planned)
- Twitter/X influential accounts monitoring
- Reddit crypto communities
- Telegram channels

## 🔧 Extending the System

### Adding New News Sources

1. Create a new class inheriting from `BaseNewsSource`
2. Implement the `fetch_news()` method
3. Add to the main monitoring loop

### Adding New LLM Providers

1. Add API configuration to `config.py`
2. Implement the provider in `llm_client.py`
3. Update the provider selection logic

## 📝 Logging and Monitoring

- **Console Output**: Real-time colored alerts and status
- **File Logging**: Detailed logs in `crypto_alerts.log`
- **Alert Storage**: Individual alerts saved in `alerts/` directory
- **Statistics**: 24-hour alert summaries and trends

## 🛡️ Error Handling

- **Graceful Degradation**: Falls back to sentiment analysis if LLM fails
- **Rate Limiting**: Respects API limits to prevent blocking
- **Retry Logic**: Automatic retry for transient failures
- **Duplicate Detection**: Prevents processing the same news multiple times

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Add your improvements
4. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## ⚠️ Disclaimer

This system is for informational purposes only. Always do your own research before making trading decisions. Cryptocurrency trading involves significant risk.

## 🆘 Support

- Check the logs in `crypto_alerts.log` for detailed error information
- Ensure your API keys are correctly configured in `.env`
- Verify your internet connection for news source access
- Check API rate limits if you're getting errors

---

**Happy Trading! 🚀📈**
