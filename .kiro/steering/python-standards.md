# Python Development Standards for SumiClock

## Code Style

### Style Guide
- Follow [Google Python Style Guide](https://google.github.io/styleguide/pyguide.html)
- Use PEP 8 as baseline with Google-specific conventions
- Use type hints for function parameters and return values
- Maximum line length: 100 characters
- Use descriptive variable and function names

### Code Formatting with Black
```bash
# Format all Python files
black src/ tests/

# Check formatting without making changes
black --check src/ tests/

# Format with specific line length
black --line-length 100 src/ tests/
```

**Black Configuration** (pyproject.toml):
```toml
[tool.black]
line-length = 100
target-version = ['py311']
include = '\.pyi?$'
extend-exclude = '''
/(
  # directories
  \.eggs
  | \.git
  | \.hg
  | \.mypy_cache
  | \.tox
  | \.venv
  | build
  | dist
)/
'''
```

### Type Checking with mypy
```bash
# Run type checking
mypy src/

# Run with strict mode
mypy --strict src/

# Check specific file
mypy src/api.py
```

**mypy Configuration** (pyproject.toml):
```toml
[tool.mypy]
python_version = "3.11"
warn_return_any = true
warn_unused_configs = true
disallow_untyped_defs = true
disallow_incomplete_defs = true
check_untyped_defs = true
disallow_untyped_decorators = false
no_implicit_optional = true
warn_redundant_casts = true
warn_unused_ignores = true
warn_no_return = true
warn_unreachable = true
strict_equality = true
```

### Docstring Style (Google Format)
```python
def create_clock_image(self, timezone: str = "UTC") -> Image.Image:
    """Create a clock image for the specified timezone.
    
    Args:
        timezone: IANA timezone identifier (e.g., 'Asia/Tokyo', 'UTC').
            Defaults to 'UTC'.
    
    Returns:
        PIL Image object in grayscale mode ('L') with clock display.
    
    Raises:
        pytz.exceptions.UnknownTimeZoneError: If timezone is invalid.
        OSError: If font file cannot be loaded.
    
    Example:
        >>> generator = ClockGenerator()
        >>> image = generator.create_clock_image('Asia/Tokyo')
        >>> image.save('clock.png')
    """
    pass
```

### Import Organization
```python
# Standard library imports
import os
import sys
from datetime import datetime
from pathlib import Path

# Third-party imports
import pytz
import redis
from fastapi import FastAPI, HTTPException
from PIL import Image, ImageDraw, ImageFont

# Local application imports
from src.config import config
from src.clock_generator import ClockGenerator
```

### Naming Conventions (Google Style)
- **Modules**: `lowercase_with_underscores.py`
- **Classes**: `CapitalizedWords` (PascalCase)
- **Functions**: `lowercase_with_underscores()`
- **Variables**: `lowercase_with_underscores`
- **Constants**: `UPPERCASE_WITH_UNDERSCORES`
- **Private**: `_leading_underscore`

## Project Structure
- Keep business logic in separate modules under `src/`
- Configuration management in `src/config.py`
- API endpoints in `src/api.py`
- Core functionality in dedicated modules

## Dependencies
- Use `requirements.txt` for dependency management
- Pin major versions for stability
- Document any system-level dependencies

## Docker
- Use multi-stage builds when possible
- Run as non-root user for security
- Keep images minimal and efficient

## Code Quality Tools

### Pre-commit Hooks
```bash
# Install pre-commit
pip install pre-commit

# Install hooks
pre-commit install

# Run manually
pre-commit run --all-files
```

**Pre-commit Configuration** (.pre-commit-config.yaml):
```yaml
repos:
  - repo: https://github.com/psf/black
    rev: 23.12.1
    hooks:
      - id: black
        language_version: python3.11
        args: [--line-length=100]
  
  - repo: https://github.com/pre-commit/mirrors-mypy
    rev: v1.8.0
    hooks:
      - id: mypy
        additional_dependencies: [types-all]
        args: [--strict]
  
  - repo: https://github.com/pycqa/flake8
    rev: 7.0.0
    hooks:
      - id: flake8
        args: [--max-line-length=100, --extend-ignore=E203]
  
  - repo: https://github.com/pycqa/isort
    rev: 5.13.2
    hooks:
      - id: isort
        args: [--profile=black, --line-length=100]
```

### Linting with flake8
```bash
# Run flake8
flake8 src/ tests/

# With specific configuration
flake8 --max-line-length=100 --extend-ignore=E203 src/
```

**flake8 Configuration** (.flake8):
```ini
[flake8]
max-line-length = 100
extend-ignore = E203, W503
exclude =
    .git,
    __pycache__,
    .venv,
    venv,
    build,
    dist
per-file-ignores =
    __init__.py:F401
```

### Import Sorting with isort
```bash
# Sort imports
isort src/ tests/

# Check without modifying
isort --check-only src/ tests/
```

**isort Configuration** (pyproject.toml):
```toml
[tool.isort]
profile = "black"
line_length = 100
multi_line_output = 3
include_trailing_comma = true
force_grid_wrap = 0
use_parentheses = true
ensure_newline_before_comments = true
```

## Testing
- Write tests for core functionality
- Use pytest for testing
- Keep tests in `tests/` directory
- Aim for meaningful test coverage
- Follow Google's testing best practices

## Development Workflow

### Quick Start
```bash
# Install dependencies
make install-dev

# Format code
make format

# Run all checks
make check

# Run tests
make test

# Run tests with coverage
make test-cov
```

### Daily Development
1. Write code following Google Python Style Guide
2. Run `make format` to auto-format
3. Run `make check` before committing
4. Write tests for new functionality
5. Ensure tests pass with `make test`

### Pre-commit Hooks
Pre-commit hooks automatically run on `git commit`:
- Trailing whitespace removal
- End-of-file fixer
- YAML/JSON/TOML validation
- Black formatting
- isort import sorting
- flake8 linting
- mypy type checking

To run manually:
```bash
pre-commit run --all-files
```

## E-Paper Display Optimization
- Generate high-contrast black and white images
- Optimize for E-paper refresh characteristics
- Consider image size and format for E-paper devices
- Cache generated images to reduce processing

## Additional Resources
- [Google Python Style Guide](https://google.github.io/styleguide/pyguide.html)
- [Black Documentation](https://black.readthedocs.io/)
- [mypy Documentation](https://mypy.readthedocs.io/)
- [pytest Documentation](https://docs.pytest.org/)
- [EditorConfig](https://editorconfig.org/)
