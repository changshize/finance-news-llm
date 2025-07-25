import os
from dotenv import load_dotenv
from typing import Dict, List

# Load environment variables
load_dotenv()

class Config:
    """Configuration management for the crypto trading alert system."""
    
    # LLM API Configuration
    OPENROUTER_API_KEY = os.getenv('OPENROUTER_API_KEY')
    DEEPSEEK_API_KEY = os.getenv('DEEPSEEK_API_KEY')
    
    # News API Configuration
    NEWS_API_KEY = os.getenv('NEWS_API_KEY')
    
    # Reddit API Configuration
    REDDIT_CLIENT_ID = os.getenv('REDDIT_CLIENT_ID')
    REDDIT_CLIENT_SECRET = os.getenv('REDDIT_CLIENT_SECRET')
    REDDIT_USER_AGENT = os.getenv('REDDIT_USER_AGENT', 'CryptoNewsBot/1.0')
    
    # Alert Configuration
    WEBHOOK_URL = os.getenv('WEBHOOK_URL')
    ALERT_THRESHOLD = int(os.getenv('ALERT_THRESHOLD', 7))
    
    # Monitoring Configuration
    CHECK_INTERVAL_MINUTES = int(os.getenv('CHECK_INTERVAL_MINUTES', 5))
    MAX_NEWS_AGE_HOURS = int(os.getenv('MAX_NEWS_AGE_HOURS', 24))
    ENABLE_SOCIAL_MONITORING = os.getenv('ENABLE_SOCIAL_MONITORING', 'true').lower() == 'true'
    ENABLE_RSS_MONITORING = os.getenv('ENABLE_RSS_MONITORING', 'true').lower() == 'true'
    ENABLE_NEWS_API = os.getenv('ENABLE_NEWS_API', 'true').lower() == 'true'
    
    # Logging Configuration
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
    LOG_FILE = os.getenv('LOG_FILE', 'crypto_alerts.log')
    
    # RSS Feed URLs
    RSS_FEEDS = {
        'coindesk': 'https://www.coindesk.com/arc/outboundfeeds/rss/',
        'cointelegraph': 'https://cointelegraph.com/rss',
        'cryptonews': 'https://cryptonews.com/news/feed/',
        'decrypt': 'https://decrypt.co/feed',
        'bitcoinist': 'https://bitcoinist.com/feed/',
    }
    
    # Crypto-related keywords for filtering
    CRYPTO_KEYWORDS = [
        'bitcoin', 'btc', 'ethereum', 'eth', 'cryptocurrency', 'crypto',
        'blockchain', 'defi', 'nft', 'altcoin', 'trading', 'exchange',
        'binance', 'coinbase', 'regulation', 'sec', 'cftc', 'fed',
        'inflation', 'interest rate', 'monetary policy', 'cbdc',
        'stablecoin', 'usdt', 'usdc', 'tether', 'solana', 'cardano',
        'polkadot', 'chainlink', 'dogecoin', 'shiba', 'meme coin'
    ]
    
    # Influential Twitter accounts to monitor
    TWITTER_ACCOUNTS = [
        'elonmusk', 'realDonaldTrump', 'jerome_powell', 'SEC_News',
        'cz_binance', 'brian_armstrong', 'VitalikButerin', 'michael_saylor'
    ]
    
    # Reddit subreddits to monitor
    REDDIT_SUBREDDITS = [
        'cryptocurrency', 'bitcoin', 'ethereum', 'cryptomarkets',
        'defi', 'altcoin', 'cryptonews', 'bitcoinmarkets'
    ]
    
    @classmethod
    def validate_config(cls) -> Dict[str, bool]:
        """Validate configuration and return status of each component."""
        status = {
            'llm_api': bool(cls.OPENROUTER_API_KEY or cls.DEEPSEEK_API_KEY),
            'news_api': bool(cls.NEWS_API_KEY) if cls.ENABLE_NEWS_API else True,
            'reddit_api': bool(cls.REDDIT_CLIENT_ID and cls.REDDIT_CLIENT_SECRET) if cls.ENABLE_SOCIAL_MONITORING else True,
            'webhook': bool(cls.WEBHOOK_URL) if cls.WEBHOOK_URL else True,
        }
        return status
    
    @classmethod
    def get_active_llm_provider(cls) -> str:
        """Determine which LLM provider to use based on available API keys."""
        if cls.OPENROUTER_API_KEY:
            return 'openrouter'
        elif cls.DEEPSEEK_API_KEY:
            return 'deepseek'
        else:
            return 'fallback'  # Use local sentiment analysis
