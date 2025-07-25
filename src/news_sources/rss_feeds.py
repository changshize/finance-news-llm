import asyncio
import aiohttp
import feedparser
from datetime import datetime
from typing import List, Dict, Optional
import logging
from dateutil import parser as date_parser

from .base import BaseNewsSource, NewsItem
from config import Config

class RSSFeedSource(BaseNewsSource):
    """RSS feed news source implementation."""
    
    def __init__(self, name: str, feed_url: str, logger: Optional[logging.Logger] = None):
        super().__init__(name, logger)
        self.feed_url = feed_url
        self.session = None
    
    async def _get_session(self) -> aiohttp.ClientSession:
        """Get or create aiohttp session."""
        if self.session is None or self.session.closed:
            timeout = aiohttp.ClientTimeout(total=30)
            self.session = aiohttp.ClientSession(timeout=timeout)
        return self.session
    
    async def fetch_news(self) -> List[NewsItem]:
        """Fetch news from RSS feed."""
        try:
            session = await self._get_session()
            
            async with session.get(self.feed_url) as response:
                if response.status != 200:
                    self.logger.error(f"Failed to fetch RSS feed {self.name}: HTTP {response.status}")
                    return []
                
                content = await response.text()
                
            # Parse RSS feed
            feed = feedparser.parse(content)
            
            if feed.bozo:
                self.logger.warning(f"RSS feed {self.name} has parsing issues: {feed.bozo_exception}")
            
            news_items = []
            
            for entry in feed.entries:
                try:
                    # Extract published date
                    published_date = None
                    if hasattr(entry, 'published'):
                        try:
                            published_date = date_parser.parse(entry.published)
                        except:
                            pass
                    
                    # Get content (try different fields)
                    content = ""
                    if hasattr(entry, 'summary'):
                        content = entry.summary
                    elif hasattr(entry, 'description'):
                        content = entry.description
                    elif hasattr(entry, 'content'):
                        if isinstance(entry.content, list) and entry.content:
                            content = entry.content[0].value
                        else:
                            content = str(entry.content)
                    
                    # Clean HTML tags from content
                    import re
                    content = re.sub(r'<[^>]+>', '', content)
                    
                    # Get author
                    author = getattr(entry, 'author', None)
                    
                    news_item = NewsItem(
                        title=entry.title,
                        content=content,
                        url=entry.link,
                        source=self.name,
                        published_date=published_date,
                        author=author
                    )
                    
                    news_items.append(news_item)
                    
                except Exception as e:
                    self.logger.error(f"Error parsing RSS entry from {self.name}: {e}")
                    continue
            
            self.logger.info(f"Fetched {len(news_items)} items from RSS feed: {self.name}")
            return news_items
            
        except Exception as e:
            self.logger.error(f"Error fetching RSS feed {self.name}: {e}")
            return []
    
    async def close(self):
        """Close the aiohttp session."""
        if self.session and not self.session.closed:
            await self.session.close()

class RSSFeedManager:
    """Manages multiple RSS feed sources."""
    
    def __init__(self, logger: Optional[logging.Logger] = None):
        self.logger = logger or logging.getLogger(__name__)
        self.sources = []
        
        # Initialize RSS sources from config
        for name, url in Config.RSS_FEEDS.items():
            source = RSSFeedSource(name, url, self.logger)
            self.sources.append(source)
    
    async def fetch_all_news(self) -> List[NewsItem]:
        """Fetch news from all RSS sources."""
        all_news = []
        
        # Fetch from all sources concurrently
        tasks = [source.fetch_news() for source in self.sources]
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        for i, result in enumerate(results):
            if isinstance(result, Exception):
                self.logger.error(f"Error fetching from {self.sources[i].name}: {result}")
            else:
                all_news.extend(result)
        
        # Filter for crypto relevance
        relevant_news = []
        for source in self.sources:
            source_news = [item for item in all_news if item.source == source.name]
            relevant_items = source.filter_relevant_news(source_news, Config.CRYPTO_KEYWORDS)
            relevant_news.extend(relevant_items)
        
        self.logger.info(f"Found {len(relevant_news)} relevant news items from RSS feeds")
        return relevant_news
    
    async def close_all(self):
        """Close all RSS source sessions."""
        for source in self.sources:
            await source.close()
