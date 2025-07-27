from pydantic import BaseModel
class TaskAdd(BaseModel):
    name: str
    status: str


class Task(TaskAdd):
    id: int
