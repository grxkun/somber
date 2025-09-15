# Somber Trading Bot 🤖

A sophisticated Python trading bot that runs on GitHub Codespaces and is controllable via Telegram. The bot features automated trading with technical analysis, risk management, and comprehensive Telegram integration.

## ✨ Features

- **Exchange Integration**: Connect to crypto exchanges using ccxt library
- **Trading Strategy**: Implements Simple Moving Average (SMA) crossover strategy
- **Risk Management**: Stop-loss and take-profit orders with position sizing
- **Telegram Control**: Full bot control via Telegram commands
- **Real-time Notifications**: Trade alerts and error notifications
- **Portfolio Management**: Track positions and performance
- **GitHub Codespaces Ready**: Pre-configured development environment

## 🚀 Quick Start on GitHub Codespaces

### 1. Open in Codespaces
Click the green "Code" button and select "Create codespace on main"

### 2. Set Environment Variables
Create a `.env` file from the template:
```bash
cp .env.example .env
```

Edit the `.env` file with your credentials:
```env
# Get token from @BotFather on Telegram
TELEGRAM_BOT_TOKEN=your_telegram_bot_token_here

# Your Telegram user ID (send /start to @userinfobot)
TELEGRAM_CHAT_ID=your_chat_id_here

# Exchange credentials (start with sandbox mode)
EXCHANGE_NAME=binance
EXCHANGE_API_KEY=your_exchange_api_key_here
EXCHANGE_SECRET=your_exchange_secret_here
EXCHANGE_SANDBOX=true
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Start the Bot
```bash
python start_bot.py
```

## 📱 Telegram Commands

### Trading Controls
- `/start_trading` - Start automated trading
- `/stop_trading` - Stop automated trading
- `/trade <symbol>` - Execute manual trade (e.g., `/trade BTC/USDT`)

### Information Commands
- `/status` - Show bot status and configuration
- `/balance` - Show account balance
- `/portfolio` - Show complete portfolio summary
- `/positions` - Show current open positions
- `/price <symbol>` - Get current price (e.g., `/price BTC/USDT`)

### General Commands
- `/start` - Show welcome message
- `/help` - Show all available commands

## ⚙️ Configuration

### Environment Variables

| Variable | Description | Example |
|----------|-------------|---------|
| `TELEGRAM_BOT_TOKEN` | Bot token from @BotFather | `123456:ABC-DEF...` |
| `TELEGRAM_CHAT_ID` | Your Telegram chat ID | `123456789` |
| `EXCHANGE_NAME` | Exchange name (ccxt) | `binance` |
| `EXCHANGE_API_KEY` | Exchange API key | `your_api_key` |
| `EXCHANGE_SECRET` | Exchange secret key | `your_secret` |
| `EXCHANGE_SANDBOX` | Use sandbox mode | `true` |
| `DEFAULT_SYMBOL` | Default trading pair | `BTC/USDT` |
| `TRADE_AMOUNT` | Trade amount in USD | `10.0` |
| `STOP_LOSS_PERCENT` | Stop loss percentage | `2.0` |
| `TAKE_PROFIT_PERCENT` | Take profit percentage | `5.0` |
| `MAX_POSITIONS` | Maximum open positions | `3` |
| `MAX_DAILY_LOSS` | Maximum daily loss limit | `100.0` |
| `MIN_BALANCE` | Minimum account balance | `50.0` |

## 🔧 Setup Instructions

### Getting Telegram Bot Token
1. Message @BotFather on Telegram
2. Send `/newbot` and follow instructions
3. Save your bot token

### Getting Your Chat ID
1. Message @userinfobot on Telegram
2. Send `/start`
3. Save your user ID

### Exchange API Setup
1. Create account on supported exchange (Binance recommended)
2. Generate API keys with trading permissions
3. **Start with sandbox mode for testing**

### Supported Exchanges
- Binance (recommended)
- Coinbase Pro
- Kraken
- Huobi
- And 100+ more via ccxt

## 🛡️ Risk Management

The bot includes multiple safety features:

- **Stop Loss Orders**: Automatically limit losses
- **Take Profit Orders**: Lock in profits
- **Position Limits**: Maximum number of open positions
- **Daily Loss Limits**: Stop trading after daily loss threshold
- **Minimum Balance**: Prevent trading below minimum balance
- **Sandbox Mode**: Test without real money

## 📊 Trading Strategy

Currently implements a Simple Moving Average (SMA) crossover strategy:

- **Buy Signal**: 20-period SMA crosses above 50-period SMA
- **Sell Signal**: 20-period SMA crosses below 50-period SMA
- **Position Sizing**: Fixed USD amount per trade
- **Risk Management**: Automatic SL/TP placement

## 🔍 Monitoring & Logging

- Real-time Telegram notifications
- Daily trading summaries
- Error alerts and notifications
- Comprehensive logging to files
- Portfolio tracking

## ⚠️ Important Warnings

1. **Start with Sandbox Mode**: Always test with sandbox before live trading
2. **Risk Management**: Only trade with money you can afford to lose
3. **API Security**: Keep your API keys secure and never share them
4. **Monitor Positions**: Regularly check your open positions
5. **Understand Strategy**: Make sure you understand the trading logic

## 🛠️ Development

### Project Structure
```
somber/
├── main.py              # Main application entry point
├── trading_bot.py       # Core trading logic
├── telegram_bot.py      # Telegram bot interface
├── start_bot.py         # Startup script with checks
├── requirements.txt     # Python dependencies
├── .env.example         # Environment template
├── .devcontainer/       # Codespaces configuration
└── README.md           # This file
```

### Adding New Strategies
1. Create new strategy method in `TradingBot` class
2. Implement buy/sell signal logic
3. Update `execute_trade()` method to use new strategy

### Contributing
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📝 License

This project is open source and available under the MIT License.

## 🆘 Support

If you encounter issues:

1. Check the logs in the `logs/` directory
2. Verify your environment variables
3. Test with sandbox mode first
4. Check exchange API permissions
5. Ensure sufficient balance

## 🚨 Disclaimer

This software is for educational purposes only. Trading cryptocurrencies involves substantial risk of loss and is not suitable for every investor. Past performance does not guarantee future results. Please trade responsibly.
