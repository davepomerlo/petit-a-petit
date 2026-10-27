#!/usr/bin/env bash
# Downloads the offline speech engine (sherpa-onnx) and two French Piper voices
# into ./.tts so scripts/make_audio.py can generate the lesson audio.
# Everything comes from GitHub releases; no account or API key needed.
set -euo pipefail

VERSION="1.12.15"
DEST="${TTS_DIR:-.tts}"
BASE="https://github.com/k2-fsa/sherpa-onnx/releases/download"

mkdir -p "$DEST"
cd "$DEST"

if [ ! -d "sherpa-onnx-v${VERSION}-linux-x64-shared" ]; then
  curl -sSL -o engine.tar.bz2 "$BASE/v${VERSION}/sherpa-onnx-v${VERSION}-linux-x64-shared.tar.bz2"
  tar xjf engine.tar.bz2 && rm engine.tar.bz2
fi

# siwis: female voice, CC BY 4.0. upmc: speaker "pierre" (male), CC BY-SA 4.0.
for voice in fr_FR-siwis-medium fr_FR-upmc-medium; do
  if [ ! -d "vits-piper-${voice}" ]; then
    curl -sSL -o voice.tar.bz2 "$BASE/tts-models/vits-piper-${voice}.tar.bz2"
    tar xjf voice.tar.bz2 && rm voice.tar.bz2
  fi
done

echo "TTS ready in $(pwd)"
