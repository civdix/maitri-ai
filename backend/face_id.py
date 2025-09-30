import face_recognition
import json, os, uuid
import numpy as np

FACE_DB_PATH = os.getenv("FACE_DB_PATH", "data/face_db.json")
os.makedirs(os.path.dirname(FACE_DB_PATH), exist_ok=True)

def _load_db():
    if os.path.exists(FACE_DB_PATH):
        with open(FACE_DB_PATH, "r") as f:
            return json.load(f)
    return {"encodings": [], "ids": [], "names": []}

def _save_db(db):
    with open(FACE_DB_PATH, "w") as f:
        json.dump(db, f)

def enroll_face(image_bgr, name: str):
    rgb = image_bgr[:, :, ::-1]
    boxes = face_recognition.face_locations(rgb, model="hog")
    encs = face_recognition.face_encodings(rgb, boxes)
    if not encs:
        return None, "No face detected"
    enc = encs[0]
    db = _load_db()
    face_id = str(uuid.uuid4())
    db["encodings"].append(enc.tolist())
    db["ids"].append(face_id)
    db["names"].append(name)
    _save_db(db)
    return face_id, None

def recognize_faces(image_bgr, tolerance=0.45):
    rgb = image_bgr[:, :, ::-1]
    boxes = face_recognition.face_locations(rgb, model="hog")
    encs = face_recognition.face_encodings(rgb, boxes)

    db = _load_db()
    known = [np.array(e) for e in db["encodings"]]
    names = db["names"]
    ids = db["ids"]

    results = []
    for box, enc in zip(boxes, encs):
        matches = face_recognition.compare_faces(known, enc, tolerance=tolerance)
        face_id = None
        name = "Unknown"
        if True in matches:
            idx = matches.index(True)
            face_id = ids[idx]
            name = names[idx]
        results.append({"box": box, "face_id": face_id, "name": name})
    return results