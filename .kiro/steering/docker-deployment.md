# Docker Deployment Guidelines for SumiClock

## Container Architecture

### Multi-Service Setup
- **app**: FastAPI application container
- **redis**: Valkey/Redis cache container
- **network**: Bridge network for service communication

### Service Dependencies
```yaml
depends_on:
  redis:
    condition: service_healthy
```
- Always wait for Redis health check before starting app
- Implement graceful degradation if Redis is unavailable

## Dockerfile Best Practices

### Security
```dockerfile
# Create non-root user
RUN groupadd -r sumiclock && useradd -r -g sumiclock sumiclock
USER sumiclock
```
- Never run containers as root
- Use dedicated user with minimal permissions
- Set proper file ownership

### Image Optimization
- Use slim base images (`python:3.11-slim`)
- Clean up apt cache after installation
- Use `--no-cache-dir` for pip installs
- Minimize layers by combining RUN commands

### Font Installation
```dockerfile
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    fonts-noto-cjk && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*
```
- Install only required fonts
- Clean up package lists to reduce image size
- Use `--no-install-recommends` to avoid unnecessary packages

## Docker Compose Configuration

### Environment Variables
```yaml
environment:
  - SUMICLOCK_REDIS_HOST=redis
  - SUMICLOCK_REDIS_PORT=6379
  - SUMICLOCK_TIMEZONE=${SUMICLOCK_TIMEZONE:-Asia/Tokyo}
  - LOG_LEVEL=${LOG_LEVEL:-INFO}
```
- Use service names for internal networking
- Provide defaults with `${VAR:-default}` syntax
- Document all environment variables

### Volume Mounts
```yaml
volumes:
  - ./src:/app/src
```
- Mount source code for development
- Avoid mounting in production
- Use named volumes for persistent data

### Health Checks
```yaml
healthcheck:
  test: ["CMD", "redis-cli", "ping"]
  interval: 5s
  timeout: 3s
  retries: 3
```
- Implement health checks for all services
- Use appropriate intervals and timeouts
- Consider startup time when setting retries

### Networking
```yaml
networks:
  sumiclock-network:
    driver: bridge
```
- Use custom networks for service isolation
- Enable service discovery via service names
- Consider network security in production

## Development Workflow

### Starting Services
```bash
# Start all services
docker compose up -d

# View logs
docker compose logs -f

# View specific service logs
docker compose logs -f app
```

### Rebuilding
```bash
# Rebuild after code changes
docker compose up -d --build

# Force rebuild
docker compose build --no-cache
```

### Stopping Services
```bash
# Stop services
docker compose down

# Stop and remove volumes
docker compose down -v
```

## Testing with Docker

### Test Environment
```yaml
# docker-compose.test.yml
services:
  test:
    build: .
    command: pytest tests/ -v
    environment:
      - SUMICLOCK_REDIS_HOST=redis-test
    depends_on:
      redis-test:
        condition: service_healthy
```

### Running Tests
```bash
# Run all tests
docker compose -f docker-compose.test.yml up --build test

# Run specific test file
docker compose -f docker-compose.test.yml run --rm test pytest tests/test_api.py -v
```

### Test Isolation
- Use separate Redis instance for tests
- Clean up test artifacts
- Avoid test interference with development environment

## Production Considerations

### Resource Limits
```yaml
deploy:
  resources:
    limits:
      cpus: '0.5'
      memory: 512M
    reservations:
      cpus: '0.25'
      memory: 256M
```

### Restart Policy
```yaml
restart: unless-stopped
```
- Use appropriate restart policy
- Consider failure scenarios
- Monitor container health

### Logging
```yaml
logging:
  driver: "json-file"
  options:
    max-size: "10m"
    max-file: "3"
```
- Configure log rotation
- Use appropriate log driver
- Consider centralized logging

### Security Hardening
- Use read-only root filesystem when possible
- Drop unnecessary capabilities
- Use secrets for sensitive data
- Scan images for vulnerabilities
- Keep base images updated

## Redis/Valkey Configuration

### Using Valkey
```yaml
redis:
  image: valkey/valkey:8
  command: redis-server --loglevel warning
```
- Valkey is Redis-compatible fork
- Use latest stable version
- Configure appropriate log level

### Persistence
```yaml
volumes:
  - redis-data:/data
```
- Consider if persistence is needed
- For cache-only: persistence not required
- For critical data: enable RDB or AOF

### Memory Management
```yaml
command: redis-server --maxmemory 256mb --maxmemory-policy allkeys-lru
```
- Set memory limits
- Use LRU eviction for cache
- Monitor memory usage

## Monitoring and Debugging

### Container Inspection
```bash
# Check container status
docker compose ps

# Inspect container
docker inspect sumiclock-app-1

# Check resource usage
docker stats
```

### Accessing Containers
```bash
# Execute command in running container
docker compose exec app bash

# Run one-off command
docker compose run --rm app python -c "import sys; print(sys.version)"
```

### Network Debugging
```bash
# Test Redis connection
docker compose exec app redis-cli -h redis ping

# Check network connectivity
docker compose exec app ping redis
```

## CI/CD Integration

### Build Pipeline
```bash
# Build and test
docker compose -f docker-compose.test.yml up --build --abort-on-container-exit

# Tag and push
docker tag sumiclock:latest registry.example.com/sumiclock:latest
docker push registry.example.com/sumiclock:latest
```

### Deployment
- Use container orchestration (Kubernetes, ECS, etc.)
- Implement rolling updates
- Monitor deployment health
- Have rollback strategy
