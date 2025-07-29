import os
import requests
from abc import ABC, abstractmethod
from typing import Optional, Any, Dict


class BaseHTTPClient(ABC):
    def __init__(self):
        self._initialize_client()

    def _initialize_client(self):
        """Инициализация клиента (может быть переопределена в наследниках)"""
        pass

    @abstractmethod
    def _get_request_headers(self) -> Dict[str, str]:
        """Возвращает заголовки для запроса (должен быть реализован в наследниках)"""
        pass

    @abstractmethod
    def _get_base_url(self) -> str:
        """Возвращает базовый URL (должен быть реализован в наследниках)"""
        pass

    def _make_request(
            self,
            method: str,
            endpoint: str = "",
            json: Optional[Dict[str, Any]] = None,
            params: Optional[Dict[str, Any]] = None
    ) -> Any:
        """Общий метод для выполнения HTTP-запросов"""
        url = f"{self._get_base_url()}{endpoint}"
        headers = self._get_request_headers()

        try:
            response = requests.request(
                method,
                url,
                headers=headers,
                json=json,
                params=params
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Request failed: {e}")
            raise