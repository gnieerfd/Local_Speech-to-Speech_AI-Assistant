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
        Kamu adalah Jarvis, seorang teknisi yang tegas dan analitis. Sebagai asisten saya, tugasmu adalah membantu saya dengan jawaban yang singkat, jelas, dan tepat sasaran. Hindari basa-basi dan jawaban yang bertele-tele.
        Jawabanmu harus berdasarkan fakta dan data teknis yang akurat. Jika kamu tidak tahu jawabannya, katakan "Saya tidak tahu" daripada memberikan informasi yang salah.
        Gunakan bahasa Indonesia yang formal dan profesional.
        Pertanyaan: {user_text}
        """
        payload = {
            "model": self.model_name,
            "prompt": prompt,
            "stream": False
        }
        
        try:
            # Mengirim request ke kontainer ollama-brain yang sedang UP
            response = requests.post(self.url, json=payload, timeout=180)
            if response.status_code == 200:
                return response.json().get('response', '').strip()
            return "Maaf, komunikasi dengan otak terputus."
        except Exception as e:
            return f"Koneksi ke Ollama gagal. Pastikan Docker aktif! ({e})"