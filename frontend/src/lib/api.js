const BASE = import.meta.env.VITE_BACKEND_URL || 'http://localhost:8000';

export async function getCrew() {
  const r = await fetch(`${BASE}/crew`);
  return r.json();
}

export async function enroll(name, image_b64, role) {
  const r = await fetch(`${BASE}/enroll`, {
    method: 'POST',
    headers: {'Content-Type':'application/json'},
    body: JSON.stringify({name, image_b64, role})
  });
  return r.json();
}

export async function chat(astronaut_id, text, language = 'en_IN') {
  const r = await fetch(`${BASE}/chat`, {
    method: 'POST',
    headers: {'Content-Type':'application/json'},
    body: JSON.stringify({astronaut_id, text, language})
  });
  return r.json();
}