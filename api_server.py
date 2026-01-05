import os
import sys
import shutil
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

@app.post("/ask_sts")
async def ask_sts(
    audio_raw: UploadFile = File(...), 
    audio_clean: UploadFile = File(...)
):
    try:
        # 1. Simpan audio asli untuk dokumentasi Mas Abas
        raw_content = await audio_raw.read()
        with open("temp_raw.wav", "wb") as f:
            f.write(raw_content)

        # 2. Proses audio_clean untuk ASR (Whisper)
        clean_content = await audio_clean.read()
        with open("temp_clean.wav", "wb") as f:
            f.write(clean_content)

        # 3. Transkripsi kedua file untuk perbandingan
        text_raw = asr_engine.transcribe("temp_raw.wav")
        text_clean = asr_engine.transcribe("temp_clean.wav")

        # 4. Ambil respon Brain (LLM) berdasarkan hasil yang CLEAN
        # Kita hanya pakai memori konteks untuk jalur Clean agar tetap akurat
        answer_clean = brain.generate_response(text_clean)
        
        # Simulasi respon untuk jalur RAW (bisa sama atau beda)
        answer_raw = brain.generate_response(text_raw) 

        # 5. Generate Suara (TTS) dari hasil yang CLEAN
        audio_base64 = tts_engine.generate(answer_clean)

        return {
            "raw": {"text": text_raw, "response": answer_raw},
            "clean": {"text": text_clean, "response": answer_clean},
            "audio": audio_base64
        }
    except Exception as e:
        print(f"Error: {e}")
        return {"error": str(e)}, 500

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)