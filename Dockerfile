FROM python:3.10-slim-buster
WORKDIR /app
COPY requirements.txt .
# COPY .env .
RUN pip install --no-cache-dir -r requirements.txt
COPY src/alembic.ini /app/alembic.ini
COPY src/alembic/ /app/alembic
COPY ./src /app
EXPOSE 8000