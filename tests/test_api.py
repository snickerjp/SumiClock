import pytest
from fastapi.testclient import TestClient
import sys
import os
from PIL import Image
import io

# Add src directory to path for imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from api import app

client = TestClient(app)

def test_get_clock_image():
    """Test if the clock image endpoint returns a valid PNG image"""
    response = client.get("/clock.png")
    assert response.status_code == 200
    assert response.headers["content-type"] == "image/png"
    
    # Test if the response content is a valid PNG image
    image = Image.open(io.BytesIO(response.content))
    assert image.format == "PNG"
    assert image.mode == "L"  # Grayscale mode
    assert image.size == (1448, 1072)  # Expected dimensions

def test_error_handling():
    """Test API error handling"""
    response = client.get("/nonexistent")
    assert response.status_code == 404