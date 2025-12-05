import pytest
from fastapi.testclient import TestClient
import sys
import os
from PIL import Image
import io
from unittest.mock import patch

# Add src directory to path for imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from api import app, Orientation

# Create a fixture for the test client
@pytest.fixture
def client():
    """
    Test client fixture for the FastAPI application
    """
    return TestClient(app)

def test_get_clock_image(client):
    """
    Test if the clock image endpoint returns a valid PNG image
    """
    response = client.get("/clock.png")
    assert response.status_code == 200
    assert response.headers["content-type"] == "image/png"
    
    # Test if the response content is a valid PNG image
    image = Image.open(io.BytesIO(response.content))
    assert image.format == "PNG"
    assert image.mode == "L"  # Grayscale mode
    assert image.size == (1448, 1072)  # Expected dimensions
    
    # Save image for debugging if needed
    test_output_path = "test_output.png"
    with open(test_output_path, "wb") as f:
        f.write(response.content)
    
    # Clean up test file after validation
    if os.path.exists(test_output_path):
        os.remove(test_output_path)

def test_get_clock_image_with_landscape_orientation(client):
    """
    Test if the clock image endpoint returns a valid landscape PNG image
    when landscape orientation is explicitly requested
    """
    response = client.get("/clock.png?orientation=landscape")
    assert response.status_code == 200
    assert response.headers["content-type"] == "image/png"
    
    # Test if the response content is a valid PNG image
    image = Image.open(io.BytesIO(response.content))
    assert image.format == "PNG"
    assert image.mode == "L"  # Grayscale mode
    assert image.size == (1448, 1072)  # Expected landscape dimensions
    
    # Clean up any test files
    test_output_path = "test_landscape.png"
    with open(test_output_path, "wb") as f:
        f.write(response.content)
    
    # Clean up test file after validation
    if os.path.exists(test_output_path):
        os.remove(test_output_path)

def test_get_clock_image_with_portrait_orientation(client):
    """
    Test if the clock image endpoint returns a valid portrait PNG image
    when portrait orientation is requested
    """
    response = client.get("/clock.png?orientation=portrait")
    assert response.status_code == 200
    assert response.headers["content-type"] == "image/png"
    
    # Test if the response content is a valid PNG image
    image = Image.open(io.BytesIO(response.content))
    assert image.format == "PNG"
    assert image.mode == "L"  # Grayscale mode
    assert image.size == (1072, 1448)  # Expected portrait dimensions (swapped)
    
    # Clean up any test files
    test_output_path = "test_portrait.png"
    with open(test_output_path, "wb") as f:
        f.write(response.content)
    
    # Clean up test file after validation
    if os.path.exists(test_output_path):
        os.remove(test_output_path)

def test_invalid_orientation_parameter(client):
    """
    Test handling of invalid orientation parameter
    """
    response = client.get("/clock.png?orientation=invalid")
    assert response.status_code == 422  # Unprocessable Entity for invalid enum value
    
    # The response should contain validation error information
    assert "validation error" in response.text.lower()

def test_error_handling(client):
    """
    Test API error handling for non-existent endpoints
    """
    response = client.get("/nonexistent")
    assert response.status_code == 404

def test_health_check(client):
    """
    Test the health check endpoint
    """
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}