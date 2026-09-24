import wave
import math
import struct
import random

SAMPLE_RATE = 44100
DURATION = 30.0  # 30 seconds
NUM_SAMPLES = int(SAMPLE_RATE * DURATION)

BPM = 85
BEAT_DUR = 60.0 / BPM
BAR_DUR = BEAT_DUR * 4

# Frequencies for Lo-Fi Chord Progression: Cmaj7, Am7, Dm7, G7
CHORDS = [
    [261.63, 329.63, 392.00, 493.88],  # Cmaj7 (C4, E4, G4, B4)
    [220.00, 261.63, 329.63, 392.00],  # Am7   (A3, C4, E4, G4)
    [146.83, 220.00, 261.63, 349.23],  # Dm7   (D3, A3, C4, F4)
    [196.00, 246.94, 293.66, 349.23],  # G7    (G3, B3, D4, F4)
]

def generate_lofi_audio():
    samples = []
    print("Synthesizing upbeat lo-fi music track...")
    
    for i in range(NUM_SAMPLES):
        t = i / SAMPLE_RATE
        bar_idx = int((t % (BAR_DUR * len(CHORDS))) / BAR_DUR)
        bar_t = t % BAR_DUR
        beat_t = t % BEAT_DUR
        beat_num = int((t % BAR_DUR) / BEAT_DUR)
        
        # 1. Warm Synth Chords (Lo-fi electric piano tone: sine + soft 2nd harmonic)
        chord_freqs = CHORDS[bar_idx]
        synth_sample = 0.0
        # Soft envelope attack & decay per bar
        chord_env = math.exp(-1.2 * (bar_t / BAR_DUR))
        
        for f in chord_freqs:
            # Main tone + subtle tremolo/vibrato (lo-fi wow & flutter)
            vibrato = 1.0 + 0.003 * math.sin(2 * math.pi * 5.0 * t)
            phase = 2 * math.pi * f * vibrato * t
            # Soft warm harmonics
            harm = math.sin(phase) + 0.3 * math.sin(phase * 2) + 0.1 * math.sin(phase * 3)
            synth_sample += harm
            
        synth_sample = (synth_sample / len(chord_freqs)) * chord_env * 0.35
        
        # 2. Upbeat Lo-fi Drums
        # Kick on beat 0 and 2.5 (upbeat syncopated kick)
        kick_sample = 0.0
        if beat_num == 0 or (beat_num == 2 and beat_t > BEAT_DUR * 0.5):
            k_t = beat_t if beat_num == 0 else (beat_t - BEAT_DUR * 0.5)
            if k_t >= 0 and k_t < 0.15:
                # Frequency sweep 120Hz -> 45Hz
                f_k = 120.0 * math.exp(-30.0 * k_t)
                kick_env = math.exp(-25.0 * k_t)
                kick_sample = math.sin(2 * math.pi * f_k * k_t) * kick_env * 0.5
                
        # Snare / Rimshot on beat 1 and 3
        snare_sample = 0.0
        if beat_num in (1, 3):
            s_t = beat_t
            if s_t < 0.12:
                noise = (random.random() * 2.0 - 1.0)
                snare_env = math.exp(-30.0 * s_t)
                snare_sample = (math.sin(2 * math.pi * 220.0 * s_t) * 0.4 + noise * 0.6) * snare_env * 0.35
                
        # Hi-hat on eighth notes
        hat_sample = 0.0
        eighth_t = t % (BEAT_DUR / 2.0)
        if eighth_t < 0.05:
            hat_env = math.exp(-70.0 * eighth_t)
            hat_noise = (random.random() * 2.0 - 1.0)
            hat_sample = hat_noise * hat_env * 0.12

        # 3. Lo-Fi Vinyl Crackle & Ambient Hiss
        vinyl = (random.random() * 2.0 - 1.0) * 0.015
        if random.random() < 0.002: # Occasional pop/crackle
            vinyl += (random.random() * 2.0 - 1.0) * 0.15

        # Mix down
        mix = synth_sample + kick_sample + snare_sample + hat_sample + vinyl
        
        # Soft master limiter
        mix = max(-0.95, min(0.95, mix))
        
        # Convert to 16-bit PCM integer
        sample_int = int(mix * 32767)
        samples.append(sample_int)

    # Write WAV file
    wav_path = "/tmp/lofi_music.wav"
    with wave.open(wav_path, "wb") as wf:
        wf.setnchannels(1) # Mono
        wf.setsampwidth(2) # 16-bit
        wf.setframerate(SAMPLE_RATE)
        data = struct.pack(f"<{len(samples)}h", *samples)
        wf.writeframes(data)
        
    print("Lo-fi music WAV created at:", wav_path)
    return wav_path

if __name__ == "__main__":
    generate_lofi_audio()
