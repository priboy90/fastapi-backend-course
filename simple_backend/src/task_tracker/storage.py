import json
from pathlib import Path
from typing import List
from models import TaskAdd, Task

class TaskStorage:
    def __init__(self, file_path: str = "tasks.json"):
        self.file_path = Path(file_path)
        if not self.file_path.exists():
            self.file_path.write_text("[]")

    def _read_tasks(self) -> List[Task]:
        with open(self.file_path, "r") as f:
            data = json.load(f)
        return [Task(**item) for item in data]

    def _write_tasks(self, tasks: List[Task]):
        with open(self.file_path, "w") as f:
            json.dump([task.dict() for task in tasks], f, indent=2)

    def get_all(self) -> List[Task]:
        return self._read_tasks()

    def create(self, task: TaskAdd) -> Task:
        tasks = self._read_tasks()
        if len(tasks) != 0:
            task_id = max(tasks, key=lambda x: x.id).id + 1
        else:
            task_id = 1
        new_task = Task(id=task_id, name=task.name, status=task.status)
        tasks.append(new_task)
        self._write_tasks(tasks)
        return new_task

    def update(self, task_id: int, new_task: TaskAdd) -> Task:
        tasks = self._read_tasks()
        for task in tasks:
            if task.id == task_id:
                task.name = new_task.name
                task.status = new_task.status
                self._write_tasks(tasks)
                return task
        raise ValueError("Задача отсутствует")

    def delete(self, task_id: int):
        tasks = self._read_tasks()
        tasks = [t for t in tasks if t.id != task_id]
        self._write_tasks(tasks)