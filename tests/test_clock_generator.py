import pytest
from datetime import datetime
import pytz
from PIL import Image
from src.clock_generator import ClockGenerator

@pytest.fixture
def generator():
    return ClockGenerator()

def test_image_creation(generator):
    """Test if the clock image is created with correct dimensions"""
    image = generator.create_clock_image()
    assert isinstance(image, Image.Image)
    assert image.size == (generator.width, generator.height)
    assert image.mode == 'L'  # Grayscale mode

def test_timezone_handling(monkeypatch):
    """Test if timezone is handled correctly"""
    # Mock datetime to return a fixed time
    fixed_time = datetime(2024, 1, 1, 12, 0, tzinfo=pytz.UTC)
    class MockDateTime:
        @classmethod
        def now(cls, tz=None):
            return fixed_time
    monkeypatch.setattr('src.clock_generator.datetime', MockDateTime)
    
    # Test UTC
    generator_utc = ClockGenerator()
    generator_utc.timezone = pytz.UTC
    image_utc = generator_utc.create_clock_image()
    
    # Test JST (UTC+9)
    generator_jst = ClockGenerator()
    generator_jst.timezone = pytz.timezone('Asia/Tokyo')
    image_jst = generator_jst.create_clock_image()
    
    assert image_utc != image_jst  # Images should be different due to timezone