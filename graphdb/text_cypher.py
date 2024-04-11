"""
借助LLM将用户问题转为Cypher查询
"""
import os
import re

from llms.openai_llm import LLM
from .neo4j_db import Neo4JDB
from .cypher_examples import get_fewshot_examples
from .summarize_result import SummarizeCypherResult

choose_more_info_prompt = """
You have only two choices, just give the optimized question or get more information about the Neo4j database.
If you choose to the front, please output the optimized question directly.
If you choose to the back, please output "I need more information" directly.
"""

question_optimize_prompt = """
Your task is to optimize the given question according to schema and properties of the Neo4j database.
The optimized question will be used in Retrieval-Augmented Generation application.
"""


class TextCypher:
    def __init__(self,
                 llm: LLM,
                 db: Neo4JDB,
                 example: str | None = None,
                 use_schema: bool = True):
        self.llm = llm
        self.db = db
        if example is None:
            self.example = get_fewshot_examples(
                openai_api_key=os.environ["OPENAI_API_KEY"],
                base_url=os.environ["OPENAI_BASEURL"],
            )
        self.use_schema = use_schema
        if self.use_schema:
            self.schema = db.get_schema()

    def generate_system_message(self) -> str:
        system = """
        Your task is to convert questions about contents in a Neo4j database to Cypher queries to query the Neo4j database.
        Use only the provided relationship types and properties.
        Do not use any other relationship types or properties that are not provided.
        """
        if self.use_schema:
            system += f"""
            If you cannot generate a Cypher statement based on the provided schema, explain the reason to the user.
            Schema:
            {self.schema}
            """
        if self.example:
            system += f"""
            You need to follow these Cypher examples when you are constructing a Cypher statement
            {self.example}
            """
        return system

    def construct_cypher(self, question: str, history: list = None) -> str:
        messages = [{"role": "system", "content": self.generate_system_message()}]
        messages.extend(history)
        messages.append({"role": "user", "content": question})
        raw_res = self.llm.generate(messages)
        return raw_res

    def construct_cypher_query(self, question: str, history: list = None, heal_cypher: bool = True) -> dict:
        if history is None:
            history = []
        cypher = self.construct_cypher(question, history=history)
        match = re.search("```([\w\W]*?)```", cypher)
        if match is None:
            return {"output": [{"message": cypher}], "generated_cypher": None, "OK": False}
        extracted_cypher = match.group(1)

        output = self.db.query(extracted_cypher)

        if heal_cypher and output and output[0].get("code") == "invalid_cypher":
            syntax_messages = [{"role": "system", "content": self.generate_system_message()}]
            syntax_messages.extend(
                [
                    {"role": "user", "content": question},
                    {"role": "assistant", "content": cypher},
                ]
            )
            # Try to heal Cypher syntax only once
            return self.construct_cypher_query(
                output[0].get("message"), syntax_messages, heal_cypher=False
            )

        return {
            "output": output,
            "generated_cypher": extracted_cypher,
            "OK": True,
        }

    def optimize_question(self, question: str, history: list = None, more_data: bool = False) -> str:
        system_message = f"""
        {question_optimize_prompt}
        Database schema:
        f{self.schema}
        """

        if more_data:
            more_data_res = self.construct_cypher_query(question, history=[])
            if more_data_res["OK"]:
                summary = SummarizeCypherResult(self.llm)
                detail_information = summary.run(question, more_data_res["output"])
            else:
                detail_information = None

            system_message = f"""
            {question_optimize_prompt}
            Database schema:
            f{self.schema}
            Some detail information:
            {detail_information}
            """
        messages = [{"role": "system", "content": system_message}, {"role": "user", "content": question}]
        raw_res = self.llm.generate(messages)
        return raw_res
