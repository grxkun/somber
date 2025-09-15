import ccxt
import logging
import asyncio
import json
import os
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
import pandas as pd
import numpy as np
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class TradingBot:
    def __init__(self):
        self.exchange_name = os.getenv('EXCHANGE_NAME', 'binance')
        self.api_key = os.getenv('EXCHANGE_API_KEY')
        self.secret = os.getenv('EXCHANGE_SECRET')
        self.sandbox = os.getenv('EXCHANGE_SANDBOX', 'true').lower() == 'true'
        
        # Trading parameters
        self.default_symbol = os.getenv('DEFAULT_SYMBOL', 'BTC/USDT')
        self.trade_amount = float(os.getenv('TRADE_AMOUNT', '10.0'))
        self.stop_loss_percent = float(os.getenv('STOP_LOSS_PERCENT', '2.0'))
        self.take_profit_percent = float(os.getenv('TAKE_PROFIT_PERCENT', '5.0'))
        self.max_positions = int(os.getenv('MAX_POSITIONS', '3'))
        
        # Risk management
        self.max_daily_loss = float(os.getenv('MAX_DAILY_LOSS', '100.0'))
        self.min_balance = float(os.getenv('MIN_BALANCE', '50.0'))
        
        self.exchange = None
        self.is_trading = False
        self.positions = {}
        self.daily_pnl = 0.0
        self.last_reset_date = datetime.now().date()
        
        # Initialize exchange
        self._initialize_exchange()
    
    def _initialize_exchange(self):
        """Initialize the exchange connection"""
        try:
            exchange_class = getattr(ccxt, self.exchange_name)
            self.exchange = exchange_class({
                'apiKey': self.api_key,
                'secret': self.secret,
                'sandbox': self.sandbox,
                'enableRateLimit': True,
            })
            logger.info(f"Initialized {self.exchange_name} exchange (sandbox: {self.sandbox})")
        except Exception as e:
            logger.error(f"Failed to initialize exchange: {e}")
            raise
    
    async def get_balance(self) -> Dict:
        """Get account balance"""
        try:
            balance = self.exchange.fetch_balance()
            return balance
        except Exception as e:
            logger.error(f"Error fetching balance: {e}")
            return {}
    
    async def get_ticker(self, symbol: str) -> Dict:
        """Get current ticker for a symbol"""
        try:
            ticker = self.exchange.fetch_ticker(symbol)
            return ticker
        except Exception as e:
            logger.error(f"Error fetching ticker for {symbol}: {e}")
            return {}
    
    async def get_ohlcv(self, symbol: str, timeframe: str = '1h', limit: int = 100) -> List:
        """Get OHLCV data for technical analysis"""
        try:
            ohlcv = self.exchange.fetch_ohlcv(symbol, timeframe, limit=limit)
            return ohlcv
        except Exception as e:
            logger.error(f"Error fetching OHLCV data for {symbol}: {e}")
            return []
    
    def calculate_sma(self, prices: List[float], period: int) -> float:
        """Calculate Simple Moving Average"""
        if len(prices) < period:
            return None
        return sum(prices[-period:]) / period
    
    def simple_strategy(self, symbol: str) -> Tuple[str, float]:
        """
        Simple moving average crossover strategy
        Returns: (signal, confidence) where signal is 'buy', 'sell', or 'hold'
        """
        try:
            # Get recent price data
            ohlcv = asyncio.run(self.get_ohlcv(symbol, '1h', 50))
            if not ohlcv:
                return 'hold', 0.0
            
            # Extract closing prices
            closes = [candle[4] for candle in ohlcv]
            
            # Calculate moving averages
            sma_20 = self.calculate_sma(closes, 20)
            sma_50 = self.calculate_sma(closes, 50)
            
            if sma_20 is None or sma_50 is None:
                return 'hold', 0.0
            
            current_price = closes[-1]
            
            # Simple crossover strategy
            if sma_20 > sma_50 and current_price > sma_20:
                # Bullish signal
                confidence = min(((sma_20 - sma_50) / sma_50) * 100, 1.0)
                return 'buy', confidence
            elif sma_20 < sma_50 and current_price < sma_20:
                # Bearish signal
                confidence = min(((sma_50 - sma_20) / sma_20) * 100, 1.0)
                return 'sell', confidence
            else:
                return 'hold', 0.0
                
        except Exception as e:
            logger.error(f"Error in strategy calculation: {e}")
            return 'hold', 0.0
    
    async def place_order(self, symbol: str, side: str, amount: float, order_type: str = 'market') -> Dict:
        """Place an order on the exchange"""
        try:
            if side.lower() not in ['buy', 'sell']:
                raise ValueError("Side must be 'buy' or 'sell'")
            
            order = self.exchange.create_order(symbol, order_type, side, amount)
            logger.info(f"Placed {side} order for {amount} {symbol}: {order['id']}")
            return order
        except Exception as e:
            logger.error(f"Error placing {side} order: {e}")
            return {}
    
    async def set_stop_loss_take_profit(self, symbol: str, side: str, entry_price: float, amount: float):
        """Set stop loss and take profit orders"""
        try:
            if side.lower() == 'buy':
                # For long position
                stop_loss_price = entry_price * (1 - self.stop_loss_percent / 100)
                take_profit_price = entry_price * (1 + self.take_profit_percent / 100)
                
                # Place stop loss (sell order)
                stop_order = self.exchange.create_order(symbol, 'stop_market', 'sell', amount, None, None, {
                    'stopPrice': stop_loss_price
                })
                
                # Place take profit (sell order)
                tp_order = self.exchange.create_order(symbol, 'limit', 'sell', amount, take_profit_price)
                
            else:  # sell
                # For short position
                stop_loss_price = entry_price * (1 + self.stop_loss_percent / 100)
                take_profit_price = entry_price * (1 - self.take_profit_percent / 100)
                
                # Place stop loss (buy order)
                stop_order = self.exchange.create_order(symbol, 'stop_market', 'buy', amount, None, None, {
                    'stopPrice': stop_loss_price
                })
                
                # Place take profit (buy order)
                tp_order = self.exchange.create_order(symbol, 'limit', 'buy', amount, take_profit_price)
            
            logger.info(f"Set SL/TP for {symbol}: SL={stop_loss_price:.4f}, TP={take_profit_price:.4f}")
            return stop_order, tp_order
            
        except Exception as e:
            logger.error(f"Error setting SL/TP: {e}")
            return None, None
    
    def check_risk_management(self) -> bool:
        """Check if trading should continue based on risk management rules"""
        # Reset daily PnL if new day
        current_date = datetime.now().date()
        if current_date > self.last_reset_date:
            self.daily_pnl = 0.0
            self.last_reset_date = current_date
        
        # Check daily loss limit
        if self.daily_pnl <= -self.max_daily_loss:
            logger.warning(f"Daily loss limit reached: ${self.daily_pnl:.2f}")
            return False
        
        # Check minimum balance
        try:
            balance = asyncio.run(self.get_balance())
            usdt_balance = balance.get('USDT', {}).get('free', 0)
            if usdt_balance < self.min_balance:
                logger.warning(f"Balance too low: ${usdt_balance:.2f}")
                return False
        except:
            pass
        
        # Check maximum positions
        if len(self.positions) >= self.max_positions:
            logger.info(f"Maximum positions reached: {len(self.positions)}")
            return False
        
        return True
    
    async def execute_trade(self, symbol: str):
        """Execute trade based on strategy signal"""
        if not self.check_risk_management():
            return None
        
        signal, confidence = self.simple_strategy(symbol)
        
        if signal == 'hold' or confidence < 0.3:
            return None
        
        try:
            # Get current price
            ticker = await self.get_ticker(symbol)
            current_price = ticker.get('last', 0)
            
            if not current_price:
                return None
            
            # Calculate position size
            amount = self.trade_amount / current_price
            
            # Place the order
            order = await self.place_order(symbol, signal, amount)
            
            if order:
                # Set stop loss and take profit
                await self.set_stop_loss_take_profit(symbol, signal, current_price, amount)
                
                # Store position
                self.positions[symbol] = {
                    'side': signal,
                    'amount': amount,
                    'entry_price': current_price,
                    'timestamp': datetime.now().isoformat(),
                    'order_id': order.get('id')
                }
                
                logger.info(f"Executed {signal} trade for {symbol} at ${current_price:.4f}")
                return order
        
        except Exception as e:
            logger.error(f"Error executing trade: {e}")
            return None
    
    def start_trading(self):
        """Start the trading bot"""
        self.is_trading = True
        logger.info("Trading bot started")
    
    def stop_trading(self):
        """Stop the trading bot"""
        self.is_trading = False
        logger.info("Trading bot stopped")
    
    def get_status(self) -> Dict:
        """Get current bot status"""
        return {
            'is_trading': self.is_trading,
            'positions': len(self.positions),
            'daily_pnl': self.daily_pnl,
            'exchange': self.exchange_name,
            'sandbox': self.sandbox
        }
    
    async def get_portfolio_summary(self) -> Dict:
        """Get portfolio summary"""
        try:
            balance = await self.get_balance()
            total_value = 0
            
            for currency, info in balance.items():
                if currency != 'info' and info.get('total', 0) > 0:
                    if currency == 'USDT':
                        total_value += info['total']
                    else:
                        # Convert to USDT value
                        try:
                            ticker = await self.get_ticker(f"{currency}/USDT")
                            price = ticker.get('last', 0)
                            total_value += info['total'] * price
                        except:
                            pass
            
            return {
                'total_value': total_value,
                'positions': self.positions,
                'balance': balance
            }
        except Exception as e:
            logger.error(f"Error getting portfolio summary: {e}")
            return {}