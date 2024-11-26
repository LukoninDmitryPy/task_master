from fastapi import FastAPI
from api.tasks import tasks_router

app = FastAPI(
    title="Task Management API",
    description="An API for managing tasks and communicating with a scheduler",
    version="1.0.0",
)

# Подключение маршрутов
app.include_router(tasks_router, prefix="/tasks", tags=["Tasks"])

# Вы можете добавить дополнительные роутеры в будущем
