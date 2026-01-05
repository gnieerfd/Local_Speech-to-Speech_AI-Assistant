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

asr = ASREngine()  
brain = BrainEngine()
tts = TTSEngine()  

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

        # Simpan file audio
        with open(raw_path, "wb") as f:
            f.write(await audio_raw.read())
        with open(clean_path, "wb") as f:
            f.write(await audio_clean.read())

        # 1. Transkripsi keduanya hanya untuk monitoring LAB
        text_raw = asr.transcribe_file(raw_path)    
        text_clean = asr.transcribe_file(clean_path) 

        # 2. EKSEKUSI: Panggil Brain HANYA satu kali
        answer_final = brain.generate_response(text_clean)

        # 3. Generate Audio respon asisten
        audio_base64 = tts.generate(answer_final)

        return {
            "raw": {
                "text": text_raw, 
                "response": "(Monitoring Only)", 
                "audio": file_to_base64(raw_path) 
            },
            "clean": {
                "text": text_clean, 
                "response": answer_final,
                "audio": file_to_base64(clean_path) 
            },
            "audio": audio_base64 
        }
    except Exception as e:
        print(f"[CRITICAL ERROR]: {e}")
        return {"error": str(e)}, 500
     
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)