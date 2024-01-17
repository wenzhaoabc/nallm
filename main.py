from fastapi import FastAPI, WebSocket, UploadFile, File

import llms
from components.enums import LanguageEnum
from components.extract_kg import ExtractKG

app = FastAPI()


@app.post("/upload")
async def create_files(file: UploadFile):
    contents = await file.read()
    with open(f"static/{file.filename}", "wb") as f:
        f.write(contents)

    return {"filename": file.filename}


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
            model_name = request_json.get("model_name", "gpt-4")
            llm = llms.get_llm(model_name=model_name)
            schema = request_json.get("schema", None)
            e = ExtractKG(llm, LanguageEnum.zh)

            with open("static/" + filename, "r", encoding="utf8") as f:
                result = e.extract(f.read())
                await websocket.send_json({"action": "kg", "data": result})


        elif msg_type == "start":
            await websocket.send_json({"type": "extract", "message": "start extract data ===="})


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", port=8080, host="127.0.0.1", reload=True)
