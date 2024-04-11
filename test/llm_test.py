from openai import OpenAI

import llms


def openai_llm_test(stream: bool = False):
    openai = llms.get_llm("gpt-4-0125-preview")
    # print(openai.max_tokens())
    messages = [
        {
            "role": "user",
            "content": """
我正在撰写本科毕业论文的开题报告，我的毕业论文的题目是：使用基于大语言模型和知识图谱的多智能体系统模拟历史时间，主要内容为：利用大语言模型（包括GPT3，Claude3）等构建多智能体系统，并为每个智能体搭建以知识图谱为格式的知识库，这个多智能体系统将模拟历史事件，主要是第一次世界大战，第二次世界大战，以及中国古代的战国时期的历史走向等。
请帮我写一下我的毕业设计的课题背景，尽量在1500字左右。背景应该涉及大语言模型的进展，知识图谱与大语言模型结合的优势，其中应该涉及通过模拟历史事件，加强对国际政治关系的认识来避免战争的研究意义等
            """
        }
    ]
    if stream:
        callback = lambda c: print(f"{c}", end="")
        openai.generate_stream(messages=messages, callback=callback)
    else:
        response = openai.generate(messages=messages)
        print(response)


def openai_llm_test2(stream: bool = False):
    client = OpenAI(api_key="sk-aD8IBWtgiXeEjgKpscNWoy7JvTPXTgRljhxuZvfRKOWYJ9N5",
                    base_url="http://region-3.seetacloud.com:60270/v1")
    completions = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": "Do you know what you are doing?"}]
    )
    print(completions.model_dump_json())
    c = completions.choices[0].message.content
    print(c)


openai_llm_test(True)
