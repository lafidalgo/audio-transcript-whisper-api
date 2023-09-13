import whisper

model = whisper.load_model("base")
result = model.transcribe("src/sample1.mp3")
print(result["text"])