import pytest
from fastapi.testclient import TestClient
from src.api import app
from PIL import Image
import io

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