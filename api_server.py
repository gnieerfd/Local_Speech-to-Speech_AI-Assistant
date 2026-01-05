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
async def ask_sts(audio: UploadFile = File(...)):
    temp_in = "temp_request.wav"
    temp_out = "response.wav"
    try:
        with open(temp_in, "wb") as buffer:
            shutil.copyfileobj(audio.file, buffer)
        
        user_text = asr.transcribe_file(temp_in) 
        
        if not user_text or user_text.strip() == "":
            return {"user": "", "assistant": "Maaf, suara tidak terdengar jelas."}

        assistant_response = brain.generate_response(user_text)

        tts.speak(assistant_response, temp_out)

        with open(temp_out, "rb") as f:
            audio_base64 = base64.b64encode(f.read()).decode('utf-8')

        return {
            "user": user_text,
            "assistant": assistant_response, 
            "audio": audio_base64
        }
    except Exception as e:
        print(f"RUNTIME ERROR: {str(e)}")
        return {"error": str(e)}
    finally:
        for f in [temp_in, temp_out]:
            if os.path.exists(f):
                os.remove(f)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)