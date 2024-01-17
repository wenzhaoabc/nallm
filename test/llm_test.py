import llms


def openai_llm_test(stream: bool = False):
    openai = llms.get_llm("gpt-4-1106-preview")
    print(openai.max_tokens())
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


openai_llm_test(stream=True)
