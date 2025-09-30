# Maitri AI — BAS Crew Well‑being Multimodal Assistant (Offline‑First, GPU‑aware)

A multimodal, on-board AI assistant for astronauts’ emotional and physical well-being using audio-video inputs. Detects crew emotional/mental state, offers short supportive counseling, speaks in Indian English or Hindi, and raises critical alerts.

Core modules
1) Input Module (mic + camera)
   - Person-aware: face detection + recognition, per-person identity
   - Video emotion (ONNXRuntime; GPU optional via CUDA)
   - Audio prosody cues (heuristic baseline; pluggable ONNX model later)
   - Multimodal fusion for robust stress/affect estimates
2) On-board Speaking AI
   - Offline STT: Vosk
   - Local LLM: Ollama (llama3.2:3b by default)
   - Offline TTS: Piper with Indian English and Hindi voices
   - 3D avatar with Three.js (humanoid GLB, simple lip-sync via WebAudio amplitude)
3) Dashboard
   - Crew overview: stress, valence, arousal, dominant emotion
   - Alerts: critical/warning events including “Unknown” identity detections
   - Per-person KPI and chat panel for counseling and monitoring
   - “Unknown” → Assign Identity flow: capture a frame and enroll a name

Offline-first, GPU-optional
- Runs fully offline by default (Vosk, Piper, ONNX, Ollama)
- GPU (CUDA) acceleration for ONNX if available; falls back to CPU

Pre-seeded roster
- Shivam Dixit (Team leader), Vrinda Sri Gaur, Priyansh Maheshwari, Kushagra Singh, Anant Pareek, Vishakha

AWS credentials (where to add)
- Preferred: attach an IAM Role to EC2 (Instance Profile). No static creds needed.
- Static creds (demo only, not recommended long term):
  - Set on the EC2 host environment (survive restarts):
    - echo "AWS_ACCESS_KEY_ID=..." | sudo tee -a /etc/environment
    - echo "AWS_SECRET_ACCESS_KEY=..." | sudo tee -a /etc/environment
    - echo "AWS_DEFAULT_REGION=ap-south-1" | sudo tee -a /etc/environment
    - sudo reboot
  - Or put in the server’s .env (read by docker compose):
    - AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_DEFAULT_REGION, S3_LOG_BUCKET (optional)
- Optional: Use SSM Parameter Store and the provided cloud-init to fetch a secure .env.

Assign Identity workflow
- Alerts panel shows “Unknown person detected near camera” as Critical.
- Click “Assign identity” to open a webcam modal.
- Capture a frame, enter name and optional role, click Enroll — this calls POST /enroll to store face encoding and create the astronaut entry.
- After enrolling, the next detections should recognize by face.

Quick Start
1) Copy .env.example to .env and adjust.
2) Download models:
   - bash backend/scripts/download_models.sh
   - Place a FER ONNX at backend/models/vision/fer.onnx (see notes inside the script).
3) Run:
   - docker compose up --build
4) Frontend: http://localhost:5173
   Backend: http://localhost:8000/docs

GPU on AWS
- Start with g4dn.xlarge (NVIDIA T4) to control costs; g5.xlarge (A10G) for more performance.
- Install NVIDIA Driver + NVIDIA Container Toolkit (cloud-init provided).
- Switch backend to onnxruntime-gpu by building with backend/requirements-gpu.txt and enabling `USE_CUDA=true` in .env.

3D Avatar model
- Put a humanoid GLB at frontend/public/models/avatar.glb (with jaw/mouth morph target if possible). Free sources: Ready Player Me, Mixamo.

Safety
- Supportive suggestions and alerts only — not medical diagnoses. Validate with domain experts. Keep all data on-device or on secure AWS resources with least privilege.

License
- MIT for scaffold. Check licenses of model downloads (Vosk models, Piper voices, FER ONNX).