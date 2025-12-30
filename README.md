# 🤖 Local Speech-to-Speech AI Assistant

[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://www.python.org/downloads/)
[![Docker](https://img.shields.io/badge/docker-required-blue.svg)](https://www.docker.com/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

> **Privacy-First, Local-Only Voice Assistant**  
> Implementasi asisten suara pintar yang berjalan 100% lokal tanpa ketergantungan pada cloud API.

---

## 📖 Deskripsi Proyek

**Jarvis S2S** adalah sistem asisten suara Speech-to-Speech (S2S) yang modular dan berjalan sepenuhnya di lokal. Sistem ini menangkap audio mentah dari mikrofon, memprosesnya menjadi teks menggunakan ASR (Automatic Speech Recognition), menganalisis konteks dengan LLM lokal, dan merespons kembali dengan suara menggunakan TTS (Text-to-Speech).

Dikembangkan dengan fokus pada:
- ✅ **Privacy**: Tidak ada data yang dikirim ke cloud
- ✅ **Efisiensi**: Optimasi untuk hardware terbatas melalui quantization
- ✅ **Modularitas**: Pemisahan komponen untuk kemudahan maintenance
- ✅ **Stabilitas**: Containerization dengan Docker untuk isolasi proses

---

## ✨ Fitur Utama

### 🎯 Core Features
- **Modular Pipeline**: Pemisahan tugas antara audio processing, VAD, ASR, Brain (LLM), dan TTS
- **Quantized Inference**: Menggunakan `int8` compute type pada Whisper untuk performa CPU optimal
- **Robust TTS Engine**: Re-inisialisasi driver SAPI5 untuk mencegah memory leak dan crash
- **Persistent Docker Brain**: LLM berjalan dalam kontainer Docker untuk stabilitas dan efisiensi

### 🔊 Audio Processing
- Real-time audio capture dengan PyAudio
- Voice Activity Detection (VAD) untuk deteksi speech
- Noise filtering dan audio normalization
- 16kHz Mono sampling untuk efisiensi

### 🧠 Intelligence
- Local LLM menggunakan Llama 3.2 1B via Ollama
- Context-aware responses
- Optimized prompt engineering
- Timeout handling untuk response stability

---

## 🏗️ Arsitektur Sistem

### 1️⃣ Logical Workflow

```
┌─────────────────┐     ┌──────────────┐     ┌─────────────┐
│  AUDIO INPUT    │────▶│ VAD HANDLER  │────▶│ ASR ENGINE  │
│   (Microphone)  │     │ Noise Filter │     │Faster-Whisper│
└─────────────────┘     └──────────────┘     └──────┬──────┘
                                                     │
                                                     ▼
┌─────────────────┐     ┌──────────────┐     ┌─────────────┐
│  AUDIO OUTPUT   │◀────│  TTS ENGINE  │◀────│BRAIN ENGINE │
│    (Speaker)    │     │   pyttsx3    │     │   Ollama    │
└─────────────────┘     └──────────────┘     └─────────────┘
```

### 2️⃣ Component Stack

| Komponen | Teknologi | Detail Spesifikasi |
|----------|-----------|-------------------|
| **Orchestrator** | Python 3.8+ | Main Loop Management |
| **Audio Library** | PyAudio & NumPy | 16kHz Mono Sampling |
| **VAD** | Custom Implementation | Threshold-based Detection |
| **ASR Engine** | Faster-Whisper | `base` model, `int8` compute |
| **LLM Engine** | Ollama | Model: `llama3.2:1b` via Docker |
| **TTS Engine** | pyttsx3 | SAPI5 Windows Driver |

### 3️⃣ Directory Structure

```
jarvis-s2s/
├── main.py                 # Entry point aplikasi
├── main_test.py           # Testing & calibration script
├── config.py              # Konfigurasi global
├── modules/
│   ├── audio_handler.py   # Audio I/O management
│   ├── vad.py            # Voice Activity Detection
│   ├── asr.py            # Speech Recognition (Whisper)
│   ├── brain.py          # LLM integration (Ollama)
│   └── tts.py            # Text-to-Speech (pyttsx3)
├── requirements.txt       # Python dependencies
├── .dockerignore
├── docker-compose.yml     # (Optional) Docker orchestration
└── README.md             # This file
```

---

## ⚙️ Instalasi & Setup

### 1️⃣ Prasyarat System

#### Hardware Requirements
- **RAM**: Minimal 8GB (16GB recommended)
- **Storage**: ~5GB free space
  - Model Whisper: ~150MB
  - Model Llama: ~1.3GB
  - Docker overhead: ~2GB
- **Processor**: Multi-core CPU (Intel i5/AMD Ryzen 5 atau lebih tinggi)

#### Software Requirements
- **OS**: Windows 10/11 (64-bit)
- **Python**: 3.8 atau lebih baru
- **Docker Desktop**: Terbaru versi
- **FFmpeg**: Required untuk audio processing

### 2️⃣ Install Dependencies

#### A. Install FFmpeg
1. Download FFmpeg dari [ffmpeg.org](https://ffmpeg.org/download.html)
2. Extract ke lokasi pilihan (contoh: `C:\ffmpeg`)
3. Tambahkan `C:\ffmpeg\bin` ke System PATH
4. Verifikasi instalasi:
```powershell
ffmpeg -version
```

#### B. Install Python Packages
```powershell
# Clone repository (jika dari Git)
git clone https://github.com/yourusername/jarvis-s2s.git
cd jarvis-s2s

# Buat virtual environment
python -m venv venv

# Aktivasi virtual environment
.\venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

**requirements.txt:**
```txt
pyaudio==0.2.13
numpy>=1.21.0
faster-whisper>=0.10.0
pyttsx3>=2.90
requests>=2.31.0
```

### 3️⃣ Setup Docker Brain (Ollama)

#### Jalankan Ollama Container
```powershell
# Pull Ollama image
docker pull ollama/ollama

# Jalankan container dengan volume mapping
docker run -d \
  -v D:\Internship\Telkom\ollama-data:/root/.ollama \
  -p 11434:11434 \
  --name ollama-brain \
  ollama/ollama
```

#### Download Model Llama
```powershell
# Masuk ke container
docker exec -it ollama-brain bash

# Download model
ollama pull llama3.2:1b

# Verifikasi model
ollama list

# Keluar dari container
exit
```

#### Verifikasi Ollama Running
```powershell
# Cek status container
docker ps

# Test API endpoint
curl http://localhost:11434/api/tags
```

### 4️⃣ Konfigurasi System

Edit file `config.py`:

```python
# Audio Configuration
SAMPLE_RATE = 16000
CHUNK_SIZE = 1024
CHANNELS = 1

# VAD Configuration
VAD_THRESHOLD = 2000  # Sesuaikan dengan kalibrasi mikrofon
SILENCE_DURATION = 2.0  # Detik silence sebelum stop recording

# Whisper Configuration
WHISPER_MODEL_SIZE = "base"  # Opsi: tiny, base, small, medium
WHISPER_COMPUTE_TYPE = "int8"
WHISPER_DEVICE = "cpu"

# Ollama Configuration
OLLAMA_URL = "http://localhost:11434"
OLLAMA_MODEL = "llama3.2:1b"
OLLAMA_TIMEOUT = 60

# TTS Configuration
TTS_RATE = 150  # Kecepatan bicara (words per minute)
TTS_VOLUME = 0.9  # Volume (0.0 - 1.0)

# FFmpeg Path
FFMPEG_PATH = r"C:\ffmpeg\bin\ffmpeg.exe"
```

### 5️⃣ Kalibrasi Mikrofon (PENTING!)

Akurasi sistem sangat bergantung pada kalibrasi peak volume.

#### Langkah Kalibrasi:
1. **Buka Sound Settings Windows**:
   - Klik kanan icon speaker di taskbar
   - Pilih "Sound settings"
   - Pilih "Sound Control Panel"
   - Tab "Recording" → Pilih mikrofon → "Properties"

2. **Sesuaikan Microphone Boost**:
   - Tab "Levels"
   - Set **Microphone Boost**: +10dB atau +20dB
   - Set **Microphone Volume**: 70-80%

3. **Jalankan Test Script**:
```powershell
python main_test.py
```

4. **Bicara dengan Volume Normal**:
   - Peak volume target: **4000 - 8000**
   - Jika terlalu rendah (<2000): Naikkan boost
   - Jika terlalu tinggi (>10000): Turunkan boost atau volume

5. **Update VAD_THRESHOLD**:
   - Edit `config.py`
   - Set `VAD_THRESHOLD` ke ~50% dari peak volume
   - Contoh: Peak 6000 → Threshold 3000

---

## 🎮 Cara Menjalankan

### 1️⃣ Start Docker Container

```powershell
# Pastikan Docker Desktop running
docker start ollama-brain

# Verifikasi status
docker ps
```

### 2️⃣ Aktivasi Virtual Environment

```powershell
cd jarvis-s2s
.\venv\Scripts\activate
```

### 3️⃣ Jalankan Aplikasi

```powershell
python main.py
```

### 4️⃣ Expected Output

```
[INFO] Initializing Jarvis S2S...
[INFO] Loading Whisper model 'base'...
[INFO] Connecting to Ollama Brain...
[INFO] TTS Engine initialized
[INFO] System ready. Listening...

Silakan berbicara...
[VAD] Speech detected!
[ASR] Transcribing audio...
pertanyaan : Apa itu kertas?

[DEBUG] Jarvis sedang berpikir...
[LLM] Response received
jawaban    : Kertas adalah materi tipis yang dihasilkan dari 
             serat tumbuhan melalui proses pulping. Kertas 
             digunakan untuk menulis, mencetak, dan membungkus.

[TTS] Jarvis sedang berbicara...
[TTS] Response delivered successfully
```

---

## 🔧 Troubleshooting

### ❌ Problem: Model Load Error

**Symptom:**
```
Error: Model file not found
```

**Solution:**
```powershell
# Verifikasi model di Docker
docker exec -it ollama-brain ollama list

# Re-download jika perlu
docker exec -it ollama-brain ollama pull llama3.2:1b
```

### ❌ Problem: Connection Timeout

**Symptom:**
```
ConnectionError: Ollama tidak merespons
```

**Solution:**
1. Cek Docker container status:
```powershell
docker ps
# Jika tidak ada, restart:
docker start ollama-brain
```

2. Tingkatkan timeout di `config.py`:
```python
OLLAMA_TIMEOUT = 120  # Naikkan jadi 2 menit
```

### ❌ Problem: Audio Tidak Terdeteksi

**Symptom:**
```
[VAD] No speech detected
```

**Solution:**
1. Jalankan test script:
```powershell
python main_test.py
```

2. Perhatikan peak volume saat bicara
3. Sesuaikan `VAD_THRESHOLD` di `config.py`:
```python
# Jika peak volume = 5000
VAD_THRESHOLD = 2500  # ~50% dari peak
```

### ❌ Problem: TTS Crash/No Sound

**Symptom:**
```
RuntimeError: SAPI5 driver crashed
```

**Solution:**
Sistem sudah dilengkapi auto-recovery. Jika masih terjadi:
1. Restart Python script
2. Update Windows speech engine:
```powershell
# PowerShell (Run as Administrator)
Get-WindowsCapability -Online | Where-Object Name -like 'Language*' | Add-WindowsCapability -Online
```

### ❌ Problem: High CPU Usage

**Solution:**
1. Gunakan model Whisper lebih kecil:
```python
WHISPER_MODEL_SIZE = "tiny"  # Dari "base"
```

2. Gunakan model LLM lebih kecil:
```powershell
docker exec -it ollama-brain ollama pull llama3.2:1b  # Sudah minimal
```

### ❌ Problem: Halusinasi Teks (Wrong Transcription)

**Solution:**
1. Tingkatkan volume bicara
2. Kurangi noise background
3. Perbaiki kalibrasi mikrofon
4. Gunakan model Whisper lebih besar:
```python
WHISPER_MODEL_SIZE = "small"  # Lebih akurat
```

---

## 🚀 Optimasi Performance

### 1️⃣ Model Selection Guide

| Use Case | Whisper Model | LLM Model | RAM Usage |
|----------|--------------|-----------|-----------|
| Quick Test | tiny | llama3.2:1b | ~4GB |
| Balanced | base | llama3.2:1b | ~6GB |
| Accurate | small | llama3.2:3b | ~10GB |
| High Quality | medium | llama3.2:7b | ~16GB+ |

### 2️⃣ Docker Optimization

```powershell
# Limit memory untuk Ollama
docker update --memory="4g" --memory-swap="6g" ollama-brain

# Restart container
docker restart ollama-brain
```

### 3️⃣ Audio Buffer Tuning

Edit `config.py`:
```python
# Untuk low-latency (tapi lebih CPU intensive)
CHUNK_SIZE = 512

# Untuk efisiensi (tapi sedikit delay)
CHUNK_SIZE = 2048
```

---

## 📊 System Monitoring

### Check Resource Usage

```powershell
# Monitor Docker container
docker stats ollama-brain

# Monitor Python process
# Windows Task Manager → Details → python.exe
```

### Logging

Aplikasi menggunakan Python logging. Edit level di `main.py`:

```python
import logging
logging.basicConfig(
    level=logging.DEBUG,  # Ubah ke INFO untuk production
    format='[%(levelname)s] %(message)s'
)
```

---

## 🛠️ Advanced Configuration

### Custom System Prompt

Edit `brain.py` untuk mengubah persona Jarvis:

```python
SYSTEM_PROMPT = """
Kamu adalah Jarvis, asisten AI yang cerdas dan membantu.
Jawab dengan singkat dan jelas dalam Bahasa Indonesia.
Maksimal 2-3 kalimat per respons.
"""
```

### Multi-Language Support

Whisper mendukung multi-bahasa. Edit `asr.py`:

```python
# Auto-detect language
result = model.transcribe(audio_path)

# Force specific language
result = model.transcribe(audio_path, language="id")  # Indonesian
result = model.transcribe(audio_path, language="en")  # English
```

---

## 📝 Development Notes

### Adding New Modules

1. Buat file di folder `modules/`
2. Import di `main.py`
3. Integrate ke main loop

Contoh: Menambahkan emotion detection
```python
# modules/emotion.py
def detect_emotion(text):
    # Your emotion detection logic
    return emotion

# main.py
from modules.emotion import detect_emotion

emotion = detect_emotion(transcription)
response = brain.generate_response(transcription, emotion=emotion)
```

### Testing Individual Components

```python
# Test ASR only
python -c "from modules.asr import ASREngine; asr = ASREngine(); print(asr.transcribe('audio.wav'))"

# Test LLM only
python -c "from modules.brain import BrainEngine; brain = BrainEngine(); print(brain.chat('Halo'))"

# Test TTS only
python -c "from modules.tts import TTSEngine; tts = TTSEngine(); tts.speak('Halo dunia')"
```

---

## 📄 License

MIT License - see [LICENSE](LICENSE) file for details

---

## 👤 Author

**Gania Rafidah Huwaida**  
- **NIM**: 235150301111047  
- **University**: Universitas Brawijaya  
- **Internship**: Telkom Indonesia (BigBox)  
- **Year**: 2024

---

## 🙏 Acknowledgments

- [Faster-Whisper](https://github.com/guillaumekln/faster-whisper) by Guillaume Klein
- [Ollama](https://ollama.ai/) untuk local LLM inference
- [pyttsx3](https://github.com/nateshmbhat/pyttsx3) untuk TTS engine
- Telkom Indonesia BigBox Team untuk guidance dan support

---

## 📞 Support

Jika menemui masalah:
1. Cek [Troubleshooting Section](#-troubleshooting)
2. Review logs untuk error details
3. Open issue di repository (jika public)
4. Contact: [your-email@example.com]

---

## 🔮 Future Roadmap

- [ ] Wake word detection ("Hey Jarvis")
- [ ] Continuous conversation mode
- [ ] Multi-turn context memory
- [ ] Web interface dashboard
- [ ] Mobile app integration
- [ ] Voice cloning for TTS
- [ ] Emotion-based response
- [ ] Integration with smart home devices

---

**Happy Coding! 🚀**