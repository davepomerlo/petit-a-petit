#!/usr/bin/env python3
"""Generate an MP3 for every phrase and dialogue line in content/lessons.json.

Only missing files are made, so editing a lesson regenerates just the new lines.
Pass --force to rebuild everything. Run scripts/setup_tts.sh first.

Voices (both offline Piper voices):
  f = siwis (female, CC BY 4.0)
  m = upmc speaker "pierre" (male, CC BY-SA 4.0)
"""
import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TTS = Path(os.environ.get("TTS_DIR", ROOT / ".tts"))
ENGINE = next(TTS.glob("sherpa-onnx-v*-linux-x64-shared"), None)
OUT = ROOT / "audio"

# length_scale > 1 slows speech a little: clearer for beginners.
VOICES = {
    "f": {"dir": "vits-piper-fr_FR-siwis-medium", "model": "fr_FR-siwis-medium.onnx", "sid": 0},
    "m": {"dir": "vits-piper-fr_FR-upmc-medium", "model": "fr_FR-upmc-medium.onnx", "sid": 1},
}
LENGTH_SCALE = "1.12"


def items():
    data = json.loads((ROOT / "content" / "lessons.json").read_text(encoding="utf-8"))
    for lesson in data["lessons"]:
        for p in lesson["phrases"]:
            yield p["id"], p["fr"], p.get("v", "f")
        for line in lesson["dialogue"]["lines"]:
            yield line["id"], line["fr"], line.get("v", "f")


def speak(text, voice, dest):
    v = VOICES[voice]
    vdir = TTS / v["dir"]
    env = dict(os.environ, LD_LIBRARY_PATH=str(ENGINE / "lib"))
    with tempfile.TemporaryDirectory() as tmp:
        wav = Path(tmp) / "out.wav"
        subprocess.run(
            [
                str(ENGINE / "bin" / "sherpa-onnx-offline-tts"),
                f"--vits-model={vdir / v['model']}",
                f"--vits-tokens={vdir / 'tokens.txt'}",
                f"--vits-data-dir={vdir / 'espeak-ng-data'}",
                f"--vits-length-scale={LENGTH_SCALE}",
                f"--sid={v['sid']}",
                f"--output-filename={wav}",
                text,
            ],
            check=True, env=env, capture_output=True,
        )
        # Mono 64 kbps MP3, loudness-matched, with a short lead-in so phones don't clip the start.
        subprocess.run(
            [
                "ffmpeg", "-y", "-loglevel", "error", "-i", str(wav),
                "-af", "adelay=120,loudnorm=I=-18:TP=-2,apad=pad_dur=0.15",
                "-ac", "1", "-ar", "24000", "-b:a", "64k", str(dest),
            ],
            check=True,
        )


def main():
    if ENGINE is None:
        sys.exit("Speech engine not found. Run scripts/setup_tts.sh first.")
    force = "--force" in sys.argv
    OUT.mkdir(exist_ok=True)
    made = 0
    for clip_id, text, voice in items():
        dest = OUT / f"{clip_id}.mp3"
        if dest.exists() and not force:
            continue
        speak(text, voice, dest)
        made += 1
        print(f"  {clip_id}  [{voice}]  {text}")
    print(f"{made} clip(s) generated.")


if __name__ == "__main__":
    main()
