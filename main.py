from agents.service import transcribe_voice
from orchestrator.service import invoke_router
from fastapi import FastAPI, UploadFile, File



app = FastAPI()

@app.post("/response")
async def response_chain(file : UploadFile = File(...)):
    text_query , preprocessed_text = await transcribe_voice(file)
    print(preprocessed_text)
    respone = invoke_router(preprocessed_text)
    print(respone)
    return {"result": respone , "query": text_query}
