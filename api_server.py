import os
import sys
import shutil
import base64
import uvicorn
from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware

# 1. Setup Pathing
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(BASE_DIR)

# 2. Import Modul (Pastikan folder 'modules' sudah benar)
try:
    from modules.asr import ASREngine
    from modules.brain import BrainEngine
    from modules.tts_engine import TTSEngine
    print("LOG: Semua modul STS berhasil dimuat!")
except Exception as e:
    print(f"ERROR: Gagal import modul. Detail: {e}")
    sys.exit()

# 3. Inisialisasi Engine (FASE KRITIS RAM 8GB!)
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

@app.post("/ask_sts") # Menggunakan terminologi STS sesuai revisi
async def ask_sts(audio: UploadFile = File(...)):
    temp_in = "temp_request.wav"
    temp_out = "response.wav"
    try:
        # A. Simpan file audio kiriman dari web
        with open(temp_in, "wb") as buffer:
            shutil.copyfileobj(audio.file, buffer)
        
        # B. Speech-to-Text (ASR) - CPU 100%
        user_text = asr.transcribe_file(temp_in) 
        
        if not user_text or user_text.strip() == "":
            return {"user": "", "assistant": "Maaf, suara tidak terdengar jelas."}

        # C. Thinking (Brain/Ollama) - Nama Jarvis DIBUANG
        # Pastikan di modules/brain.py lo juga sudah ganti prompt-nya!
        assistant_response = brain.generate_response(user_text)

        # D. Text-to-Speech (TTS) - Generate Suara Jawaban
        tts.speak(assistant_response, temp_out)

        # E. Encode Audio ke Base64
        with open(temp_out, "rb") as f:
            audio_base64 = base64.b64encode(f.read()).decode('utf-8')

        return {
            "user": user_text,
            "assistant": assistant_response, # Mengganti key 'jarvis' jadi 'assistant'
            "audio": audio_base64
        }
    except Exception as e:
        print(f"RUNTIME ERROR: {str(e)}")
        return {"error": str(e)}
    finally:
        # Bersihkan semua file sementara
        for f in [temp_in, temp_out]:
            if os.path.exists(f):
                os.remove(f)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)