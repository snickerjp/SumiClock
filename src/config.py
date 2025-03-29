import os
from pathlib import Path
import yaml
import logging

logger = logging.getLogger(__name__)

def get_env_value(key: str, default_value: str) -> str:
    """Get value from environment variable or return default"""
    env_key = f"SUMICLOCK_{key.upper()}"
    return os.getenv(env_key, default_value)

def load_config():
    """Load configuration from config.yaml with environment variable support"""
    config_path = Path(__file__).parent.parent / "config.yaml"
    logger.debug(f"Loading configuration from: {config_path}")
    
    try:
        with open(config_path, "r") as f:
            config = yaml.safe_load(f)
            
        # Override with environment variables if provided
        if 'redis' in config:
            config['redis']['host'] = get_env_value('REDIS_HOST', config['redis']['host'])
            config['redis']['port'] = int(get_env_value('REDIS_PORT', str(config['redis']['port'])))
            config['redis']['cache_expire_seconds'] = int(get_env_value(
                'REDIS_CACHE_EXPIRE_SECONDS', 
                str(config['redis']['cache_expire_seconds'])
            ))
        
        if 'clock' in config:
            config['clock']['timezone'] = get_env_value('TIMEZONE', config['clock']['timezone'])
            
        logger.info("Configuration loaded successfully")
        return config
        
    except FileNotFoundError:
        logger.warning(f"Configuration file not found at {config_path}, using defaults")
    except yaml.YAMLError as e:
        logger.error(f"Error parsing configuration file: {e}")
    except Exception as e:
        logger.error(f"Unexpected error loading configuration: {e}")

    # Default settings
    default_config = {
        "redis": {
            "host": get_env_value('REDIS_HOST', "redis"),
            "port": int(get_env_value('REDIS_PORT', "6379")),
            "cache_expire_seconds": int(get_env_value('REDIS_CACHE_EXPIRE_SECONDS', "30"))
        },
        "clock": {
            "timezone": get_env_value('TIMEZONE', "UTC"),
            "width": 1448,
            "height": 1072,
            "font_size": 200,
            "font_path": "/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc"
        }
    }
    logger.info("Using default configuration")
    return default_config

config = load_config()