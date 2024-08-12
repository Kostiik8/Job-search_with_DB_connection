import time
from typing import List, Dict, Any

import requests


class GetInfoHHCompany:
    """Класс для работы с API HeadHunter."""

    def __init__(self) -> None:
        self.base_url: str = "https://api.hh.ru"
        self.headers: Dict[str, str] = {"User-Agent": "HH-User-Agent"}

    def get_employer_info(self, employer_id: int):
        """Получить информацию о работодателе по ID."""
        response = requests.get(f"{self.base_url}/employers/{employer_id}", headers=self.headers)
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Ошибка {response.status_code}: {response.text}")
            return None

    def get_vacancies_by_employer(self, employer_id: int, max_vacancies: int = 100) -> List[Dict[str, Any]]:
        """Получить все вакансии работодателя по ID."""
        vacancies: List[Dict[str, Any]] = []
        page: int = 0
        per_page: int = min(max_vacancies, 100)

        while len(vacancies) < max_vacancies:
            params = {"employer_id": employer_id, "page": page, "per_page": per_page}
            response = requests.get(f"{self.base_url}/vacancies", headers=self.headers, params=params)
            if response.status_code != 200:
                print(f"Ошибка {response.status_code}: {response.text}")
                break

            data = response.json()
            vacancies.extend(data.get("items", []))

            if data.get("pages") and page >= data["pages"] - 1:
                break
            page += 1

        return vacancies


employer_ids = [1455, 3529, 2120, 4181, 2180, 80, 1740, 78638, 2537115, 3127]

hh_api = GetInfoHHCompany()

for employer_id in employer_ids:
    time.sleep(1)
    employer_info = hh_api.get_employer_info(employer_id)
    if employer_info:
        print(f"Работодатель: {employer_info['name']}")
        vacancies = hh_api.get_vacancies_by_employer(employer_id)
        print(f"Количество вакансий: {len(vacancies)}")
        for vacancy in vacancies:
            print(f" - {vacancy['name']} (город: {vacancy['area']['name']})")
        print("\n" + "=" * 40 + "\n")
