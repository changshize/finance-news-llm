#!/usr/bin/env python3
"""
Setup script for the Crypto Trading Alert System
"""

import os
import sys
import subprocess
from pathlib import Path

def check_python_version():
    """Check if Python version is compatible."""
    if sys.version_info < (3, 8):
        print("❌ Python 3.8 or higher is required")
        sys.exit(1)
    print(f"✅ Python {sys.version.split()[0]} detected")

def install_dependencies():
    """Install required dependencies."""
    print("📦 Installing dependencies...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Dependencies installed successfully")
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install dependencies: {e}")
        sys.exit(1)

def setup_environment():
    """Set up environment configuration."""
    env_file = Path(".env")
    env_example = Path(".env.example")
    
    if not env_file.exists():
        if env_example.exists():
            print("📝 Creating .env file from template...")
            with open(env_example, 'r') as src, open(env_file, 'w') as dst:
                dst.write(src.read())
            print("✅ .env file created")
        else:
            print("❌ .env.example not found")
            return False
    else:
        print("✅ .env file already exists")
    
    return True

def create_directories():
    """Create necessary directories."""
    directories = ["logs", "alerts", "data"]
    
    for directory in directories:
        Path(directory).mkdir(exist_ok=True)
        print(f"✅ Created directory: {directory}")

def display_setup_instructions():
    """Display setup instructions to the user."""
    print("\n" + "="*60)
    print("🎉 SETUP COMPLETE!")
    print("="*60)
    print("\n📋 NEXT STEPS:")
    print("\n1. Configure your API keys in the .env file:")
    print("   - Get OpenRouter API key (free): https://openrouter.ai/")
    print("   - Or get DeepSeek API key: https://platform.deepseek.com/")
    print("   - Optional: Get NewsAPI key (free): https://newsapi.org/")
    print("   - Optional: Set up Discord/Slack webhook for notifications")
    
    print("\n2. Edit .env file with your API keys:")
    print("   nano .env")
    
    print("\n3. Test the configuration:")
    print("   python main.py")
    
    print("\n4. Run the system:")
    print("   python main.py")
    
    print("\n📚 DOCUMENTATION:")
    print("   - RSS feeds are monitored by default (no API key needed)")
    print("   - System will use fallback sentiment analysis if no LLM API is configured")
    print("   - Alerts are logged to console and saved to alerts/ directory")
    print("   - Check crypto_alerts.log for detailed logs")
    
    print("\n🔧 CONFIGURATION OPTIONS:")
    print("   - ALERT_THRESHOLD: Minimum importance score (1-10) to trigger alerts")
    print("   - CHECK_INTERVAL_MINUTES: How often to check for news")
    print("   - Enable/disable different news sources in .env")
    
    print("\n" + "="*60)

def main():
    """Main setup function."""
    print("🚀 Setting up Crypto Trading Alert System...")
    print("="*50)
    
    # Check Python version
    check_python_version()
    
    # Install dependencies
    install_dependencies()
    
    # Setup environment
    if not setup_environment():
        print("❌ Environment setup failed")
        sys.exit(1)
    
    # Create directories
    create_directories()
    
    # Display instructions
    display_setup_instructions()

if __name__ == "__main__":
    main()
