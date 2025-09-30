from pydantic import BaseModel
from typing import Optional, List

class CrewSummary(BaseModel):
    id: int
    name: str
    stress: float
    valence: float
    arousal: float
    dominant_emotion: str

class ChatRequest(BaseModel):
    astronaut_id: int
    text: str
    language: Optional[str] = "en_IN"

class SpeakRequest(BaseModel):
    text: str
    language: Optional[str] = "en_IN"

class EnrollRequest(BaseModel):
    name: str
    image_b64: str
    role: Optional[str] = None

class StreamMessage(BaseModel):
    type: str
    image_b64: Optional[str] = None
    audio_b64: Optional[str] = None
    timestamp: Optional[float] = None

class AlertOut(BaseModel):
    id: int
    astronaut_id: Optional[int] = None
    created_at: str
    level: str
    type: str
    message: str