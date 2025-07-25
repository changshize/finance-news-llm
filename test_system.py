#!/usr/bin/env python3
"""
Test script for the Crypto Trading Alert System
"""

import asyncio
import sys
from pathlib import Path

# Add src to path
sys.path.append(str(Path(__file__).parent))

from config import Config
from src.utils.logger import setup_logger
from src.news_sources.rss_feeds import RSSFeedManager
from src.ai_analysis.llm_client import LLMClient
from src.alerts.alert_manager import AlertManager

async def test_configuration():
    """Test system configuration."""
    print("🔧 Testing Configuration...")
    
    status = Config.validate_config()
    for component, is_valid in status.items():
        emoji = "✅" if is_valid else "❌"
        print(f"  {emoji} {component}: {'OK' if is_valid else 'Missing/Invalid'}")
    
    provider = Config.get_active_llm_provider()
    print(f"  🤖 LLM Provider: {provider}")
    
    return all(status.values())

async def test_rss_feeds():
    """Test RSS feed fetching."""
    print("\n📡 Testing RSS Feeds...")
    
    logger = setup_logger('test')
    rss_manager = RSSFeedManager(logger)
    
    try:
        news_items = await rss_manager.fetch_all_news()
        print(f"  ✅ Fetched {len(news_items)} news items")
        
        if news_items:
            sample = news_items[0]
            print(f"  📰 Sample: {sample.title[:50]}...")
            print(f"  🔗 Source: {sample.source}")
        
        await rss_manager.close_all()
        return True
        
    except Exception as e:
        print(f"  ❌ RSS test failed: {e}")
        return False

async def test_llm_analysis():
    """Test LLM analysis."""
    print("\n🤖 Testing LLM Analysis...")
    
    logger = setup_logger('test')
    llm_client = LLMClient(logger)
    
    # Test with sample news
    test_title = "SEC Approves Bitcoin ETF Applications"
    test_content = "The Securities and Exchange Commission has approved several Bitcoin ETF applications from major financial institutions, marking a significant milestone for cryptocurrency adoption."
    
    try:
        analysis = await llm_client.analyze_news(test_title, test_content, "test")
        
        print(f"  ✅ Analysis completed")
        print(f"  📊 Importance: {analysis['importance']}/10")
        print(f"  📈 Sentiment: {analysis['sentiment']}")
        print(f"  💡 Summary: {analysis['summary'][:50]}...")
        
        await llm_client.close()
        return True
        
    except Exception as e:
        print(f"  ❌ LLM test failed: {e}")
        return False

async def test_alert_system():
    """Test alert generation."""
    print("\n🚨 Testing Alert System...")
    
    logger = setup_logger('test')
    alert_manager = AlertManager(logger)
    
    # Test alert data
    test_news = {
        'title': 'Test Bitcoin News Alert',
        'content': 'This is a test alert for Bitcoin price movement.',
        'url': 'https://example.com/test',
        'source': 'test',
        'published_date': '2024-01-01T12:00:00Z'
    }
    
    test_analysis = {
        'importance': 8,
        'sentiment': 'bullish',
        'summary': 'Test alert for system verification',
        'trading_signal': 'Test signal',
        'confidence': 7
    }
    
    try:
        alert = await alert_manager.process_news_analysis(test_news, test_analysis)
        
        if alert:
            print(f"  ✅ Alert generated successfully")
            print(f"  📊 Importance: {alert['importance']}/10")
            print(f"  📈 Sentiment: {alert['sentiment']}")
        else:
            print(f"  ⚠️  Alert below threshold ({Config.ALERT_THRESHOLD})")
        
        # Test stats
        stats = alert_manager.get_alert_stats()
        print(f"  📈 Alert stats: {stats}")
        
        await alert_manager.close()
        return True
        
    except Exception as e:
        print(f"  ❌ Alert test failed: {e}")
        return False

async def run_full_test():
    """Run complete system test."""
    print("🧪 CRYPTO ALERT SYSTEM TEST")
    print("=" * 40)
    
    tests = [
        ("Configuration", test_configuration),
        ("RSS Feeds", test_rss_feeds),
        ("LLM Analysis", test_llm_analysis),
        ("Alert System", test_alert_system),
    ]
    
    results = []
    
    for test_name, test_func in tests:
        try:
            result = await test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ {test_name} test crashed: {e}")
            results.append((test_name, False))
    
    # Summary
    print("\n" + "=" * 40)
    print("📋 TEST SUMMARY")
    print("=" * 40)
    
    passed = 0
    for test_name, result in results:
        emoji = "✅" if result else "❌"
        status = "PASSED" if result else "FAILED"
        print(f"{emoji} {test_name}: {status}")
        if result:
            passed += 1
    
    print(f"\n🎯 Overall: {passed}/{len(results)} tests passed")
    
    if passed == len(results):
        print("🎉 All tests passed! System is ready to use.")
        print("\n🚀 To start monitoring:")
        print("   python main.py")
    else:
        print("⚠️  Some tests failed. Check your configuration:")
        print("   - Verify API keys in .env file")
        print("   - Check internet connection")
        print("   - Review error messages above")

if __name__ == "__main__":
    asyncio.run(run_full_test())
