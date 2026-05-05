import os
from groq import Groq
from tenacity import retry, stop_after_attempt, wait_exponential
import logging
import redis
import hashlib

logging.basicConfig(level=logging.INFO)

class GroqClient:
    def __init__(self):
        self.api_key = os.getenv('GROQ_API_KEY')
        self.redis = redis.Redis(host='localhost', port=6379, db=0)
        if self.api_key and not self.api_key.startswith('gsk_test') and self.api_key != 'your_groq_api_key_here':
            self.client = Groq(api_key=self.api_key)
        else:
            self.client = None
            logging.warning('Groq client disabled: invalid or placeholder API key')

    @retry(stop=stop_after_attempt(2), wait=wait_exponential(multiplier=1, min=2, max=4))
    def call_groq(self, prompt):
        if not self.client:
            raise RuntimeError('Groq client unavailable')
        # Check cache
        cache_key = hashlib.sha256(prompt.encode()).hexdigest()
        cached = self.redis.get(cache_key)
        if cached:
            return cached.decode()
        try:
            response = self.client.chat.completions.create(
                messages=[{"role": "user", "content": prompt}],
                model="llama3-70b-8192"
            )
            result = response.choices[0].message.content
            # Cache for 15 min
            self.redis.setex(cache_key, 900, result)
            return result
        except Exception as e:
            logging.error(f"Groq API error: {e}")
            raise