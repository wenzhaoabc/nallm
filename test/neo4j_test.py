from graphdb.neo4j_db import Neo4JDB

driver = Neo4JDB()

schema = driver.get_schema()

print(schema)
