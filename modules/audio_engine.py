import pyaudio
import numpy as np
from config import SAMPLE_RATE, CHUNK_SIZE, CHANNELS 

class AudioEngine:
    def __init__(self):
        self.p = pyaudio.PyAudio()
        self.stream = None

    def list_devices(self):
        """Mencetak daftar hardware audio yang terdeteksi sistem."""
        print("\n--- DAFTAR HARDWARE AUDIO ---")
        for i in range(self.p.get_device_count()):
            info = self.p.get_device_info_by_index(i)
            print(f"Index {i}: {info['name']}")

    def start_stream(self, device_index=None):
        """Membuka aliran audio dari mikrofon."""
        try:
            self.stream = self.p.open(
                format=pyaudio.paInt16,
                channels=CHANNELS,
                rate=SAMPLE_RATE,
                input=True,
                input_device_index=device_index,
                frames_per_buffer=CHUNK_SIZE
            )
            print(f"LOG: Aliran audio dibuka pada Index {device_index}")
        except Exception as e:
            print(f"ERROR: Gagal membuka stream: {e}")

    def listen_chunk(self):
        """Membaca potongan sinyal audio digital."""
        try:
            data = self.stream.read(CHUNK_SIZE, exception_on_overflow=False)
            return np.frombuffer(data, dtype=np.int16)
        except Exception as e:
            print(f"ERROR: Gagal membaca chunk: {e}")
            return None

    def stop_stream(self):
        """Menutup koneksi hardware."""
        if self.stream:
            self.stream.stop_stream()
            self.stream.close()
        self.p.terminate()