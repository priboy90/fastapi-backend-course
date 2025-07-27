from typing import Annotated

from fastapi import FastAPI, Depends
from pydantic import BaseModel

app = FastAPI()

class TaskAdd(BaseModel):
    name: str
    status: str

class Task(TaskAdd):
    id: int



# Инициализируем список задач в оперативной памяти
tasks = [
    Task(id=1, name="Task 1", status="Running"),
    Task(id=2, name="Task 2", status="Completed"),
    Task(id=3, name="Task 3", status="Failed"),
    Task(id=4, name="Task 4", status="Completed"),
    Task(id=5, name="Task 5", status="Completed"),
    Task(id=6, name="Task 6", status="Completed"),
    Task(id=7, name="Task 7", status="Completed")
]



@app.get("/tasks")
def get_tasks():
    return tasks


@app.post("/tasks", response_model=TaskAdd)
def create_task(task: Annotated[TaskAdd, Depends()], ):
    task_id = max(tasks, key=lambda x: x.id).id + 1
    new_task = Task(id=task_id, name=task.name, status=task.status)
    tasks.append(new_task)
    return task


@app.put("/tasks/{task_id}", response_model=TaskAdd)
def update_task(task_id: int, task: Annotated[TaskAdd, Depends()],):
    for t in tasks:
        if t.id == task_id:
            t.name = task.name
            t.status = task.status
            return t
    return {"error": "Task not found"}



@app.delete("/tasks/{task_id}")
def delete_task(task_id: int):
    global tasks
    tasks = [t for t in tasks if t.id != task_id]
    return {"message": "Task deleted"}
