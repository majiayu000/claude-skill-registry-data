---
name: captions
description: >
  Step 5 of the content pipeline, short-form only. Adds captions built
  from the canonical transcript — never a fresh transcription — using
  the embedded-captions vendor skill for the actual rendering/style
  work. Use once a short-form (9:16) job has its graphics rendered (or
  at least a rough cut) and needs burned-in captions.
---

# Captions

Short-form only. Long-form (16:9) jobs don't get burned-in captions in
this pipeline.

LOCK: captions are built from `outputs/.transcript.json` — the
canonical, cut-remapped, corrections-applied transcript — and **never**
by re-transcribing. The embedded-captions vendor skill normally runs
its own WhisperX pass; this skill's whole job is to feed it our already-
correct transcript instead and confirm it actually skipped its own.

## 1. Bridge the canonical transcript into embedded-captions' project shape

```bash
uv run .claude/skills/captions/scripts/prepare_captions_project.py <job-name> [--language en]
```

This creates `projects/<job>/captions/` with:
- `source.mp4` — a copy of the latest render (`outputs/<job>-graphics.mp4`
  if graphics are done, else `outputs/.roughcut.mp4`)
- `transcript.json` — `outputs/.transcript.json` converted into
  embedded-captions' exact normalized schema
  (`{"words":[{"text","start","end","type":"word"}], "language_code"}`).

If this job's audio isn't English, pass `--language <code>` — the
default is `en`.

## 2. Run embedded-captions against `projects/<job>/captions/`

Follow `/embedded-captions` from here, using `projects/<job>/captions/`
as its project directory. Its own `scripts/prepare.sh` runs matting,
transcription, and audio-envelope in parallel — **watch its log for the
transcription step and confirm it reports finding an existing
`transcript.json` and skips re-running Whisper.** If it re-transcribes
anyway (schema drift, a version bump changed its expectations), STOP —
do not let it overwrite anything in this pipeline's `transcript/` or
`outputs/.transcript.json`, and fix `prepare_captions_project.py`'s
output schema instead of accepting a fresh transcription.

Pick the caption identity/style per the user's ask — the quiet `anchor`
rail is the default; only go fully cinematic (embedding words behind the
subject) if the user explicitly wants that treatment.

## 3. Safe zones still apply

Whatever embedded-captions produces, the burned-in captions must land
inside y 200–1620 on the 1080x1920 canvas — no key visuals (including
caption text) in the top 200px or bottom 300px.

## 4. Bring the captioned output back into this job

Copy embedded-captions' finished render into
`projects/<job>/outputs/<job>-captioned.mp4`. Continue to `/music`
(optional) or straight to `/export`.
