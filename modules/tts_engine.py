from gtts import gTTS
import os
import re
import base64

class TTSEngine:
    def __init__(self):
        self.lang = 'id'

    def generate(self, text): # Ubah nama jadi 'generate' agar sinkron
        """Merubah teks menjadi base64 audio via Cloud."""
        print(f"[TTS] Assistant sedang men-generate suara natural (Google Cloud)...")
        output_path = "response.wav"
        try:
            # Cleaning text dari markdown agar suara gTTS tidak aneh
            clean_text = re.sub(r'[*#_~]', '', text)
            
            # Proses Cloud TTS
            tts = gTTS(text=clean_text, lang=self.lang, slow=False)
            tts.save(output_path)
            
            # Encode file ke Base64 agar bisa dikirim ke Frontend
            with open(output_path, "rb") as audio_file:
                encoded_string = base64.b64encode(audio_file.read()).decode('utf-8')
            
            print(f"[SUCCESS] Audio siap dikirim dalam format Base64")
            return encoded_string # Kembalikan nilai string
            
        except Exception as e:
            print(f"[ERROR TTS] gTTS Gagal: {e}")
            return None