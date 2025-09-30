from sqlmodel import SQLModel, Session, create_engine, select
from models import Astronaut, Metric, Conversation, Alert
import os

DB_URL = os.getenv("DB_URL", "sqlite:///data/app.db")
engine = create_engine(DB_URL, connect_args={"check_same_thread": False})

def init_db():
    SQLModel.metadata.create_all(engine)

def get_session():
    return Session(engine)

def get_astronaut_by_name(name: str):
    with get_session() as s:
        return s.exec(select(Astronaut).where(Astronaut.name == name)).first()

def get_astronaut_by_id(aid: int):
    with get_session() as s:
        return s.get(Astronaut, aid)

def upsert_astronaut(name: str, face_id: str | None, role: str | None = None):
    with get_session() as s:
        a = s.exec(select(Astronaut).where(Astronaut.name == name)).first()
        if not a:
            a = Astronaut(name=name, face_id=face_id, role=role)
            s.add(a)
        else:
            if face_id:
                a.face_id = face_id
            if role and not a.role:
                a.role = role
        s.commit()
        s.refresh(a)
        return a

def add_metric(aid: int, stress: float, valence: float, arousal: float, dominant_emotion: str, notes: str | None = None):
    with get_session() as s:
        m = Metric(astronaut_id=aid, stress=stress, valence=valence, arousal=arousal, dominant_emotion=dominant_emotion, notes=notes)
        s.add(m)
        s.commit()
        s.refresh(m)
        return m

def add_conversation(aid: int, user_text: str, ai_text: str):
    with get_session() as s:
        c = Conversation(astronaut_id=aid, user_text=user_text, ai_text=ai_text)
        s.add(c)
        s.commit()
        s.refresh(c)
        return c

def latest_metric(aid: int):
    with get_session() as s:
        stmt = select(Metric).where(Metric.astronaut_id == aid).order_by(Metric.timestamp.desc())
        return s.exec(stmt).first()

def list_astronauts():
    with get_session() as s:
        return s.exec(select(Astronaut)).all()

def list_metrics(aid: int, limit: int = 100):
    with get_session() as s:
        stmt = select(Metric).where(Metric.astronaut_id == aid).order_by(Metric.timestamp.desc()).limit(limit)
        return s.exec(stmt).all()

def add_alert(level: str, type_: str, message: str, astronaut_id: int | None = None):
    with get_session() as s:
        a = Alert(level=level, type=type_, message=message, astronaut_id=astronaut_id)
        s.add(a)
        s.commit()
        s.refresh(a)
        return a

def list_alerts(limit: int = 50):
    with get_session() as s:
        stmt = select(Alert).order_by(Alert.created_at.desc()).limit(limit)
        return s.exec(stmt).all()