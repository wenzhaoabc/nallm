from openai import OpenAI
import llms
import json


def openai_llm_test(stream: bool = False):
    openai = llms.get_llm("glm-3-turbo")
    # print(openai.max_tokens())
    messages = [
        {
            "role": "user",
            "content": "This is a test message!"
        }
    ]
    if stream:
        callback = lambda c: print(f"{c}", end="")
        openai.generate_stream(messages=messages, callback=callback)
    else:
        response = openai.generate(messages=messages)
        print(response)


# openai_llm_test(stream=True)


def openai_llm_test2(stream: bool = False):
    client = OpenAI(api_key="",
                    base_url="http://region-3.seetacloud.com:60270/v1")
    completions = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": "Do you know what you are doing?"}]
    )
    print(completions.model_dump_json())
    c = completions.choices[0].message.content
    print(c)


openai_llm_test2()
