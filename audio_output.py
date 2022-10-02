import numpy as np
import sounddevice as sd

sd.default.samplerate = 44100


def audio_output(freq):
    time = 0.3

    frequency = freq

    # Generate time of samples between 0 and time seconds
    samples = np.arange(44100 * time) / 44100.0
    # Recall that a sinusoidal wave of frequency f has formula w(t) = A*sin(2*pi*f*t)
    wave1 = 10000 * np.sin(2 * np.pi * frequency * samples)
    wave2 = 10000 * np.sin(2 * np.pi * 2*frequency * samples)
    # Convert it to wav format (16 bits)
    wav_wave1 = np.array(wave1, dtype=np.int16)
    wav_wave2 = np.array(wave2, dtype=np.int16)
    wave = [wav_wave1 , wav_wave2]
    
    for i in range(len(wave)):    
        sd.play(wave[i], blocking=True)


