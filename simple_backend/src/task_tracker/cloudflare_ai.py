import os
from typing import Optional, Dict
from pydantic import BaseModel
from http_client import BaseHTTPClient


class CloudflareAIUsage(BaseModel):
    prompt_tokens: int
    completion_tokens: int
    total_tokens: int


class CloudflareAIResponse(BaseModel):
    response: str
    usage: CloudflareAIUsage


class CloudflareAIResult(BaseModel):
    result: CloudflareAIResponse
    success: bool
    errors: list
    messages: list


class CloudflareAI(BaseHTTPClient):
    def __init__(self):
        self.api_key = os.getenv("CLOUDFLARE_API_KEY")
        self.account_id = os.getenv("CLOUDFLARE_ACCOUNT_ID")
        self.model = os.getenv("CLOUDFLARE_MODEL", "@cf/meta/llama-2-7b-chat-int8")
        super().__init__()

    def _get_request_headers(self) -> Dict[str, str]:
        return {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

    def _get_base_url(self) -> str:
        return f"https://api.cloudflare.com/client/v4/accounts/{self.account_id}/ai/run/{self.model}"

    def get_task_solution_suggestions(self, task_description: str) -> Optional[str]:
        """Получает предложения по решению задачи от LLM"""
        prompt = f"""
        Предложи способ решения задачи: 
        "{task_description}".
        """

        try:
            response = self._make_request(
                "POST",
                json={"messages": [{"role": "system", "content": prompt}]}
            )
            result = CloudflareAIResult(**response)
            if result.success:
                return result.result.response
            return None
        except Exception as e:
            print(f"Error calling Cloudflare AI: {e}")
            return None