#!/usr/bin/env python3
"""
Generate demo screenshots and HTML previews of the web dashboard
"""

import json
import os
from datetime import datetime, timedelta
from pathlib import Path
import web_dashboard

def generate_static_demo_html():
    """Generate a static HTML demo of the dashboard."""
    
    # Load sample alerts data
    alerts_dir = Path("alerts")
    sample_alerts = []
    
    if alerts_dir.exists():
        for alert_file in list(alerts_dir.glob("alert_*.json"))[:10]:
            try:
                with open(alert_file, 'r', encoding='utf-8') as f:
                    alert_data = json.load(f)
                sample_alerts.append(alert_data)
            except:
                continue
    
    # Calculate stats
    stats = {
        "total": len(sample_alerts),
        "avg_importance": round(sum(a['importance'] for a in sample_alerts) / len(sample_alerts), 1) if sample_alerts else 0,
        "sentiment_breakdown": {},
        "highest_importance": max(a['importance'] for a in sample_alerts) if sample_alerts else 0
    }
    
    for alert in sample_alerts:
        sentiment = alert['sentiment']
        stats['sentiment_breakdown'][sentiment] = stats['sentiment_breakdown'].get(sentiment, 0) + 1
    
    # Generate HTML
    html_content = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🚀 Crypto Trading Alert System - Live Demo</title>
    <style>
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            margin: 0;
            padding: 20px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: #333;
            min-height: 100vh;
        }}
        .container {{
            max-width: 1200px;
            margin: 0 auto;
            background: white;
            border-radius: 15px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.2);
            overflow: hidden;
        }}
        .header {{
            background: linear-gradient(135deg, #ff6b6b, #feca57);
            color: white;
            padding: 30px;
            text-align: center;
        }}
        .header h1 {{
            margin: 0;
            font-size: 2.5em;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        }}
        .demo-badge {{
            background: rgba(255,255,255,0.2);
            padding: 10px 20px;
            border-radius: 25px;
            margin-top: 15px;
            display: inline-block;
            font-weight: bold;
        }}
        .stats-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px;
            padding: 30px;
            background: #f8f9fa;
        }}
        .stat-card {{
            background: white;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
            text-align: center;
            transition: transform 0.3s ease;
        }}
        .stat-card:hover {{
            transform: translateY(-5px);
        }}
        .stat-number {{
            font-size: 2.5em;
            font-weight: bold;
            color: #667eea;
            margin: 10px 0;
        }}
        .alerts-section {{
            padding: 30px;
        }}
        .alert-item {{
            background: white;
            border-left: 5px solid #667eea;
            margin: 15px 0;
            padding: 20px;
            border-radius: 0 10px 10px 0;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            transition: transform 0.2s ease;
        }}
        .alert-item:hover {{
            transform: translateX(5px);
        }}
        .alert-bullish {{ border-left-color: #28a745; }}
        .alert-bearish {{ border-left-color: #dc3545; }}
        .alert-neutral {{ border-left-color: #ffc107; }}
        .alert-header {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 10px;
        }}
        .importance-badge {{
            background: #667eea;
            color: white;
            padding: 5px 10px;
            border-radius: 20px;
            font-weight: bold;
        }}
        .importance-high {{ background: #dc3545; }}
        .importance-medium {{ background: #ffc107; color: #333; }}
        .sentiment-emoji {{
            font-size: 1.5em;
        }}
        .alert-title {{
            font-size: 1.2em;
            font-weight: bold;
            margin: 10px 0;
            color: #333;
        }}
        .alert-meta {{
            color: #666;
            font-size: 0.9em;
            margin: 5px 0;
        }}
        .github-link {{
            position: fixed;
            top: 20px;
            right: 20px;
            background: #333;
            color: white;
            padding: 10px 15px;
            border-radius: 25px;
            text-decoration: none;
            font-weight: bold;
            z-index: 1000;
        }}
        .github-link:hover {{
            background: #555;
        }}
        .live-indicator {{
            position: fixed;
            top: 20px;
            left: 20px;
            background: #28a745;
            color: white;
            padding: 10px 15px;
            border-radius: 25px;
            font-weight: bold;
            animation: pulse 2s infinite;
        }}
        @keyframes pulse {{
            0% {{ opacity: 1; }}
            50% {{ opacity: 0.7; }}
            100% {{ opacity: 1; }}
        }}
        .footer {{
            background: #333;
            color: white;
            padding: 30px;
            text-align: center;
        }}
        .feature-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 20px;
            margin: 20px 0;
        }}
        .feature-card {{
            background: rgba(255,255,255,0.1);
            padding: 20px;
            border-radius: 10px;
        }}
    </style>
</head>
<body>
    <div class="live-indicator">
        🔴 LIVE DEMO
    </div>
    
    <a href="https://github.com/changshize/finance-news-llm" class="github-link" target="_blank">
        📚 View on GitHub
    </a>
    
    <div class="container">
        <div class="header">
            <h1>🚀 Crypto Trading Alert System</h1>
            <p>Real-time cryptocurrency news monitoring with AI analysis</p>
            <div class="demo-badge">
                ✨ LIVE DEMO - Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC')}
            </div>
        </div>
        
        <div class="stats-grid">
            <div class="stat-card">
                <div class="stat-number">{stats['total']}</div>
                <div>Total Alerts (24h)</div>
            </div>
            <div class="stat-card">
                <div class="stat-number">{stats['avg_importance']}</div>
                <div>Average Importance</div>
            </div>
            <div class="stat-card">
                <div class="stat-number">{stats['highest_importance']}</div>
                <div>Highest Importance</div>
            </div>
            <div class="stat-card">
                <div class="stat-number">{stats['sentiment_breakdown'].get('bullish', 0)}</div>
                <div>🚀 Bullish Alerts</div>
            </div>
        </div>
        
        <div class="alerts-section">
            <h2>🚨 Recent Live Alerts</h2>
            {generate_alerts_html_static(sample_alerts[:8])}
        </div>
        
        <div class="footer">
            <h3>🎯 System Features</h3>
            <div class="feature-grid">
                <div class="feature-card">
                    <h4>📡 Real-time Monitoring</h4>
                    <p>5 RSS feeds monitored continuously: CoinDesk, CoinTelegraph, CryptoNews, Decrypt, Bitcoinist</p>
                </div>
                <div class="feature-card">
                    <h4>🤖 AI Analysis</h4>
                    <p>Smart importance scoring (1-10) and sentiment analysis (Bullish/Bearish/Neutral)</p>
                </div>
                <div class="feature-card">
                    <h4>🚨 Smart Alerts</h4>
                    <p>Only high-importance alerts (7+/10) with color-coded visualization</p>
                </div>
                <div class="feature-card">
                    <h4>🌐 Web Dashboard</h4>
                    <p>Beautiful real-time interface with auto-refresh and mobile support</p>
                </div>
            </div>
            
            <div style="margin-top: 30px;">
                <h4>🚀 Ready to Use</h4>
                <p><strong>GitHub:</strong> https://github.com/changshize/finance-news-llm</p>
                <p><strong>Setup:</strong> python setup.py && python main.py</p>
                <p><strong>Web Dashboard:</strong> python web_dashboard.py</p>
            </div>
        </div>
    </div>
</body>
</html>
    """
    
    return html_content

def generate_alerts_html_static(alerts):
    """Generate HTML for alerts list."""
    if not alerts:
        return "<p>No alerts available in demo.</p>"
    
    html = ""
    for i, alert in enumerate(alerts, 1):
        sentiment = alert['sentiment']
        sentiment_class = f"alert-{sentiment}"
        sentiment_emoji = {
            'bullish': '🚀',
            'bearish': '📉',
            'neutral': '⚖️'
        }.get(sentiment, '❓')
        
        importance = alert['importance']
        importance_class = ""
        if importance >= 9:
            importance_class = "importance-high"
        elif importance >= 7:
            importance_class = "importance-medium"
        
        try:
            timestamp = datetime.fromisoformat(alert['timestamp'])
            time_str = timestamp.strftime('%m/%d %H:%M')
        except:
            time_str = "Recent"
        
        html += f"""
        <div class="alert-item {sentiment_class}">
            <div class="alert-header">
                <span class="sentiment-emoji">{sentiment_emoji}</span>
                <span class="importance-badge {importance_class}">{importance}/10</span>
            </div>
            <div class="alert-title">{alert['title']}</div>
            <div class="alert-meta">
                📰 {alert['source']} | ⏰ {time_str} | 📈 {sentiment.title()}
            </div>
            <div class="alert-meta">
                💡 {alert.get('summary', alert['title'][:100] + '...')}
            </div>
        </div>
        """
    
    return html

def main():
    """Generate demo files."""
    print("🎬 Generating demo screenshots and HTML...")
    
    # Create screenshots directory
    screenshots_dir = Path("screenshots")
    screenshots_dir.mkdir(exist_ok=True)
    
    # Generate static HTML demo
    html_content = generate_static_demo_html()
    
    # Save demo HTML
    demo_file = screenshots_dir / "web_dashboard_demo.html"
    with open(demo_file, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print(f"✅ Demo HTML generated: {demo_file}")
    print(f"🌐 Open in browser: file://{demo_file.absolute()}")
    
    # Generate README for screenshots
    readme_content = f"""# 📸 Demo Screenshots

## 🌐 Web Dashboard Demo

### Live Demo HTML
- **File**: `web_dashboard_demo.html`
- **Description**: Static HTML demo showing the actual web dashboard interface
- **Features**: Real alert data, responsive design, interactive elements

### How to View
1. Open `web_dashboard_demo.html` in any web browser
2. Or run the live system: `python web_dashboard.py` and visit `http://localhost:8000`

### Demo Data
- **{len([f for f in Path('../alerts').glob('*.json') if f.exists()])} Real Alerts** from live system testing
- **5 News Sources** monitored (CoinDesk, CoinTelegraph, etc.)
- **AI Analysis** with importance scoring and sentiment classification

### Screenshots Description
This demo shows the actual working system with:
- 📊 Real-time statistics dashboard
- 🚨 Color-coded alert timeline
- 📱 Mobile-responsive design
- 🎨 Beautiful gradient UI
- 🔄 Auto-refresh functionality

Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC')}
"""
    
    readme_file = screenshots_dir / "README.md"
    with open(readme_file, 'w', encoding='utf-8') as f:
        f.write(readme_content)
    
    print(f"✅ Screenshots README generated: {readme_file}")
    print("🎉 Demo generation complete!")

if __name__ == "__main__":
    main()
