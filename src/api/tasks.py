from fastapi import APIRouter, HTTPException, Query
from typing import List

from db.repository import Repository
from db.connection import Session
from api.schemas import TaskBase, TaskResponse, TaskCreate
from utils.rbmq_connect import send_message
from config import AMQP

tasks_router = APIRouter()
db = Repository(Session)


@tasks_router.get(
    "/",
    response_model=List[TaskResponse],
    summary="Get All Tasks",
    description="Retrieve a list of all tasks from the database.",
)
async def get_tasks(sort_order: str = Query("desc", enum=["asc", "desc"])):
    tasks = db.get_tasks(order_by=sort_order)
    if not tasks:
        raise HTTPException(status_code=404, detail="No tasks found")
    return tasks

@tasks_router.get(
    "/{id}",
    response_model=TaskResponse,
    summary="Get a Task by ID",
    description="Retrieve details of a specific task by its ID.",
)
async def get_task(id: int):
    task = db.get_task(id=id)
    if not task:
        raise HTTPException(status_code=404, detail=f"Task with ID {id} not found")
    return task

@tasks_router.post(
    "/",
    response_model=TaskCreate,
    summary="Create a New Task",
    description="Create a new task and send it to the scheduler via RabbitMQ.",
)
async def create_task(item: TaskBase):
    # Prepare the task with default params
    new_task = item.model_dump()
    new_task.update({"params": "new_task"})

    # Send message to the scheduler
    try:
        await send_message(new_task, AMQP["work_queue"], durable=True)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to send task: {e}")

    return new_task