import pyaudio

def test_mic():
    p = pyaudio.PyAudio()
    # Standar AI: 16kHz, Mono
    RATE = 16000 
    CHUNK = 1024
    
    print("--- Mencoba membuka mikrofon ---")
    try:
        stream = p.open(format=pyaudio.paInt16,
                        channels=1,
                        rate=RATE,
                        input=True,
                        frames_per_buffer=CHUNK)
        
        print("BERHASIL: Mikrofon terdeteksi dan aktif.")
        stream.stop_stream()
        stream.close()
    except Exception as e:
        print(f"GAGAL: {e}")
    finally:
        p.terminate()

if __name__ == "__main__":
    test_mic()