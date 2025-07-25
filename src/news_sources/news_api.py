import asyncio
import aiohttp
from datetime import datetime, timedelta
from typing import List, Optional
import logging
from dateutil import parser as date_parser

from .base import BaseNewsSource, NewsItem
from config import Config

class NewsAPISource(BaseNewsSource):
    """NewsAPI.org news source implementation."""
    
    def __init__(self, logger: Optional[logging.Logger] = None):
        super().__init__("NewsAPI", logger)
        self.api_key = Config.NEWS_API_KEY
        self.base_url = "https://newsapi.org/v2"
        self.session = None
    
    async def _get_session(self) -> aiohttp.ClientSession:
        """Get or create aiohttp session."""
        if self.session is None or self.session.closed:
            timeout = aiohttp.ClientTimeout(total=30)
            headers = {
                'X-API-Key': self.api_key,
                'User-Agent': 'CryptoAlertSystem/1.0'
            }
            self.session = aiohttp.ClientSession(timeout=timeout, headers=headers)
        return self.session
    
    async def fetch_news(self) -> List[NewsItem]:
        """Fetch crypto-related news from NewsAPI."""
        if not self.api_key:
            self.logger.warning("NewsAPI key not configured, skipping")
            return []
        
        try:
            # Search for crypto-related news
            crypto_queries = [
                'cryptocurrency OR bitcoin OR ethereum',
                'crypto regulation OR SEC bitcoin',
                'blockchain OR DeFi OR NFT'
            ]
            
            all_news = []
            
            for query in crypto_queries:
                news_items = await self._fetch_query(query)
                all_news.extend(news_items)
                
                # Small delay between queries to respect rate limits
                await asyncio.sleep(1)
            
            # Remove duplicates based on URL
            seen_urls = set()
            unique_news = []
            for item in all_news:
                if item.url not in seen_urls:
                    seen_urls.add(item.url)
                    unique_news.append(item)
            
            self.logger.info(f"Fetched {len(unique_news)} unique items from NewsAPI")
            return unique_news
            
        except Exception as e:
            self.logger.error(f"Error fetching from NewsAPI: {e}")
            return []
    
    async def _fetch_query(self, query: str) -> List[NewsItem]:
        """Fetch news for a specific query."""
        session = await self._get_session()
        
        # Get news from last 24 hours
        from_date = (datetime.now() - timedelta(hours=24)).strftime('%Y-%m-%d')
        
        params = {
            'q': query,
            'from': from_date,
            'sortBy': 'publishedAt',
            'language': 'en',
            'pageSize': 20  # Max 20 articles per query
        }
        
        url = f"{self.base_url}/everything"
        
        async with session.get(url, params=params) as response:
            if response.status != 200:
                error_text = await response.text()
                self.logger.error(f"NewsAPI request failed: {response.status} - {error_text}")
                return []
            
            data = await response.json()
            
            if data['status'] != 'ok':
                self.logger.error(f"NewsAPI error: {data.get('message', 'Unknown error')}")
                return []
            
            news_items = []
            
            for article in data['articles']:
                try:
                    # Skip articles without content
                    if not article.get('title') or not article.get('description'):
                        continue
                    
                    # Parse published date
                    published_date = None
                    if article.get('publishedAt'):
                        try:
                            published_date = date_parser.parse(article['publishedAt'])
                        except:
                            pass
                    
                    # Combine description and content
                    content = article.get('description', '')
                    if article.get('content'):
                        content += f" {article['content']}"
                    
                    news_item = NewsItem(
                        title=article['title'],
                        content=content,
                        url=article['url'],
                        source=f"NewsAPI-{article.get('source', {}).get('name', 'Unknown')}",
                        published_date=published_date,
                        author=article.get('author')
                    )
                    
                    news_items.append(news_item)
                    
                except Exception as e:
                    self.logger.error(f"Error parsing NewsAPI article: {e}")
                    continue
            
            return news_items
    
    async def close(self):
        """Close the aiohttp session."""
        if self.session and not self.session.closed:
            await self.session.close()
