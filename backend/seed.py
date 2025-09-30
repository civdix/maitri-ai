from db import upsert_astronaut

ROSTER = [
    ("Shivam Dixit", "Team leader"),
    ("Vrinda Sri Gaur", None),
    ("Priyansh Maheshwari", None),
    ("Kushagra Singh", None),
    ("Anant Pareek", None),
    ("Vishakha", None),
]

def seed():
    for name, role in ROSTER:
        upsert_astronaut(name=name, face_id=None, role=role)