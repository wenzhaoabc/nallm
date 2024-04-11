import base64
from typing import Union, List, Literal, Optional

import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel
from sentence_transformers import SentenceTransformer

app = FastAPI()

embedding_mode = SentenceTransformer("paraphrase-albert-small-v2",
                                     cache_folder="C:\\Users\\shuai\\workspace\\projects\\nallm\\retrieval\\static")


class EmbeddingReq(BaseModel):
    input: Union[str, List[str]]
    model: str = "bge-large-zh-v1.5"
    encoding_format: Literal["float", "base64"] = "float"
    dimensions: Optional[int] = None
    user: Optional[str] = None


@app.post("/v1/embeddings")
async def embeddings(req: EmbeddingReq):
    text = [req.input] if type(req.input) is str else req.input
    embedded = embedding_mode.encode(text, convert_to_numpy=True, normalize_embeddings=True)

    if req.encoding_format == "base64":
        bytes_arr = [row.tobytes() for row in embedded]
        embedding_list = [base64.b64encode(b).decode() for b in bytes_arr]
    else:
        embedding_list = [row.tolist() for row in embedded]

    return {
        "data": [
            {"index": index, "embedding": embedding, "object": "embedding"}
            for index, embedding in enumerate(embedding_list)
        ],
        "model": "bge-large-zh-v1.5",
        "object": "list",
        "usage": {"prompt_tokens": 0, "total_tokens": 0, "completion_tokens": 0}
    }


if __name__ == '__main__':
    uvicorn.run("emb:app", port=8080, host="127.0.0.1", reload=True)
