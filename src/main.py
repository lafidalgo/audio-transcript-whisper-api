from fastapi import FastAPI, UploadFile, File, Depends
from pydantic import BaseModel
from typing import List, Optional
from PIL import Image
from io import BytesIO

app = FastAPI()

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
        img_data = await file.read()

        # Convert the image bytes to a PIL Image
        img = Image.open(BytesIO(img_data))

        # Apply tesseract
        results[file.filename] = "Test"

    return {"results": results,
            "params": params}