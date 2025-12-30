import requests

class BrainEngine:
    def __init__(self, model_name="llama3.2:1b"):
        # Port 11434 adalah port standar Ollama di Docker yang sudah kamu jalankan
        self.url = "http://localhost:11434/api/generate"
        self.model_name = model_name

        # Di dalam brain.py, ubah bagian prompt:
    def generate_response(self, user_text):
        # Prompt Engineering agar Jarvis lebih "pintar" dan to-the-point
        prompt = f"""
        Kamu adalah Jarvis, penasihat teknis Gania yang tegas dan analitis.
        Gunakan bahasa casual (lo/gue atau santai). 
        Jangan validasi kalau tidak perlu. Kritik kalau logikanya lemah.
        Jawab maksimal 1-2 kalimat pendek saja.
        Pertanyaan: {user_text}
        """
        payload = {
            "model": self.model_name,
            "prompt": prompt,
            "stream": False
        }
        
        try:
            # Mengirim request ke kontainer ollama-brain yang sedang UP
            response = requests.post(self.url, json=payload, timeout=60)
            if response.status_code == 200:
                return response.json().get('response', '').strip()
            return "Maaf, komunikasi dengan otak terputus."
        except Exception as e:
            return f"Koneksi ke Ollama gagal. Pastikan Docker aktif! ({e})"