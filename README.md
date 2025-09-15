# Somber - Somnia Trading Bot

A trading bot for the Somnia network with Telegram integration.

## Setup

### Prerequisites

- Python 3.8 or higher
- pip (Python package installer)

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/grxkun/somber.git
   cd somber
   ```

2. Install required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Set up environment variables:
   ```bash
   cp .env.example .env
   ```

4. Edit the `.env` file with your actual credentials:
   ```bash
   nano .env  # or use your preferred editor
   ```

### Environment Variables

The following environment variables are required for the bot to function:

| Variable | Description | Required |
|----------|-------------|----------|
| `SOMNIA_API_URL` | Somnia network API endpoint URL | Yes |
| `TELEGRAM_BOT_TOKEN` | Telegram bot token from @BotFather | Yes |
| `DEBUG` | Enable debug mode (true/false) | No (default: false) |
| `LOG_LEVEL` | Logging level (DEBUG, INFO, WARNING, ERROR) | No (default: INFO) |

#### Getting Your Credentials

1. **Somnia API URL**: 
   - Use the provided mainnet endpoint or get your own from Somnia network
   - Format: `https://mainnet.somnia.validationcloud.io/v1/YOUR_API_KEY`

2. **Telegram Bot Token**:
   - Message @BotFather on Telegram
   - Create a new bot with `/newbot`
   - Copy the token provided

### Configuration Example

Your `.env` file should look like this:



## Usage

### Running the Bot

```bash
python bot.py
```

### Testing Configuration

Test your environment variables setup:

```bash
python config.py
```

This will validate your configuration and show you what values are loaded.

## Development

### Project Structure

```
somber/
├── .env                 # Environment variables (DO NOT COMMIT)
├── .env.example         # Environment variables template
├── .gitignore          # Git ignore rules
├── README.md           # This file
├── requirements.txt    # Python dependencies
├── config.py           # Configuration management
└── bot.py             # Main bot application
```

### Adding New Environment Variables

1. Add the variable to `.env.example` with a placeholder value
2. Add the variable to your local `.env` file with the actual value
3. Update the `Config` class in `config.py` to load the new variable
4. Update this README with documentation for the new variable

### Security Notes

- **Never commit the `.env` file** - it contains sensitive credentials
- The `.env` file is already included in `.gitignore`
- Always use environment variables for sensitive data
- Use `.env.example` to document required variables without exposing secrets

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Update documentation if needed
5. Submit a pull request

## License

This project is licensed under the MIT License.
