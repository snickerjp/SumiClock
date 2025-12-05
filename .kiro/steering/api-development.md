# API Development Guidelines for SumiClock

## FastAPI Best Practices

### Endpoint Design
- Use clear, RESTful endpoint names
- Return appropriate HTTP status codes
- Include proper error handling with HTTPException
- Use Response models for type safety

### Response Types
- For image endpoints: Use `Response` with appropriate `media_type`
- For JSON endpoints: Use Pydantic models
- Always set correct Content-Type headers

### Error Handling
```python
try:
    # Operation
except SpecificException as e:
    logger.error(f"Error description: {e}", exc_info=True)
    raise HTTPException(status_code=500, detail=str(e))
```

## Caching Strategy

### Redis Integration
- Always check Redis connection before operations
- Implement graceful fallback when Redis is unavailable
- Use meaningful cache keys with timestamps
- Set appropriate TTL based on data freshness requirements

### Cache Key Design
- Include relevant parameters in cache key
- Use consistent naming convention: `{resource}:{identifier}`
- Example: `clock_image:202512031430` for minute-based caching

### Cache Expiration
- For clock images: 30-60 seconds (configurable)
- Consider timezone when setting expiration
- Use `setex` for atomic set-with-expiration

## Image Generation

### E-Paper Optimization
- Always use grayscale mode ('L') for E-paper displays
- Use high contrast (pure black 0, pure white 255)
- Avoid gradients and anti-aliasing when possible
- Optimize PNG compression with `optimize=True`

### Image Response
```python
# Convert PIL Image to bytes
img_byte_arr = io.BytesIO()
image.save(img_byte_arr, format='PNG', optimize=True)
img_byte_arr = img_byte_arr.getvalue()

return Response(content=img_byte_arr, media_type="image/png")
```

## Logging

### Log Levels
- DEBUG: Cache hits/misses, detailed operations
- INFO: Startup, configuration, successful operations
- WARNING: Fallback scenarios, non-critical issues
- ERROR: Exceptions, failed operations (with exc_info=True)

### Log Messages
- Include context: what, where, why
- Use structured logging when possible
- Log configuration on startup
- Log cache operations for debugging

## Configuration

### Environment Variables
- Prefix all env vars with `SUMICLOCK_`
- Provide sensible defaults
- Document all configuration options
- Support both config.yaml and env vars

### Configuration Priority
1. Environment variables (highest)
2. config.yaml
3. Hard-coded defaults (lowest)

## Testing Endpoints

### Manual Testing
```bash
# Get clock image
curl http://localhost:8000/clock.png -o clock.png

# Check response headers
curl -I http://localhost:8000/clock.png

# Test with different timezones
docker compose up -d -e SUMICLOCK_TIMEZONE=America/New_York
```

### Automated Testing
- Test successful image generation
- Test error handling
- Test cache behavior
- Verify image format and dimensions
