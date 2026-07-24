import os
import requests
from dotenv import load_dotenv
import re

class AITranslator:
    def __init__(self):
        load_dotenv()
        self.api_key = os.getenv("OPENROUTER_API_KEY")
        if not self.api_key:
            raise ValueError("OPENROUTER_API_KEY not found.")
        self.url = "https://openrouter.ai/api/v1/chat/completions"
        self.model = "meta-llama/llama-3.2-3b-instruct"

    def translate(self, medical_text):
        try:
            cleaned_text = self._clean_text(medical_text)
            prompt = f"Simplify this medical text for a patient: {cleaned_text}"

            # Simplified headers - only the essential ones
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json",
            }

            payload = {
                "model": self.model,
                "messages": [{"role": "user", "content": prompt}],
                "max_tokens": 300,
            }

            # Add a timeout to prevent hanging
            response = requests.post(
                self.url,
                headers=headers,
                json=payload,
                timeout=30  # seconds
            )

            # This will raise an error for bad status codes
            response.raise_for_status()

            data = response.json()
            return data["choices"][0]["message"]["content"]

        except requests.exceptions.ConnectionError:
            return "Network error: Cannot reach OpenRouter. Check your internet connection."
        except requests.exceptions.Timeout:
            return "Request timed out. Please try again."
        except requests.exceptions.HTTPError as e:
            return f"HTTP error {e.response.status_code}: {e.response.text}"
        except Exception as e:
            return f"Translation failed: {str(e)}"

    def _clean_text(self, text):
        text = re.sub(r'\s+', ' ', text).strip()
        text = re.sub(r'[^\w\s.,!?\'"-]', '', text)
        return text
