# Testing Strategy for SumiClock

## Testing Philosophy

### Test Pyramid
1. **Unit Tests** (70%): Test individual components in isolation
2. **Integration Tests** (20%): Test component interactions
3. **End-to-End Tests** (10%): Test complete user workflows

### Key Principles
- Write tests before fixing bugs
- Keep tests fast and independent
- Test behavior, not implementation
- Use meaningful test names
- Maintain test code quality

## Unit Testing

### Clock Generator Tests
```python
def test_image_creation(generator):
    """Test if the clock image is created with correct dimensions"""
    image = generator.create_clock_image()
    assert isinstance(image, Image.Image)
    assert image.size == (generator.width, generator.height)
    assert image.mode == "L"  # Grayscale mode
```

### What to Test
- Image dimensions match configuration
- Image mode is correct (grayscale)
- Timezone conversion works correctly
- Font loading with fallback
- Time formatting

### Test Fixtures
```python
@pytest.fixture
def generator():
    return ClockGenerator()

@pytest.fixture
def mock_redis():
    return MagicMock(spec=redis.Redis)
```

## Integration Testing

### API Tests
```python
def test_get_clock_image():
    """Test if the clock image endpoint returns a valid PNG image"""
    response = client.get("/clock.png")
    assert response.status_code == 200
    assert response.headers["content-type"] == "image/png"
    
    # Verify image content
    image = Image.open(io.BytesIO(response.content))
    assert image.format == "PNG"
    assert image.mode == "L"
    assert image.size == (1448, 1072)
```

### What to Test
- API endpoints return correct status codes
- Response headers are correct
- Response content is valid
- Error handling works properly
- Cache behavior is correct

### Redis Integration
```python
def test_cache_hit():
    """Test that cached images are returned"""
    # First request generates image
    response1 = client.get("/clock.png")
    
    # Second request should use cache
    response2 = client.get("/clock.png")
    
    assert response1.content == response2.content
```

## Test Environment

### Docker-based Testing
```bash
# Run all tests
docker compose -f docker-compose.test.yml up --build test

# Run with coverage
docker compose -f docker-compose.test.yml run --rm test pytest --cov=src tests/
```

### Test Configuration
- Use separate Redis instance for tests
- Use test-specific configuration
- Clean up test artifacts
- Isolate test environment

### Environment Variables
```yaml
environment:
  - SUMICLOCK_REDIS_HOST=redis-test
  - SUMICLOCK_TIMEZONE=UTC
  - LOG_LEVEL=DEBUG
```

## Test Data

### Time-based Testing
```python
from freezegun import freeze_time

@freeze_time("2025-12-03 14:30:00")
def test_specific_time():
    """Test clock generation at specific time"""
    generator = ClockGenerator()
    image = generator.create_clock_image()
    # Verify time is rendered correctly
```

### Timezone Testing
```python
@pytest.mark.parametrize("timezone,expected_offset", [
    ("UTC", 0),
    ("Asia/Tokyo", 9),
    ("America/New_York", -5),
])
def test_timezone_offsets(timezone, expected_offset):
    """Test various timezone conversions"""
    # Test implementation
```

## Mocking

### When to Mock
- External services (Redis, APIs)
- File system operations
- Time-dependent operations
- Network calls

### Redis Mocking
```python
from unittest.mock import MagicMock, patch

@patch('src.api.redis_client')
def test_cache_failure(mock_redis):
    """Test graceful handling of Redis failures"""
    mock_redis.get.side_effect = redis.RedisError("Connection failed")
    
    response = client.get("/clock.png")
    assert response.status_code == 200  # Should still work
```

### Font Mocking
```python
@patch('PIL.ImageFont.truetype')
def test_font_fallback(mock_truetype):
    """Test font loading fallback"""
    mock_truetype.side_effect = OSError("Font not found")
    
    generator = ClockGenerator()
    image = generator.create_clock_image()
    assert image is not None  # Should use default font
```

## Performance Testing

### Response Time
```python
import time

def test_response_time():
    """Test that response time is acceptable"""
    start = time.time()
    response = client.get("/clock.png")
    duration = time.time() - start
    
    assert response.status_code == 200
    assert duration < 1.0  # Should respond within 1 second
```

### Cache Performance
```python
def test_cache_improves_performance():
    """Test that caching improves response time"""
    # First request (no cache)
    start1 = time.time()
    client.get("/clock.png")
    duration1 = time.time() - start1
    
    # Second request (cached)
    start2 = time.time()
    client.get("/clock.png")
    duration2 = time.time() - start2
    
    assert duration2 < duration1  # Cached should be faster
```

## Error Testing

### Error Scenarios
```python
def test_error_handling():
    """Test API error handling"""
    response = client.get("/nonexistent")
    assert response.status_code == 404

def test_invalid_timezone():
    """Test handling of invalid timezone"""
    with pytest.raises(pytz.exceptions.UnknownTimeZoneError):
        config['clock']['timezone'] = 'Invalid/Timezone'
        ClockGenerator()
```

### Edge Cases
- Empty configuration
- Missing font files
- Redis connection failures
- Invalid image dimensions
- Timezone edge cases (DST transitions)

## Test Coverage

### Coverage Goals
- Aim for 80%+ code coverage
- Focus on critical paths
- Don't chase 100% coverage
- Test edge cases and error paths

### Running Coverage
```bash
# Generate coverage report
pytest --cov=src --cov-report=html tests/

# View coverage report
open htmlcov/index.html
```

### Coverage Analysis
```bash
# Show missing lines
pytest --cov=src --cov-report=term-missing tests/

# Fail if coverage below threshold
pytest --cov=src --cov-fail-under=80 tests/
```

## Continuous Testing

### Pre-commit Hooks
```bash
# Run tests before commit
pytest tests/ -v

# Run linting
flake8 src/ tests/
black --check src/ tests/
```

### CI Pipeline
```yaml
# .github/workflows/test.yml
- name: Run tests
  run: |
    docker compose -f docker-compose.test.yml up --build --abort-on-container-exit
```

## Test Maintenance

### Keeping Tests Healthy
- Run tests regularly
- Fix flaky tests immediately
- Update tests when code changes
- Remove obsolete tests
- Refactor test code

### Test Documentation
- Use descriptive test names
- Add docstrings to complex tests
- Document test setup requirements
- Explain non-obvious assertions

## Visual Testing

### Image Comparison
```python
from PIL import ImageChops

def test_image_consistency():
    """Test that generated images are consistent"""
    image1 = generator.create_clock_image()
    image2 = generator.create_clock_image()
    
    # Images should be identical at same time
    diff = ImageChops.difference(image1, image2)
    assert diff.getbbox() is None  # No differences
```

### Snapshot Testing
- Save reference images
- Compare generated images to references
- Update snapshots when design changes
- Use visual regression testing tools

## Future Testing Enhancements

### Potential Additions
- Load testing with locust or k6
- Security testing (OWASP checks)
- Accessibility testing
- Cross-browser testing (for web interface)
- Device-specific testing (Kindle, Kobo)
- Chaos engineering (failure injection)
