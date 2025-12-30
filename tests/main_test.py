import numpy as np  # Ini yang tadi kurang!
from audio_engine import AudioEngine

def main():
    engine = AudioEngine()
    
    # 1. Menampilkan daftar hardware
    engine.list_devices()
    
    # 2. Masukkan Index 1 (karena tadi sudah berhasil buka stream)
    idx = int(input("\nMasukkan Index Mikrofon: "))
    
    engine.start_stream(device_index=idx)
    
    print("\n--- Mulai Tes Suara (Bicara sekarang!) ---")
    try:
        # Loop untuk mengetes 100 potongan suara (sekitar 6 detik)
        for _ in range(100):
            audio_data = engine.listen_chunk()
            if audio_data is not None:
                # Menghitung amplitudo puncak (Peak)
                peak = np.abs(audio_data).max()
                
                # Visualisasi baris '#' berdasarkan volume
                # Semakin keras kamu bicara, semakin banyak tanda '#'
                bars = "#" * int(peak / 500)
                print(f"Volume: {bars} ({peak})")
    except KeyboardInterrupt:
        print("\nTes dihentikan oleh user.")
    finally:
        print("\nTes selesai.")
        engine.stop_stream()

if __name__ == "__main__":
    main()