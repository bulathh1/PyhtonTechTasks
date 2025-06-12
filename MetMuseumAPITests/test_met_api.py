import pytest
import requests

BASE_URL = "https://collectionapi.metmuseum.org/public/collection/v1"

def test_get_artwork():
    response = requests.get(f"{BASE_URL}/objects/436535")
    assert response.status_code == 200