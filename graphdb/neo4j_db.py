import os

from neo4j import GraphDatabase

node_properties_query = """
CALL apoc.meta.data()
YIELD label, other, elementType, type, property
WHERE NOT type = "RELATIONSHIP" AND elementType = "node"
WITH label AS nodeLabels, collect({property:property, type:type}) AS properties
RETURN {labels: nodeLabels, properties: properties} AS output
"""

rel_properties_query = """
CALL apoc.meta.data()
YIELD label, other, elementType, type, property
WHERE NOT type = "RELATIONSHIP" AND elementType = "relationship"
WITH label AS nodeLabels, collect({property:property, type:type}) AS properties
RETURN {type: nodeLabels, properties: properties} AS output
"""

rel_query = """
CALL apoc.meta.data()
YIELD label, other, elementType, type, property
WHERE type = "RELATIONSHIP" AND elementType = "node"
RETURN "(:" + label + ")-[:" + property + "]->(:" + toString(other[0]) + ")" AS output
"""


def schema_text(node_props, rel_props, rels) -> str:
    return f"""
  This is the schema representation of the Neo4j database.
  Node properties are the following:
  {node_props}
  Relationship properties are the following:
  {rel_props}
  The relationships are the following
  {rels}
  """


class Neo4JDB:
    def __init__(self, uri: str = "", auth: str = "") -> None:
        self.uri = os.environ.get("NEO4J_URI")
        self.auth = (os.environ.get("NEO4J_USER"), os.environ.get("NEO4J_PASSWD"))
        self.schema = ""

    def load_cypher(self, cypher: str):
        with GraphDatabase.driver(self.uri, auth=self.auth) as driver:
            driver.execute_query(cypher)

    def query(self, cypher: str):
        with GraphDatabase.driver(self.uri, auth=self.auth) as driver:
            result, _, _ = driver.execute_query(cypher)
        return result

    def get_schema(self):
        with GraphDatabase.driver(self.uri, auth=self.auth):
            node_props = [el["output"] for el in self.query(node_properties_query)]
            rel_props = [el["output"] for el in self.query(rel_properties_query)]
            rels = [el["output"] for el in self.query(rel_query)]
            schema = schema_text(node_props, rel_props, rels)
            self.schema = schema
            return schema

    def check_if_empty(self) -> bool:
        data = self.query(
            """
        MATCH (n)
        WITH count(n) as c
        RETURN CASE WHEN c > 0 THEN true ELSE false END AS output
        """
        )
        return data[0]["output"]
