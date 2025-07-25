#!/usr/bin/env python3
"""
Quick demo script to showcase the Crypto Trading Alert System
"""

import os
import sys
import time
import webbrowser
from pathlib import Path

def print_banner():
    """Print demo banner."""
    print("🚀" + "="*60 + "🚀")
    print("    CRYPTO TRADING ALERT SYSTEM - QUICK DEMO")
    print("🚀" + "="*60 + "🚀")
    print()

def show_menu():
    """Show demo menu options."""
    print("📋 DEMO OPTIONS:")
    print()
    print("1. 🌐 Open Web Dashboard Demo (HTML)")
    print("2. 📊 Show System Statistics")
    print("3. 🖥️  Display Console Demo")
    print("4. 🏗️  Show System Architecture")
    print("5. 📄 View Sample Alert Data")
    print("6. 🧪 Run System Tests")
    print("7. 🚀 Start Live Monitoring")
    print("8. 🌐 Start Web Dashboard Server")
    print("9. 📸 View All Screenshots")
    print("0. ❌ Exit")
    print()

def open_web_demo():
    """Open the web dashboard demo in browser."""
    demo_file = Path("screenshots/web_dashboard_demo.html")
    if demo_file.exists():
        print("🌐 Opening web dashboard demo in browser...")
        webbrowser.open(f"file://{demo_file.absolute()}")
        print("✅ Demo opened! Check your browser.")
    else:
        print("❌ Demo file not found. Run: python generate_demo_screenshots.py")

def show_statistics():
    """Show system statistics."""
    print("📊 SYSTEM STATISTICS")
    print("="*50)
    
    # Count alerts
    alerts_dir = Path("alerts")
    if alerts_dir.exists():
        alert_files = list(alerts_dir.glob("alert_*.json"))
        print(f"🚨 Total Alerts Generated: {len(alert_files)}")
        
        if alert_files:
            import json
            sentiments = {"bullish": 0, "bearish": 0, "neutral": 0}
            importances = []
            sources = {}
            
            for alert_file in alert_files:
                try:
                    with open(alert_file, 'r') as f:
                        data = json.load(f)
                    sentiments[data.get('sentiment', 'neutral')] += 1
                    importances.append(data.get('importance', 0))
                    source = data.get('source', 'unknown')
                    sources[source] = sources.get(source, 0) + 1
                except:
                    continue
            
            avg_importance = sum(importances) / len(importances) if importances else 0
            
            print(f"📈 Average Importance: {avg_importance:.1f}/10")
            print(f"🎯 Highest Importance: {max(importances) if importances else 0}/10")
            print()
            print("📊 Sentiment Breakdown:")
            print(f"  🚀 Bullish: {sentiments['bullish']}")
            print(f"  📉 Bearish: {sentiments['bearish']}")
            print(f"  ⚖️  Neutral: {sentiments['neutral']}")
            print()
            print("📰 Top Sources:")
            for source, count in sorted(sources.items(), key=lambda x: x[1], reverse=True)[:5]:
                print(f"  📡 {source}: {count} alerts")
    else:
        print("📭 No alerts found. Run the system first: python main.py")
    
    print()

def show_console_demo():
    """Display console demo."""
    demo_file = Path("screenshots/console_demo.md")
    if demo_file.exists():
        print("🖥️  CONSOLE DEMO OUTPUT")
        print("="*50)
        with open(demo_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Show first part of console demo
        lines = content.split('\n')
        for i, line in enumerate(lines[:50]):  # Show first 50 lines
            print(line)
        
        if len(lines) > 50:
            print("\n... (truncated, see screenshots/console_demo.md for full output)")
    else:
        print("❌ Console demo not found.")
    print()

def show_architecture():
    """Show system architecture info."""
    print("🏗️  SYSTEM ARCHITECTURE")
    print("="*50)
    print("📡 News Sources Layer:")
    print("  - RSS Feeds (CoinDesk, CoinTelegraph, CryptoNews, Decrypt, Bitcoinist)")
    print("  - NewsAPI Integration")
    print("  - Social Media Monitoring (Reddit, Twitter)")
    print()
    print("🔍 Processing Layer:")
    print("  - News Filtering & Deduplication")
    print("  - AI Analysis Engine (LLM + Sentiment)")
    print("  - Importance Scoring (1-10 scale)")
    print()
    print("🚨 Alert Layer:")
    print("  - Threshold-based Alert Generation (7+/10)")
    print("  - Multi-channel Notifications")
    print("  - Real-time Processing")
    print()
    print("📊 Output Layer:")
    print("  - Console Output with Colors")
    print("  - Web Dashboard Interface")
    print("  - JSON File Storage")
    print("  - Webhook Notifications")
    print()
    print("📸 Full architecture diagrams: screenshots/system_architecture.md")
    print()

def show_sample_data():
    """Show sample alert data."""
    sample_file = Path("screenshots/sample_alerts.json")
    if sample_file.exists():
        print("📄 SAMPLE ALERT DATA")
        print("="*50)
        
        import json
        with open(sample_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # Show first 2 alerts as examples
        for i, alert in enumerate(data[:2], 1):
            print(f"Alert #{i}:")
            print(f"  🎯 Importance: {alert['importance']}/10")
            print(f"  📈 Sentiment: {alert['sentiment']}")
            print(f"  📰 Source: {alert['source']}")
            print(f"  📝 Title: {alert['title']}")
            print(f"  🔗 URL: {alert['url']}")
            print()
        
        print(f"... and {len(data)-2} more alerts in screenshots/sample_alerts.json")
    else:
        print("❌ Sample data not found.")
    print()

def run_tests():
    """Run system tests."""
    print("🧪 Running system tests...")
    os.system("python test_system.py")

def start_monitoring():
    """Start live monitoring."""
    print("🚀 Starting live monitoring system...")
    print("Press Ctrl+C to stop")
    print()
    os.system("python main.py")

def start_web_server():
    """Start web dashboard server."""
    print("🌐 Starting web dashboard server...")
    print("Visit http://localhost:8000 in your browser")
    print("Press Ctrl+C to stop")
    print()
    os.system("python web_dashboard.py")

def view_screenshots():
    """View all screenshots."""
    screenshots_dir = Path("screenshots")
    if screenshots_dir.exists():
        print("📸 AVAILABLE DEMO FILES:")
        print("="*50)
        for file in screenshots_dir.iterdir():
            if file.is_file():
                print(f"📄 {file.name}")
        print()
        print("🌐 To view HTML demo: open screenshots/web_dashboard_demo.html in browser")
        print("📖 To read docs: open .md files in text editor or GitHub")
    else:
        print("❌ Screenshots directory not found.")
    print()

def main():
    """Main demo function."""
    print_banner()
    
    while True:
        show_menu()
        
        try:
            choice = input("👉 Select option (0-9): ").strip()
            print()
            
            if choice == "0":
                print("👋 Thanks for trying the Crypto Trading Alert System!")
                print("🔗 GitHub: https://github.com/changshize/finance-news-llm")
                break
            elif choice == "1":
                open_web_demo()
            elif choice == "2":
                show_statistics()
            elif choice == "3":
                show_console_demo()
            elif choice == "4":
                show_architecture()
            elif choice == "5":
                show_sample_data()
            elif choice == "6":
                run_tests()
            elif choice == "7":
                start_monitoring()
            elif choice == "8":
                start_web_server()
            elif choice == "9":
                view_screenshots()
            else:
                print("❌ Invalid option. Please select 0-9.")
            
            if choice in ["6", "7", "8"]:  # Commands that run external programs
                print("\n" + "="*60)
                print("Press Enter to continue...")
                input()
            
        except KeyboardInterrupt:
            print("\n👋 Demo interrupted. Goodbye!")
            break
        except Exception as e:
            print(f"❌ Error: {e}")

if __name__ == "__main__":
    main()
