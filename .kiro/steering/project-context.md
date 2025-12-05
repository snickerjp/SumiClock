# SumiClock Project Context

## Project Overview
SumiClock is a minimalist digital clock image generator optimized for E-paper displays (Kindle, Kobo). It generates clean, high-contrast clock images that are perfect for low-power E-ink screens.

## Technology Stack
- **Backend**: FastAPI (Python 3.11)
- **Caching**: Redis
- **Image Generation**: Pillow (PIL)
- **Deployment**: Docker & Docker Compose
- **Font**: Noto Sans CJK

## Key Features
- Real-time clock image generation
- Timezone support
- Redis caching for performance
- Configurable image dimensions
- E-paper optimized output (black & white, high contrast)

## Target Devices
- Kindle e-readers
- Kobo e-readers
- Other E-paper displays

## Development Goals
- Maintain minimal, clean design
- Optimize for E-paper display characteristics
- Keep response times low with caching
- Support multiple timezones
- Easy configuration via YAML

## Current Status
- Basic functionality implemented
- Docker deployment working
- Redis caching functional
- Need to improve E-paper display optimization
