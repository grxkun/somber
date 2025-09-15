#!/usr/bin/env python3
"""
Test script to demonstrate Somber Trading Bot functionality
This script tests the bot without requiring actual API keys
"""

import os
import asyncio
from unittest.mock import Mock, patch
from trading_bot import TradingBot

def test_bot_initialization():
    """Test bot initialization with mock credentials"""
    print("🧪 Testing Bot Initialization...")
    
    # Set mock environment variables
    os.environ.update({
        'EXCHANGE_API_KEY': 'test_api_key',
        'EXCHANGE_SECRET': 'test_secret',
        'TELEGRAM_BOT_TOKEN': 'test_token',
        'EXCHANGE_SANDBOX': 'true',
        'DEFAULT_SYMBOL': 'BTC/USDT',
        'TRADE_AMOUNT': '10.0'
    })
    
    try:
        # Mock the exchange initialization to avoid real API calls
        with patch('ccxt.binance') as mock_exchange:
            mock_exchange.return_value = Mock()
            
            bot = TradingBot()
            
            print(f"✅ Bot initialized successfully")
            print(f"   Exchange: {bot.exchange_name}")
            print(f"   Symbol: {bot.default_symbol}")
            print(f"   Trade Amount: ${bot.trade_amount}")
            print(f"   Stop Loss: {bot.stop_loss_percent}%")
            print(f"   Take Profit: {bot.take_profit_percent}%")
            print(f"   Sandbox Mode: {bot.sandbox}")
            
            return bot
    
    except Exception as e:
        print(f"❌ Bot initialization failed: {e}")
        return None

def test_strategy_calculation():
    """Test trading strategy with mock data"""
    print("\n🧪 Testing Trading Strategy...")
    
    try:
        with patch('ccxt.binance') as mock_exchange:
            mock_exchange.return_value = Mock()
            
            bot = TradingBot()
            
            # Mock OHLCV data (timestamp, open, high, low, close, volume)
            mock_ohlcv = [
                [1609459200000, 29000, 29500, 28500, 29200, 1000],  # Historical data
                [1609462800000, 29200, 29800, 29000, 29400, 1200],
                [1609466400000, 29400, 30000, 29200, 29800, 1500],
                [1609470000000, 29800, 30200, 29600, 30000, 1300],
                [1609473600000, 30000, 30500, 29800, 30200, 1100],
                # ... more data points for SMA calculation
            ] * 10  # Repeat to have enough data points
            
            # Mock the get_ohlcv method
            async def mock_get_ohlcv(symbol, timeframe='1h', limit=100):
                return mock_ohlcv
            
            bot.get_ohlcv = mock_get_ohlcv
            
            # Test strategy
            signal, confidence = bot.simple_strategy('BTC/USDT')
            
            print(f"✅ Strategy calculation completed")
            print(f"   Signal: {signal}")
            print(f"   Confidence: {confidence:.2f}")
            
    except Exception as e:
        print(f"❌ Strategy test failed: {e}")

def test_risk_management():
    """Test risk management features"""
    print("\n🧪 Testing Risk Management...")
    
    try:
        with patch('ccxt.binance') as mock_exchange:
            mock_exchange.return_value = Mock()
            
            bot = TradingBot()
            
            # Test initial risk check
            can_trade = bot.check_risk_management()
            print(f"✅ Risk management check: {'✅ Can trade' if can_trade else '❌ Cannot trade'}")
            
            # Test with maximum positions
            bot.positions = {'BTC/USDT': {}, 'ETH/USDT': {}, 'ADA/USDT': {}}
            can_trade_max_pos = bot.check_risk_management()
            print(f"   Max positions check: {'✅ Can trade' if can_trade_max_pos else '❌ Cannot trade (max positions)'}")
            
            # Test daily loss limit
            bot.positions = {}
            bot.daily_pnl = -150.0  # Exceeds max daily loss
            can_trade_loss = bot.check_risk_management()
            print(f"   Daily loss check: {'✅ Can trade' if can_trade_loss else '❌ Cannot trade (daily loss limit)'}")
            
    except Exception as e:
        print(f"❌ Risk management test failed: {e}")

def test_bot_status():
    """Test bot status functionality"""
    print("\n🧪 Testing Bot Status...")
    
    try:
        with patch('ccxt.binance') as mock_exchange:
            mock_exchange.return_value = Mock()
            
            bot = TradingBot()
            
            # Test status when stopped
            status = bot.get_status()
            print(f"✅ Bot status (stopped): {status}")
            
            # Test status when started
            bot.start_trading()
            status_started = bot.get_status()
            print(f"✅ Bot status (started): {status_started}")
            
            bot.stop_trading()
            
    except Exception as e:
        print(f"❌ Status test failed: {e}")

def main():
    """Run all tests"""
    print("🚀 Starting Somber Trading Bot Functionality Tests\n")
    print("=" * 60)
    
    # Run tests
    bot = test_bot_initialization()
    if bot:
        test_strategy_calculation()
        test_risk_management()
        test_bot_status()
    
    print("\n" + "=" * 60)
    print("🎉 All tests completed!")
    print("\n📝 Next steps:")
    print("1. Set up your .env file with real API credentials")
    print("2. Start with sandbox mode for testing")
    print("3. Create a Telegram bot and get your chat ID")
    print("4. Run: python start_bot.py")

if __name__ == "__main__":
    main()