from typing import Any

from src.create_DB import connect_to_db


class DBManager:
    def __init__(self):
        """Инициализация подключения к базе данных."""
        self.conn = connect_to_db()
        self.cursor = self.conn.cursor()

    def get_companies_and_vacancies_count(self) -> Any:
        """Получает список всех компаний и количество вакансий у каждой компании."""
        query = """
        SELECT e.name AS company_name, COUNT(v.id) AS vacancies_count
        FROM employers e
        LEFT JOIN vacancies v ON e.employer_id = v.employer_id
        GROUP BY e.name
        ORDER BY vacancies_count DESC;
        """
        self.cursor.execute(query)
        results = self.cursor.fetchall()
        return results

    def get_all_vacancies(self) -> Any:
        """Получает список всех вакансий с указанием названия компании, вакансии и зарплаты и ссылки на вакансию."""
        query = """
        SELECT e.name AS company_name, v.name AS vacancy_name, v.salary_from, v.salary_to, v.url
        FROM vacancies v
        JOIN employers e ON v.employer_id = e.employer_id
        ORDER BY v.published_at DESC;
        """
        self.cursor.execute(query)
        results = self.cursor.fetchall()
        return results

    def get_avg_salary(self) -> Any:
        """Получает среднюю зарплату по вакансиям."""
        query = """
        SELECT AVG((salary_from + salary_to) / 2.0) AS avg_salary
        FROM vacancies
        WHERE salary_from IS NOT NULL AND salary_to IS NOT NULL;
        """
        self.cursor.execute(query)
        avg_salary = self.cursor.fetchone()[0]
        return avg_salary

    def get_vacancies_with_higher_salary(self) -> Any:
        """Получает список всех вакансий, у которых зарплата выше средней по всем вакансиям."""
        avg_salary = self.get_avg_salary()
        query = """
        SELECT e.name AS company_name, v.name AS vacancy_name, v.salary_from, v.salary_to, v.url
        FROM vacancies v
        JOIN employers e ON v.employer_id = e.employer_id
        WHERE (salary_from + salary_to) / 2.0 > %s
        ORDER BY (salary_from + salary_to) / 2.0 DESC;
        """
        self.cursor.execute(query, (avg_salary,))
        results = self.cursor.fetchall()
        return results

    def get_vacancies_with_keyword(self, keyword: str) -> Any:
        """Получает список всех вакансий, в названии которых содержатся переданные в метод слова."""
        query = """
        SELECT e.name AS company_name, v.name AS vacancy_name, v.salary_from, v.salary_to, v.url
        FROM vacancies v
        JOIN employers e ON v.employer_id = e.employer_id
        WHERE v.name ILIKE %s
        ORDER BY v.published_at DESC;
        """
        self.cursor.execute(query, (f"%{keyword}%",))
        results = self.cursor.fetchall()
        return results

    def close_connection(self) -> None:
        """Закрытие соединения с базой данных."""
        self.cursor.close()
        self.conn.close()
