from typing import Callable

from zhipuai import ZhipuAI
from mylog import log


class ZhiPuLlmRetrieval:
    def __init__(
        self, api_key: str, model: str, base_url: str = "", temperature: float = 0.5
    ):
        self.model = model
        self.temperature = temperature
        self.client = ZhipuAI(api_key=api_key)

    def generate(self, messages: list[dict]) -> str:
        completes = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            temperature=self.temperature,
            stream=False,
        )
        log.info(completes)
        return completes.choices[0].message.content

    def generate_stream(
        self, messages: list[dict], callback: Callable[[str], any]
    ) -> str:
        completes = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            temperature=self.temperature,
            stream=True,
        )

        result = ""
        for chunk in completes:
            if chunk.choices[0].delta.content is not None:
                callback(chunk.choices[0].delta.content)
                result += chunk.choices[0].delta.content

        return result

    def max_tokens(self):
        model_tokens = {
            "glm-4": 128000,
            "glm-3-turbo": 128000,
            "chatglm_turbo": 32000,
        }
        if self.model in model_tokens.keys():
            return model_tokens[self.model]
        else:
            return 8192
