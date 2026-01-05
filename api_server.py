import os
import sys
import base64
import uvicorn
import subprocess 
from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from config import FFMPEG_PATH 

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

def transcode_to_mp3(input_path, output_path):
    try:
        ffmpeg_exe = os.path.join(FFMPEG_PATH, "ffmpeg.exe")
        command = [ffmpeg_exe, "-y", "-i", input_path, "-codec:a", "libmp3lame", "-b:a", "192k", output_path]
        subprocess.run(command, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        return True
    except Exception as e:
        print(f"[FFMPEG ERROR]: {e}")
        return False

@app.post("/ask_sts")
async def ask_sts(audio_raw: UploadFile = File(...), audio_clean: UploadFile = File(...)):
    # Nama file sementara
    raw_in = "raw_input.tmp"
    clean_in = "clean_input.tmp"
    raw_out = "raw_output.mp3"
    clean_out = "clean_output.mp3"

    try:
        # 1. Simpan input asli dari iPhone (biasanya AAC/MP4)
        with open(raw_in, "wb") as f: f.write(await audio_raw.read())
        with open(clean_in, "wb") as f: f.write(await audio_clean.read())

        # 2. Transkripsi (Faster-Whisper pinter, dia bisa baca .tmp walau isinya mp4)
        text_raw = asr.transcribe_file(raw_in)    
        text_clean = asr.transcribe_file(clean_in) 

        # 3. TRANSCODING: Ubah ke MP3 murni buat dikirim balik ke iPhone
        transcode_to_mp3(raw_in, raw_out)
        transcode_to_mp3(clean_in, clean_out)

        # 4. Proses Otak AI (Hanya satu kali biar history aman)
        answer_final = brain.generate_response(text_clean)

        # 5. Generate Suara Asisten (TTS lo udah output MP3 kan?)
        audio_base64 = tts.generate(answer_final)

        return {
            "raw": {
                "text": text_raw, 
                "audio": file_to_base64(raw_out) # Kirim MP3 hasil transcode
            },
            "clean": {
                "text": text_clean, 
                "response": answer_final,
                "audio": file_to_base64(clean_out) # Kirim MP3 hasil transcode
            },
            "audio": audio_base64 
        }
    except Exception as e:
        print(f"[CRITICAL ERROR]: {e}")
        return {"error": str(e)}, 500
    finally:
        # 6. CLEANUP: Hapus file biar nggak menuhin SSD laptop Acer lo
        for f in [raw_in, clean_in, raw_out, clean_out]:
            if os.path.exists(f): os.remove(f)
     
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)