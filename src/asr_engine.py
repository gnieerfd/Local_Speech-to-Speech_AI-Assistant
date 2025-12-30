import os
import numpy as np 
from faster_whisper import WhisperModel
from config import WHISPER_MODEL_SIZE, COMPUTE_TYPE, FFMPEG_PATH

# Paksa sistem mengenali FFmpeg
os.environ["PATH"] += os.pathsep + FFMPEG_PATH

class ASREngine:
    def __init__(self):
        print(f"LOG: Loading Whisper Model ({WHISPER_MODEL_SIZE})...")
        # Inisialisasi model Whisper dngan optimasi CTranslate2
        self.model = WhisperModel(WHISPER_MODEL_SIZE, device="cpu", compute_type=COMPUTE_TYPE)
        print("LOG: Model ASR siap.")
        
    def transcribe(self, audio_data):
        peak = np.abs(audio_data).max()
        print(f"LOG: Peak Volume Sinyal: {peak}") # Untuk debug

        if peak > 0:
            audio_data = (audio_data.astype(np.float32) / peak) * 32767.0
        
        audio_float32 = audio_data / 32768.0
        
        segments, info = self.model.transcribe(
            audio_float32, 
            beam_size=10, 
            language="id",
            vad_filter=True, 
            initial_prompt="Halo Gania, apa kabar? Saya asisten Telkom."
        )
        
        return "".join([s.text for s in segments]).strip()