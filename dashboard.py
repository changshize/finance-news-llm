#!/usr/bin/env python3
"""
Simple dashboard for monitoring the Crypto Trading Alert System
"""

import json
import time
from datetime import datetime, timedelta
from pathlib import Path
from typing import List, Dict
import sys

def load_recent_alerts(hours: int = 24) -> List[Dict]:
    """Load recent alerts from the alerts directory."""
    alerts_dir = Path("alerts")
    if not alerts_dir.exists():
        return []
    
    cutoff_time = datetime.now() - timedelta(hours=hours)
    recent_alerts = []
    
    for alert_file in alerts_dir.glob("alert_*.json"):
        try:
            with open(alert_file, 'r', encoding='utf-8') as f:
                alert_data = json.load(f)
            
            # Check if alert is recent
            alert_time = datetime.fromisoformat(alert_data['timestamp'])
            if alert_time >= cutoff_time:
                recent_alerts.append(alert_data)
                
        except Exception as e:
            print(f"Error loading {alert_file}: {e}")
            continue
    
    return sorted(recent_alerts, key=lambda x: x['timestamp'], reverse=True)

def display_alert_summary(alerts: List[Dict]):
    """Display a summary of alerts."""
    if not alerts:
        print("📭 No alerts in the last 24 hours")
        return
    
    print(f"📊 ALERT SUMMARY (Last 24 hours)")
    print("=" * 50)
    print(f"Total Alerts: {len(alerts)}")
    
    # Sentiment breakdown
    sentiment_counts = {}
    importance_sum = 0
    
    for alert in alerts:
        sentiment = alert['sentiment']
        sentiment_counts[sentiment] = sentiment_counts.get(sentiment, 0) + 1
        importance_sum += alert['importance']
    
    avg_importance = importance_sum / len(alerts) if alerts else 0
    
    print(f"Average Importance: {avg_importance:.1f}/10")
    print("\nSentiment Breakdown:")
    for sentiment, count in sentiment_counts.items():
        emoji = {"bullish": "🚀", "bearish": "📉", "neutral": "⚖️"}.get(sentiment, "❓")
        print(f"  {emoji} {sentiment.title()}: {count}")
    
    # Top sources
    source_counts = {}
    for alert in alerts:
        source = alert['source']
        source_counts[source] = source_counts.get(source, 0) + 1
    
    print("\nTop Sources:")
    sorted_sources = sorted(source_counts.items(), key=lambda x: x[1], reverse=True)
    for source, count in sorted_sources[:5]:
        print(f"  📰 {source}: {count}")

def display_recent_alerts(alerts: List[Dict], limit: int = 10):
    """Display recent alerts."""
    if not alerts:
        return
    
    print(f"\n🚨 RECENT ALERTS (Top {min(limit, len(alerts))})")
    print("=" * 50)
    
    for i, alert in enumerate(alerts[:limit], 1):
        importance = alert['importance']
        sentiment = alert['sentiment']
        title = alert['title']
        source = alert['source']
        timestamp = alert['timestamp']
        
        # Format timestamp
        try:
            dt = datetime.fromisoformat(timestamp)
            time_str = dt.strftime("%m/%d %H:%M")
        except:
            time_str = timestamp[:16]
        
        # Sentiment emoji
        sentiment_emoji = {
            "bullish": "🚀",
            "bearish": "📉", 
            "neutral": "⚖️"
        }.get(sentiment, "❓")
        
        # Importance color (using text indicators)
        if importance >= 9:
            importance_indicator = "🔴"
        elif importance >= 7:
            importance_indicator = "🟡"
        else:
            importance_indicator = "🔵"
        
        print(f"{i:2d}. {importance_indicator} {sentiment_emoji} [{importance}/10] {time_str}")
        print(f"    📰 {source}")
        print(f"    📝 {title[:70]}{'...' if len(title) > 70 else ''}")
        
        if alert.get('trading_signal'):
            print(f"    💡 {alert['trading_signal']}")
        
        print()

def display_crypto_mentions(alerts: List[Dict]):
    """Display most mentioned cryptocurrencies."""
    crypto_counts = {}
    
    for alert in alerts:
        for crypto in alert.get('crypto_mentions', []):
            crypto_counts[crypto] = crypto_counts.get(crypto, 0) + 1
    
    if not crypto_counts:
        return
    
    print("💰 MOST MENTIONED CRYPTOCURRENCIES")
    print("=" * 50)
    
    sorted_cryptos = sorted(crypto_counts.items(), key=lambda x: x[1], reverse=True)
    for crypto, count in sorted_cryptos[:10]:
        print(f"  {crypto}: {count} mentions")

def display_system_status():
    """Display system status information."""
    print("🔧 SYSTEM STATUS")
    print("=" * 50)
    
    # Check if main process is running (simple check)
    log_file = Path("crypto_alerts.log")
    if log_file.exists():
        # Check last modification time
        last_modified = datetime.fromtimestamp(log_file.stat().st_mtime)
        time_diff = datetime.now() - last_modified
        
        if time_diff.total_seconds() < 600:  # 10 minutes
            print("✅ System appears to be running (recent log activity)")
        else:
            print("⚠️  System may not be running (no recent log activity)")
        
        print(f"📝 Last log update: {last_modified.strftime('%Y-%m-%d %H:%M:%S')}")
    else:
        print("❌ No log file found - system may not have been started")
    
    # Check configuration
    env_file = Path(".env")
    if env_file.exists():
        print("✅ Configuration file (.env) exists")
    else:
        print("❌ Configuration file (.env) not found")

def main():
    """Main dashboard function."""
    print("🚀 CRYPTO TRADING ALERT SYSTEM DASHBOARD")
    print("=" * 60)
    print(f"📅 Generated at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # Load recent alerts
    alerts = load_recent_alerts(24)
    
    # Display sections
    display_system_status()
    print()
    
    display_alert_summary(alerts)
    print()
    
    display_recent_alerts(alerts, 10)
    
    display_crypto_mentions(alerts)
    
    print("\n" + "=" * 60)
    print("💡 Commands:")
    print("  python main.py          - Start the monitoring system")
    print("  python test_system.py   - Test system configuration")
    print("  python dashboard.py     - Show this dashboard")
    print("  tail -f crypto_alerts.log - Watch live logs")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n👋 Dashboard closed")
        sys.exit(0)
