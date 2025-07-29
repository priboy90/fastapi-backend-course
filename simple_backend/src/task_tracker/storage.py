import os
import requests
from typing import List, Dict, Any
from models import TaskAdd, Task
from pydantic import parse_obj_as
from cloudflare_ai import CloudflareAI
from http_client import BaseHTTPClient

class TaskStorage(BaseHTTPClient):
    def __init__(self):
        self.api_key = os.getenv("JSONBIN_API_KEY")
        self.bin_id = os.getenv("JSONBIN_BIN_ID")
        self.ai = CloudflareAI()
        super().__init__()

    def _get_request_headers(self) -> Dict[str, str]:
        return {
            "Content-Type": "application/json",
            "X-Master-Key": self.api_key,
            "X-Bin-Versioning": "false"
        }

    def _get_base_url(self) -> str:
        return f"https://api.jsonbin.io/v3/b/{self.bin_id}"

    def _initialize_client(self):
        """Создает пустой бин при первом запуске"""
        try:
            current_data = self._fetch_bin()
            if current_data is None:
                self._update_bin([])
        except requests.exceptions.RequestException:
            self._update_bin([])

    def _fetch_bin(self):
        """Получает данные из JSONBin.io"""
        return self._make_request("GET").get('record')

    def _update_bin(self, data):
        """Обновляет данные в JSONBin.io"""
        self._make_request("PUT", json=data)

    def get_all(self) -> List[Task]:
        """Получает все задачи"""
        data = self._fetch_bin() or []
        return parse_obj_as(List[Task], data)

    def create(self, task: TaskAdd) -> Task:
        """Создает новую задачу с автоматическим ID и получает решения от AI"""
        tasks = self.get_all()
        task_id = max([t.id for t in tasks], default=0) + 1

        suggestions = self.ai.get_task_solution_suggestions(task.name)

        new_task = Task(
            id=task_id,
            name=task.name,
            status=task.status,
            answer_ai=suggestions
        )

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