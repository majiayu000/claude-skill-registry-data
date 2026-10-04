---
name: voiceover
description: Generate, audition, regenerate or fix narration audio for a paper video from narration.json (stage 4 of paper-to-video). Use for text-to-speech, changing voice or pace, mispronunciations, clips flagged LOW, or adding a voice-over on top of an existing video.
---

# Voice-over

```bash
uv run scripts/generate_voice.py P                         # all segments; unchanged ones are skipped
uv run scripts/generate_voice.py P --only 03-method,07-results
uv run scripts/generate_voice.py P --force                 # regenerate all
uv run scripts/generate_voice.py P --audition Charon,Puck,Kore,Fenrir --only 01-title   # -> audio/audition/
uv run scripts/generate_voice.py P --provider say          # free offline draft (macOS)
uv run scripts/generate_voice.py P --provider silent       # silence of estimated length, for timing only
```

Output: `P/audio/<id>.wav` (24 kHz mono) and `<id>.json` (text hash, voice, duration, similarity).
A clip is regenerated automatically when its text, voice, model, style or provider changes.

## Providers (`tts.provider` in narration.json, or `--provider`)

| provider | needs | notes |
|---|---|---|
| `openrouter` | `OPENROUTER_API_KEY` in `.env` | default; model `google/gemini-3.1-flash-tts-preview`, voices such as Charon, Puck, Kore, Fenrir, Aoede |
| `gemini` | `GEMINI_API_KEY` | Google AI Studio directly; same voices |
| `say` | macOS | robotic but free; good for timing drafts |
| `silent` | nothing | ~2.6 words/s of silence |

`.env` is looked up in the project folder, the current folder, then the repo root. Never print or commit keys.

## Pace and style

`tts.style` is a natural-language instruction prepended to every text. Gemini TTS follows it and does
not speak it; other models may read it aloud, and the transcription check will catch that. Per-segment
overrides: `{"id": "...", "text": "...", "tts": {"voice": "Puck"}}`.

## Verification

With `verify.model` set and an OpenRouter key, each clip is transcribed back and compared word for word
with the script; below `min_similarity` it retries up to `retries` times and keeps the best take. Clips
still below the threshold are listed under NEEDS ATTENTION with what was heard. Fixes: rephrase the
sentence, spell a term the way it sounds, or split long sentences. Rewording usually works best. Listen to flagged clips before accepting them.

## Voice-over on an existing video

Either add a narration segment to `narration.json` and reference its id from a clip item in
`timeline.json` (`"narration": "<id>"`, see the video-editing skill), or do it directly:
```bash
uv run scripts/videotools.py dub in.mp4 P/audio/04-demo.wav out.mp4 --offset 1.0 --duck 0.2
```
The original audio drops to `--duck` (0.2 = 20 %) while the voice speaks; the last frame is held if the
voice outlasts the video (`--no-extend` to cut instead).
