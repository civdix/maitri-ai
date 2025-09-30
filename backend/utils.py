import base64, numpy as np, cv2

def decode_base64_image(b64: str):
    raw = base64.b64decode(b64)
    img_array = np.frombuffer(raw, dtype=np.uint8)
    frame = cv2.imdecode(img_array, cv2.IMREAD_COLOR)
    return frame

def decode_base64_pcm16(b64: str):
    raw = base64.b64decode(b64)
    audio = np.frombuffer(raw, dtype=np.int16)
    return audio