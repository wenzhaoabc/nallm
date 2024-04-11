from typing import Callable

from openai import OpenAI
from mylog import log


class OpenAILlmRetrieval:
    def __init__(self, api_key: str, base_url: str, model: str, temperature: float = 0.5):
        self.model = model
        self.temperature = temperature
        self.client = OpenAI(api_key=api_key, base_url=base_url)

    def generate(self, messages: list[dict]) -> str:
        completes = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            temperature=self.temperature
        )
        log.info(completes)
        return completes.choices[0].message.content

    def generate_stream(self, messages: list[dict], callback: Callable[[str], any]) -> str:
        completes = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            temperature=self.temperature,
            stream=True
        )

        result = ""
        for chunk in completes:
            if chunk.choices[0].delta.content is not None:
                callback(chunk.choices[0].delta.content)
                result += chunk.choices[0].delta.content

        return result

    def max_tokens(self):
        model_tokens = {
            "gpt-4-1106-preview": 128000,
            "gpt-4": 8192,  # 8.192K
            "gpt-4-32k": 32768,  # 32.768K
            "gpt-4-0613": 8192,  # 8192
            "gpt-4-32k-0613": 32000,
        }
        if self.model in model_tokens.keys():
            return model_tokens[self.model]
        else:
            return 8192
