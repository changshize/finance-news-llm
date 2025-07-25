#!/usr/bin/env python3
"""
Simple web dashboard for the Crypto Trading Alert System
"""

import json
import os
from datetime import datetime, timedelta
from pathlib import Path
from typing import List, Dict
from http.server import HTTPServer, BaseHTTPRequestHandler
import urllib.parse

class DashboardHandler(BaseHTTPRequestHandler):
    """HTTP request handler for the web dashboard."""
    
    def do_GET(self):
        """Handle GET requests."""
        if self.path == '/' or self.path == '/index.html':
            self.serve_dashboard()
        elif self.path == '/api/alerts':
            self.serve_alerts_api()
        elif self.path == '/api/stats':
            self.serve_stats_api()
        else:
            self.send_error(404)
    
    def serve_dashboard(self):
        """Serve the main dashboard HTML."""
        html_content = self.generate_dashboard_html()
        
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(html_content.encode('utf-8'))
    
    def serve_alerts_api(self):
        """Serve alerts data as JSON API."""
        alerts = self.load_recent_alerts(24)
        
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(json.dumps(alerts, indent=2).encode('utf-8'))
    
    def serve_stats_api(self):
        """Serve statistics data as JSON API."""
        alerts = self.load_recent_alerts(24)
        stats = self.calculate_stats(alerts)
        
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(json.dumps(stats, indent=2).encode('utf-8'))
    
    def load_recent_alerts(self, hours: int = 24) -> List[Dict]:
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
                continue
        
        return sorted(recent_alerts, key=lambda x: x['timestamp'], reverse=True)
    
    def calculate_stats(self, alerts: List[Dict]) -> Dict:
        """Calculate statistics from alerts."""
        if not alerts:
            return {"total": 0, "avg_importance": 0, "sentiment_breakdown": {}}
        
        sentiment_counts = {}
        total_importance = 0
        crypto_counts = {}
        source_counts = {}
        
        for alert in alerts:
            # Sentiment breakdown
            sentiment = alert['sentiment']
            sentiment_counts[sentiment] = sentiment_counts.get(sentiment, 0) + 1
            
            # Importance
            total_importance += alert['importance']
            
            # Crypto mentions
            for crypto in alert.get('crypto_mentions', []):
                crypto_counts[crypto] = crypto_counts.get(crypto, 0) + 1
            
            # Source breakdown
            source = alert['source']
            source_counts[source] = source_counts.get(source, 0) + 1
        
        return {
            "total": len(alerts),
            "avg_importance": round(total_importance / len(alerts), 2),
            "sentiment_breakdown": sentiment_counts,
            "highest_importance": max(alert['importance'] for alert in alerts),
            "top_cryptos": sorted(crypto_counts.items(), key=lambda x: x[1], reverse=True)[:5],
            "top_sources": sorted(source_counts.items(), key=lambda x: x[1], reverse=True)[:5]
        }
    
    def generate_dashboard_html(self) -> str:
        """Generate the dashboard HTML."""
        alerts = self.load_recent_alerts(24)
        stats = self.calculate_stats(alerts)
        
        return f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🚀 Crypto Trading Alert System</title>
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
        .refresh-btn {{
            position: fixed;
            bottom: 20px;
            right: 20px;
            background: #667eea;
            color: white;
            border: none;
            padding: 15px 20px;
            border-radius: 50px;
            cursor: pointer;
            font-size: 1em;
            box-shadow: 0 4px 15px rgba(0,0,0,0.2);
        }}
        .refresh-btn:hover {{
            background: #5a6fd8;
            transform: translateY(-2px);
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
        }}
        .github-link:hover {{
            background: #555;
        }}
    </style>
</head>
<body>
    <a href="https://github.com/changshize/finance-news-llm" class="github-link" target="_blank">
        📚 View on GitHub
    </a>
    
    <div class="container">
        <div class="header">
            <h1>🚀 Crypto Trading Alert System</h1>
            <p>Real-time cryptocurrency news monitoring with AI analysis</p>
            <p>Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC')}</p>
        </div>
        
        <div class="stats-grid">
            <div class="stat-card">
                <div class="stat-number">{stats.get('total', 0)}</div>
                <div>Total Alerts (24h)</div>
            </div>
            <div class="stat-card">
                <div class="stat-number">{stats.get('avg_importance', 0)}</div>
                <div>Average Importance</div>
            </div>
            <div class="stat-card">
                <div class="stat-number">{stats.get('highest_importance', 0)}</div>
                <div>Highest Importance</div>
            </div>
            <div class="stat-card">
                <div class="stat-number">{stats.get('sentiment_breakdown', {}).get('bullish', 0)}</div>
                <div>🚀 Bullish Alerts</div>
            </div>
        </div>
        
        <div class="alerts-section">
            <h2>🚨 Recent Alerts</h2>
            {self.generate_alerts_html(alerts[:10])}
        </div>
    </div>
    
    <button class="refresh-btn" onclick="location.reload()">
        🔄 Refresh
    </button>
    
    <script>
        // Auto-refresh every 30 seconds
        setTimeout(() => location.reload(), 30000);
    </script>
</body>
</html>
        """
    
    def generate_alerts_html(self, alerts: List[Dict]) -> str:
        """Generate HTML for alerts list."""
        if not alerts:
            return "<p>No alerts in the last 24 hours.</p>"
        
        html = ""
        for alert in alerts:
            sentiment = alert['sentiment']
            sentiment_class = f"alert-{sentiment}"
            sentiment_emoji = {
                'bullish': '🚀',
                'bearish': '📉',
                'neutral': '⚖️'
            }.get(sentiment, '❓')
            
            timestamp = datetime.fromisoformat(alert['timestamp'])
            time_str = timestamp.strftime('%m/%d %H:%M')
            
            html += f"""
            <div class="alert-item {sentiment_class}">
                <div class="alert-header">
                    <span class="sentiment-emoji">{sentiment_emoji}</span>
                    <span class="importance-badge">{alert['importance']}/10</span>
                </div>
                <div class="alert-title">{alert['title']}</div>
                <div class="alert-meta">
                    📰 {alert['source']} | ⏰ {time_str} | 📈 {sentiment.title()}
                </div>
                <div class="alert-meta">
                    💡 {alert.get('summary', 'No summary available')}
                </div>
            </div>
            """
        
        return html

def start_web_server(port: int = 8000):
    """Start the web dashboard server."""
    server_address = ('', port)
    httpd = HTTPServer(server_address, DashboardHandler)
    
    print(f"🌐 Starting web dashboard at http://localhost:{port}")
    print(f"📊 Dashboard URL: http://localhost:{port}")
    print(f"🔗 GitHub: https://github.com/changshize/finance-news-llm")
    print("Press Ctrl+C to stop the server")
    
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n👋 Web dashboard stopped")
        httpd.server_close()

if __name__ == "__main__":
    start_web_server()
