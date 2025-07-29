import os
import requests
from typing import Optional
from pydantic import BaseModel


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


class CloudflareAI:
    def __init__(self):
        self.api_key = os.getenv("CLOUDFLARE_API_KEY")
        self.account_id = os.getenv("CLOUDFLARE_ACCOUNT_ID")
        self.model = os.getenv("CLOUDFLARE_MODEL", "@cf/meta/llama-2-7b-chat-int8")
        self.base_url = f"https://api.cloudflare.com/client/v4/accounts/{self.account_id}/ai/run/{self.model}"

        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

    def get_task_solution_suggestions(self, task_description: str) -> Optional[str]:
        """Получает предложения по решению задачи от LLM"""
        prompt = f"""
        Предложи способ решения задачи: 
        "{task_description}".
        """

        try:
            response = requests.post(
                self.base_url,
                headers=self.headers,
                json={"messages": [{"role": "system", "content": prompt}]}
            )
            response.raise_for_status()

            result = CloudflareAIResult(**response.json())
            if result.success:
                return result.result.response
            return None
        except Exception as e:
            print(f"Error calling Cloudflare AI: {e}")
            return None
