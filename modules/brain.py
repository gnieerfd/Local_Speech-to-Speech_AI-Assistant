import http.client
import json

class BrainEngine:
    def __init__(self):
        self.host = "telkom-ai-dag.api.apilogy.id"
        self.api_key = "bsF7x7lBEfb0PfCXJXBaczUY7Yeas9gY"
        self.path = "/Telkom-LLM/0.0.4/llm/chat/completions"
        
        self.history = []
        self.max_history = 8 
        self.system_prompt = (
            "Anda adalah Asisten STS Telkom yang cerdas. Jawablah dengan padat. "
            "Anda harus mengingat konteks percakapan sebelumnya."
        )

    def generate_response(self, user_text):
        print(f"[BRAIN] Menghubungi Cloud dengan Memori Konteks...")
        try:
            conn = http.client.HTTPSConnection(self.host)
            
            messages = [{"role": "system", "content": self.system_prompt}]
            
            messages.extend(self.history)
            
            messages.append({"role": "user", "content": user_text})

            payload_data = {
                "model": "telkom-ai",
                "messages": messages, 
                "max_tokens": 500, 
                "temperature": 0.7,
                "stream": False 
            }

            headers = {
                'Content-Type': "application/json",
                'Accept': "application/json",
                'x-api-key': self.api_key
            }
            print(f"DEBUG PAYLOAD MESSAGES: {json.dumps(messages, indent=2)}")
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