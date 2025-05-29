from fastapi import FastAPI, UploadFile, File
from agents.service import transcribe_voice

from fastapi.responses import JSONResponse
from fastapi import status

app = FastAPI()

@app.post("/transcribe")
async def transcribe(file : UploadFile = File(...)):

    transcript , preprocessed_text = await transcribe_voice(file)
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={"transcription": transcript , "preprocessed": preprocessed_text}
    )