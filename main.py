import json
import time
from typing import Optional

from fastapi import FastAPI, WebSocket, UploadFile
from pydantic import BaseModel

import llms
from components.enums import LanguageEnum
from components.extract_kg import ExtractKG
from components.kg_clean import DataDisambiguation
from components.kg_cypher import KG2Cypher

app = FastAPI()


class T2CModel(BaseModel):
    filename: str
    language: LanguageEnum = LanguageEnum.zh
    model: str = "gpt-3.5"
    prompt: Optional[str] = None
    example: Optional[str] = None


@app.post("/upload")
async def create_files(file: UploadFile):
    contents = await file.read()
    with open(f"static/{file.filename}", "wb") as f:
        f.write(contents)

    return {"filename": file.filename}


@app.post("/t2c")
async def test_2_cypher(body: T2CModel):
    llm = llms.get_llm(body.model)
    text = ""
    with open("static/" + body.filename, "r", encoding="utf-8") as f:
        text = f.read()
    print(body)
    print(text)
    # 提取知识图谱
    e = ExtractKG(llm=llm, language=body.language, example=body.example)
    kg = e.extract(text)
    # 对知识图谱中的节点和关系进行国过滤清洗
    cleaner = DataDisambiguation(llm=llm)
    kg = cleaner.disambiguate(kg)
    kg_filename = str(int(time.time())) + ".json"
    with open("kgs/" + kg_filename, "w", encoding="utf-8") as f:
        json.dump(kg, f, indent=4)
    # 知识图谱转为适用于neo4j的cypher脚本
    t = KG2Cypher(llm=llm)
    cypher = t.process(kg)

    return {"cypher": cypher, "kg": kg}


@app.websocket("/t2c")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    await websocket.send_json({"type": "debug", "message": "connected"})

    while True:
        data = await websocket.receive_json()
        msg_type = data["action"]
        request_json = data["data"]
        if msg_type == "kg":
            await websocket.send_json({"action": "acc", "data": request_json})
            filename = request_json.get("filename", "test.txt")
            modelname = request_json.get("modelname", "gpt-4")
            llm = llms.get_llm(model_name=modelname)
            schema = request_json.get("schema", None)
            example = request_json.get("example", None)
            e = ExtractKG(llm, LanguageEnum.zh, example=example)

            with open("static/" + filename, "r", encoding="utf8") as f:
                result = e.extract(f.read())
                await websocket.send_json({"action": "kg", "data": result})

            c = KG2Cypher(llm=llm, schema=None)
            cypher = c.process(result)
            print(cypher)

            await websocket.send_json({"action": "cypher", "data": cypher})

        elif msg_type == "start":
            await websocket.send_json(
                {"type": "extract", "message": "start extract data ===="}
            )


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", port=8080, host="127.0.0.1", reload=True)
