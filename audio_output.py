import numpy as np
import sounddevice as sd

def audio_output(np_array):
    
    time = 0.5

    # Generate time of samples between 0 and time seconds
    samples = np.arange(50000 * time) / 50000
    waves = []
    for dat in np_array:
        wave = 15000* np.sin(2 * np.pi * dat * samples)
        wav_wave = np.array(wave, dtype=np.int16)
        waves.append(wav_wave)
  
    for i in range(len(waves)):    
        sd.play(waves[i], blocking=True)
        



