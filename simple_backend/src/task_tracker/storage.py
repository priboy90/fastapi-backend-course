import os
import requests
from typing import List
from models import TaskAdd, Task
from pydantic import parse_obj_as

class TaskStorage:
    def __init__(self):
        self.api_key = os.getenv("JSONBIN_API_KEY")
        self.bin_id = os.getenv("JSONBIN_BIN_ID")
        self.base_url = f"https://api.jsonbin.io/v3/b/{self.bin_id}"
        self.headers = {
            "Content-Type": "application/json",
            "X-Master-Key": self.api_key,
            "X-Bin-Versioning": "false"
        }
        self._initialize_bin()


    def _initialize_bin(self):
        """Создает пустой бин при первом запуске"""
        try:
            current_data = self._fetch_bin()
            if current_data is None:
                self._update_bin([])
        except requests.exceptions.RequestException:
            self._update_bin([])

    def _fetch_bin(self):
        """Получает данные из JSONBin.io"""
        response = requests.get(self.base_url, headers=self.headers)
        response.raise_for_status()
        return response.json().get('record')

    def _update_bin(self, data):
        """Обновляет данные в JSONBin.io"""
        response = requests.put(
            self.base_url,
            headers=self.headers,
            json=data
        )
        response.raise_for_status()


    def get_all(self) -> List[Task]:
        """Получает все задачи"""
        data = self._fetch_bin() or []
        return parse_obj_as(List[Task], data)

    def create(self, task: TaskAdd) -> Task:
        """Создает новую задачу с автоматическим ID"""
        tasks = self.get_all()
        task_id = max([t.id for t in tasks], default=0) + 1
        new_task = Task(id=task_id, name=task.name, status=task.status)
        tasks.append(new_task)
        self._update_bin([t.dict() for t in tasks])
        return new_task

    def update(self, task_id: int, new_task: TaskAdd) -> Task:
        """Обновляет задачу по ID"""
        tasks = self.get_all()
        for task in tasks:
            if task.id == task_id:
                task.name = new_task.name
                task.status = new_task.status
                self._update_bin([t.dict() for t in tasks])
                return task
        raise ValueError("Задача отсутствует")

    def delete(self, task_id: int):
        """Удаляет задачу по ID"""
        tasks = self.get_all()
        tasks = [t for t in tasks if t.id != task_id]
        self._update_bin([t.dict() for t in tasks])