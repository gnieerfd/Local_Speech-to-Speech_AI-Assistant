import http.client
import json

class BrainEngine:
    def __init__(self):
        # Konfigurasi API tetap dari Mas Abas
        self.host = "telkom-ai-dag.api.apilogy.id"
        self.api_key = "bsF7x7lBEfb0PfCXJXBaczUY7Yeas9gY"
        self.path = "/Telkom-LLM/0.0.4/llm/chat/completions"
        
        # Kapasitas Memori: Simpan 4 percakapan terakhir (User + Assistant)
        self.history = []
        self.max_history = 8 # 4 user + 4 assistant
        
        self.system_prompt = (
            "Anda adalah Asisten STS Telkom yang cerdas. Jawablah dengan padat. "
            "Anda harus mengingat konteks percakapan sebelumnya."
        )

    def generate_response(self, user_text):
        print(f"[BRAIN] Menghubungi Cloud dengan Memori Konteks...")
        try:
            conn = http.client.HTTPSConnection(self.host)
            
            # 1. Susun Payload (System + History + Current User)
            messages = [{"role": "system", "content": self.system_prompt}]
            
            # Tambahkan riwayat yang ada
            messages.extend(self.history)
            
            # Tambahkan input user terbaru
            messages.append({"role": "user", "content": user_text})

            payload_data = {
                "model": "telkom-ai",
                "messages": messages, # Kirim seluruh konteks
                "max_tokens": 500, # Kurangi agar lebih cepat
                "temperature": 0.7,
                "stream": False 
            }

            headers = {
                'Content-Type': "application/json",
                'Accept': "application/json",
                'x-api-key': self.api_key
            }

            conn.request("POST", self.path, json.dumps(payload_data), headers)
            res = conn.getresponse()
            data = res.read().decode("utf-8")
            
            response_json = json.loads(data)
            assistant_answer = response_json['choices'][0]['message']['content'].strip()

            # 2. Update Memori: Simpan user input dan assistant answer
            self.history.append({"role": "user", "content": user_text})
            self.history.append({"role": "assistant", "content": assistant_answer})

            # 3. Truncate Memori: Jangan sampai kepenuhan
            if len(self.history) > self.max_history:
                self.history = self.history[-self.max_history:]

            return assistant_answer

        except Exception as e:
            print(f"[ERROR BRAIN] Gagal akses Cloud API: {e}")
            return "Maaf, memori saya sedang penuh, bisa ulangi lagi?"