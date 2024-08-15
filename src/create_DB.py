import os
from typing import Dict, Any

import psycopg2
from dotenv import load_dotenv

load_dotenv()


def connect_to_db():
    """Функция для подключения к базе данных."""
    conn = psycopg2.connect(
        dbname=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT"),
    )
    return conn


def create_tables(conn):
    """Функция для создания таблиц в базе данных."""
    cur = conn.cursor()
    cur.execute(
        """
    CREATE TABLE IF NOT EXISTS employers (
        id SERIAL PRIMARY KEY,
        employer_id INT UNIQUE,
        name VARCHAR(255),
        url VARCHAR(255),
        description TEXT,
        open_vacancies INTEGER
    )
    """
    )

    cur.execute(
        """
    CREATE TABLE IF NOT EXISTS vacancies (
        id SERIAL PRIMARY KEY,
        vacancy_id INTEGER UNIQUE,
        employer_id INTEGER REFERENCES employers(employer_id),
        name VARCHAR(255),
        city VARCHAR(255),
        salary_from INTEGER,
        salary_to INTEGER,
        currency VARCHAR(10),
        published_at TIMESTAMP,
        description TEXT,
        url VARCHAR(255)
    )
    """
    )

    conn.commit()
    cur.close()


def insert_employer(cursor, employer: dict) -> None:
    """Вставка данных работодателя в базу данных."""
    cursor.execute(
        """
        INSERT INTO employers (employer_id, name, url, description, open_vacancies)
        VALUES (%s, %s, %s, %s, %s)
        ON CONFLICT (employer_id) DO NOTHING
    """,
        (
            employer["id"],
            employer["name"],
            employer["alternate_url"],
            employer["description"],
            employer["open_vacancies"],
        ),
    )


def insert_vacancy(cursor, vacancy: Dict[str, Any], employer_id: int) -> None:
    """Вставка данных вакансии в базу данных."""
    salary = vacancy.get("salary") or {}
    cursor.execute(
        """
        INSERT INTO vacancies (vacancy_id, employer_id, name, city, salary_from,
         salary_to, currency, published_at, description, url)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        ON CONFLICT (vacancy_id) DO NOTHING
    """,
        (
            vacancy["id"],
            employer_id,
            vacancy["name"],
            vacancy["area"]["name"],
            salary.get("from"),
            salary.get("to"),
            salary.get("currency"),
            vacancy["published_at"],
            vacancy.get("snippet", {}).get("responsibility", ""),
            vacancy["alternate_url"],
        ),
    )
