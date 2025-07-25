from abc import ABC, abstractmethod
from typing import List, Dict, Optional
from datetime import datetime
import logging

class NewsItem:
    """Represents a single news item."""
    
    def __init__(
        self,
        title: str,
        content: str,
        url: str,
        source: str,
        published_date: Optional[datetime] = None,
        author: Optional[str] = None
    ):
        self.title = title
        self.content = content
        self.url = url
        self.source = source
        self.published_date = published_date or datetime.now()
        self.author = author
        self.hash_id = self._generate_hash()
    
    def _generate_hash(self) -> str:
        """Generate a unique hash for this news item."""
        import hashlib
        content_for_hash = f"{self.title}{self.url}{self.source}"
        return hashlib.md5(content_for_hash.encode('utf-8')).hexdigest()
    
    def to_dict(self) -> Dict:
        """Convert news item to dictionary."""
        return {
            'title': self.title,
            'content': self.content,
            'url': self.url,
            'source': self.source,
            'published_date': self.published_date.isoformat() if self.published_date else None,
            'author': self.author,
            'hash_id': self.hash_id
        }
    
    def __str__(self) -> str:
        return f"NewsItem(title='{self.title[:50]}...', source='{self.source}')"

class BaseNewsSource(ABC):
    """Abstract base class for news sources."""
    
    def __init__(self, name: str, logger: Optional[logging.Logger] = None):
        self.name = name
        self.logger = logger or logging.getLogger(__name__)
        self._seen_hashes = set()
    
    @abstractmethod
    async def fetch_news(self) -> List[NewsItem]:
        """Fetch news items from the source."""
        pass
    
    def is_duplicate(self, news_item: NewsItem) -> bool:
        """Check if news item has been seen before."""
        if news_item.hash_id in self._seen_hashes:
            return True
        self._seen_hashes.add(news_item.hash_id)
        return False
    
    def filter_relevant_news(self, news_items: List[NewsItem], keywords: List[str]) -> List[NewsItem]:
        """Filter news items for crypto relevance."""
        relevant_items = []
        
        for item in news_items:
            # Skip duplicates
            if self.is_duplicate(item):
                continue
            
            # Check if title or content contains crypto keywords
            text_to_check = f"{item.title} {item.content}".lower()
            if any(keyword.lower() in text_to_check for keyword in keywords):
                relevant_items.append(item)
                self.logger.debug(f"Found relevant news: {item.title[:50]}...")
        
        return relevant_items
    
    def __str__(self) -> str:
        return f"{self.__class__.__name__}(name='{self.name}')"
