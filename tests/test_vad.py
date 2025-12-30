from audio_engine import AudioEngine
from vad_handler import VADHandler
from config import DEFAULT_MIC_INDEX

def main():
    engine = AudioEngine()
    vad = VADHandler()
    
    engine.start_stream(device_index=DEFAULT_MIC_INDEX)
    print("\n--- SISTEM SIAGA (Ngomong dong!) ---")
    
    try:
        while True:
            # 1. Dengar potongan suara
            chunk = engine.listen_chunk()
            
            # 2. Filter lewat VAD
            speech_data = vad.process_chunk(chunk)
            
            # 3. Jika VAD mengembalikan satu kalimat utuh
            if speech_data is not None:
                print(f"LOG: Satu kalimat tertangkap! Ukuran data: {len(speech_data)} samples.")
                print("Siaga kembali...\n")
                
    except KeyboardInterrupt:
        print("\nSistem dimatikan.")
    finally:
        engine.stop_stream()

if __name__ == "__main__":
    main()