from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List
from datetime import datetime

class Astronaut(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    role: Optional[str] = None
    face_id: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)

    metrics: List["Metric"] = Relationship(back_populates="astronaut")
    conversations: List["Conversation"] = Relationship(back_populates="astronaut")

class Metric(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    astronaut_id: int = Field(foreign_key="astronaut.id")
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    stress: float
    valence: float
    arousal: float
    dominant_emotion: str
    notes: Optional[str] = None

    astronaut: Optional[Astronaut] = Relationship(back_populates="metrics")

class Conversation(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    astronaut_id: int = Field(foreign_key="astronaut.id")
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    user_text: str
    ai_text: str

    astronaut: Optional[Astronaut] = Relationship(back_populates="conversations")

class Alert(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    astronaut_id: Optional[int] = Field(default=None, foreign_key="astronaut.id")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    level: str  # "critical" | "warning" | "info"
    type: str   # "stress" | "identity" | "system"
    message: str
