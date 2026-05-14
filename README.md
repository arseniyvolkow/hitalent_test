# Organizational Structure API

This is a technical exercise implementation for an Organizational Structure API using FastAPI, PostgreSQL, and SQLAlchemy.

## Features

- **Departments**: Create, update, delete (cascade/reassign), and fetch with nested tree structure (up to depth 5).
- **Employees**: Create employees within departments.
- **Tree Logic**: Prevents cyclic dependencies and ensures unique names within the same parent department.
- **Architecture**: Follows SOLID, DRY, and OOP principles with Service-oriented architecture and Dependency Injection.
- **Async**: Fully asynchronous database operations using `asyncpg` and SQLAlchemy's async extension.
- **Logging**: Basic logging configuration for application monitoring.

## Tech Stack

- **FastAPI**: Web framework.
- **PostgreSQL**: Database.
- **SQLAlchemy**: ORM.
- **Alembic**: Database migrations.
- **Docker & Docker Compose**: Containerization.
- **Pytest**: Testing.

## Getting Started

### Prerequisites

- Docker and Docker Compose installed.

### Installation & Setup

1. **Clone the repository**:
   ```bash
   git clone <repository_url>
   cd hitalent
   ```

2. **Start the services**:
   ```bash
   docker-compose up --build
   ```

3. **Initialize Database**:
   The initial migration is already provided in `alembic/versions/`. To apply it, run:
   ```bash
   docker-compose exec api alembic upgrade head
   ```
   (If you make changes to models, you can generate new migrations using `alembic revision --autogenerate`)

### API Documentation

Once the app is running, you can access the interactive OpenAPI documentation at:
- Swagger UI: [http://localhost:8000/docs](http://localhost:8000/docs)
- Redoc: [http://localhost:8000/redoc](http://localhost:8000/redoc)

### Running Tests

Before running tests for the first time, create the test database:
```bash
docker-compose exec db psql -U postgres -c "CREATE DATABASE hitalent_test;"
```

Then, run the automated tests:
```bash
docker-compose exec api pytest
```

## Project Structure

```
hitalent/
├── app/
│   ├── main.py            # Entry point
│   ├── api/               # API routers and endpoints
│   ├── core/              # Configuration and DB setup
│   ├── models.py          # SQLAlchemy models
│   ├── schemas.py         # Pydantic schemas
│   ├── dependencies.py    # Dependency injection
│   └── services/          # Business logic (Services)
├── alembic/               # Database migrations
├── tests/                 # Pytest tests
├── Dockerfile
├── docker-compose.yml
├── pytest.ini             # Pytest configuration
└── requirements.txt
```
