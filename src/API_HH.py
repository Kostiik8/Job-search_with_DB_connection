from typing import Any

import requests


class GetInfoHHCompany:
    """Класс для работы с API HeadHunter."""

    def __init__(self):
        self.base_url: str = "https://api.hh.ru"
        self.headers: dict[str, str] = {"User-Agent": "HH-User-Agent"}

    def get_employer_info(self, employer_id: int) -> Any:
        """Получить информацию о работодателе по ID."""
        response = requests.get(f"{self.base_url}/employers/{employer_id}", headers=self.headers)
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Ошибка {response.status_code}: {response.text}")
            return None

    def get_vacancies_by_employer(self, employer_id: int, max_vacancies: int = 100):
        """Получить все вакансии работодателя по ID."""
        vacancies: list[dict] = []
        page: int = 0
        per_page: int = min(max_vacancies, 100)

        while len(vacancies) < max_vacancies:
            params: dict[str, int] = {"employer_id": employer_id, "page": page, "per_page": per_page}
            response = requests.get(f"{self.base_url}/vacancies", headers=self.headers, params=params)
            if response.status_code != 200:
                print(f"Ошибка {response.status_code}: {response.text}")
                break

            data: dict = response.json()
            vacancies.extend(data.get("items", []))

            if data.get("pages") and page >= data["pages"] - 1:
                break
            page += 1

        return vacancies
