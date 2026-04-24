import logging
import os
import time
from typing import Any, Dict, Optional

import requests
from requests.exceptions import RequestException

logger = logging.getLogger("GroqClient")
logger.setLevel(logging.INFO)
handler = logging.StreamHandler()
formatter = logging.Formatter("%(asctime)s %(levelname)s %(name)s %(message)s")
handler.setFormatter(formatter)
logger.addHandler(handler)


class GroqClient:
    def __init__(self, api_key: Optional[str] = None, base_url: Optional[str] = None):
        self.api_key = api_key or os.getenv("GROQ_API_KEY")
        if not self.api_key:
            raise RuntimeError("GROQ_API_KEY must be set in environment or .env")

        self.base_url = base_url or os.getenv(
            "GROQ_API_URL",
            "https://api.groq.com/v1/models/llama-3.3-70b/infer",
        )
        self.session = requests.Session()
        self.session.headers.update(
            {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json",
            }
        )

    def _post(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        backoff_seconds = 1
        for attempt in range(1, 4):
            try:
                logger.info("Groq request attempt %s", attempt)
                response = self.session.post(self.base_url, json=payload, timeout=10)
                response.raise_for_status()
                return response.json()
            except RequestException as exc:
                logger.warning(
                    "Groq request failed on attempt %s: %s",
                    attempt,
                    exc,
                )
                if attempt == 3:
                    logger.error("Groq request exhausted retries")
                    raise
                time.sleep(backoff_seconds)
                backoff_seconds *= 2

    def generate_report(self, prompt: str) -> str:
        payload = {
            "input": prompt,
            "max_output_tokens": 1024,
            "temperature": 0.2,
        }
        response_json = self._post(payload)
        output = response_json.get("output")

        if isinstance(output, list) and output:
            first = output[0]
            if isinstance(first, dict) and "content" in first:
                return first["content"]
            return str(first)

        return str(output or "")
