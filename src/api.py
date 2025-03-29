from fastapi import FastAPI, Response, HTTPException
from fastapi.responses import StreamingResponse
import io
from datetime import datetime, timedelta
import logging
import redis
from config import config
from clock_generator import ClockGenerator

logger = logging.getLogger(__name__)

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

def get_cache_key():
    """Generate cache key based on current time and timezone"""
    current_minute = datetime.now().strftime("%Y%m%d%H%M")
    timezone = config['clock']['timezone']
    return f"clock_image:{timezone}:{current_minute}"

def get_cached_image():
    """Get cached image from Redis"""
    if redis_client:
        try:
            cache_key = get_cache_key()
            cached_image = redis_client.get(cache_key)
            if cached_image:
                logger.debug(f"Cache hit: {cache_key}")
                return cached_image
            logger.debug(f"Cache miss: {cache_key}")
        except redis.RedisError as e:
            logger.error(f"Failed to get Redis cache: {e}")
    return None

def cache_image(image_bytes):
    """Cache image in Redis"""
    if redis_client:
        try:
            cache_key = get_cache_key()
            # Cache expiration from config
            redis_client.setex(
                cache_key,
                timedelta(seconds=redis_config['cache_expire_seconds']),
                image_bytes
            )
            logger.debug(f"Cache saved: {cache_key}")
        except redis.RedisError as e:
            logger.error(f"Failed to save Redis cache: {e}")

@app.get("/clock.png")
async def get_clock():
    try:
        # Check cached image
        cached_image = get_cached_image()
        if cached_image:
            return Response(content=cached_image, media_type="image/png")
        
        # Generate new image
        logger.debug("Generating new clock image")
        generator = ClockGenerator()
        image = generator.create_clock_image()
        
        # Convert image to byte stream
        img_byte_arr = io.BytesIO()
        image.save(img_byte_arr, format='PNG', optimize=True)
        img_byte_arr = img_byte_arr.getvalue()
        
        # Cache image
        cache_image(img_byte_arr)
        
        return Response(content=img_byte_arr, media_type="image/png")
    
    except Exception as e:
        logger.error(f"Error generating clock image: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))