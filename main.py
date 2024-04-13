import datetime
import json
from typing import Optional

from flask import Flask, request, jsonify
from pydantic import BaseModel

import llms
from components.enums import LanguageEnum
from components.extract_kg import ExtractKG
from components.kg_clean import DataDisambiguation
from components.kg_cypher import KG2Cypher
from graphdb import Neo4JDB
from graphdb.summarize_result import SummarizeCypherResult
from graphdb.text_cypher import TextCypher
from utils import upload_to_oss, download_from_oss

app = Flask(__name__)


class T2CModel(BaseModel):
    file_url: str
    language: LanguageEnum = LanguageEnum.zh
    model: str = "gpt-3.5"
    prompt: Optional[str] = None
    example: Optional[str] = None


@app.route("/upload", methods=["GET", "POST"])
def create_files():
    file = request.files.get("file")
    if file is None:
        return 400, json.dumps({"error": "no file"})

    file_name = file.filename
    file_type = file_name.split(".")[-1] or "txt"

    timestamp_str = datetime.datetime.now().strftime("%Y%m%d%H%M%S")

    content = file.stream.read()
    filename = f"{timestamp_str}_origin.{file_type}"
    file_url = upload_to_oss(filename, content)

    return jsonify({"url": file_url})


@app.post("/t2c")
def test_2_cypher():
    body_json = request.get_json()
    body = T2CModel(**body_json)

    llm = llms.get_llm(body.model)
    text = download_from_oss(file_url=body.file_url)

    # 提取知识图谱
    e = ExtractKG(llm=llm, language=body.language, example=body.example)
    kg = e.extract(text)
    # 对知识图谱中的节点和关系进行过滤清洗
    cleaner = DataDisambiguation(llm=llm)
    kg = cleaner.disambiguate(kg)

    timestamp_str = datetime.datetime.now().strftime("%d%m%Y%H%M%S")
    kg_filename = f"{timestamp_str}_kg.json"
    file_oss_url = upload_to_oss(kg_filename, json.dumps(kg))

    # 知识图谱转为适用于neo4j的cypher脚本
    t = KG2Cypher(llm=llm, file_url=file_oss_url)
    cypher = t.process(kg)

    db = Neo4JDB()
    execute_results = []
    for k, v in cypher.items():
        res = db.load_cypher(v)
        execute_results.append(res)

    return jsonify({"cypher": cypher, "kg": kg, "kg_url": file_oss_url, "execute_results": execute_results})


@app.route("/execute_cypher", methods=["POST"])
def execute_cypher():
    cypher = request.data.decode()
    # cypher = body_json.get("cypher")
    if cypher is None:
        return 400, jsonify({"error": "no cypher"})
    db = Neo4JDB()
    execute_result = db.query(cypher)
    return jsonify({"cypher": cypher, "message": "OK", "execute_result": execute_result})


@app.route("/load_json", methods=["POST"])
def load_json_to_neo4j():
    body_json = request.get_json()
    file_url = body_json["file_url"]
    driver = Neo4JDB()
    res = driver.import_json(file_url=file_url)
    return jsonify(res)


@app.route("/schema", methods=["GET"])
def get_neo4j_schema():
    driver = Neo4JDB()
    res = driver.get_schema()
    return res


@app.route("/question_2_cypher", methods=["POST"])
def text_2_cypher():
    body_json = request.get_json()
    question = body_json["question"]
    model = body_json["model"]
    llm = llms.get_llm(model, temperature=0.1)
    db = Neo4JDB()

    t2c = TextCypher(llm=llm, db=db)
    res = t2c.construct_cypher_query(question, history=[])

    summary = SummarizeCypherResult(llm)
    answer = summary.run(question, results=res["output"])
    res.update({"answer": answer})
    return jsonify(res)


@app.route("/answer_question", methods=["POST"])
def refactor_questions_llm():
    body_json = request.get_json()
    question = body_json["question"]
    model = body_json["model"]
    llm = llms.get_llm(model, temperature=0.1)
    db = Neo4JDB()
    t2c = TextCypher(llm=llm, db=db)


@app.route("/optimize_question", methods=["POST"])
def optimize_question_with_kg():
    body_json = request.get_json()
    question = body_json["question"]
    model = body_json["model"]
    llm = llms.get_llm(model, temperature=0.1)
    db = Neo4JDB()
    t2c = TextCypher(llm=llm, db=db, use_example=True)
    res = t2c.optimize_question(question, history=[], more_data=True)

    return jsonify({"optimized": res})


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8080, debug=True, load_dotenv=True)
    # import uvicorn
    # uvicorn.run("main:app", port=8080, host="127.0.0.1", reload=True)
