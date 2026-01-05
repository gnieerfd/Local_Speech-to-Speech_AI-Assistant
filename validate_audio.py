# 1. Import library dasar sistem
import os
import shutil
import pyaudio
import numpy as np

ffmpeg_path = r"D:\Internship\Telkom\ffmpeg-8.0.1-essentials_build\bin"
os.environ["PATH"] += os.pathsep + ffmpeg_path

if shutil.which("ffmpeg"):
    print("LOG: FFmpeg terdeteksi oleh Python (SUCCESS)")
else:
    raise RuntimeError("FFmpeg tetap tidak terdeteksi. Cek kembali penulisan path!")

def test_microphone_input():
    p = pyaudio.PyAudio()
    RATE = 16000 # Standar ASR
    CHUNK = 1024
    
    print("\n--- Testing Real-time Mic Input ---")
    try:
        stream = p.open(format=pyaudio.paInt16,
                        channels=1,
                        rate=RATE,
                        input=True,
                        frames_per_buffer=CHUNK)
        
        print("Mulai bicara (Tes selama 3 detik)...")
        for _ in range(0, int(RATE / CHUNK * 3)):
            data = np.frombuffer(stream.read(CHUNK), dtype=np.int16)
            peak = np.abs(data).max()
            bars = "#" * int(peak / 500)
            print(f"Volume: {bars}")
            
        print("\nSTATUS: Mikrofon AKTIF.")
        stream.stop_stream()
        stream.close()
    except Exception as e:
        print(f"\nSTATUS: Gagal akses mikrofon! {e}")
    finally:
        p.terminate()

if __name__ == "__main__":
    test_microphone_input()