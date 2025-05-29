from fastapi import UploadFile, File
from faster_whisper import WhisperModel
from pathlib import Path
import re
import string
model = WhisperModel("base" , device="cpu")

tmp_dir = Path("tmp")
tmp_dir.mkdir(parents=True, exist_ok=True)

def preprocess(text):
    text = text.lower()
    text = text.translate(str.maketrans('', '', string.punctuation))
    text = re.sub(r'\s+', ' ', text).strip()
    return text

async def transcribe_voice(file : UploadFile = File(...)):
    audio_path = tmp_dir/file.filename
    with open(audio_path, "wb") as f:
        f.write(await file.read())
    
    segments , _ = model.transcribe(audio_path)
    transcript = " ".join([seg.text for seg in segments])
    preprocessed_transcript = preprocess(transcript)
    return transcript , preprocessed_transcript