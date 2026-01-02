import http.client
import json

class BrainEngine:
    def __init__(self):
        # Konfigurasi API dari Mas Abas
        self.host = "telkom-ai-dag.api.apilogy.id"
        self.api_key = "bsF7x7lBEfb0PfCXJXBaczUY7Yeas9gY"
        self.path = "/Telkom-LLM/0.0.4/llm/chat/completions"
        
        # System Prompt disiplin untuk TTS
        self.system_prompt = (
            "Anda adalah asisten suara pintar yang dikembangkan oleh Gania Rafidah Huwaida. "
            "Jawablah dengan jelas, padat, dan sangat profesional. "
            "PENTING: Jangan gunakan format markdown seperti bintang (*) atau pagar (#) "
            "dalam jawaban Anda, karena jawaban Anda akan langsung dibacakan oleh mesin TTS."
        )

    def generate_response(self, user_text):
        print(f"[BRAIN] Menghubungi Cloud Telkom-LLM...")
        try:
            conn = http.client.HTTPSConnection(self.host)
            
            # Payload data mengikuti instruksi Mas Abas
            payload_data = {
                "model": "telkom-ai",
                "messages": [
                    {"role": "system", "content": self.system_prompt},
                    {"role": "user", "content": user_text}
                ],
                "max_tokens": 1000,
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
            
            # Parsing data JSON
            response_json = json.loads(data)
            return response_json['choices'][0]['message']['content'].strip()

        except Exception as e:
            print(f"[ERROR BRAIN] Gagal akses Cloud API: {e}")
            return "Maaf, koneksi ke pusat data sedang mengalami gangguan."