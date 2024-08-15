# Курсовая работа
## Описание:
Приложение для получения данных работодателя и их вакансий на HH.ru. Оно позволяет получать 10 интересующих
вакансий и выводить: Компанию, колличество вакансий, зарплату, сссылку на вакансию и краткое описание и  
выводит список всех вакансий, в названии которых содержатся переданные в метод слова.
Так же создает в базе данных таблицы с вакансиями и работодателем содержащие: id, имя, ссылку,
описание. 
## Установка:
1. Клонируйте репозиторий:
```
git@github.com:Kostiik8/Job-search_with_DB_connection.git
```
2. Установите зависимости:
```
pip install poetry
poetry install
poetry add requests
pip install pytest
pip install  pytest-cov
poetry add python-dotenv 
poetry add --group lint mypy
poetry add --group lint black
poetry add --group lint isort
poetry add --group lint flake8 
poetry add requests-mock

```
## Тестирование
С помощью линтеров mypy, black, flake8, isort можете проверить код на соответствие PEP8
Пример команды:
```
flake8 module_name
flake8 . (все модули)
```

## Test Coverage
При необходимости можете проверить с помощью команд:
```
poetry add --group dev pytest
pytest --cov 
pytest  
```

## Модули
```
API_HH.py - Получает данные с HH.ru через API
create_DB.py - Создает таблицы в БД и наполняет их данными полученными с API_HH
db_operations.py - Взаимодействия с БД: Получение списка всех компаний, среднюю зарплату
и поиск по ключевому слову
user_interface.py - Выводит пользователю всю информацию в человекочитаемом формате, понятным текстом
main.py - вызов всей программы 
```
