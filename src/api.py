from fastapi import FastAPI, Response, HTTPException, Query
from fastapi.responses import StreamingResponse
from enum import Enum
import io
from datetime import datetime, timedelta
import logging
import redis
from typing import Optional
from config import config
from clock_generator import ClockGenerator

logger = logging.getLogger(__name__)

class Orientation(str, Enum):
    """Valid orientation values for the clock display"""
    LANDSCAPE = "landscape"
    PORTRAIT = "portrait"

app = FastAPI(title="SumiClock API")

# Redis client configuration from config
redis_config = config['redis']
try:
    redis_client = redis.Redis(
        host=redis_config['host'],
        port=redis_config['port'],
        db=0,
        socket_connect_timeout=1
    )
    # Connection test
    redis_client.ping()
    logger.info(f"Connected to Redis: {redis_config['host']}:{redis_config['port']}")
except (redis.ConnectionError, redis.TimeoutError) as e:
    logger.warning(f"Cannot connect to Redis: {e}")
    logger.warning(f"Running without cache. Settings: HOST={redis_config['host']}, PORT={redis_config['port']}")
    redis_client = None

def get_cache_key(orientation=None):
    """
    Generate cache key based on current time, timezone and orientation
    
    Args:
        orientation: Optional orientation parameter (landscape or portrait)
    
    Returns:
        str: Cache key string
    """
    current_minute = datetime.now().strftime("%Y%m%d%H%M")
    timezone = config['clock']['timezone']
    orientation_part = f":{orientation}" if orientation else ""
    return f"clock_image:{timezone}{orientation_part}:{current_minute}"

def get_cached_image(orientation=None):
    """
    Get cached image from Redis
    
    Args:
        orientation: Optional orientation parameter
        
    Returns:
        bytes: Cached image data or None if not found
    """
    if redis_client:
        try:
            cache_key = get_cache_key(orientation)
            cached_image = redis_client.get(cache_key)
            if cached_image:
                logger.debug(f"Cache hit: {cache_key}")
                return cached_image
            logger.debug(f"Cache miss: {cache_key}")
        except redis.RedisError as e:
            logger.error(f"Failed to get Redis cache: {e}")
    return None

def cache_image(image_bytes, orientation=None):
    """
    Cache image in Redis
    
    Args:
        image_bytes: PNG image data as bytes
        orientation: Optional orientation parameter
    """
    if redis_client:
        try:
            cache_key = get_cache_key(orientation)
            # Cache expiration from config
            redis_client.setex(
                cache_key,
                timedelta(seconds=redis_config['cache_expire_seconds']),
                image_bytes
            )
            logger.debug(f"Cache saved: {cache_key}")
        except redis.RedisError as e:
            logger.error(f"Failed to save Redis cache: {e}")

@app.get("/health")
async def health_check():
    """
    Health check endpoint
    """
    try:
        # Check Redis connection if configured
        if redis_client:
            redis_client.ping()
        return {"status": "healthy"}
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        raise HTTPException(status_code=500, detail="Service unhealthy")

@app.get("/clock.png")
async def get_clock(orientation: Optional[Orientation] = None):
    """
    Get clock image endpoint
    
    Args:
        orientation: Optional orientation parameter (landscape or portrait)
                   If not provided, the default from config will be used
    
    Returns:
        Response: PNG image of the clock
    """
    try:
        # Check cached image
        cached_image = get_cached_image(orientation)
        if cached_image:
            return Response(content=cached_image, media_type="image/png")
        
        # Generate new image
        logger.debug(f"Generating new clock image with orientation: {orientation or 'default'}")
        generator = ClockGenerator()
        
        # Apply orientation if specified
        if orientation:
            is_portrait = orientation == Orientation.PORTRAIT
            generator.portrait_mode = is_portrait
            
            # Handle dimensions swapping if needed
            if is_portrait and generator.width > generator.height:
                width = generator.width
                generator.width = generator.height
                generator.height = width
        
        image = generator.create_clock_image()
        
        # Convert image to byte stream
        img_byte_arr = io.BytesIO()
        image.save(img_byte_arr, format='PNG', optimize=True)
        img_byte_arr = img_byte_arr.getvalue()
        
        # Cache image
        cache_image(img_byte_arr, orientation)
        
        return Response(content=img_byte_arr, media_type="image/png")
    
    except Exception as e:
        logger.error(f"Error generating clock image: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))