from audio_engine import AudioEngine
from vad_handler import VADHandler
from asr_engine import ASREngine
from config import DEFAULT_MIC_INDEX

def main():
    engine = AudioEngine()
    vad = VADHandler()
    asr = ASREngine() # Inisialisasi otak pendengar
    
    engine.start_stream(device_index=DEFAULT_MIC_INDEX)
    print("\n--- ASISTEN SIAGA: BICARALAH ---")
    
    try:
        while True:
            chunk = engine.listen_chunk()
            speech_data = vad.process_chunk(chunk)
            
            if speech_data is not None:
                print("LOG: Sedang menerjemahkan...")
                # Proses transkripsi
                text = asr.transcribe(speech_data)
                
                if text:
                    print(f"\n>>> GANIA: {text}")
                else:
                    print("LOG: Suara tidak jelas atau hanya noise.")
                print("Siaga kembali...\n")
                
    except KeyboardInterrupt:
        print("\nSistem dimatikan.")
    finally:
        engine.stop_stream()

if __name__ == "__main__":
    main()