from gtts import gTTS
import os
import re

class TTSEngine:
    def __init__(self):
        self.lang = 'id'

    def speak(self, text, output_path):
        """Merubah teks menjadi file audio natural via Cloud."""
        print(f"[TTS] Assistant sedang men-generate suara natural (Google Cloud)...")
        try:
            clean_text = re.sub(r'[*#_~]', '', text)
            
            tts = gTTS(text=clean_text, lang=self.lang, slow=False)
            
            tts.save(output_path)
            print(f"[SUCCESS] Audio natural tersimpan: {output_path}")
            
        except Exception as e:
            print(f"[ERROR TTS] gTTS Gagal: {e}")