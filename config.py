import os

FFMPEG_PATH = r"D:\Internship\Telkom\ffmpeg-8.0.1-essentials_build\bin"
os.environ["PATH"] += os.pathsep + FFMPEG_PATH

SAMPLE_RATE = 16000 
CHUNK_SIZE = 1024
CHANNELS = 1
DEFAULT_MIC_INDEX = 1 

VAD_THRESHOLD = 500  
SILENCE_LIMIT = 15  

WHISPER_MODEL_SIZE = "base" 
COMPUTE_TYPE = "int8"