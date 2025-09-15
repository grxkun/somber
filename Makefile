# Somber Trading Bot Makefile

.PHONY: help install setup test health start clean

# Default target
help:
	@echo "🤖 Somber Trading Bot - Available Commands:"
	@echo ""
	@echo "  install    - Install Python dependencies"
	@echo "  setup      - Initial setup (copy .env template)"
	@echo "  health     - Run health check"
	@echo "  test       - Run functionality tests"
	@echo "  start      - Start the trading bot"
	@echo "  clean      - Clean up temporary files"
	@echo ""
	@echo "📚 Quick start:"
	@echo "  make setup install health"
	@echo ""

# Install dependencies
install:
	@echo "📦 Installing dependencies..."
	pip install -r requirements.txt
	@echo "✅ Dependencies installed!"

# Initial setup
setup:
	@echo "⚙️  Setting up environment..."
	@if [ ! -f .env ]; then \
		cp .env.example .env; \
		echo "✅ Created .env file from template"; \
		echo "📝 Please edit .env with your API credentials"; \
	else \
		echo "⚠️  .env file already exists"; \
	fi
	@mkdir -p logs
	@echo "✅ Setup complete!"

# Run health check
health:
	@echo "🏥 Running health check..."
	python health_check.py

# Run tests
test:
	@echo "🧪 Running tests..."
	python test_functionality.py

# Start the bot
start:
	@echo "🚀 Starting Somber Trading Bot..."
	python start_bot.py

# Clean up
clean:
	@echo "🧹 Cleaning up..."
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	rm -rf .pytest_cache
	@echo "✅ Cleanup complete!"

# Quick setup for new users
quickstart: setup install health
	@echo ""
	@echo "🎉 Quick setup complete!"
	@echo ""
	@echo "📝 Next steps:"
	@echo "  1. Edit .env with your API credentials"
	@echo "  2. Run 'make health' to verify setup"
	@echo "  3. Run 'make start' to launch the bot"