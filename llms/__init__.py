import os

from llms.openai_llm import OpenAILlmRetrieval
from llms.zhipu_llm import ZhiPuLlmRetrieval

models = [
    "gpt-4-1106-preview",  # 128K
    "gpt-4",  # 8.192K
    "gpt-4-32k",  # 32.768K
    "gpt-4-0613",  # 8192
    "gpt-4-32k-0613",
    "gpt-3.5-turbo-1106",
    "gpt-3.5-turbo",
    "gpt-3.5-turbo-16k",
    "qwen-turbo",  # 6K
    "qwen-plus",  # 30K
    "qwen-max-1201",  # 6K
    "qwen-max-longcontext",  # 28K
    "chatglm_turbo",
]


def get_llm(model_name: str = "glm-4", temperature: float = 0.5) -> object:
    if model_name not in models:
        return None
    elif model_name.startswith("gpt"):
        return OpenAILlmRetrieval(
            api_key=os.environ["OPENAI_API_KEY"],
            base_url=os.environ["OPENAI_BASEURL"],
            model=model_name,
            temperature=temperature,
        )
    elif model_name.startswith("glm"):
        return ZhiPuLlmRetrieval()
    else:
        return None
