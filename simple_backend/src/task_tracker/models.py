from pydantic import BaseModel


class TaskAdd(BaseModel):
    name: str
    status: str
    answer_ai: str = "Рекомендации появятся после создания задачи"


class Task(TaskAdd):
    id: int
