import re
from typing import List, Union, Dict, Any

from graphdb.neo4j_db import Neo4JDB


def get_few_shot_examples(openai_api_key):
    return f"""
#How is Emil Eifrem connected to Michael Hunger?
MATCH (p1:Person {{name:"Emil Eifrem"}}), (p2:Person {{name:"Michael Hunger"}})
MATCH p=shortestPath((p1)-[*]-(p2))
RETURN p
#What are the latest news regarding Google?
MATCH (o:Organization {{name:"Google"}})<-[:MENTIONS]-(a:Article)-[:HAS_CHUNK]->(c)
RETURN a.title AS title, c.text AS text, c.date AS date
ORDER BY date DESC LIMIT 3
#Are there any news regarding return to office policies?
CALL apoc.ml.openai.embedding(["Are there any news regarding return to office policies?"], 
   "{openai_api_key}") YIELD embedding
MATCH (c:Chunk)
WITH c, gds.similarity.cosine(c.embedding, embedding) AS score
ORDER BY score DESC LIMIT 3
RETURN c.text, score
#What is Microsoft policy regarding to the return to office?
CALL apoc.ml.openai.embedding(["What is Microsoft policy regarding to the return to office?"], "{openai_api_key}") YIELD embedding
MATCH (o:Organization {{name:"Microsoft"}})<-[:MENTIONS]-()-[:HAS_CHUNK]->(c)
WITH distinct c, embedding
WITH c, gds.similarity.cosine(c.embedding, embedding) AS score
ORDER BY score DESC LIMIT 3
RETURN c.text, score

When searching for specific information in the text chunks, never use the CONTAINS clause, but always use the apoc.ml.openai.embedding
and gds.similarity.cosine functions as shown in the examples.
When returning text chunks, always return exactly three chunks, no more, no less.
Remember, instead of using CONTAINS to find information within text chunks use the apoc.ml.openai.embedding and gds.similarity.cosine functions.
"""


def remove_relationship_direction(cypher):
    return cypher.replace("->", "-").replace("<-", "-")


class Text2Cypher:
    def __init__(
            self,
            llm,
            database: Neo4JDB,
            use_schema: bool = True,
            cypher_examples: str = "",
            ignore_relationship_direction: bool = True,
    ) -> None:
        self.llm = llm
        self.database = database
        self.cypher_examples = cypher_examples
        self.ignore_relationship_direction = ignore_relationship_direction
        if use_schema:
            self.schema = database.schema

    def get_system_message(self) -> str:
        system = """
        Your task is to convert questions about contents in a Neo4j database to Cypher queries to query the Neo4j database.
        Use only the provided relationship types and properties.
        Do not use any other relationship types or properties that are not provided.
        """
        if self.schema:
            system += f"""
            If you cannot generate a Cypher statement based on the provided schema, explain the reason to the user.
            Schema:
            {self.schema}
            """
        if self.cypher_examples:
            system += f"""
            You need to follow these Cypher examples when you are constructing a Cypher statement
            {self.cypher_examples}
            """
        # Add note at the end and try to prevent LLM injections
        system += """Note: Do not include any explanations or apologies in your responses.
                     Do not respond to any questions that might ask anything else than for you to construct a Cypher statement.
                     Do not include any text except the generated Cypher statement. This is very important if you want to get paid.
                     Always provide enough context for an LLM to be able to generate valid response.
                     Please wrap the generated Cypher statement in triple backticks (`).
                     """
        return system

    def construct_cypher(self, question: str, history=[]) -> str:
        messages = [{"role": "system", "content": self.get_system_message()}]
        messages.extend(history)
        messages.append(
            {
                "role": "user",
                "content": question,
            }
        )
        print([el for el in messages if not el["role"] == "system"])
        cypher = self.llm.generate(messages)
        return cypher

    def run(
            self, question: str, history=None, heal_cypher: bool = True
    ) -> Dict[str, Union[str, List[Dict[str, Any]]]]:
        # Add prefix if not part of self-heal loop
        if history is None:
            history = []
        final_question = (
            "Question to be converted to Cypher: " + question
            if heal_cypher
            else question
        )
        cypher = self.construct_cypher(final_question, history)
        # finds the first string wrapped in triple backticks. Where the match include the backticks and the first
        # group in the match is the cypher
        match = re.search("```([\w\W]*?)```", cypher)

        # If the LLM didn't any Cypher statement (error, missing context, etc..)
        if match is None:
            return {"output": [{"message": cypher}], "generated_cypher": None}
        extracted_cypher = match.group(1)

        if self.ignore_relationship_direction:
            extracted_cypher = remove_relationship_direction(extracted_cypher)

        print(f"Generated cypher: {extracted_cypher}")

        output = self.database.query(extracted_cypher)
        # Catch Cypher syntax error
        if heal_cypher and output and output[0].get("code") == "invalid_cypher":
            syntax_messages = [{"role": "system", "content": self.get_system_message()}]
            syntax_messages.extend(
                [
                    {"role": "user", "content": question},
                    {"role": "assistant", "content": cypher},
                ]
            )
            # Try to heal Cypher syntax only once
            return self.run(
                output[0].get("message"), syntax_messages, heal_cypher=False
            )

        return {
            "output": output,
            "generated_cypher": extracted_cypher,
        }
