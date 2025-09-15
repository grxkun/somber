"""
Somnia Trading Bot
Main bot application that uses environment variables for configuration
"""

import logging
import sys
from config import get_config

# Set up logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)


class SomniaTradeBot:
    """Main trading bot class"""
    
    def __init__(self):
        """Initialize the bot with configuration"""
        try:
            self.config = get_config()
            self.config.validate()
            logger.info("Bot initialized successfully")
        except ValueError as e:
            logger.error(f"Failed to initialize bot: {e}")
            sys.exit(1)
    
    def connect_to_somnia_api(self):
        """Connect to Somnia API using environment variable"""
        api_url = self.config.somnia_api_url
        logger.info(f"Connecting to Somnia API at: {api_url}")
        
        # TODO: Implement actual API connection
        # import requests
        # response = requests.get(f"{api_url}/health")
        # return response.status_code == 200
        
        return True
    
    def setup_telegram_bot(self):
        """Setup Telegram bot using environment variable"""
        token = self.config.telegram_bot_token
        logger.info("Setting up Telegram bot...")
        
        # TODO: Implement actual Telegram bot setup
        # from telegram import Bot
        # self.telegram_bot = Bot(token=token)
        # return self.telegram_bot
        
        return True
    
    def run(self):
        """Run the bot"""
        logger.info("Starting Somnia Trading Bot...")
        
        # Connect to APIs
        if self.connect_to_somnia_api():
            logger.info("✅ Connected to Somnia API")
        else:
            logger.error("❌ Failed to connect to Somnia API")
            return
        
        if self.setup_telegram_bot():
            logger.info("✅ Telegram bot setup complete")
        else:
            logger.error("❌ Failed to setup Telegram bot")
            return
        
        logger.info("🚀 Bot is running!")
        
        # TODO: Implement trading logic
        logger.info("Trading logic not implemented yet")


if __name__ == "__main__":
    bot = SomniaTradeBot()
    bot.run()