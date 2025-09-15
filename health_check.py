#!/usr/bin/env python3
"""
Health check script for Somber Trading Bot
Quick status check without starting the full bot
"""

import os
import sys
from pathlib import Path
from dotenv import load_dotenv

def check_environment():
    """Check environment configuration"""
    print("🔍 Checking Environment Configuration...")
    
    # Load .env file if it exists
    env_file = Path('.env')
    if env_file.exists():
        load_dotenv()
        print("✅ .env file found and loaded")
    else:
        print("⚠️  .env file not found (using system environment)")
    
    # Check required variables
    required_vars = {
        'TELEGRAM_BOT_TOKEN': 'Telegram bot token',
        'EXCHANGE_API_KEY': 'Exchange API key',
        'EXCHANGE_SECRET': 'Exchange secret key'
    }
    
    missing = []
    for var, desc in required_vars.items():
        if os.getenv(var):
            print(f"✅ {desc}: {'*' * 10}{os.getenv(var)[-4:]}")
        else:
            print(f"❌ {desc}: Not set")
            missing.append(var)
    
    # Check optional but important variables
    optional_vars = {
        'TELEGRAM_CHAT_ID': os.getenv('TELEGRAM_CHAT_ID', 'Not set'),
        'EXCHANGE_NAME': os.getenv('EXCHANGE_NAME', 'binance'),
        'EXCHANGE_SANDBOX': os.getenv('EXCHANGE_SANDBOX', 'true'),
        'DEFAULT_SYMBOL': os.getenv('DEFAULT_SYMBOL', 'BTC/USDT'),
        'TRADE_AMOUNT': os.getenv('TRADE_AMOUNT', '10.0'),
    }
    
    print("\n📋 Configuration:")
    for var, value in optional_vars.items():
        print(f"   {var}: {value}")
    
    return len(missing) == 0

def check_dependencies():
    """Check if all required dependencies are installed"""
    print("\n🔍 Checking Dependencies...")
    
    required_packages = [
        ('ccxt', 'Cryptocurrency exchange library'),
        ('telegram', 'Telegram bot library'),
        ('pandas', 'Data analysis library'),
        ('numpy', 'Numerical computing library'),
        ('dotenv', 'Environment variable loader'),
        ('schedule', 'Task scheduler')
    ]
    
    missing = []
    for package, description in required_packages:
        try:
            __import__(package)
            print(f"✅ {description}: {package}")
        except ImportError:
            print(f"❌ {description}: {package} (not installed)")
            missing.append(package)
    
    return len(missing) == 0

def check_file_structure():
    """Check if all required files exist"""
    print("\n🔍 Checking File Structure...")
    
    required_files = [
        ('main.py', 'Main application file'),
        ('trading_bot.py', 'Trading bot logic'),
        ('telegram_bot.py', 'Telegram interface'),
        ('start_bot.py', 'Startup script'),
        ('requirements.txt', 'Dependencies list'),
        ('.env.example', 'Environment template'),
        ('.gitignore', 'Git ignore rules')
    ]
    
    missing = []
    for filename, description in required_files:
        if Path(filename).exists():
            print(f"✅ {description}: {filename}")
        else:
            print(f"❌ {description}: {filename} (missing)")
            missing.append(filename)
    
    return len(missing) == 0

def test_import():
    """Test if bot modules can be imported"""
    print("\n🔍 Testing Module Imports...")
    
    # Set minimal required env vars for import test
    os.environ.setdefault('EXCHANGE_API_KEY', 'test')
    os.environ.setdefault('EXCHANGE_SECRET', 'test')
    os.environ.setdefault('TELEGRAM_BOT_TOKEN', 'test')
    
    try:
        from trading_bot import TradingBot
        print("✅ TradingBot module imports successfully")
        
        from telegram_bot import TelegramTradingBot
        print("✅ TelegramTradingBot module imports successfully")
        
        import main
        print("✅ Main module imports successfully")
        
        return True
    except Exception as e:
        print(f"❌ Import failed: {e}")
        return False

def main():
    """Run all health checks"""
    print("🏥 Somber Trading Bot - Health Check")
    print("=" * 50)
    
    checks = [
        ("Environment", check_environment),
        ("Dependencies", check_dependencies),
        ("File Structure", check_file_structure),
        ("Module Imports", test_import)
    ]
    
    results = []
    for check_name, check_func in checks:
        try:
            result = check_func()
            results.append((check_name, result))
        except Exception as e:
            print(f"❌ {check_name} check failed: {e}")
            results.append((check_name, False))
    
    # Summary
    print("\n" + "=" * 50)
    print("📊 Health Check Summary:")
    
    all_passed = True
    for check_name, passed in results:
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"   {check_name}: {status}")
        if not passed:
            all_passed = False
    
    if all_passed:
        print("\n🎉 All health checks passed!")
        print("✅ Your bot is ready to run!")
        print("\n🚀 To start the bot:")
        print("   python start_bot.py")
    else:
        print("\n⚠️  Some health checks failed!")
        print("📋 Please fix the issues above before starting the bot.")
        print("\n📚 Setup guide:")
        print("   1. Copy .env.example to .env")
        print("   2. Fill in your API credentials")
        print("   3. Install dependencies: pip install -r requirements.txt")
        print("   4. Run health check again: python health_check.py")
    
    return 0 if all_passed else 1

if __name__ == "__main__":
    sys.exit(main())