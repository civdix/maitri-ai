import os, json
from vosk import Model, KaldiRecognizer
import numpy as np

VOSK_MODEL_PATH = os.getenv("VOSK_MODEL_PATH", "models/vosk/en-in")

class STTStream:
    def __init__(self, sample_rate=16000):
        self.model = Model(VOSK_MODEL_PATH)
        self.rec = KaldiRecognizer(self.model, sample_rate)
        self.sample_rate = sample_rate

    def accept_audio(self, audio_int16):
        ok = self.rec.AcceptWaveform(audio_int16.tobytes())
        if ok:
            res = json.loads(self.rec.Result())
            return res.get("text", "")
        else:
            return None

    def final_result(self):
        res = json.loads(self.rec.FinalResult())
        return res.get("text", "")