# API Организационной Структуры

Это реализация тестового задания для API организационной структуры с использованием FastAPI, PostgreSQL и SQLAlchemy.

## Особенности

- **Подразделения (Departments)**: Создание, обновление, удаление (cascade/reassign) и получение данных с вложенной структурой дерева (глубина до 5).
- **Сотрудники (Employees)**: Создание сотрудников внутри подразделений.
- **Логика дерева**: Предотвращение циклических зависимостей и обеспечение уникальности названий подразделений внутри одного родительского подразделения.
- **Архитектура**: Соблюдение принципов SOLID, DRY и ООП с использованием сервисного слоя (Service Layer) и внедрения зависимостей (Dependency Injection).
- **Async**: Полностью асинхронные операции с базой данных с использованием `asyncpg` и расширения SQLAlchemy для async.

## Технологический стек

- **FastAPI**: Веб-фреймворк.
- **PostgreSQL**: База данных.
- **SQLAlchemy**: ORM.
- **Alembic**: Миграции базы данных.
- **Docker & Docker Compose**: Контейнеризация.
- **Pytest**: Тестирование.

## Начало работы

### Предварительные условия

- Установленные Docker и Docker Compose.

### Установка и настройка

1. **Клонируйте репозиторий**:
   ```bash
   git clone <repository_url>
   cd hitalent
   ```

2. **Запустите сервисы**:
   ```bash
   docker-compose up --build
   ```

3. **Инициализируйте базу данных**:
   Начальная миграция уже включена в папку `alembic/versions/`. Чтобы применить ее, выполните:
   ```bash
   docker-compose exec api alembic upgrade head
   ```
   (Если вы внесете изменения в модели, вы можете сгенерировать новые миграции с помощью `alembic revision --autogenerate`)

### Документация API

После запуска приложения интерактивная документация OpenAPI доступна по адресам:
- Swagger UI: [http://localhost:8000/docs](http://localhost:8000/docs)
- Redoc: [http://localhost:8000/redoc](http://localhost:8000/redoc)

### Запуск тестов

Перед первым запуском тестов создайте тестовую базу данных:
```bash
docker-compose exec db psql -U postgres -c "CREATE DATABASE hitalent_test;"
```

Затем запустите автоматические тесты:
```bash
docker-compose exec api pytest
```

## Структура проекта

```
hitalent/
├── app/
│   ├── main.py            # Точка входа
│   ├── api/               # Роутеры API
│   ├── core/              # Конфигурация и настройка БД
│   ├── models.py          # Модели SQLAlchemy
│   ├── schemas.py         # Схемы Pydantic
│   ├── dependencies.py    # Внедрение зависимостей
│   └── services/          # Бизнес-логика (Сервисы)
├── alembic/               # Миграции базы данных
├── tests/                 # Тесты Pytest
├── Dockerfile
├── docker-compose.yml
├── pytest.ini             # Конфигурация Pytest
└── requirements.txt
```
equirements.txt
```
