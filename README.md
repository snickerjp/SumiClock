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

### Testing

Run tests using Docker:
```bash
# Run tests in a temporary container
docker compose run --rm app python -m pytest
```

## API Endpoints

- `GET /clock.png`: Returns the current time as a PNG image
  - Response: PNG image (1448x1072, grayscale)
  - Cache: Redis-based caching (30 seconds)

## E-paper Device Setup

### Kindle

1. Enable USB Networking on your Kindle
2. Create a cron job or script to fetch the clock image:
```bash
wget -O /mnt/us/screensaver/clock.png http://your-server:8000/clock.png
```

### Kobo

1. Install KOReader or similar customization
2. Set up a periodic task to fetch the clock image:
```bash
wget -O /mnt/onboard/.screensaver/clock.png http://your-server:8000/clock.png
```

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