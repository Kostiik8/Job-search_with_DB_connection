import time

from src.API_HH import GetInfoHHCompany
from src.create_DB import connect_to_db, create_tables, insert_employer, insert_vacancy
from src.user_interface import display_data


def main():
    employer_ids = [1455, 3529, 2120, 4181, 2180, 80, 1740, 78638, 2537115, 3127]

    conn = connect_to_db()
    create_tables(conn)
    cursor = conn.cursor()

    hh_api = GetInfoHHCompany()

    for employer_id in employer_ids:
        time.sleep(1)
        employer_info = hh_api.get_employer_info(employer_id)
        if employer_info:
            insert_employer(cursor, employer_info)
            vacancies = hh_api.get_vacancies_by_employer(employer_id)
            for vacancy in vacancies:
                insert_vacancy(cursor, vacancy, employer_id)

    conn.commit()
    cursor.close()
    conn.close()

    display_data()


if __name__ == "__main__":
    main()
