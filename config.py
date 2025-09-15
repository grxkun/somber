"""
Configuration module for Somnia Trading Bot
Loads environment variables and provides configuration management
"""

import os
from typing import Optional
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


class Config:
    """Configuration class for the Somnia Trading Bot"""
    
    def __init__(self):
        self._load_config()
    
    def _load_config(self):
        """Load configuration from environment variables"""
        # Somnia API Configuration
        self.somnia_api_url = self._get_env_var('SOMNIA_API_URL', required=True)
        
        # Telegram Bot Configuration
        self.telegram_bot_token = self._get_env_var('TELEGRAM_BOT_TOKEN', required=True)
        
        # Optional Configuration
        self.debug = self._get_env_var('DEBUG', default='false').lower() == 'true'
        self.log_level = self._get_env_var('LOG_LEVEL', default='INFO').upper()
    
    def _get_env_var(self, key: str, required: bool = False, default: Optional[str] = None) -> str:
        """
        Get environment variable with validation
        
        Args:
            key: Environment variable name
            required: Whether the variable is required
            default: Default value if not found
            
        Returns:
            Environment variable value
            
        Raises:
            ValueError: If required variable is missing
        """
        value = os.getenv(key, default)
        
        if required and not value:
            raise ValueError(f"Required environment variable '{key}' is not set. "
                           f"Please check your .env file or environment configuration.")
        
        return value
    
    def validate(self):
        """Validate configuration"""
        errors = []
        
        if not self.somnia_api_url:
            errors.append("SOMNIA_API_URL is required")
        elif not self.somnia_api_url.startswith(('http://', 'https://')):
            errors.append("SOMNIA_API_URL must be a valid URL")
        
        if not self.telegram_bot_token:
            errors.append("TELEGRAM_BOT_TOKEN is required")
        elif ':' not in self.telegram_bot_token:
            errors.append("TELEGRAM_BOT_TOKEN appears to be invalid format")
        
        if errors:
            raise ValueError("Configuration validation failed:\n" + "\n".join(f"- {error}" for error in errors))


# Global configuration instance
config = Config()


def get_config() -> Config:
    """Get the global configuration instance"""
    return config


if __name__ == "__main__":
    # Test configuration loading
    try:
        config.validate()
        print("✅ Configuration loaded successfully!")
        print(f"Somnia API URL: {config.somnia_api_url}")
        print(f"Telegram Bot Token: {'*' * (len(config.telegram_bot_token) - 10)}{config.telegram_bot_token[-10:]}")
        print(f"Debug Mode: {config.debug}")
        print(f"Log Level: {config.log_level}")
    except ValueError as e:
        print(f"❌ Configuration error: {e}")