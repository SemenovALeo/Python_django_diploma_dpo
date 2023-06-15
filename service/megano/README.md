# MEGANO SHOP

<h3 align="center">Интернет магазин по продаже техники
</h3>
Проект разработан на фреймворке Django. За отображение страниц отвечает приложение frontend, 

а обращение за данными происходит по API, который реализован с использованием Django Rest Framework.

## Установка и запуск проекта через Docker контейнер
1. Клонировать репозиторий
2. Создание бд и загрузка фикстур:
    * `docker-compose run --rm web-app sh -c "python3 manage.py make migrations"` - создание миграций
    * `docker-compose run --rm web-app sh -c "python3 manage.py migrate"` - миграция 
    * `docker-compose run --rm web-app sh -c "python3 manage.py loaddata ./fixtures/* "` - установка фикстур
5. `docker-compose run --rm web-app sh -c "python3 manage.py runserver"` - запуск сервера

## Установка и запуск проекта без Docker
1. Клонировать репозиторий megano, создать и войти в виртуальное окружение
2. `pip install -r requirements.txt` - установка зависимостей
3. Установка frontend:
    * `cd diploma-frontend && python setup.py sdist` - создание архива с библиотекой фронтенда
    * `pip install ./dist/diploma-frontend-0.6.tar.gz` - установка фронтенда
4. Создание бд и загрузка фикстур:
    * `cd ../megano && python manage.py make migrations` - создание миграций
    * `python manage.py migrate` - миграция 
    * `python manage.py loaddata ./fixtures/* ` - установка фикстур
5. `python manage.py runserver` - запуск сервера
