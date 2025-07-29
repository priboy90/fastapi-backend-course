from typing import Annotated
from fastapi import FastAPI, Depends, HTTPException
from storage import TaskStorage
from dotenv import load_dotenv
from models import TaskAdd, Task

app = FastAPI()
load_dotenv()
storage = TaskStorage()

@app.get("/tasks")
def get_tasks():
    return storage.get_all()

@app.post("/tasks", response_model=Task)
def create_task(task: Annotated[TaskAdd, Depends()]):
    return storage.create(task)

@app.put("/tasks/{task_id}", response_model=Task)
def update_task(task_id: int, task: Annotated[TaskAdd, Depends()]):
    try:
        return storage.update(task_id, task)
    except ValueError:
        raise HTTPException(status_code=404, detail="Задача отсутствует")

@app.delete("/tasks/{task_id}")
def delete_task(task_id: int):
    storage.delete(task_id)
    return {"message": "Задача удалена"}