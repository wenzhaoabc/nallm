import os

from openai import OpenAI

# client = OpenAI(api_key=os.environ['OPENAI_API_KEY'], base_url=os.environ['OPENAI_BASEURL'])
client = OpenAI(api_key='<KEY>', base_url="http://127.0.0.1:8080/v1")

res = client.embeddings.create(input=["Hello", "Hi"], model="text-embedding-3-small")

for embedding in res.data:
    print(len(embedding.embedding))
    print(embedding.embedding)
    print(embedding.index)

print(res.usage)
