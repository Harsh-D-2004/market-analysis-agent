from fastapi import FastAPI
from pydantic import BaseModel
from orchestrator.service import invoke_router

app = FastAPI()

class Queryrequest(BaseModel):
    query: str

@app.post("/query")
def query(req: Queryrequest):
    respone = invoke_router(req.query)
    print(respone)
    return {"result": respone}
