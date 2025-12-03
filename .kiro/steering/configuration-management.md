# Configuration Management for SumiClock

## Configuration Philosophy

### Principles
- **Environment-first**: Environment variables override file configuration
- **Sensible defaults**: Application works out-of-the-box
- **Type safety**: Validate configuration values
- **Documentation**: All options clearly documented

### Configuration Sources (Priority Order)
1. Environment variables (highest priority)
2. config.yaml file
3. Hard-coded defaults (lowest priority)

## Configuration Structure

### YAML Configuration
```yaml
redis:
  host: redis
  port: 6379
  cache_expire_seconds: 30

clock:
  timezone: Asia/Tokyo
  width: 1448
  height: 1072
  font_size: 200
  font_path: /usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc
```

### Environment Variables
```bash
# Redis configuration
SUMICLOCK_REDIS_HOST=redis
SUMICLOCK_REDIS_PORT=6379
SUMICLOCK_REDIS_CACHE_EXPIRE_SECONDS=30

# Clock configuration
SUMICLOCK_TIMEZONE=Asia/Tokyo

# Application configuration
LOG_LEVEL=INFO
```

## Configuration Loading

### Implementation Pattern
```python
def get_env_value(key: str, default_value: str) -> str:
    """Get value from environment variable or return default"""
    env_key = f"SUMICLOCK_{key.upper()}"
    return os.getenv(env_key, default_value)

def load_config():
    """Load configuration from config.yaml with environment variable support"""
    # Load from file
    with open(config_path, "r") as f:
        config = yaml.safe_load(f)
    
    # Override with environment variables
    config['redis']['host'] = get_env_value('REDIS_HOST', config['redis']['host'])
    
    return config
```

### Error Handling
- Gracefully handle missing config file
- Provide clear error messages
- Fall back to defaults when appropriate
- Log configuration source

## Redis Configuration

### Connection Settings
```yaml
redis:
  host: redis          # Hostname or IP
  port: 6379          # Port number
  db: 0               # Database number (optional)
  socket_connect_timeout: 1  # Connection timeout in seconds
```

### Cache Settings
```yaml
redis:
  cache_expire_seconds: 30  # TTL for cached images
```

### Best Practices
- Use service names in Docker Compose
- Set reasonable connection timeouts
- Implement connection retry logic
- Handle connection failures gracefully

## Clock Configuration

### Display Settings
```yaml
clock:
  width: 1448         # Image width in pixels
  height: 1072        # Image height in pixels
  font_size: 200      # Font size in points
```

### Common E-Paper Resolutions
- Kindle Paperwhite: 1448x1072
- Kindle Oasis: 1680x1264
- Kobo Libra: 1264x1680
- Kobo Forma: 1440x1920

### Timezone Configuration
```yaml
clock:
  timezone: Asia/Tokyo  # IANA timezone identifier
```

### Valid Timezone Examples
- `UTC`: Coordinated Universal Time
- `Asia/Tokyo`: Japan Standard Time
- `America/New_York`: Eastern Time
- `Europe/London`: British Time
- `Australia/Sydney`: Australian Eastern Time

### Font Configuration
```yaml
clock:
  font_path: /usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc
```

### Font Selection
- Use TrueType (.ttf) or OpenType (.otf) fonts
- Ensure font supports required characters
- Consider font weight and style
- Test font rendering on target device

## Logging Configuration

### Log Levels
```bash
LOG_LEVEL=DEBUG   # Detailed debugging information
LOG_LEVEL=INFO    # General information (default)
LOG_LEVEL=WARNING # Warning messages only
LOG_LEVEL=ERROR   # Error messages only
```

### Logging Best Practices
- Use INFO for production
- Use DEBUG for development
- Log configuration on startup
- Include context in log messages

## Environment-Specific Configuration

### Development
```yaml
# config.yaml (development)
redis:
  host: localhost
  cache_expire_seconds: 10  # Shorter cache for testing

clock:
  timezone: UTC
```

```bash
# .env (development)
LOG_LEVEL=DEBUG
SUMICLOCK_REDIS_HOST=localhost
```

### Production
```yaml
# config.yaml (production)
redis:
  host: redis-prod.example.com
  cache_expire_seconds: 60

clock:
  timezone: Asia/Tokyo
```

```bash
# Environment variables (production)
LOG_LEVEL=INFO
SUMICLOCK_REDIS_HOST=redis-prod.example.com
SUMICLOCK_REDIS_PORT=6379
```

### Testing
```yaml
# config.yaml (testing)
redis:
  host: redis-test
  cache_expire_seconds: 5

clock:
  timezone: UTC
  width: 800
  height: 600
```

## Configuration Validation

### Type Checking
```python
def validate_config(config: dict) -> bool:
    """Validate configuration values"""
    # Check required fields
    assert 'redis' in config
    assert 'clock' in config
    
    # Validate types
    assert isinstance(config['redis']['port'], int)
    assert isinstance(config['clock']['width'], int)
    
    # Validate ranges
    assert config['redis']['port'] > 0
    assert config['clock']['width'] > 0
    
    return True
```

### Timezone Validation
```python
import pytz

def validate_timezone(timezone: str) -> bool:
    """Validate timezone string"""
    try:
        pytz.timezone(timezone)
        return True
    except pytz.exceptions.UnknownTimeZoneError:
        logger.error(f"Invalid timezone: {timezone}")
        return False
```

## Docker Configuration

### Docker Compose Environment
```yaml
services:
  app:
    environment:
      - SUMICLOCK_REDIS_HOST=redis
      - SUMICLOCK_REDIS_PORT=6379
      - SUMICLOCK_TIMEZONE=${SUMICLOCK_TIMEZONE:-Asia/Tokyo}
      - LOG_LEVEL=${LOG_LEVEL:-INFO}
```

### Using .env File
```bash
# .env
SUMICLOCK_TIMEZONE=America/New_York
LOG_LEVEL=DEBUG
```

```bash
# Docker Compose automatically loads .env
docker compose up -d
```

### Override at Runtime
```bash
# Override specific variables
docker compose up -d \
  -e SUMICLOCK_TIMEZONE=Europe/London \
  -e LOG_LEVEL=DEBUG
```

## Configuration Documentation

### README Documentation
- List all configuration options
- Provide example values
- Explain each option's purpose
- Show environment variable names

### Inline Documentation
```python
config = {
    "redis": {
        "host": "redis",  # Redis server hostname
        "port": 6379,     # Redis server port
        "cache_expire_seconds": 30  # Cache TTL in seconds
    }
}
```

## Security Considerations

### Sensitive Data
- Never commit secrets to version control
- Use environment variables for sensitive data
- Consider using secrets management (Vault, AWS Secrets Manager)
- Rotate credentials regularly

### Configuration Files
```bash
# .gitignore
config.local.yaml
.env
*.secret
```

### Docker Secrets
```yaml
services:
  app:
    secrets:
      - redis_password

secrets:
  redis_password:
    file: ./secrets/redis_password.txt
```

## Configuration Testing

### Test Different Configurations
```python
def test_config_loading():
    """Test configuration loading from file"""
    config = load_config()
    assert 'redis' in config
    assert 'clock' in config

def test_env_override():
    """Test environment variable override"""
    os.environ['SUMICLOCK_REDIS_HOST'] = 'test-redis'
    config = load_config()
    assert config['redis']['host'] == 'test-redis'
```

### Test Default Values
```python
def test_default_config():
    """Test that defaults are sensible"""
    config = load_config()
    assert config['redis']['port'] == 6379
    assert config['clock']['timezone'] == 'UTC'
```

## Configuration Migration

### Version Compatibility
- Support old configuration formats
- Provide migration scripts
- Document breaking changes
- Use semantic versioning

### Migration Example
```python
def migrate_config_v1_to_v2(old_config: dict) -> dict:
    """Migrate configuration from v1 to v2"""
    new_config = old_config.copy()
    
    # Rename fields
    if 'cache_ttl' in new_config['redis']:
        new_config['redis']['cache_expire_seconds'] = \
            new_config['redis'].pop('cache_ttl')
    
    return new_config
```

## Future Configuration Enhancements

### Potential Features
- Hot reload configuration without restart
- Configuration validation on startup
- Configuration UI/API
- Multiple clock configurations
- Per-device configuration profiles
- A/B testing configuration
