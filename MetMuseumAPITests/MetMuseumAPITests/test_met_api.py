
import pytest
import requests
import logging
from datetime import datetime
from typing import Dict, List
from models import Artwork, ArtworkList, Department
from pydantic import ValidationError

BASE_URL = "https://collectionapi.metmuseum.org/public/collection/v1"

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("met_api_tests.log", mode='w', encoding='utf-8'),
        logging.StreamHandler()
    ]
)

def log_response(response: requests.Response):
    """Логирование деталей запроса и ответа."""
    logging.info(f"Request: {response.request.method} {response.url}")
    if response.status_code != 200:
        logging.error(f"Error Response: {response.status_code} - {response.text[:200]}")
    else:
        logging.debug(f"Response Data: {response.json()}")

# Фикстуры
@pytest.fixture(scope="module")
def sample_artwork():
    return {
        "valid_id": 436535,  
        "invalid_id": 999999999,
        "artist": "Van Gogh",
        "department_id": 11  
    }

@pytest.fixture(scope="module")
def search_queries():
    return {
        "basic": {"q": "Van Gogh", "hasImages": True},
        "filtered": {
            "q": "monet", 
            "dateBegin": 1870,
            "dateEnd": 1880,
            "medium": "Oil on canvas",
            "departmentId": 11
        }
    }

# 1Тесты получения объектов
class TestGetObject:
    def test_valid_object(self, sample_artwork):
        """Проверка получения существующего объекта"""
        response = requests.get(f"{BASE_URL}/objects/{sample_artwork['valid_id']}")
        log_response(response)
        
        assert response.status_code == 200
        artwork = Artwork(**response.json())
        assert artwork.objectID == sample_artwork['valid_id']
        assert artwork.title
        assert isinstance(artwork.primaryImage, (str, type(None)))

    def test_invalid_object(self, sample_artwork):
        """Проверка обработки несуществующего ID"""
        response = requests.get(f"{BASE_URL}/objects/{sample_artwork['invalid_id']}")
        log_response(response)
        
        assert response.status_code == 404
        assert "message" in response.json()

    def test_response_time(self, sample_artwork):
        """Проверка времени ответа API"""
        start_time = datetime.now()
        response = requests.get(f"{BASE_URL}/objects/{sample_artwork['valid_id']}")
        end_time = datetime.now()
        
        assert response.status_code == 200
        assert (end_time - start_time).total_seconds() < 2.0
        log_response(response)

# 2 Тесты поиска
class TestSearch:
    def test_basic_search(self, search_queries):
        """Проверка базового поиска"""
        response = requests.get(f"{BASE_URL}/search", params=search_queries['basic'])
        log_response(response)
        
        assert response.status_code == 200
        results = ArtworkList(**response.json())
        assert results.total > 0
        assert len(results.objectIDs) > 0

    def test_filtered_search(self, search_queries):
        """Проверка поиска с фильтрами"""
        response = requests.get(f"{BASE_URL}/search", params=search_queries['filtered'])
        log_response(response)
        
        assert response.status_code == 200
        results = ArtworkList(**response.json())
        assert results.total >= 0  

    @pytest.mark.parametrize("limit", [1, 5, 10], ids=["limit=1", "limit=5", "limit=10"])
    def test_pagination(self, search_queries, limit):
        """Проверка пагинации"""
        params = {**search_queries['basic'], "limit": limit}
        response = requests.get(f"{BASE_URL}/search", params=params)
        log_response(response)
        
        data = response.json()
        assert len(data["objectIDs"]) <= limit

    def test_invalid_search_params(self):
        """Проверка невалидных параметров поиска"""
        params = {"q": "", "limit": -1}
        response = requests.get(f"{BASE_URL}/search", params=params)
        log_response(response)
        
        assert response.status_code in [400, 422]

# 3Тесты отделов музея
class TestDepartments:
    def test_get_all_departments(self):
        """Проверка получения списка отделов"""
        response = requests.get(f"{BASE_URL}/departments")
        log_response(response)
        
        assert response.status_code == 200
        departments = response.json()["departments"]
        assert len(departments) > 0
        
   
        department = Department(**departments[0])
        assert department.departmentId > 0
        assert department.displayName

    def test_objects_by_department(self, sample_artwork):
        """Проверка получения объектов по отделу"""
        params = {"departmentIds": sample_artwork['department_id']}
        response = requests.get(f"{BASE_URL}/search", params=params)
        log_response(response)
        
        assert response.status_code == 200
        results = ArtworkList(**response.json())
        assert results.total >= 0

# 4 Тесты валидации данных
class TestDataValidation:
    def test_artwork_validation(self, sample_artwork):
        """Проверка валидации структуры объекта"""
        response = requests.get(f"{BASE_URL}/objects/{sample_artwork['valid_id']}")
        
        
        try:
            artwork = Artwork(**response.json())
            assert artwork.objectID == sample_artwork['valid_id']
        except ValidationError as e:
            pytest.fail(f"Validation error: {e}")

    def test_empty_response_handling(self):
        """Проверка обработки пустого ответа"""
        with pytest.raises(ValidationError):
            Artwork(**{})

# 5 Дополнительные тесты
class TestAdditionalFeatures:
    def test_response_headers(self, sample_artwork):
        """Проверка заголовков ответа"""
        response = requests.get(f"{BASE_URL}/objects/{sample_artwork['valid_id']}")
        
        assert "Content-Type" in response.headers
        assert "application/json" in response.headers["Content-Type"]
        log_response(response)

    def test_rate_limiting(self):
        """Проверка ограничения запросов"""
        for _ in range(5): 
            response = requests.get(f"{BASE_URL}/objects/1")
            assert response.status_code in [200, 429]  
            if response.status_code == 429:
                logging.warning("Rate limit reached")
                break