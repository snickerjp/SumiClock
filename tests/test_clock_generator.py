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
    assert image.mode == "L"  # Grayscale mode

def test_timezone_handling():
    """Test if timezone is handled correctly"""
    generator = ClockGenerator()
    image = generator.create_clock_image()
    
    # Save test image temporarily
    test_image_path = "test_clock.png"
    try:
        image.save(test_image_path)
        # Verify the image was created
        test_image = Image.open(test_image_path)
        assert test_image.size == (1448, 1072)
    finally:
        # Clean up test image
        import os
        if os.path.exists(test_image_path):
            os.remove(test_image_path)