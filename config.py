import os

# 1. Path System (Wajib untuk FFmpeg)
FFMPEG_PATH = r"D:\Internship\Telkom\ffmpeg-8.0.1-essentials_build\bin"
os.environ["PATH"] += os.pathsep + FFMPEG_PATH

# 2. Parameter Audio
SAMPLE_RATE = 16000 
CHUNK_SIZE = 1024
CHANNELS = 1
DEFAULT_MIC_INDEX = 1 # Sesuaikan dengan hasil main_test.py kamu

# 3. Parameter VAD (Voice Activity Detection)
VAD_THRESHOLD = 500  # Turunkan sedikit agar suara "Ini Budi" tertangkap
SILENCE_LIMIT = 15  

# 4. Parameter Whisper ASR (PENTING!)
# Kita naikkan ke 'small' agar tidak halusinasi bahasa Inggris lagi
WHISPER_MODEL_SIZE = "base" 
# 'int8' agar CPU laptop kamu tetap dingin dan prosesnya cepat
COMPUTE_TYPE = "int8"