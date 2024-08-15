from src.db_operations import DBManager


def display_data():
    """Получает данные из базы и выводит их пользователю."""
    db_manager = DBManager()

    # Получение и вывод информации о компаниях и вакансиях
    print("Количество компаний и вакансий:")
    companies_and_vacancies = db_manager.get_companies_and_vacancies_count()
    for company, count in companies_and_vacancies:
        print(f"Компания: {company}, Вакансий: {count}")

    print("\nВсе вакансии:")
    all_vacancies = db_manager.get_all_vacancies()
    for vacancy in all_vacancies:
        print(
            f"Компания: {vacancy[0]}, Вакансия: {vacancy[1]},"
            f" Зарплата: {vacancy[2]}-{vacancy[3]}, Ссылка: {vacancy[4]}"
        )

    avg_salary = db_manager.get_avg_salary()
    print(f"\nСредняя зарплата по вакансиям: {avg_salary:.2f}")

    print("\nВакансии с зарплатой выше средней:")
    high_salary_vacancies = db_manager.get_vacancies_with_higher_salary()
    for vacancy in high_salary_vacancies:
        print(
            f"Компания: {vacancy[0]}, Вакансия: {vacancy[1]},"
            f" Зарплата: {vacancy[2]}-{vacancy[3]}, Ссылка: {vacancy[4]}"
        )

    keyword = "python"
    print(f"\nВакансии по ключевому слову '{keyword}':")
    keyword_vacancies = db_manager.get_vacancies_with_keyword(keyword)
    for vacancy in keyword_vacancies:
        print(
            f"Компания: {vacancy[0]}, Вакансия: {vacancy[1]},"
            f" Зарплата: {vacancy[2]}-{vacancy[3]}, Ссылка: {vacancy[4]}"
        )

    db_manager.close_connection()
