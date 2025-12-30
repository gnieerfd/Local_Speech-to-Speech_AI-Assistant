from src.audio_engine import AudioEngine
from src.vad_handler import VADHandler
from src.asr_engine import ASREngine
from src.brain import BrainEngine
from src.tts_engine import TTSEngine
from config import DEFAULT_MIC_INDEX

def main():
    # Inisialisasi Pipeline Lengkap
    engine = AudioEngine()
    vad = VADHandler()
    asr = ASREngine()
    brain = BrainEngine()
    tts = TTSEngine()
    
    engine.start_stream(device_index=DEFAULT_MIC_INDEX)
    print("\n" + "="*40)
    print(" S2S - FULLY OPERATIONAL")
    print("="*40 + "\n")
    
    try:
        while True:
            chunk = engine.listen_chunk()
            speech_data = vad.process_chunk(chunk)
            
            if speech_data is not None:
                user_text = asr.transcribe(speech_data)
                
                if user_text:
                    print(f"User  : {user_text}")
                    print("Jarvis sedang berpikir...")
                    # Brain merespon
                    ai_response = brain.generate_response(user_text)
                    print(f"Jawaban  : {ai_response}")
                    
                    # TTS berbicara
                    tts.say(ai_response)
                
                print("\n[READY] Silakan bicara lagi...")
                
    except KeyboardInterrupt:
        print("\n[STOP] Mematikan sistem...")
    finally:
        if 'tts' in locals():
            del tts 
        engine.stop_stream()
        print("[LOG] Driver audio dilepaskan.")

if __name__ == "__main__":
    main()