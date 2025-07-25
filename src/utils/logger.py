import logging
import sys
from datetime import datetime
from pathlib import Path
from colorama import Fore, Style, init
from config import Config

# Initialize colorama for cross-platform colored output
init(autoreset=True)

class ColoredFormatter(logging.Formatter):
    """Custom formatter to add colors to log levels."""
    
    COLORS = {
        'DEBUG': Fore.CYAN,
        'INFO': Fore.GREEN,
        'WARNING': Fore.YELLOW,
        'ERROR': Fore.RED,
        'CRITICAL': Fore.MAGENTA + Style.BRIGHT,
    }
    
    def format(self, record):
        log_color = self.COLORS.get(record.levelname, '')
        record.levelname = f"{log_color}{record.levelname}{Style.RESET_ALL}"
        return super().format(record)

def setup_logger(name: str = 'crypto_alerts') -> logging.Logger:
    """Set up logger with both console and file handlers."""
    
    logger = logging.getLogger(name)
    logger.setLevel(getattr(logging, Config.LOG_LEVEL.upper()))
    
    # Clear existing handlers
    logger.handlers.clear()
    
    # Console handler with colors
    console_handler = logging.StreamHandler(sys.stdout)
    console_formatter = ColoredFormatter(
        '%(asctime)s | %(levelname)s | %(message)s',
        datefmt='%H:%M:%S'
    )
    console_handler.setFormatter(console_formatter)
    logger.addHandler(console_handler)
    
    # File handler
    log_file = Path(Config.LOG_FILE)
    file_handler = logging.FileHandler(log_file, encoding='utf-8')
    file_formatter = logging.Formatter(
        '%(asctime)s | %(levelname)s | %(name)s | %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    file_handler.setFormatter(file_formatter)
    logger.addHandler(file_handler)
    
    return logger

def log_alert(logger: logging.Logger, alert_data: dict):
    """Log an alert with special formatting."""
    importance = alert_data.get('importance', 0)
    sentiment = alert_data.get('sentiment', 'neutral')
    title = alert_data.get('title', 'Unknown')
    source = alert_data.get('source', 'Unknown')
    
    # Color code based on importance and sentiment
    if importance >= 9:
        color = Fore.RED + Style.BRIGHT
    elif importance >= 7:
        color = Fore.YELLOW + Style.BRIGHT
    else:
        color = Fore.CYAN
    
    sentiment_emoji = {
        'bullish': '🚀',
        'bearish': '📉',
        'neutral': '⚖️'
    }.get(sentiment, '❓')
    
    alert_msg = (
        f"{color}🚨 CRYPTO ALERT {sentiment_emoji}\n"
        f"Importance: {importance}/10 | Sentiment: {sentiment.upper()}\n"
        f"Source: {source}\n"
        f"Title: {title}{Style.RESET_ALL}"
    )
    
    logger.warning(alert_msg)
