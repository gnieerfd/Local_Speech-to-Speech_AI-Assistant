import pyttsx3
import time

class TTSEngine:
    def __init__(self):
        # Kita hanya simpan konfigurasinya, bukan engine-nya
        self.rate = 175

    def say(self, text):
        print(f"[TTS] Jarvis sedang berbicara...")
        try:
            # Inisialisasi ULANG setiap kali bicara untuk memastikan 
            # COM object segar dan tidak 'hang' karena CPU bottleneck
            engine = pyttsx3.init()
            engine.setProperty('rate', self.rate)
            
            voices = engine.getProperty('voices')
            # Gunakan suara Indonesia jika tersedia
            engine.setProperty('voice', voices[1].id if len(voices) > 1 else voices[0].id)
            
            engine.say(text)
            engine.runAndWait()
            
            # WAJIB: Hentikan dan hapus objek untuk membebaskan memori
            engine.stop()
            del engine
            
            # Beri jeda kecil agar driver audio Windows bisa 'bernapas'
            time.sleep(0.5)
            
        except Exception as e:
            print(f"[ERROR TTS] Gagal mengeluarkan suara: {e}")