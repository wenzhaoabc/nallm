import os

from llms.openai_llm import LLM

models = [
    "gpt-4-0125-preview",
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
    "qwen-max",  # 6K
    "qwen-max-longcontext",  # 28K
    "yi-34b-chat-0205",
    "yi-vl-plus",
]


def get_llm(model_name: str = "yi-34b-chat-0205", temperature: float = 0.5) -> LLM:
    if model_name not in models:
        raise ValueError(f"Model name {model_name} not in {models}")
    return LLM(
        api_key=os.environ["OPENAI_API_KEY"],
        base_url=os.environ["OPENAI_BASEURL"],
        model=model_name,
        temperature=temperature,
    )
