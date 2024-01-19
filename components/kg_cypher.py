#

import random
import json
from components.extract_data import extract_cypher_from_rawtext
from components.prompts import to_cypher_system_prompt, to_cypher_user_prompt


class KG2Cypher(object):
    def __init__(
        self,
        llm,
        schema: str = None,
    ) -> None:
        self.llm = llm
        self.schema = schema

    def request_to_ai(self, conetent: str) -> str:
        messages = [
            {"role": "system", "content": to_cypher_system_prompt()},
            {"role": "user", "content": to_cypher_user_prompt(content=conetent)},
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
        ai_res = self.request_to_ai(json.dumps(example))
        cypher = extract_cypher_from_rawtext(ai_res)
        return cypher
