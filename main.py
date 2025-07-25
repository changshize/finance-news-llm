#!/usr/bin/env python3
"""
Cryptocurrency Trading Alert System
Real-time news monitoring with AI analysis for crypto trading opportunities
"""

import asyncio
import signal
import sys
from datetime import datetime
from typing import List, Dict

from config import Config
from src.utils.logger import setup_logger
from src.news_sources.rss_feeds import RSSFeedManager
from src.news_sources.news_api import NewsAPISource
from src.ai_analysis.llm_client import LLMClient
from src.alerts.alert_manager import AlertManager

class CryptoAlertSystem:
    """Main application class for the crypto alert system."""
    
    def __init__(self):
        self.logger = setup_logger()
        self.rss_manager = None
        self.news_api_source = None
        self.llm_client = None
        self.alert_manager = None
        self.running = False
        
        # Setup signal handlers for graceful shutdown
        signal.signal(signal.SIGINT, self._signal_handler)
        signal.signal(signal.SIGTERM, self._signal_handler)
    
    def _signal_handler(self, signum, frame):
        """Handle shutdown signals."""
        self.logger.info(f"Received signal {signum}, shutting down gracefully...")
        self.running = False
    
    async def initialize(self):
        """Initialize all system components."""
        self.logger.info("🚀 Initializing Crypto Trading Alert System...")
        
        # Validate configuration
        config_status = Config.validate_config()
        self.logger.info("Configuration status:")
        for component, status in config_status.items():
            status_emoji = "✅" if status else "❌"
            self.logger.info(f"  {status_emoji} {component}: {'OK' if status else 'Missing/Invalid'}")
        
        if not config_status['llm_api']:
            self.logger.warning("⚠️  No LLM API configured, using fallback sentiment analysis")
        
        # Initialize components
        if Config.ENABLE_RSS_MONITORING:
            self.rss_manager = RSSFeedManager(self.logger)
            self.logger.info(f"📡 RSS monitoring enabled for {len(Config.RSS_FEEDS)} feeds")

        if Config.ENABLE_NEWS_API and Config.NEWS_API_KEY:
            self.news_api_source = NewsAPISource(self.logger)
            self.logger.info("📰 NewsAPI monitoring enabled")

        self.llm_client = LLMClient(self.logger)
        self.alert_manager = AlertManager(self.logger)
        
        self.logger.info(f"🎯 Alert threshold set to {Config.ALERT_THRESHOLD}/10")
        self.logger.info(f"⏱️  Check interval: {Config.CHECK_INTERVAL_MINUTES} minutes")
        
        self.logger.info("✅ System initialization complete!")
    
    async def run_monitoring_cycle(self):
        """Run a single monitoring cycle."""
        try:
            self.logger.info("🔍 Starting monitoring cycle...")
            
            all_news = []
            
            # Fetch RSS news
            if self.rss_manager and Config.ENABLE_RSS_MONITORING:
                rss_news = await self.rss_manager.fetch_all_news()
                all_news.extend([item.to_dict() for item in rss_news])
                self.logger.info(f"📰 Found {len(rss_news)} relevant RSS news items")

            # Fetch NewsAPI news
            if self.news_api_source and Config.ENABLE_NEWS_API:
                news_api_items = await self.news_api_source.fetch_news()
                all_news.extend([item.to_dict() for item in news_api_items])
                self.logger.info(f"📡 Found {len(news_api_items)} relevant NewsAPI items")
            
            if not all_news:
                self.logger.info("📭 No new relevant news found")
                return
            
            # Analyze news with AI
            alerts_generated = 0
            for news_item in all_news:
                try:
                    # Analyze with LLM
                    analysis = await self.llm_client.analyze_news(
                        news_item['title'],
                        news_item['content'],
                        news_item['source']
                    )
                    
                    # Generate alert if needed
                    alert = await self.alert_manager.process_news_analysis(news_item, analysis)
                    if alert:
                        alerts_generated += 1
                    
                    # Small delay to avoid rate limiting
                    await asyncio.sleep(0.5)
                    
                except Exception as e:
                    self.logger.error(f"Error processing news item: {e}")
                    continue
            
            self.logger.info(f"🚨 Generated {alerts_generated} alerts from {len(all_news)} news items")
            
            # Log system stats
            stats = self.alert_manager.get_alert_stats()
            if stats['total'] > 0:
                self.logger.info(f"📊 24h Stats: {stats['total']} alerts, avg importance: {stats['avg_importance']}")
            
        except Exception as e:
            self.logger.error(f"Error in monitoring cycle: {e}")
    
    async def run(self):
        """Main application loop."""
        await self.initialize()
        
        self.running = True
        self.logger.info(f"🎬 Starting monitoring loop (checking every {Config.CHECK_INTERVAL_MINUTES} minutes)")
        
        try:
            while self.running:
                cycle_start = datetime.now()
                
                await self.run_monitoring_cycle()
                
                # Calculate sleep time
                cycle_duration = (datetime.now() - cycle_start).total_seconds()
                sleep_time = max(0, (Config.CHECK_INTERVAL_MINUTES * 60) - cycle_duration)
                
                if sleep_time > 0:
                    self.logger.info(f"😴 Sleeping for {sleep_time:.1f} seconds until next cycle...")
                    
                    # Sleep in small chunks to allow for graceful shutdown
                    while sleep_time > 0 and self.running:
                        chunk_sleep = min(10, sleep_time)  # Sleep in 10-second chunks
                        await asyncio.sleep(chunk_sleep)
                        sleep_time -= chunk_sleep
                
        except KeyboardInterrupt:
            self.logger.info("👋 Received keyboard interrupt")
        except Exception as e:
            self.logger.error(f"💥 Unexpected error in main loop: {e}")
        finally:
            await self.cleanup()
    
    async def cleanup(self):
        """Clean up resources."""
        self.logger.info("🧹 Cleaning up resources...")
        
        if self.rss_manager:
            await self.rss_manager.close_all()

        if self.news_api_source:
            await self.news_api_source.close()

        if self.llm_client:
            await self.llm_client.close()

        if self.alert_manager:
            await self.alert_manager.close()
        
        self.logger.info("✅ Cleanup complete. Goodbye! 👋")

async def main():
    """Main entry point."""
    system = CryptoAlertSystem()
    await system.run()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n👋 Goodbye!")
        sys.exit(0)
