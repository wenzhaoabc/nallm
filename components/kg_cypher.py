"""
Created on Fri Mar 1 24:
@author: WEN
"""
import random
import json
import re

from components.extract_data import extract_cypher_from_rawtext
from components.prompts import to_cypher_system_prompt, to_cypher_user_prompt

default_cypher = """
CALL apoc.load.json("file:///path/to/json") YIELD value AS data

// 处理节点
UNWIND data.nodes AS node
CALL apoc.merge.node([node.label], {name: node.name}, node.properties) YIELD node as n

UNWIND  data.relationships AS rel
MATCH (start {name: rel.start}), (end {name: rel.end})
CALL apoc.create.relationship(start, rel.type, rel.properties, end) YIELD rel as r
"""


class KG2Cypher(object):
    def __init__(
            self,
            llm,
            filename: str,
            schema: str = None,
    ) -> None:
        self.llm = llm
        self.filename = filename
        self.schema = schema

    def request_to_ai(self, content: str) -> str:
        messages = [
            {"role": "system", "content": to_cypher_system_prompt()},
            {"role": "user", "content": to_cypher_user_prompt(content=content)},
        ]
        call_back = lambda x: print(x, end="")
        raw_res = self.llm.generate_stream(messages=messages, callback=call_back)
        return raw_res

    def process(self, kgs: dict[str, list]) -> str:
        example = dict[str, list]()
        example["nodes"] = random.sample(kgs["nodes"], len(kgs["nodes"]))
        example["relationships"] = random.sample(
            kgs["relationships"], len(kgs["relationships"])
        )
        # TODO 默认Cypher脚本及JSON文本访问URI
        # ai_res = self.request_to_ai(json.dumps(example))
        # cypher = extract_cypher_from_rawtext(ai_res)
        cypher = default_cypher
        new_path = "https://raw.githubusercontent.com/" + self.filename
        new_script = re.sub(r'(?<=apoc.load.json\(").+?(?="\))', new_path, cypher)
        return new_script
