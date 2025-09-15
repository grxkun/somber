#!/usr/bin/env python3
"""
Somber Trading Bot - Main Application
A Python trading bot controllable via Telegram with risk management features.
"""

import asyncio
import logging
import schedule
import time
import threading
from datetime import datetime
from telegram_bot import TelegramTradingBot
from trading_bot import TradingBot

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class SomberTradingBot:
    def __init__(self):
        """Initialize the complete trading bot system"""
        self.telegram_bot = TelegramTradingBot()
        self.trading_bot = self.telegram_bot.trading_bot
        self.running = False
        
        # Schedule daily summary
        schedule.every().day.at("00:00").do(self._send_daily_summary)
        
        # Schedule periodic trading checks (every 5 minutes when trading is active)
        schedule.every(5).minutes.do(self._periodic_trading_check)
    
    def _send_daily_summary(self):
        """Send daily summary via Telegram"""
        try:
            asyncio.run(self.telegram_bot.send_daily_summary())
        except Exception as e:
            logger.error(f"Error sending daily summary: {e}")
    
    def _periodic_trading_check(self):
        """Periodic check for trading opportunities"""
        if not self.trading_bot.is_trading:
            return
        
        try:
            logger.info("Checking for trading opportunities...")
            
            # Execute trade for default symbol
            result = asyncio.run(self.trading_bot.execute_trade(self.trading_bot.default_symbol))
            
            if result:
                logger.info(f"Automated trade executed: {result.get('id')}")
                
                # Send notification if chat_id is configured
                if self.telegram_bot.chat_id:
                    asyncio.run(self._send_auto_trade_notification(result))
        
        except Exception as e:
            logger.error(f"Error in periodic trading check: {e}")
            # Send error notification
            asyncio.run(self.telegram_bot.send_error_notification(str(e)))
    
    async def _send_auto_trade_notification(self, order):
        """Send automated trade notification"""
        try:
            symbol = order.get('symbol', 'Unknown')
            side = order.get('side', 'unknown')
            amount = order.get('amount', 0)
            price = order.get('price', 0)
            
            side_icon = "🟢" if side == 'buy' else "🔴"
            
            message = f"""
🤖 **Automated Trade Executed**

{side_icon} **{symbol}**
**Side:** {side.upper()}
**Amount:** {amount:.8f}
**Price:** ${price:.4f}
**Value:** ${amount * price:.2f}

**Order ID:** {order.get('id', 'N/A')}
**Time:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} UTC

*This trade was executed automatically based on the trading strategy.*
            """
            
            await self.telegram_bot.application.bot.send_message(
                chat_id=self.telegram_bot.chat_id, 
                text=message, 
                parse_mode='Markdown'
            )
            
        except Exception as e:
            logger.error(f"Error sending auto trade notification: {e}")
    
    def _run_scheduler(self):
        """Run the scheduler in a separate thread"""
        while self.running:
            schedule.run_pending()
            time.sleep(1)
    
    def start(self):
        """Start the complete trading bot system"""
        logger.info("Starting Somber Trading Bot...")
        
        self.running = True
        
        # Start scheduler in a separate thread
        scheduler_thread = threading.Thread(target=self._run_scheduler, daemon=True)
        scheduler_thread.start()
        
        # Send startup notification
        if self.telegram_bot.chat_id:
            try:
                startup_message = """
🚀 **Somber Trading Bot Started**

The bot is now online and ready to trade!

**Configuration:**
• Exchange: {exchange} ({mode})
• Default Symbol: {symbol}
• Trade Amount: ${amount:.2f}
• Stop Loss: {sl}%
• Take Profit: {tp}%

Use /help to see available commands.
                """.format(
                    exchange=self.trading_bot.exchange_name.title(),
                    mode="Sandbox" if self.trading_bot.sandbox else "Live",
                    symbol=self.trading_bot.default_symbol,
                    amount=self.trading_bot.trade_amount,
                    sl=self.trading_bot.stop_loss_percent,
                    tp=self.trading_bot.take_profit_percent
                )
                
                asyncio.run(
                    self.telegram_bot.application.bot.send_message(
                        chat_id=self.telegram_bot.chat_id,
                        text=startup_message,
                        parse_mode='Markdown'
                    )
                )
            except Exception as e:
                logger.error(f"Error sending startup notification: {e}")
        
        # Start Telegram bot (this blocks)
        logger.info("Starting Telegram bot interface...")
        self.telegram_bot.run()
    
    def stop(self):
        """Stop the trading bot system"""
        logger.info("Stopping Somber Trading Bot...")
        self.running = False
        self.trading_bot.stop_trading()

def main():
    """Main entry point"""
    try:
        # Create and start the bot
        bot = SomberTradingBot()
        bot.start()
        
    except KeyboardInterrupt:
        logger.info("Received interrupt signal, shutting down...")
    except Exception as e:
        logger.error(f"Fatal error: {e}")
        raise
    finally:
        logger.info("Somber Trading Bot shutdown complete")

if __name__ == "__main__":
    main()