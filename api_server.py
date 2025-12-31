import os
import sys
import shutil
from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

# Tambahkan path project ke sys.path
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(BASE_DIR)

# Diagnosa file sebelum import
path_asr = os.path.join(BASE_DIR, "modules", "asr.py")
if not os.path.exists(path_asr):
    print(f"CRITICAL ERROR: File {path_asr} tidak ditemukan!")
    sys.exit()

try:
    from modules.asr import ASREngine
    from modules.brain import BrainEngine
    print("LOG: Modul ASR dan Brain berhasil dimuat!")
except Exception as e:
    print(f"ERROR: Gagal import modul. Detail: {e}")
    sys.exit()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Inisialisasi Engine (Fase Kritis RAM!)
asr = ASREngine()
brain = BrainEngine()

@app.post("/ask_jarvis")
async def ask_jarvis(audio: UploadFile = File(...)):
    temp_path = "temp_request.wav"
    try:
        with open(temp_path, "wb") as buffer:
            shutil.copyfileobj(audio.file, buffer)
        
        # Proses ASR - CPU 100%
        user_text = asr.transcribe_file(temp_path) 
        
        if not user_text or user_text.strip() == "":
            return {"user": "", "jarvis": "Gue nggak denger apa-apa."}

        # Proses Brain - Docker CPU 700%
        jarvis_response = brain.generate_response(user_text)

        return {"user": user_text, "jarvis": jarvis_response}
    except Exception as e:
        return {"error": str(e)}
    finally:
        if os.path.exists(temp_path):
            os.remove(temp_path)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)