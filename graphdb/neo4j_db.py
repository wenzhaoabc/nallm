import os
from neo4j import GraphDatabase, RoutingControl
from mylog import log


class Neo4JDB:
    def __init__(self, uri: str = "", auth: str = "") -> None:
        self.driver = GraphDatabase.driver(
            uri=os.environ.get("NEO4J_URI", ""),
            auth=(os.environ.get("NEO4J_USER"), os.environ.get("NEO4J_PASSWD")),
        )

    def load_cypher(self, cypher: str):
        
        print(cypher)
        log.info(cypher)
        pass
