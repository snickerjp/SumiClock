import pytest
from fastapi.testclient import TestClient
from src.api import app

client = TestClient(app)

def test_get_clock_image():
    """Test if the clock image endpoint returns correct response"""
    response = client.get("/clock.png")
    assert response.status_code == 200
    assert response.headers["content-type"] == "image/png"
    assert len(response.content) > 0  # Image should not be empty

def test_redis_caching():
    """Test if Redis caching works correctly"""
    # First request should generate new image
    response1 = client.get("/clock.png")
    image1 = response1.content
    
    # Second request within the same minute should return cached image
    response2 = client.get("/clock.png")
    image2 = response2.content
    
    assert response1.status_code == 200
    assert response2.status_code == 200
    assert image1 == image2  # Images should be identical due to caching