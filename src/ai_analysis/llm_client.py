import asyncio
import aiohttp
import json
from typing import Dict, Optional, List
import logging
from datetime import datetime

from config import Config

class LLMClient:
    """Client for interacting with various LLM APIs."""
    
    def __init__(self, logger: Optional[logging.Logger] = None):
        self.logger = logger or logging.getLogger(__name__)
        self.provider = Config.get_active_llm_provider()
        self.session = None
        
        # API configurations
        self.api_configs = {
            'openrouter': {
                'base_url': 'https://openrouter.ai/api/v1/chat/completions',
                'headers': {
                    'Authorization': f'Bearer {Config.OPENROUTER_API_KEY}',
                    'Content-Type': 'application/json',
                    'HTTP-Referer': 'https://github.com/changshize/finance-news-llm',
                    'X-Title': 'Crypto Trading Alert System'
                },
                'model': 'qwen/qwen-2.5-7b-instruct:free'  # Free model
            },
            'deepseek': {
                'base_url': 'https://api.deepseek.com/v1/chat/completions',
                'headers': {
                    'Authorization': f'Bearer {Config.DEEPSEEK_API_KEY}',
                    'Content-Type': 'application/json'
                },
                'model': 'deepseek-chat'
            }
        }
    
    async def _get_session(self) -> aiohttp.ClientSession:
        """Get or create aiohttp session."""
        if self.session is None or self.session.closed:
            timeout = aiohttp.ClientTimeout(total=60)
            self.session = aiohttp.ClientSession(timeout=timeout)
        return self.session
    
    async def analyze_news(self, title: str, content: str, source: str) -> Dict:
        """Analyze news using LLM and return structured analysis."""
        
        if self.provider == 'fallback':
            return await self._fallback_analysis(title, content)
        
        prompt = self._create_analysis_prompt(title, content, source)
        
        try:
            response = await self._call_llm_api(prompt)
            return self._parse_llm_response(response)
        except Exception as e:
            self.logger.error(f"LLM analysis failed, using fallback: {e}")
            return await self._fallback_analysis(title, content)
    
    def _create_analysis_prompt(self, title: str, content: str, source: str) -> str:
        """Create analysis prompt for the LLM."""
        return f"""
You are a cryptocurrency trading analyst. Analyze the following news and provide a structured assessment.

NEWS SOURCE: {source}
TITLE: {title}
CONTENT: {content[:1000]}...

Please analyze this news and respond with a JSON object containing:
1. "importance": A score from 1-10 indicating how much this news could impact crypto markets
2. "sentiment": Either "bullish", "bearish", or "neutral"
3. "summary": A brief 1-2 sentence summary of the key points
4. "trading_signal": Specific trading recommendation (e.g., "Consider long BTC", "Watch for volatility", "No immediate action")
5. "affected_cryptos": List of cryptocurrencies that might be most affected
6. "time_horizon": "immediate" (minutes-hours), "short" (days), or "long" (weeks-months)
7. "confidence": Your confidence in this analysis (1-10)

Focus on:
- Regulatory changes and government announcements
- Major institutional adoption or rejection
- Technical developments and partnerships
- Market manipulation or whale movements
- Macroeconomic factors affecting crypto

Respond ONLY with valid JSON, no additional text.
"""
    
    async def _call_llm_api(self, prompt: str) -> str:
        """Call the configured LLM API."""
        config = self.api_configs[self.provider]
        session = await self._get_session()
        
        payload = {
            "model": config['model'],
            "messages": [
                {"role": "user", "content": prompt}
            ],
            "temperature": 0.3,
            "max_tokens": 500
        }
        
        async with session.post(
            config['base_url'],
            headers=config['headers'],
            json=payload
        ) as response:
            if response.status != 200:
                error_text = await response.text()
                raise Exception(f"API call failed: {response.status} - {error_text}")
            
            result = await response.json()
            return result['choices'][0]['message']['content']
    
    def _parse_llm_response(self, response: str) -> Dict:
        """Parse LLM response and extract structured data."""
        try:
            # Try to extract JSON from response
            import re
            json_match = re.search(r'\{.*\}', response, re.DOTALL)
            if json_match:
                json_str = json_match.group()
                data = json.loads(json_str)
                
                # Validate required fields
                required_fields = ['importance', 'sentiment', 'summary']
                for field in required_fields:
                    if field not in data:
                        raise ValueError(f"Missing required field: {field}")
                
                # Ensure importance is within range
                data['importance'] = max(1, min(10, int(data.get('importance', 5))))
                
                # Ensure sentiment is valid
                valid_sentiments = ['bullish', 'bearish', 'neutral']
                if data.get('sentiment', '').lower() not in valid_sentiments:
                    data['sentiment'] = 'neutral'
                
                return data
            else:
                raise ValueError("No JSON found in response")
                
        except Exception as e:
            self.logger.error(f"Failed to parse LLM response: {e}")
            # Return fallback analysis
            return {
                'importance': 5,
                'sentiment': 'neutral',
                'summary': 'Analysis failed, manual review required',
                'trading_signal': 'Monitor situation',
                'affected_cryptos': [],
                'time_horizon': 'short',
                'confidence': 3
            }
    
    async def _fallback_analysis(self, title: str, content: str) -> Dict:
        """Fallback analysis using simple sentiment analysis."""
        try:
            from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
            analyzer = SentimentIntensityAnalyzer()
            
            # Analyze sentiment
            text = f"{title} {content}"
            scores = analyzer.polarity_scores(text)
            
            # Determine sentiment
            if scores['compound'] >= 0.1:
                sentiment = 'bullish'
            elif scores['compound'] <= -0.1:
                sentiment = 'bearish'
            else:
                sentiment = 'neutral'
            
            # Calculate importance based on keywords
            importance_keywords = {
                'regulation': 8, 'sec': 8, 'ban': 9, 'approval': 8,
                'etf': 7, 'institutional': 6, 'adoption': 6,
                'hack': 8, 'security': 7, 'partnership': 5,
                'upgrade': 6, 'fork': 7, 'halving': 8
            }
            
            importance = 3  # Base importance
            text_lower = text.lower()
            for keyword, score in importance_keywords.items():
                if keyword in text_lower:
                    importance = max(importance, score)
            
            return {
                'importance': importance,
                'sentiment': sentiment,
                'summary': title[:100] + '...' if len(title) > 100 else title,
                'trading_signal': f'Monitor {sentiment} sentiment',
                'affected_cryptos': [],
                'time_horizon': 'short',
                'confidence': 6
            }
            
        except Exception as e:
            self.logger.error(f"Fallback analysis failed: {e}")
            return {
                'importance': 5,
                'sentiment': 'neutral',
                'summary': 'Analysis unavailable',
                'trading_signal': 'Manual review required',
                'affected_cryptos': [],
                'time_horizon': 'short',
                'confidence': 1
            }
    
    async def close(self):
        """Close the aiohttp session."""
        if self.session and not self.session.closed:
            await self.session.close()
