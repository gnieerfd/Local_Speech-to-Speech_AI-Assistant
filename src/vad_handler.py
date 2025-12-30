import numpy as np
from config import VAD_THRESHOLD, SILENCE_LIMIT

class VADHandler:
    def __init__(self):
        self.silence_counter = 0
        self.is_recording = False
        self.recorded_chunks = []

    def process_chunk(self, audio_chunk):
        """
        Logika: Jika energi > threshold, mulai rekam. 
        Jika hening > limit, berhenti dan kembalikan audio.
        """
        if audio_chunk is None:
            return None

        # Hitung energi puncak chunk
        energy = np.abs(audio_chunk).max()

        if energy > VAD_THRESHOLD:
            if not self.is_recording:
                print("LOG: Suara terdeteksi, mulai merekam...")
                self.is_recording = True
            
            self.is_recording = True
            self.silence_counter = 0 # Reset hitungan hening
            self.recorded_chunks.append(audio_chunk)
            return None
        
        else:
            if self.is_recording:
                self.silence_counter += 1
                self.recorded_chunks.append(audio_chunk)
                
                # Jika sudah terlalu lama hening
                if self.silence_counter > SILENCE_LIMIT:
                    print(f"LOG: Hening terdeteksi. Durasi rekaman: {len(self.recorded_chunks)} chunks.")
                    full_audio = np.concatenate(self.recorded_chunks)
                    
                    # Reset status
                    self.is_recording = False
                    self.recorded_chunks = []
                    self.silence_counter = 0
                    
                    return full_audio
            return None