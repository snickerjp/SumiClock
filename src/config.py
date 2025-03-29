import os
from pathlib import Path
import yaml
import logging

logger = logging.getLogger(__name__)

def load_config():
    """Load configuration from config.yaml"""
    config_path = Path(__file__).parent.parent / "config.yaml"
    logger.debug(f"Loading configuration from: {config_path}")
    
    try:
        with open(config_path, "r") as f:
            config = yaml.safe_load(f)
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
            "host": "redis",
            "port": 6379,
            "cache_expire_seconds": 30
        },
        "clock": {
            "timezone": "UTC",
            "width": 1448,
            "height": 1072,
            "font_size": 200,
            "font_path": "/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc"
        }
    }
    logger.info("Using default configuration")
    return default_config

config = load_config()