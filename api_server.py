import os
import sys
import base64
import uvicorn
from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(BASE_DIR)

try:
    from modules.asr import ASREngine
    from modules.brain import BrainEngine
    from modules.tts_engine import TTSEngine
    print("LOG: Semua modul STS berhasil dimuat!")
except Exception as e:
    print(f"ERROR: Gagal import modul. Detail: {e}")
    sys.exit()

# Inisialisasi Engine
asr = ASREngine()  # Nama variabel: asr
brain = BrainEngine()
tts = TTSEngine()  # Nama variabel: tts

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)
def file_to_base64(filepath):
    with open(filepath, "rb") as f:
        return base64.b64encode(f.read()).decode("utf-8")

@app.post("/ask_sts")
async def ask_sts(
    audio_raw: UploadFile = File(...), 
    audio_clean: UploadFile = File(...)
):
    try:
        raw_path = "temp_raw.wav"
        clean_path = "temp_clean.wav"

        with open(raw_path, "wb") as f:
            f.write(await audio_raw.read())
        with open(clean_path, "wb") as f:
            f.write(await audio_clean.read())

        text_raw = asr.transcribe_file(raw_path)    
        text_clean = asr.transcribe_file(clean_path) 

        answer_clean = brain.generate_response(text_clean)
        answer_raw = brain.generate_response(text_raw) 

        audio_base64 = tts.generate(answer_clean)

        # REVISI DISINI: Kirimkan audio aslinya juga dalam format Base64
        return {
            "raw": {
                "text": text_raw, 
                "response": answer_raw,
                "audio": file_to_base64(raw_path) # Panggil fungsinya!
            },
            "clean": {
                "text": text_clean, 
                "response": answer_clean,
                "audio": file_to_base64(clean_path) # Panggil fungsinya!
            },
            "audio": audio_base64 # Suara asisten
        }
    except Exception as e:
        print(f"[CRITICAL ERROR]: {e}")
        return {"error": str(e)}, 500
    
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)