from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
import whisper
import torch
import uvicorn
import shutil
import os

app = FastAPI()

# Enable CORS (Allows ESP32 to access the API)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change "*" to specific ESP32 IP if needed
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


model = whisper.load_model("small", device='cuda')


@app.post("/transcribe/")
async def transcribe_audio(file: UploadFile = File(...)):
    try:
        # Save file temporarily
        temp_audio_path = f"temp_audio_{file.filename}"
        with open(temp_audio_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        # Transcribe audio
        result = model.transcribe(temp_audio_path)

        # Delete temporary file after transcription
        os.remove(temp_audio_path)

        return {"transcript": result["text"], 'device': 'cuda'}

    except Exception as e:
        return {"error": str(e)}


# Run the API
if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
