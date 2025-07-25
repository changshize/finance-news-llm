import re
import hashlib
from datetime import datetime, timedelta
from typing import List, Dict, Optional
from urllib.parse import urlparse
import pytz

def clean_text(text: str) -> str:
    """Clean and normalize text for analysis."""
    if not text:
        return ""
    
    # Remove extra whitespace and newlines
    text = re.sub(r'\s+', ' ', text.strip())
    
    # Remove HTML tags if any
    text = re.sub(r'<[^>]+>', '', text)
    
    # Remove special characters but keep basic punctuation
    text = re.sub(r'[^\w\s.,!?;:\-$%]', '', text)
    
    return text

def extract_crypto_mentions(text: str) -> List[str]:
    """Extract cryptocurrency mentions from text."""
    crypto_patterns = [
        r'\b(?:BTC|Bitcoin)\b',
        r'\b(?:ETH|Ethereum)\b',
        r'\b(?:ADA|Cardano)\b',
        r'\b(?:SOL|Solana)\b',
        r'\b(?:DOT|Polkadot)\b',
        r'\b(?:LINK|Chainlink)\b',
        r'\b(?:DOGE|Dogecoin)\b',
        r'\b(?:SHIB|Shiba)\b',
        r'\b(?:USDT|Tether)\b',
        r'\b(?:USDC|USD Coin)\b',
        r'\$[A-Z]{2,10}\b',  # Generic crypto symbols like $BTC
    ]
    
    mentions = []
    for pattern in crypto_patterns:
        matches = re.findall(pattern, text, re.IGNORECASE)
        mentions.extend([match.upper() for match in matches])
    
    return list(set(mentions))  # Remove duplicates

def calculate_text_hash(text: str) -> str:
    """Calculate MD5 hash of text for deduplication."""
    return hashlib.md5(text.encode('utf-8')).hexdigest()

def is_recent_news(published_date: datetime, max_age_hours: int = 24) -> bool:
    """Check if news is within the specified age limit."""
    if not published_date:
        return True  # Assume recent if no date provided
    
    # Make sure published_date is timezone-aware
    if published_date.tzinfo is None:
        published_date = pytz.UTC.localize(published_date)
    
    now = datetime.now(pytz.UTC)
    age_limit = now - timedelta(hours=max_age_hours)
    
    return published_date >= age_limit

def extract_domain(url: str) -> str:
    """Extract domain name from URL."""
    try:
        parsed = urlparse(url)
        return parsed.netloc.lower()
    except:
        return "unknown"

def contains_crypto_keywords(text: str, keywords: List[str]) -> bool:
    """Check if text contains any cryptocurrency-related keywords."""
    text_lower = text.lower()
    return any(keyword.lower() in text_lower for keyword in keywords)

def format_alert_message(alert_data: Dict) -> str:
    """Format alert data into a readable message."""
    title = alert_data.get('title', 'Unknown')
    source = alert_data.get('source', 'Unknown')
    importance = alert_data.get('importance', 0)
    sentiment = alert_data.get('sentiment', 'neutral')
    url = alert_data.get('url', '')
    summary = alert_data.get('summary', '')
    crypto_mentions = alert_data.get('crypto_mentions', [])
    
    message = f"""
🚨 CRYPTO TRADING ALERT 🚨

📊 Importance: {importance}/10
📈 Sentiment: {sentiment.upper()}
🏷️ Cryptos: {', '.join(crypto_mentions) if crypto_mentions else 'General'}
📰 Source: {source}

📝 Title: {title}

💡 Summary: {summary}

🔗 URL: {url}

⏰ Detected at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC')}
    """.strip()
    
    return message

def rate_limit_key(source: str, identifier: str = "") -> str:
    """Generate a rate limiting key for API calls."""
    return f"{source}_{identifier}_{datetime.now().strftime('%Y%m%d_%H')}"

def validate_url(url: str) -> bool:
    """Validate if a string is a proper URL."""
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except:
        return False
