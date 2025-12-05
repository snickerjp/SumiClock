import pytest
from datetime import datetime
import sys
import os
import pytz
from PIL import Image
from unittest.mock import patch, MagicMock, mock_open
from pathlib import Path

# Add src directory to path for imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from clock_generator import ClockGenerator
from weather_icon_generator import WeatherIconGenerator

@pytest.fixture
def mock_config():
    return {
        'clock': {
            'timezone': 'UTC',
            'width': 1448,
            'height': 1072,
            'font_size': 200,
            'date_font_size': 100,
            'weather_font_size': 120,
            'font_path': '/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc',
            'display_weather': False,
            'weather_api_key': '',
            'weather_city': 'Tokyo',
            'weather_units': 'metric',
            'dark_mode_start': 18,
            'dark_mode_end': 6,
            'portrait_mode': False
        }
    }

@pytest.fixture
def generator(mock_config):
    with patch('clock_generator.config', mock_config):
        with patch('os.makedirs'):  # Mock directory creation
            return ClockGenerator(timezone="UTC")

def test_image_creation(generator):
    """Test if the clock image is created with correct dimensions"""
    image = generator.create_clock_image()
    assert isinstance(image, Image.Image)
    assert image.size == (generator.width, generator.height)
    assert image.mode == "L"  # Grayscale mode

def test_portrait_mode():
    """Test if portrait mode layout is created correctly"""
    with patch('clock_generator.config', {
        'clock': {
            'timezone': 'UTC',
            'width': 1072,  # Swapped dimensions for portrait
            'height': 1448,
            'font_size': 200,
            'date_font_size': 100,
            'weather_font_size': 120,
            'font_path': '/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc',
            'display_weather': False,
            'portrait_mode': True  # Enable portrait mode
        }
    }):
        with patch('os.makedirs'):
            generator = ClockGenerator()
            # Check that portrait mode is enabled
            assert generator.portrait_mode is True
            
            # Create image and verify dimensions
            image = generator.create_clock_image()
            assert image.size == (1072, 1448)  # Portrait dimensions

def test_timezone_handling():
    """Test if timezone is handled correctly"""
    test_timezone = "UTC"
    with patch('clock_generator.config', {
        'clock': {
            'timezone': 'Asia/Tokyo',  # Set a different timezone in config to ensure override works
            'width': 1448,
            'height': 1072,
            'font_size': 200,
            'date_font_size': 100,
            'weather_font_size': 120,
            'font_path': '/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc',
            'display_weather': False,
        }
    }):
        with patch('os.makedirs'):  # Mock directory creation
            generator = ClockGenerator(timezone=test_timezone)
            assert str(generator.timezone) == test_timezone
            
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
                if os.path.exists(test_image_path):
                    os.remove(test_image_path)

@pytest.mark.parametrize("hour,expected", [
    (12, False),  # Daytime (light mode)
    (20, True),   # Nighttime (dark mode)
    (5, True),    # Early morning (dark mode)
    (18, True),   # 6 PM (dark mode starts)
    (6, False),   # 6 AM (dark mode ends)
])
def test_dark_mode_detection(mock_config, hour, expected):
    """Test the dark mode time-based detection"""
    with patch('clock_generator.config', mock_config):
        with patch('os.makedirs'):  # Mock directory creation
            generator = ClockGenerator()
            assert generator._is_dark_mode(hour) == expected

@patch('clock_generator.requests.get')
def test_weather_integration(mock_get, mock_config):
    """Test weather integration when enabled"""
    # Enable weather
    mock_config['clock']['display_weather'] = True
    mock_config['clock']['weather_api_key'] = 'test_key'
    
    # Mock weather API response
    mock_weather_response = MagicMock()
    mock_weather_response.status_code = 200
    mock_weather_response.json.return_value = {
        "weather": [{"description": "clear sky", "icon": "01d"}],
        "main": {"temp": 22.5}
    }
    
    # Set up mock for different responses
    mock_get.return_value = mock_weather_response
    
    # Create a real PIL Image for testing
    test_image = Image.new('RGBA', (100, 100), (255, 255, 255, 255))
    
    with patch('clock_generator.config', mock_config):
        with patch('os.makedirs'):  # Mock directory creation
            with patch.object(Path, 'exists', return_value=True):  # Mock icon file existence
                with patch('PIL.Image.open', return_value=test_image):
                    # Use real Image objects for the weather icon test
                    with patch.object(WeatherIconGenerator, 'get_icon', return_value=test_image):
                        generator = ClockGenerator()
                        image = generator.create_clock_image()
                        
                        # Verify API was called
                        mock_get.assert_called_once()
                        assert isinstance(image, Image.Image)

@patch('clock_generator.requests.get')
def test_weather_integration_portrait_mode(mock_get):
    """Test weather integration in portrait mode"""
    portrait_config = {
        'clock': {
            'timezone': 'UTC',
            'width': 1072,  # Swapped dimensions
            'height': 1448,
            'font_size': 200,
            'date_font_size': 100,
            'weather_font_size': 120,
            'font_path': '/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc',
            'display_weather': True,
            'weather_api_key': 'test_key',
            'weather_city': 'Tokyo',
            'weather_units': 'metric',
            'portrait_mode': True  # Enable portrait mode
        }
    }
    
    # Mock weather API response
    mock_weather_response = MagicMock()
    mock_weather_response.status_code = 200
    mock_weather_response.json.return_value = {
        "weather": [{"description": "clear sky", "icon": "01d"}],
        "main": {"temp": 22.5}
    }
    
    # Set up mock for response
    mock_get.return_value = mock_weather_response
    
    # Create a real PIL Image for testing
    test_image = Image.new('RGBA', (100, 100), (255, 255, 255, 255))
    
    with patch('clock_generator.config', portrait_config):
        with patch('os.makedirs'):
            with patch.object(Path, 'exists', return_value=True):
                with patch('PIL.Image.open', return_value=test_image):
                    with patch.object(WeatherIconGenerator, 'get_icon', return_value=test_image):
                        generator = ClockGenerator()
                        # Verify portrait mode is enabled
                        assert generator.portrait_mode is True
                        
                        # Verify weather display is enabled
                        assert generator.display_weather is True
                        
                        # Generate image (this should create a correctly sized image regardless of our mock images)
                        image = generator.create_clock_image()
                        
                        # Verify the image has the correct dimensions directly
                        assert image.size == (1072, 1448)
                        
                        # Verify API was called
                        mock_get.assert_called_once()

@patch('cairosvg.svg2png')
def test_generate_weather_icons(mock_svg2png):
    """Test weather icon generation with the new SVG-based implementation"""
    # Mock the SVG to PNG conversion
    mock_svg2png.return_value = b'test_png_data'
    
    # Create a real PIL Image for testing
    img = Image.new('RGBA', (100, 100), (0, 0, 0, 255))
    
    # Mock file operations
    with patch('builtins.open', mock_open(read_data='<svg><path d="M10,10"/></svg>')):
        with patch('PIL.Image.open', return_value=img):
            # Test both light and dark modes
            generator = WeatherIconGenerator(icon_size=(100, 100))
            
            # Test light mode icon
            light_icon = generator.get_icon('01d', is_dark=False)
            assert light_icon is not None
            
            # Test dark mode icon
            dark_icon = generator.get_icon('01d', is_dark=True)
            assert dark_icon is not None
            
            # Verify svg2png was called
            assert mock_svg2png.call_count == 2

def test_get_weather_icon_with_local_icons(mock_config):
    """Test retrieving local weather icons with SVG files"""
    # Enable weather
    mock_config['clock']['display_weather'] = True
    mock_config['clock']['weather_api_key'] = 'test_key'
    
    # Create a real PIL Image for testing
    img = Image.new('RGBA', (100, 100), (0, 0, 0, 255))
    
    with patch('clock_generator.config', mock_config):
        with patch.object(Path, 'exists', return_value=True):
            # Mock SVG file reading
            with patch('builtins.open', mock_open(read_data='<svg><path d="M10,10"/></svg>')):
                # Mock SVG to PNG conversion
                with patch('cairosvg.svg2png', return_value=b'test_png_data'):
                    # Mock image processing with real Image object
                    with patch('PIL.Image.open', return_value=img):
                        generator = ClockGenerator()
                        icon = generator._get_weather_icon("01d")
                        
                        # Verify the icon was retrieved
                        assert icon is not None

# Function to clean up test output files after tests
def cleanup_test_files():
    """Clean up any test image files created during testing"""
    test_files = ["test_clock.png", "test_output.png", "test_portrait.png", "test_portrait_weather.png"]
    for file in test_files:
        if os.path.exists(file):
            os.remove(file)

# Run cleanup after tests
@pytest.fixture(scope="session", autouse=True)
def cleanup_after_tests():
    yield
    cleanup_test_files()