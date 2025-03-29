# SumiClock

A minimalist digital clock image generator for E-paper displays (Kindle, Kobo), built with FastAPI and Redis caching.

## Overview

SumiClock generates a clean, high-contrast digital clock image optimized for e-paper displays. It uses Redis for caching and supports custom timezone settings.

## Quick Start with Docker

The easiest way to run SumiClock is using Docker and Docker Compose:

```bash
# Clone the repository
git clone https://github.com/yourusername/sumiclock.git
cd sumiclock

# Start the application
docker compose up -d
```

The clock image will be available at:
```
http://localhost:8000/clock.png
```

## Configuration

All configuration is managed through `config.yaml`:

```yaml
redis:
  host: redis
  port: 6379
  cache_expire_seconds: 30

clock:
  timezone: "Asia/Tokyo"  # Any valid IANA timezone
  width: 1448            # Image width
  height: 1072          # Image height
  font_size: 200
  font_path: /usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc
```

## Project Structure

```
.
├── src/                # Source code
│   ├── api.py         # FastAPI application
│   ├── clock_generator.py  # Clock image generation
│   ├── config.py      # Configuration management
│   └── main.py        # Application entry point
├── tests/             # Test files
├── compose.yaml       # Docker Compose configuration
├── config.yaml        # Application configuration
└── Dockerfile         # Container definition
```

## Development

### Prerequisites

- Docker
- Docker Compose
- Python 3.11 or later (for local development)

### Using Docker Compose

1. Start the services:
```bash
docker compose up -d
```

2. View logs:
```bash
docker compose logs -f
```

3. Stop the services:
```bash
docker compose down
```

### Building the Image

```bash
docker compose build
# or
docker build -t sumiclock .
```

## Testing

Tests can be run using the dedicated test environment with Docker Compose:

```bash
# Run all tests
docker compose -f docker-compose.test.yml up --build test

# Run specific test file
docker compose -f docker-compose.test.yml run --rm test pytest tests/test_api.py -v

# Run specific test case
docker compose -f docker-compose.test.yml run --rm test pytest tests/test_api.py::test_get_clock_image -v
```

The test environment includes:
- Isolated Redis instance for testing
- Proper Python path configuration
- Automatic cleanup of test artifacts

### Available Tests

- `test_api.py`: Tests for the FastAPI endpoints
  - `test_get_clock_image`: Validates image generation and response
  - `test_error_handling`: Verifies proper error responses

- `test_clock_generator.py`: Tests for the clock image generation
  - `test_image_creation`: Validates image dimensions and format
  - `test_timezone_handling`: Verifies timezone conversion

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Run tests (`docker compose run --rm app python -m pytest`)
4. Commit your changes (`git commit -m 'Add amazing feature'`)
5. Push to the branch (`git push origin feature/amazing-feature`)
6. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Credits

- Font: Noto Sans CJK by Google
- Built with FastAPI, Redis, and Pillow