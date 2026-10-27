# Petit à petit

フランス語 はじめの一歩 — a French starter app for Japanese speakers at beginner level.
Skills are taught in this order: **reading → speaking → listening → writing**.

The interface switches between Japanese and English (English mode keeps the Japanese underneath).

## What's in it

Five lessons, each with phrase cards, pronunciation tips written for Japanese speakers, a short dialogue and four practice modes:

| Mode | What you do |
|---|---|
| 読む Read | Flip phrase cards, then a quiz: French → meaning, plus questions on the dialogue |
| 話す Speak | Hear a phrase, say it; the phone's speech recognition checks each word |
| 聞く Listen | Audio only: pick what you heard, or what it means |
| 書く Write | Arrange word tiles into a sentence, or type short phrases (accent keys included) |
| まとめ練習 Mixed | 10 questions across all four, weighted toward reading |

Weak phrases come up more often. Progress is saved on the device.

Lessons: 1 あいさつ Greetings · 2 自己紹介 Introductions · 3 数字 Numbers 1–10 · 4 カフェで At the café · 5 道をたずねる Asking the way

## Files

```
index.html               the whole app (no build step)
content/lessons.json     all lesson content — edit this to add lessons
audio/                   one MP3 per phrase and dialogue line
scripts/setup_tts.sh     downloads the offline French voices
scripts/make_audio.py    makes MP3s for any line that doesn't have one yet
sw.js, manifest.webmanifest, icons/   offline support + installable app
.github/workflows/       audio.yml regenerates audio; pages.yml publishes the app
```

## Put it online (GitHub Pages)

1. Create a repo `petit-a-petit` on GitHub and upload these files (keep the folders).
2. Repo **Settings → Pages → Source: GitHub Actions**.
3. Repo **Settings → Actions → General → Workflow permissions: Read and write**.
4. Push to `main`. The app appears at `https://davepomerlo.github.io/petit-a-petit/`.
5. On Android, open that link in Chrome → ⋮ menu → **Add to Home screen** / **Install app**.

Speech recognition needs Chrome on Android (or desktop Chrome) and microphone permission.
Without it, speaking practice falls back to listen-repeat-and-self-check.

## Adding a lesson

Add an entry to `content/lessons.json` (copy an existing one; give each phrase and line a new `id`).
Push, and the **Generate lesson audio** workflow makes the new MP3s and commits them.
Then bump `VERSION` in `sw.js` so installed phones refresh their offline copy.

To make audio on your own Linux/WSL machine instead:

```
bash scripts/setup_tts.sh
python3 scripts/make_audio.py          # only missing clips
python3 scripts/make_audio.py --force  # rebuild all
```

Phrases use a female voice by default; add `"v": "m"` to a phrase for the male voice.
Dialogue lines set `"v"` per speaker.

## Audio credits

Synthetic voices generated offline with [sherpa-onnx](https://github.com/k2-fsa/sherpa-onnx) and Piper models:
`fr_FR-siwis-medium` (CC BY 4.0) and `fr_FR-upmc-medium`, speaker *pierre* (CC BY-SA 4.0).
They are clear and consistent but synthetic — swap in native-speaker recordings later by dropping MP3s with the same file names into `audio/`.

## Next step: Android app

The plan is web app first, Android wrapper later (a Trusted Web Activity or Capacitor build from the same `index.html`).
