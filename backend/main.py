import os
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, JSONResponse
from pydantic import BaseModel
from typing import Dict, Optional
from datetime import datetime
import cv2
from db import init_db, list_astronauts, upsert_astronaut, add_metric, latest_metric, get_astronaut_by_id, add_conversation, add_alert, list_alerts
from schemas import CrewSummary, ChatRequest, EnrollRequest, SpeakRequest, AlertOut
from utils import decode_base64_image, decode_base64_pcm16
from face_id import enroll_face, recognize_faces
from emotion_video import VideoEmotion
from emotion_audio import audio_emotion_from_prosody
from fusion import fuse
from conversation import chat
from tts import synthesize
from stt import STTStream
import base64
import tempfile

HOST = os.getenv("HOST", "0.0.0.0")
PORT = int(os.getenv("PORT", "8000"))
CRIT_THRESH = float(os.getenv("CRITICAL_STRESS_THRESHOLD", "0.8"))
SEED_ROSTER = os.getenv("SEED_ROSTER", "false").lower() == "true"

app = FastAPI(title="Maitri AI")

origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins, allow_credentials=True,
    allow_methods=["*"], allow_headers=["*"])

video_model = None

@app.on_event("startup")
def on_startup():
    init_db()
    global video_model
    video_model = VideoEmotion()
    if SEED_ROSTER:
        try:
            from seed import seed
            seed()
        except Exception as e:
            print("Seed failed:", e)

@app.get("/health")
def health():
    return {"status": "ok", "time": datetime.utcnow().isoformat()}

@app.get("/crew")
def crew():
    out = []
    for a in list_astronauts():
        m = latest_metric(a.id)
        if m:
            out.append(CrewSummary(
                id=a.id, name=a.name, stress=m.stress, valence=m.valence, arousal=m.arousal,
                dominant_emotion=m.dominant_emotion
            ).model_dump())
        else:
            out.append(CrewSummary(
                id=a.id, name=a.name, stress=0.0, valence=0.5, arousal=0.5,
                dominant_emotion="neutral"
            ).model_dump())
    return out

@app.post("/enroll")
def enroll(req: EnrollRequest):
    img = decode_base64_image(req.image_b64)
    face_id, err = enroll_face(img, req.name)
    if err:
        return JSONResponse(status_code=400, content={"error": err})
    a = upsert_astronaut(req.name, face_id, role=req.role)
    return {"astronaut_id": a.id, "face_id": face_id}

@app.get("/alerts", response_model=list[AlertOut])
def alerts():
    items = list_alerts()
    out = []
    for a in items:
        out.append(AlertOut(
            id=a.id, astronaut_id=a.astronaut_id, created_at=a.created_at.isoformat(),
            level=a.level, type=a.type, message=a.message
        ))
    return out

@app.websocket("/ws/stream")
async def stream(ws: WebSocket):
    await ws.accept()
    try:
        while True:
            data = await ws.receive_json()
            mtype = data.get("type")
            if mtype == "video_frame":
                frame = decode_base64_image(data["image_b64"])
                faces = recognize_faces(frame)
                for f in faces:
                    top,right,bottom,left = f["box"]
                    face_crop = frame[top:bottom, left:right]
                    if face_crop.size == 0:
                        continue
                    label, conf, _ = video_model.predict(face_crop)

                    if f["name"] == "Unknown":
                        add_alert(level="critical", type_="identity", message="Unknown person detected near camera", astronaut_id=None)
                        a = upsert_astronaut("Unknown", None)
                    else:
                        a = upsert_astronaut(f["name"], f.get("face_id"))

                    audio_scores = {"arousal": 0.5, "valence": 0.5, "stress": 0.3}
                    fused = fuse(label, conf, audio_scores)
                    add_metric(a.id, fused["stress"], fused["valence"], fused["arousal"], fused["dominant_emotion"])

                    if fused["stress"] >= CRIT_THRESH:
                        add_alert(level="critical", type_="stress",
                                  message=f"High stress detected for {a.name} ({fused['stress']:.2f})",
                                  astronaut_id=a.id)

            elif mtype == "audio_chunk":
                audio = decode_base64_pcm16(data["audio_b64"])
                _scores = audio_emotion_from_prosody(audio, 16000)
            else:
                pass
    except WebSocketDisconnect:
        return

class ChatResp(BaseModel):
    text: str
    audio_b64: Optional[str] = None

@app.post("/chat", response_model=ChatResp)
def chat_api(req: ChatRequest):
    a = get_astronaut_by_id(req.astronaut_id)
    if not a:
        return JSONResponse(status_code=404, content={"error": "Astronaut not found"})
    m = latest_metric(a.id)
    metrics_context = f"Latest stress={m.stress:.2f}, valence={m.valence:.2f}, arousal={m.arousal:.2f}, emotion={m.dominant_emotion}" if m else "No metrics available."
    messages = [
        {"role": "system", "content": "You are a calm, supportive BAS onboard assistant. Keep responses short and practical, encourage breathing, hydration, and safety."},
        {"role": "user", "content": f"Astronaut: {a.name}. Context: {metrics_context}. User said: {req.text}"}
    ]
    ai_text = chat(messages)
    add_conversation(a.id, req.text, ai_text)

    with tempfile.NamedTemporaryFile(suffix=".wav", delete=True) as f:
        out_path = f.name
        synthesize(ai_text, out_path, language=req.language or "en_IN")
        audio_bytes = open(out_path, "rb").read()
    audio_b64 = base64.b64encode(audio_bytes).decode("utf-8")
    return ChatResp(text=ai_text, audio_b64=audio_b64)

@app.post("/speak.wav")
def speak(req: SpeakRequest):
    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as f:
        out = f.name
    synthesize(req.text, out, language=req.language or "en_IN")
    return FileResponse(out, media_type="audio/wav", filename="speech.wav")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host=HOST, port=PORT, reload=False)