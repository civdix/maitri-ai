import os

VIDEO_W = float(os.getenv("FUSION_VIDEO_WEIGHT", "0.6"))
AUDIO_W = float(os.getenv("FUSION_AUDIO_WEIGHT", "0.4"))

def fuse(video_emotion_label: str, video_conf: float, audio_scores: dict):
    priors = {
        "happy": (0.8, 0.6), "neutral": (0.5, 0.5), "sad": (0.2, 0.3),
        "anger": (0.2, 0.7), "disgust": (0.2, 0.5), "fear": (0.2, 0.8),
        "surprise": (0.6, 0.8),
    }
    v_val, v_aro = priors.get(video_emotion_label, (0.5, 0.5))
    v_val *= video_conf
    v_aro *= video_conf

    a_val = audio_scores.get("valence", 0.5)
    a_aro = audio_scores.get("arousal", 0.5)
    a_str = audio_scores.get("stress", 0.0)

    valence = VIDEO_W * v_val + AUDIO_W * a_val
    arousal = VIDEO_W * v_aro + AUDIO_W * a_aro
    stress = 0.5 * (1 - valence) + 0.5 * arousal
    stress = max(stress, a_str)

    return {
        "stress": float(max(0.0, min(1.0, stress))),
        "valence": float(max(0.0, min(1.0, valence))),
        "arousal": float(max(0.0, min(1.0, arousal))),
        "dominant_emotion": video_emotion_label
    }