# -*- coding: utf-8 -*-
#api接口
from fastapi import FastAPI, UploadFile, File, Query
from pydantic import BaseModel
from logger import logger
from knowledeg_base import KnowledgeBaseServres
from rag import Ragservice

app = FastAPI(title="RAG 知识库问答 API")
kb = KnowledgeBaseServres()
rag = Ragservice()

class QueryRequest(BaseModel):
    question: str
    session_id: str = "default"

@app.post("/upload_txt")
async def upload_txt(file: UploadFile = File(...)):
    try:
        content = await file.read()
        text = content.decode("utf-8")
        res = kb.upload_by_str(text, file.filename)
        logger.info(f"API 上传文件：{file.filename}")
        return {"code": 200, "msg": res}
    except Exception as e:
        logger.error(f"上传失败：{str(e)}")
        return {"code": 500, "msg": f"错误：{str(e)}"}

@app.post("/chat")
async def chat(req: QueryRequest):
    try:
        res = rag.chain.invoke(
            {"input": req.question},
            config={"configurable": {"session_id": req.session_id}}
        )
        logger.info(f"用户提问：{req.question}")
        return {"code": 200, "answer": res}
    except Exception as e:
        logger.error(f"对话失败：{str(e)}")
        return {"code": 500, "msg": str(e)}

@app.get("/")
def index():
    return {"message": "RAG API 运行正常"}


@app.get("/w")
async def kk():
    return {"message": "你好11"}