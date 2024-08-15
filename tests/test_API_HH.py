import pytest
import requests_mock

from src.API_HH import GetInfoHHCompany


@pytest.fixture
def hh_api():
    return GetInfoHHCompany()


@pytest.fixture
def mock_requests():
    with requests_mock.Mocker() as m:
        yield m


def test_get_employer_info_success(hh_api, mock_requests):
    employer_id = 123456
    url = f"https://api.hh.ru/employers/{employer_id}"
    mock_response = {"id": employer_id, "name": "Test Employer", "description": "This is a test employer."}

    mock_requests.get(url, json=mock_response, status_code=200)

    response = hh_api.get_employer_info(employer_id)
    assert response == mock_response


def test_get_employer_info_failure(hh_api, mock_requests):
    employer_id = 123456
    url = f"https://api.hh.ru/employers/{employer_id}"

    mock_requests.get(url, status_code=404, text="Not Found")

    response = hh_api.get_employer_info(employer_id)
    assert response is None


def test_get_vacancies_by_employer_success(hh_api, mock_requests):
    employer_id = 123456
    url = "https://api.hh.ru/vacancies"
    mock_response = {
        "items": [
            {"id": "1", "name": "Vacancy 1"},
            {"id": "2", "name": "Vacancy 2"},
        ],
        "pages": 1,
    }

    mock_requests.get(url, json=mock_response, status_code=200)

    vacancies = hh_api.get_vacancies_by_employer(employer_id, max_vacancies=10)
    assert len(vacancies) == 2
    assert vacancies == mock_response["items"]


def test_get_vacancies_by_employer_failure(hh_api, mock_requests):
    employer_id = 123456
    url = "https://api.hh.ru/vacancies"

    mock_requests.get(url, status_code=500, text="Internal Server Error")

    vacancies = hh_api.get_vacancies_by_employer(employer_id, max_vacancies=10)
    assert len(vacancies) == 0
