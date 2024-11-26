from datetime import datetime as dt
from pydantic import BaseModel
from typing import Optional

class TaskBase(BaseModel):
    name: str
    description: Optional[str] = None

class TaskResponse(TaskBase):
    id: int
    status: str
    created_at: Optional[dt] = None
    updated_at: Optional[dt] = None

class TaskCreate(TaskBase):
    pass
