import re

# 原始的脚本
script = """
CALL apoc.load.json("file:///path/to/your/json/file.json") YIELD value
UNWIND value.nodes AS node
MERGE (n:`label`{name:node.name}) SET n += node.properties
WITH node
UNWIND value.relationships AS rel
MATCH (start:`label`{name:rel.start})
MATCH (end:`label`{name:rel.end})
MERGE (start)-[r:`relationship type value`]->(end) SET r += rel.properties
"""

# 新的文件路径
new_path = "https://raw.githubusercontent.com/1233.json"

# 使用正则表达式替换apoc.load.json的参数
new_script = re.sub(r'(?<=apoc.load.json\(").+?(?="\))', new_path, script)

print(new_script)