# Somber - Somnia Trading Bot

A Python trading bot for the Somnia network with Telegram integration. The bot loads configuration from environment variables and provides validation for required settings.

Always reference these instructions first and fallback to search or bash commands only when you encounter unexpected information that does not match the info here.

## Working Effectively

### Prerequisites and Setup
- Python 3.8+ is required (Python 3.12.3 confirmed working)
- Use pip for dependency management
- All configuration is managed through environment variables

### Bootstrap, Install, and Build Steps
```bash
# 1. Install Python dependencies (takes ~4 seconds, NEVER CANCEL)
pip install -r requirements.txt

# 2. Set up environment configuration
cp .env.example .env
# Edit .env file with your actual credentials (see Configuration section below)

# 3. Validate configuration
python3 config.py

# 4. Test bot startup
python3 bot.py
```

**TIMING**: Dependency installation completes in approximately 4 seconds. Set timeout to 30+ seconds to be safe.

### Configuration Management
- **ALWAYS** set up the .env file before running the bot or config validation will fail
- Copy `.env.example` to `.env` and replace ALL placeholder values:
  - Replace `YOUR_API_KEY_HERE` with your actual Somnia API key
  - Replace `YOUR_BOT_TOKEN_HERE` with your actual Telegram bot token from @BotFather
- Run `python3 config.py` to validate your configuration before running the bot
- **CRITICAL**: Never commit the `.env` file - it contains sensitive credentials and is already in `.gitignore`

### Validation and Testing
- **ALWAYS** run `python3 config.py` after making configuration changes
- **ALWAYS** test bot startup with `python3 bot.py` after code changes
- **ALWAYS** run syntax validation: `python3 -m py_compile *.py`
- **ALWAYS** test module imports: `python3 -c "import config; import bot"`

### Complete User Scenarios
After making any changes, validate with this complete workflow:

1. **Configuration Setup**:
   ```bash
   cp .env.example .env
   # Edit .env with actual values
   python3 config.py  # Should show ✅ Configuration loaded successfully
   ```

2. **Bot Startup Test**:
   ```bash
   python3 bot.py  # Should show bot starting successfully with ✅ messages
   ```

3. **Error Scenarios Testing**:
   ```bash
   # Test without .env file (should fail gracefully)
   mv .env .env.backup
   python3 config.py  # Should show clear error about missing variables
   mv .env.backup .env
   
   # Test with invalid URL (should fail validation)
   # Edit .env to have invalid SOMNIA_API_URL
   python3 config.py  # Should show URL validation error
   ```

## Project Structure

### Repository Root
```
somber/
├── .env                 # Environment variables (NEVER COMMIT - in .gitignore)
├── .env.example         # Template for environment variables
├── .gitignore          # Git ignore rules (includes .env)
├── README.md           # Project documentation
├── requirements.txt    # Python dependencies (python-dotenv, requests, python-telegram-bot)
├── config.py           # Configuration management with validation
└── bot.py             # Main bot application
```

### Key Files
- **`bot.py`**: Main application entry point. Contains `SomniaTradeBot` class with initialization, API connections, and run logic
- **`config.py`**: Configuration management. Loads environment variables, validates required settings, provides error handling. Can be run standalone for testing
- **`requirements.txt`**: Python dependencies. Install with `pip install -r requirements.txt`
- **`.env.example`**: Template showing required environment variables with placeholder values

## Common Tasks

### Configuration Testing
```bash
# Test current configuration
python3 config.py

# Expected successful output:
# ✅ Configuration loaded successfully!
# Somnia API URL: https://mainnet.somnia.validationcloud.io/v1/[API-KEY]
# Telegram Bot Token: *******[last-10-chars]
# Debug Mode: False
# Log Level: INFO
```

### Bot Operations
```bash
# Run the bot
python3 bot.py

# Expected successful startup log:
# INFO - Bot initialized successfully
# INFO - Starting Somnia Trading Bot...
# INFO - Connecting to Somnia API at: [URL]
# INFO - ✅ Connected to Somnia API
# INFO - Setting up Telegram bot...
# INFO - ✅ Telegram bot setup complete
# INFO - 🚀 Bot is running!
# INFO - Trading logic not implemented yet
```

### Error Handling Verification
- Missing .env file: Clear error message about missing environment variables
- Invalid SOMNIA_API_URL: "must be a valid URL" validation error
- Invalid TELEGRAM_BOT_TOKEN: "appears to be invalid format" validation error
- Configuration validation runs automatically on bot startup and will exit with status 1 on errors

### Environment Variables Reference
| Variable | Required | Format | Example |
|----------|----------|--------|---------|
| `SOMNIA_API_URL` | Yes | Valid HTTPS URL | `https://mainnet.somnia.validationcloud.io/v1/KEY` |
| `TELEGRAM_BOT_TOKEN` | Yes | Format: `number:string` | `123456789:ABCD-your-bot-token` |
| `DEBUG` | No | `true` or `false` | `false` (default) |
| `LOG_LEVEL` | No | DEBUG/INFO/WARNING/ERROR | `INFO` (default) |

## Development Guidelines

### Making Changes
- **ALWAYS** validate syntax after code changes: `python3 -m py_compile *.py`
- **ALWAYS** test configuration loading after changing `config.py`: `python3 config.py`
- **ALWAYS** test bot startup after changes: `python3 bot.py`
- **NEVER** commit the `.env` file - sensitive credentials must stay local
- Configuration validation happens automatically during bot initialization

### Code Structure
- Configuration logic is centralized in `config.py` with the `Config` class
- Environment variable loading uses `python-dotenv` for `.env` file support
- All required variables are validated with clear error messages
- Bot initialization fails fast if configuration is invalid

### Adding New Configuration
1. Add variable to `.env.example` with placeholder value
2. Add loading logic to `Config._load_config()` method
3. Add validation rules to `Config.validate()` method if needed
4. Update this documentation with the new variable

### Debugging
- Set `DEBUG=true` and `LOG_LEVEL=DEBUG` in `.env` for verbose logging
- Run `python3 config.py` to test configuration in isolation
- Check that all required dependencies are installed: `pip list | grep -E "(dotenv|requests|telegram)"`

## Dependencies and Versions
- **python-dotenv==1.0.0**: Environment variable loading from .env files
- **requests==2.31.0**: HTTP client for API calls (pre-installed)
- **python-telegram-bot==20.7**: Telegram bot API integration

Installation is fast (~4 seconds) and reliable. No additional build steps required.