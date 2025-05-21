# Сервис анализа транзакций

Микросервис для учета и анализа финансовых транзакций с возможностью:
- Импорта транзакций из JSON
- Автоматической категоризации расходов
- Проверки лимитов трат
- Получения статистики через API

## Требования

- Python 
- Django


## Установка

1. Клонируйте репозиторий:

git clone https://github.com/Rufatello/transaction.git

2. Создайте и активируйте виртуальное окружение:

python -m venv venv
source venv/bin/activate  # Linux/MacOS
venv\Scripts\activate     # Windows

3. Установите зависимости:

pip install -r requirements.txt

4. Настройте базу данных в settings.py
 
  DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': '',
         ...
    }
}
## Настройка 
1. Примените миграции:
   
python manage.py migrate

2. Создайте суперпользователя

python manage.py csu

## Запуск 
1. Запустите сервер разработки

python manage.py runserver

2. Импорт транзакций
python manage.py import_json
Пример ответа с валидацией:
![image](https://github.com/user-attachments/assets/8228a62b-f776-4dbf-9fb5-b4e1a9cf8fc7)

3. Получение статистики
Пример запроса: http://localhost:8000/transaction/users/7/stats/?from_date=2024-11-27&to_date=2024-11-29
Пример ответа:
![image](https://github.com/user-attachments/assets/7c6d5037-696f-47e9-a32f-498260a14dbc)



   
