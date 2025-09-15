#!/usr/bin/env python3
"""
Startup script for Somber Trading Bot
This script handles environment setup and starts the bot safely.
"""

import os
import sys
import logging
from pathlib import Path

def check_environment():
    """Check if all required environment variables are set"""
    required_vars = [
        'TELEGRAM_BOT_TOKEN',
        'EXCHANGE_API_KEY',
        'EXCHANGE_SECRET'
    ]
    
    missing_vars = []
    for var in required_vars:
        if not os.getenv(var):
            missing_vars.append(var)
    
    if missing_vars:
        print("❌ Missing required environment variables:")
        for var in missing_vars:
            print(f"   - {var}")
        print("\nPlease set these variables in your .env file or environment.")
        print("Check .env.example for reference.")
        return False
    
    return True

def setup_logging():
    """Setup logging configuration"""
    log_dir = Path("logs")
    log_dir.mkdir(exist_ok=True)
    
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_dir / "trading_bot.log"),
            logging.StreamHandler(sys.stdout)
        ]
    )

def main():
    """Main startup function"""
    print("🚀 Starting Somber Trading Bot...")
    
    # Setup logging
    setup_logging()
    logger = logging.getLogger(__name__)
    
    # Check environment
    if not check_environment():
        sys.exit(1)
    
    # Import and start the bot
    try:
        from main import main as run_bot
        logger.info("Environment check passed, starting bot...")
        run_bot()
    except ImportError as e:
        logger.error(f"Failed to import bot modules: {e}")
        print("❌ Failed to import required modules. Make sure to install dependencies:")
        print("   pip install -r requirements.txt")
        sys.exit(1)
    except KeyboardInterrupt:
        logger.info("Bot stopped by user")
        print("\n✅ Bot stopped successfully")
    except Exception as e:
        logger.error(f"Fatal error: {e}")
        print(f"❌ Fatal error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()