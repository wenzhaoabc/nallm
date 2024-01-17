import components.text_splitter
from components.extract_data import get_nodes_relationships_from_rawtext
from components.prompts import to_kg_system_prompt, to_kg_user_prompt
from components.enums import LanguageEnum
from mylog import log


class ExtractKG:
    def __init__(self, llm, language: LanguageEnum):
        self.llm = llm
        self.language = language

    def request_to_ai(self, content: str) -> str:
        messages = [
            {"role": "system", "content": to_kg_system_prompt(self.language)},
            {"role": "user", "content": to_kg_user_prompt(content, language=self.language)}
        ]
        log.info("request_to_ai messages: " + str(messages))
        call_back = lambda c: print(c, end="")
        res = self.llm.generate_stream(messages, call_back)
        log.info("request_to_ai res: " + str(res))
        return res

    def get_token_num(self, content: str) -> int:
        if self.language == LanguageEnum.zh:
            return len(content) * 2
        else:
            # TODO compute content tokens
            return len(content) * 3 // 4

    def extract(self, content: str) -> list[dict]:
        allowed_tokens = (self.llm.max_tokens() -
                          self.get_token_num(to_kg_system_prompt(self.language)) -
                          self.get_token_num(to_kg_user_prompt("", language=self.language)))
        chunk_size = allowed_tokens // 2 if self.language == LanguageEnum.zh else allowed_tokens * 4
        chunks = components.text_splitter.text_splitter_txt_zh(content, chunk_size, chunk_size // 10)

        results = []
        for chunk in chunks:
            raw_text = self.request_to_ai(chunk)
            chunk_node_relationships = get_nodes_relationships_from_rawtext(raw_text)
            log.debug("chunk_node_relationships" + str(chunk_node_relationships))
            results.append(chunk_node_relationships)

        return results
