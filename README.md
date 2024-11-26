# Task Management API

This project is a simple Task Management API built with **FastAPI** and **SQLAlchemy**, using **Alembic** for database migrations. It provides three main endpoints for managing tasks. The application is containerized using **Docker Compose** for easy setup and deployment.

## Features

- **Endpoints**:
  - `POST /tasks`: Create a new task.
  - `GET /tasks`: Retrieve all tasks.
  - `GET /tasks/{id}`: Retrieve a specific task by ID.
- **Database Management**:
  - Uses **SQLAlchemy** ORM.
  - Handles schema migrations with **Alembic**.

---

## Prerequisites

Ensure you have the following installed on your system:
- **Docker** (https://www.docker.com/)
- **Docker Compose** (bundled with Docker Desktop)
- **Python 3.9+** (only required for development, not for running with Docker)

---

## Quick Start with Docker Compose

1. Clone the repository:
   ```bash
   git clone <repository_url>
   cd <repository_folder>
   ```
3. Define variables
    Set params in config.py_template, alembic.ini(db::63), docker-compose.yaml(db::58-60)
    ```bash
    cp src/config.py_template src/config.py
    ```
2. Start the services with Docker Compose:
   ```bash
   docker-compose up --build -d
   ```
3. Init alembic
   ```bash
   cd src
   docker exec -it task_master_app alembic revision --autogenerate -m "Name_of_migration"
   docker exec -it task_master_app alembic upgrade head
   ```
   on first start:
   ```bash
   docker compose restart task_scheduler task_worker
   ```


## Example API usage

### SwaggerAPI on 127.0.0.1:8000/docs