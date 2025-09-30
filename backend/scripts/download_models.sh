#!/usr/bin/env bash
set -euo pipefail

mkdir -p models/vosk/en-in
mkdir -p models/piper/en_IN
mkdir -p models/piper/hi_IN
mkdir -p models/vision

echo "Downloading Vosk en-IN (small)..."
cd models/vosk/en-in
if [ ! -f .downloaded ]; then
  curl -L -o vosk-en-in.zip https://alphacephei.com/vosk/models/vosk-model-small-en-in-0.4.zip
  unzip -q vosk-en-in.zip
  mv vosk-model-small-en-in-0.4/* .
  rmdir vosk-model-small-en-in-0.4 || true
  rm -f vosk-en-in.zip
  touch .downloaded
fi
cd ../../..

echo "Downloading Piper voices..."
if [ ! -f models/piper/en_IN/en_IN-amy-low.onnx ]; then
  curl -L -o models/piper/en_IN/en_IN-amy-low.onnx https://huggingface.co/rhasspy/piper-voices/resolve/main/en/en_IN/amy/en_IN-amy-low.onnx
  curl -L -o models/piper/en_IN/en_IN-amy-low.onnx.json https://huggingface.co/rhasspy/piper-voices/resolve/main/en/en_IN/amy/en_IN-amy-low.onnx.json
fi
if [ ! -f models/piper/hi_IN/hi_IN-anu-low.onnx ]; then
  curl -L -o models/piper/hi_IN/hi_IN-anu-low.onnx https://huggingface.co/rhasspy/piper-voices/resolve/main/hi/hi_IN/anu/hi_IN-anu-low.onnx
  curl -L -o models/piper/hi_IN/hi_IN-anu-low.onnx.json https://huggingface.co/rhasspy/piper-voices/resolve/main/hi/hi_IN/anu/hi_IN-anu-low.onnx.json
fi

echo "Facial emotion model (placeholder)..."
if [ ! -f models/vision/fer.onnx ]; then
  echo "Please place your FER ONNX at models/vision/fer.onnx"
fi

echo "Done."
