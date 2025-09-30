import onnxruntime as ort
import numpy as np
import cv2, os

VIDEO_EMOTION_MODEL_PATH = os.getenv("VIDEO_EMOTION_MODEL_PATH", "models/vision/fer.onnx")
USE_CUDA = os.getenv("USE_CUDA", "false").lower() == "true"

EMO_LABELS = ["neutral", "happy", "sad", "surprise", "anger", "disgust", "fear"]

class VideoEmotion:
    def __init__(self):
        providers = ["CPUExecutionProvider"]
        if USE_CUDA:
            try:
                available = ort.get_available_providers()
                if "CUDAExecutionProvider" in available:
                    providers = ["CUDAExecutionProvider", "CPUExecutionProvider"]
            except Exception:
                pass
        self.session = ort.InferenceSession(VIDEO_EMOTION_MODEL_PATH, providers=providers)
        self.size = (224, 224)

    def predict(self, face_bgr):
        img = cv2.resize(face_bgr, self.size)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        img = img.astype(np.float32) / 255.0
        img = np.transpose(img, (2,0,1))[None, ...]
        inputs = {self.session.get_inputs()[0].name: img}
        out = self.session.run(None, inputs)[0]
        probs = self._softmax(out[0])
        idx = int(np.argmax(probs))
        return EMO_LABELS[idx], float(probs[idx]), probs.tolist()

    @staticmethod
    def _softmax(x):
        e = np.exp(x - np.max(x))
        return e / e.sum()