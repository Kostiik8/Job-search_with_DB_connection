from datetime import datetime

import pytest
from dotenv import load_dotenv

from src.create_DB import connect_to_db, create_tables, insert_employer, insert_vacancy

load_dotenv()


@pytest.fixture(scope="module")
def db_connection():
    """Подключение к бд."""
    conn = connect_to_db()
    yield conn
    conn.close()


def test_create_tables(db_connection):
    """Проверка на создание таблиц."""
    create_tables(db_connection)
    cur = db_connection.cursor()
    cur.execute("SELECT table_name FROM information_schema.tables WHERE table_schema = 'public'")
    tables = cur.fetchall()
    cur.close()

    table_names = {table[0] for table in tables}
    assert "employers" in table_names
    assert "vacancies" in table_names


def test_insert_employer(db_connection):
    """Вставка в таблицу работодателя."""
    create_tables(db_connection)
    cur = db_connection.cursor()

    employer = {
        "id": 123,
        "name": "Test Employer",
        "alternate_url": "https://example.com",
        "description": "A test employer",
        "open_vacancies": 5,
    }

    insert_employer(cur, employer)
    db_connection.commit()

    cur.execute("SELECT * FROM employers WHERE employer_id = %s", (employer["id"],))
    result = cur.fetchone()
    cur.close()

    assert result is not None
    assert result[1] == employer["id"]
    assert result[2] == employer["name"]
    assert result[3] == employer["alternate_url"]
    assert result[4] == employer["description"]
    assert result[5] == employer["open_vacancies"]


def test_insert_vacancy(db_connection):
    """Вставка в таблицу вакансий."""
    create_tables(db_connection)
    cur = db_connection.cursor()

    employer: dict[str, int | str] = {
        "id": 123,
        "name": "Test Employer",
        "alternate_url": "https://example.com",
        "description": "A test employer",
        "open_vacancies": 5,
    }

    insert_employer(cur, employer)
    db_connection.commit()

    vacancy = {
        "id": 456,
        "name": "Test Vacancy",
        "area": {"name": "Test City"},
        "salary": {"from": 50000, "to": 70000, "currency": "USD"},
        "published_at": "2024-08-15T00:00:00",
        "snippet": {"responsibility": "Test responsibility"},
        "alternate_url": "https://example.com/vacancy",
    }

    published_at_dt = datetime.fromisoformat(str(vacancy["published_at"]))

    insert_vacancy(cur, vacancy, int(employer["id"]))
    db_connection.commit()

    cur.execute("SELECT * FROM vacancies WHERE vacancy_id = %s", (vacancy["id"],))
    result = cur.fetchone()
    assert result is not None
    cur.close()

    assert result[1] == vacancy["id"]
    assert result[2] == employer["id"]
    assert result[3] == vacancy["name"]
    assert result[8] == published_at_dt
    assert result[10] == vacancy["alternate_url"]
