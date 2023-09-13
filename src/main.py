from fastapi import FastAPI, UploadFile, File, Depends
from pydantic import BaseModel
from typing import List, Optional
from PIL import Image
from io import BytesIO
import whisper
import tempfile
import os

app = FastAPI()

model = whisper.load_model(name="small", download_root="/whisper-model")

class Params(BaseModel):
    output_type: Optional[str] = "string"
    lang: Optional[str] = "eng"
    config: Optional[str] = "--psm 6"
    nice: Optional[int] = 0 
    timeout: Optional[int] = 0

@app.get("/")
def home():
    return "OCR Pytesseract with FastAPI - Version 1.0"

@app.post("/ocr/")
async def submit(params: Params = Depends(), files: List[UploadFile] = File(...)):
    results = {}

    for file in files:
        # Read the image file as bytes
        audio_data = await file.read()

        # Create a temporary file
        with tempfile.NamedTemporaryFile(dir='src', delete=False, suffix=".mp3") as temp_file:
            temp_file_path = temp_file.name
            # You can write data to the temporary file if needed
            temp_file.write(audio_data)
        
        filename = os.path.basename(temp_file_path)
        file_path = os.path.join('src', filename)

        # Apply Whisper
        result = model.transcribe(file_path)
        os.remove(temp_file_path)
        # Get the transcription
        transcription = result["text"]
        results[file.filename] = transcription

    return {"results": results,
            "params": params}