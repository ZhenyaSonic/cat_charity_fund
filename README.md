# Приложение QRKot
### Приложение для Благотворительного фонда поддержки котиков QRKot. Фонд собирает пожертвования на различные целевые проекты: на медицинское обслуживание нуждающихся хвостатых, на обустройство кошачьей колонии в подвале, на корм оставшимся без попечения кошкам — на любые цели, связанные с поддержкой кошачьей популяции.

## Используемые технологии
* Python 3.9
* FastAPI
* SQLAlchemy
* Pydantic
* Alembic
* Uvicorn

## Запуск проекта
Клонировать проект с GitHub

```git clone git@github.com:ZhenyaSonic/cat_charity_fund.git ```

Создание виртуального окружения

```python -m venv venv ```

Активация виртуального окружения

```source venv/Scripts/activate ```

После активации обновляем pip

``` python -m pip install --upgrade pip ```
Установка пакетов по файлу

```pip install -r requirements.txt ```

## Использование и запуск проекта
Создание в корне проект файла .env со следующим содержанием
* ```APP_TITLE=Благотворительного фонда поддержки котиков QRKot```
* ```DATABASE_URL=sqlite+aiosqlite:///./fastapi.db```
* ```SECRET='YOUR_SECRET_KEY'```
* ```FIRST_SUPERUSER_EMAIL='Ваш e-mail суперпользователя'```
* ```FIRST_SUPERUSER_PASSWORD='Ваш пароль суперпользователя' ```

Создание файла миграции

``` alembic revision```

Применение миграций

```alembic upgrade ```

Запуск проекта

```uvicorn app.main:app --reload ```

Автор
Евгений https://github.com/ZhenyaSonic