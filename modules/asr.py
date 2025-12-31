import os
import numpy as np 
from faster_whisper import WhisperModel
from config import WHISPER_MODEL_SIZE, COMPUTE_TYPE, FFMPEG_PATH

# Paksa sistem mengenali FFmpeg - Wajib untuk baca file audio
os.environ["PATH"] += os.pathsep + FFMPEG_PATH

class ASREngine:
    def __init__(self):
        print(f"LOG: Loading Whisper Model ({WHISPER_MODEL_SIZE})...")
        # Tetap di CPU karena RAM 8GB lo sudah sesak oleh Docker
        self.model = WhisperModel(WHISPER_MODEL_SIZE, device="cpu", compute_type=COMPUTE_TYPE)
        print("LOG: Model ASR siap.")
        
    def transcribe(self, audio_data):
        """Fungsi untuk Mic Lokal (Input: Numpy Array)"""
        peak = np.abs(audio_data).max()
        if peak > 0:
            audio_data = (audio_data.astype(np.float32) / peak) * 32767.0
        
        audio_float32 = audio_data / 32768.0
        return self._run_inference(audio_float32)

    def transcribe_file(self, file_path):
        """Fungsi untuk Web API (Input: Path File .wav)"""
        if not os.path.exists(file_path):
            print(f"ERROR: File {file_path} tidak ditemukan.")
            return ""
            
        print(f"LOG: Memproses file audio: {file_path}")
        # Faster-whisper bisa langsung terima path file sebagai input
        return self._run_inference(file_path)

    def _run_inference(self, input_data):
        """Logika inti transkripsi (Shared Logic)"""
        # Proses ini bakal narik CPU i5 lo sampai 100%
        segments, info = self.model.transcribe(
            input_data, 
            beam_size=10, 
            language="id",
            vad_filter=True, 
            initial_prompt="Halo Gania, apa kabar? Saya asisten Telkom."
        )
        
        result_text = "".join([s.text for s in segments]).strip()
        print(f"DEBUG ASR: {result_text}")
        return result_text