import os
import asyncio
import logging
from datetime import datetime
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
from dotenv import load_dotenv
from trading_bot import TradingBot

# Load environment variables
load_dotenv()

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class TelegramTradingBot:
    def __init__(self):
        self.bot_token = os.getenv('TELEGRAM_BOT_TOKEN')
        self.chat_id = os.getenv('TELEGRAM_CHAT_ID')
        
        if not self.bot_token:
            raise ValueError("TELEGRAM_BOT_TOKEN environment variable is required")
        
        # Initialize trading bot
        self.trading_bot = TradingBot()
        
        # Initialize Telegram application
        self.application = Application.builder().token(self.bot_token).build()
        
        # Add command handlers
        self._add_handlers()
    
    def _add_handlers(self):
        """Add command handlers to the Telegram bot"""
        handlers = [
            CommandHandler("start", self.start_command),
            CommandHandler("help", self.help_command),
            CommandHandler("start_trading", self.start_trading_command),
            CommandHandler("stop_trading", self.stop_trading_command),
            CommandHandler("status", self.status_command),
            CommandHandler("balance", self.balance_command),
            CommandHandler("portfolio", self.portfolio_command),
            CommandHandler("positions", self.positions_command),
            CommandHandler("trade", self.manual_trade_command),
            CommandHandler("price", self.price_command),
        ]
        
        for handler in handlers:
            self.application.add_handler(handler)
    
    async def start_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /start command"""
        welcome_message = """
🤖 Welcome to Somber Trading Bot!

This bot helps you trade cryptocurrencies automatically using technical analysis.

Available commands:
/help - Show all available commands
/start_trading - Start automated trading
/stop_trading - Stop automated trading
/status - Show bot status
/balance - Show account balance
/portfolio - Show portfolio summary
/positions - Show open positions
/trade <symbol> - Execute manual trade
/price <symbol> - Get current price

⚠️ **Risk Warning**: Trading cryptocurrencies involves significant risk. Only trade with money you can afford to lose.
        """
        await update.message.reply_text(welcome_message)
    
    async def help_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /help command"""
        help_text = """
📋 **Available Commands:**

**Trading Controls:**
/start_trading - Start automated trading
/stop_trading - Stop automated trading
/trade <symbol> - Execute manual trade (e.g., /trade BTC/USDT)

**Information:**
/status - Show bot status and configuration
/balance - Show account balance
/portfolio - Show complete portfolio summary
/positions - Show current open positions
/price <symbol> - Get current price (e.g., /price BTC/USDT)

**General:**
/start - Show welcome message
/help - Show this help message

**Examples:**
/trade BTC/USDT - Execute trade for Bitcoin
/price ETH/USDT - Get Ethereum price
        """
        await update.message.reply_text(help_text, parse_mode='Markdown')
    
    async def start_trading_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /start_trading command"""
        try:
            self.trading_bot.start_trading()
            message = "✅ **Trading Started!**\n\nThe bot will now monitor markets and execute trades based on the configured strategy."
            await update.message.reply_text(message, parse_mode='Markdown')
            
            # Send status update
            await self._send_status_update(update)
            
        except Exception as e:
            logger.error(f"Error starting trading: {e}")
            await update.message.reply_text(f"❌ Error starting trading: {str(e)}")
    
    async def stop_trading_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /stop_trading command"""
        try:
            self.trading_bot.stop_trading()
            message = "🛑 **Trading Stopped!**\n\nAutomated trading has been disabled. Existing positions remain open."
            await update.message.reply_text(message, parse_mode='Markdown')
            
        except Exception as e:
            logger.error(f"Error stopping trading: {e}")
            await update.message.reply_text(f"❌ Error stopping trading: {str(e)}")
    
    async def status_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /status command"""
        await self._send_status_update(update)
    
    async def _send_status_update(self, update: Update):
        """Send detailed status update"""
        try:
            status = self.trading_bot.get_status()
            
            status_icon = "🟢" if status['is_trading'] else "🔴"
            
            message = f"""
{status_icon} **Bot Status**

**Trading:** {'Active' if status['is_trading'] else 'Stopped'}
**Exchange:** {status['exchange'].title()} ({'Sandbox' if status['sandbox'] else 'Live'})
**Open Positions:** {status['positions']}
**Daily P&L:** ${status['daily_pnl']:.2f}

**Configuration:**
• Default Symbol: {self.trading_bot.default_symbol}
• Trade Amount: ${self.trading_bot.trade_amount:.2f}
• Stop Loss: {self.trading_bot.stop_loss_percent}%
• Take Profit: {self.trading_bot.take_profit_percent}%
• Max Positions: {self.trading_bot.max_positions}

*Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} UTC*
            """
            await update.message.reply_text(message, parse_mode='Markdown')
            
        except Exception as e:
            logger.error(f"Error getting status: {e}")
            await update.message.reply_text(f"❌ Error getting status: {str(e)}")
    
    async def balance_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /balance command"""
        try:
            balance = await self.trading_bot.get_balance()
            
            if not balance:
                await update.message.reply_text("❌ Unable to fetch balance")
                return
            
            message = "💰 **Account Balance:**\n\n"
            
            # Show only currencies with balance > 0
            for currency, info in balance.items():
                if currency != 'info' and isinstance(info, dict):
                    total = info.get('total', 0)
                    free = info.get('free', 0)
                    used = info.get('used', 0)
                    
                    if total > 0:
                        message += f"**{currency}:** {total:.8f}\n"
                        message += f"  • Free: {free:.8f}\n"
                        message += f"  • Used: {used:.8f}\n\n"
            
            await update.message.reply_text(message, parse_mode='Markdown')
            
        except Exception as e:
            logger.error(f"Error fetching balance: {e}")
            await update.message.reply_text(f"❌ Error fetching balance: {str(e)}")
    
    async def portfolio_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /portfolio command"""
        try:
            portfolio = await self.trading_bot.get_portfolio_summary()
            
            if not portfolio:
                await update.message.reply_text("❌ Unable to fetch portfolio")
                return
            
            message = f"""
📊 **Portfolio Summary**

**Total Value:** ${portfolio.get('total_value', 0):.2f}
**Open Positions:** {len(portfolio.get('positions', {}))}

**Positions:**
            """
            
            positions = portfolio.get('positions', {})
            if positions:
                for symbol, pos in positions.items():
                    side_icon = "📈" if pos['side'] == 'buy' else "📉"
                    message += f"\n{side_icon} **{symbol}**\n"
                    message += f"  • Side: {pos['side'].upper()}\n"
                    message += f"  • Amount: {pos['amount']:.8f}\n"
                    message += f"  • Entry: ${pos['entry_price']:.4f}\n"
                    message += f"  • Time: {pos['timestamp'][:19]}\n"
            else:
                message += "\nNo open positions"
            
            await update.message.reply_text(message, parse_mode='Markdown')
            
        except Exception as e:
            logger.error(f"Error fetching portfolio: {e}")
            await update.message.reply_text(f"❌ Error fetching portfolio: {str(e)}")
    
    async def positions_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /positions command"""
        try:
            positions = self.trading_bot.positions
            
            if not positions:
                await update.message.reply_text("📭 No open positions")
                return
            
            message = "📈 **Open Positions:**\n\n"
            
            for symbol, pos in positions.items():
                side_icon = "🟢" if pos['side'] == 'buy' else "🔴"
                message += f"{side_icon} **{symbol}**\n"
                message += f"  • Side: {pos['side'].upper()}\n"
                message += f"  • Amount: {pos['amount']:.8f}\n"
                message += f"  • Entry Price: ${pos['entry_price']:.4f}\n"
                message += f"  • Opened: {pos['timestamp'][:19]}\n\n"
            
            await update.message.reply_text(message, parse_mode='Markdown')
            
        except Exception as e:
            logger.error(f"Error fetching positions: {e}")
            await update.message.reply_text(f"❌ Error fetching positions: {str(e)}")
    
    async def manual_trade_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /trade command"""
        try:
            if not context.args:
                await update.message.reply_text(
                    "Please specify a symbol. Example: /trade BTC/USDT"
                )
                return
            
            symbol = context.args[0].upper()
            
            # Validate symbol format
            if '/' not in symbol:
                await update.message.reply_text(
                    "Invalid symbol format. Use format like BTC/USDT"
                )
                return
            
            await update.message.reply_text(f"🔄 Analyzing {symbol} for trading opportunity...")
            
            # Execute trade
            order = await self.trading_bot.execute_trade(symbol)
            
            if order:
                await update.message.reply_text(
                    f"✅ Trade executed for {symbol}!\n"
                    f"Order ID: {order.get('id', 'N/A')}"
                )
                
                # Send trade notification
                await self._send_trade_notification(symbol, order, update)
            else:
                await update.message.reply_text(
                    f"❌ No trading opportunity found for {symbol} at this time."
                )
                
        except Exception as e:
            logger.error(f"Error executing manual trade: {e}")
            await update.message.reply_text(f"❌ Error executing trade: {str(e)}")
    
    async def price_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /price command"""
        try:
            if not context.args:
                symbol = self.trading_bot.default_symbol
            else:
                symbol = context.args[0].upper()
            
            ticker = await self.trading_bot.get_ticker(symbol)
            
            if not ticker:
                await update.message.reply_text(f"❌ Unable to fetch price for {symbol}")
                return
            
            price = ticker.get('last', 0)
            change = ticker.get('change', 0)
            percentage = ticker.get('percentage', 0)
            
            change_icon = "📈" if change >= 0 else "📉"
            
            message = f"""
{change_icon} **{symbol} Price**

**Current:** ${price:.4f}
**24h Change:** ${change:.4f} ({percentage:.2f}%)
**High:** ${ticker.get('high', 0):.4f}
**Low:** ${ticker.get('low', 0):.4f}
**Volume:** {ticker.get('baseVolume', 0):.2f}

*Updated: {datetime.now().strftime('%H:%M:%S')} UTC*
            """
            
            await update.message.reply_text(message, parse_mode='Markdown')
            
        except Exception as e:
            logger.error(f"Error fetching price: {e}")
            await update.message.reply_text(f"❌ Error fetching price: {str(e)}")
    
    async def _send_trade_notification(self, symbol: str, order: dict, update: Update):
        """Send trade notification"""
        try:
            side = order.get('side', 'unknown')
            amount = order.get('amount', 0)
            price = order.get('price', 0)
            
            side_icon = "🟢" if side == 'buy' else "🔴"
            
            message = f"""
{side_icon} **Trade Executed**

**Symbol:** {symbol}
**Side:** {side.upper()}
**Amount:** {amount:.8f}
**Price:** ${price:.4f}
**Value:** ${amount * price:.2f}

**Order ID:** {order.get('id', 'N/A')}
**Time:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} UTC
            """
            
            await update.message.reply_text(message, parse_mode='Markdown')
            
        except Exception as e:
            logger.error(f"Error sending trade notification: {e}")
    
    async def send_error_notification(self, error_message: str):
        """Send error notification to the chat"""
        try:
            if self.chat_id:
                message = f"⚠️ **Trading Bot Error**\n\n{error_message}\n\n*Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} UTC*"
                await self.application.bot.send_message(chat_id=self.chat_id, text=message, parse_mode='Markdown')
        except Exception as e:
            logger.error(f"Error sending error notification: {e}")
    
    async def send_daily_summary(self):
        """Send daily trading summary"""
        try:
            if self.chat_id:
                status = self.trading_bot.get_status()
                portfolio = await self.trading_bot.get_portfolio_summary()
                
                message = f"""
📊 **Daily Trading Summary**

**P&L:** ${status['daily_pnl']:.2f}
**Portfolio Value:** ${portfolio.get('total_value', 0):.2f}
**Open Positions:** {len(self.trading_bot.positions)}
**Trades Executed:** N/A

*Report generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} UTC*
                """
                
                await self.application.bot.send_message(chat_id=self.chat_id, text=message, parse_mode='Markdown')
        except Exception as e:
            logger.error(f"Error sending daily summary: {e}")
    
    def run(self):
        """Start the Telegram bot"""
        logger.info("Starting Telegram bot...")
        self.application.run_polling()

if __name__ == "__main__":
    try:
        telegram_bot = TelegramTradingBot()
        telegram_bot.run()
    except Exception as e:
        logger.error(f"Failed to start Telegram bot: {e}")
        raise