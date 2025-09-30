import os, subprocess

PIPER_VOICE_PATH_EN = os.getenv("PIPER_VOICE_PATH_EN", "models/piper/en_IN/en_IN-amy-low.onnx")
PIPER_VOICE_CONFIG_EN = os.getenv("PIPER_VOICE_CONFIG_EN", "models/piper/en_IN/en_IN-amy-low.onnx.json")
PIPER_VOICE_PATH_HI = os.getenv("PIPER_VOICE_PATH_HI", "models/piper/hi_IN/hi_IN-anu-low.onnx")
PIPER_VOICE_CONFIG_HI = os.getenv("PIPER_VOICE_CONFIG_HI", "models/piper/hi_IN/hi_IN-anu-low.onnx.json")

def synthesize(text: str, out_wav_path: str, language: str = "en_IN"):
    if language == "hi_IN":
        model = PIPER_VOICE_PATH_HI
        cfg = PIPER_VOICE_CONFIG_HI
    else:
        model = PIPER_VOICE_PATH_EN
        cfg = PIPER_VOICE_CONFIG_EN

    cmd = [
        "piper",
        "--model", model,
        "--config", cfg,
        "--output_file", out_wav_path,
        "--sentence_silence", "0.3",
    ]
    p = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    out, err = p.communicate(input=text, timeout=90)
    if p.returncode != 0:
        raise RuntimeError(f"Piper synthesis failed: {err}")
    return out_wav_path
