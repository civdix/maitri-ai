import numpy as np

def audio_emotion_from_prosody(audio_int16, sample_rate: int):
    x = audio_int16.astype(np.float32) / 32768.0
    if len(x) == 0:
        return {"arousal": 0.0, "valence": 0.5, "stress": 0.0}
    rms = np.sqrt(np.mean(x**2))
    zcr = np.mean(np.abs(np.diff(np.sign(x))))
    arousal = np.clip(rms * 5.0, 0, 1)
    stress = np.clip((rms * 2.0 + zcr * 0.5), 0, 1)
    valence = np.clip(0.6 - stress*0.3 + (1-arousal)*0.2, 0, 1)
    return {"arousal": float(arousal), "valence": float(valence), "stress": float(stress)}
