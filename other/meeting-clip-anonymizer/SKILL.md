---
name: meeting-clip-anonymizer
description: Turn a recorded call into branded short clips while anonymizing the other participant (voice pitch-shifted, face hidden, PII bleeped). Use when repurposing Zoom/Meet/Fathom calls into YouTube/Shorts.
---

# Meeting Clip Anonymizer

Repurpose a recorded call into polished clips **without exposing the other person**: their voice is
pitch-shifted (anonymized), their face is replaced by a branded card whenever they're on screen, and
names/figures are bleeped.

## When to use
- Repurposing coaching/sales/podcast calls into content where only YOU are the public face.
- Any time you need a participant's *words* but must protect their *identity*.

## The capabilities (in order of reusability)
1. **`voice_anonymize.py` (standalone, start here):** deepen a speaker's voice on given intervals.
   Pure ffmpeg, duration-preserving, instant. `python voice_anonymize.py in.mp4 out.mp4 --intervals 0:9,41:48 --pitch 0.82`
2. **Full pipeline (`pipeline/`):** silence-removal + face-hiding (branded bullet cards) + voice-anon +
   PII bleep + branded captions/circles/cards/music/zoom + cloud render.

## Workflow (agent steps)
1. **Transcribe** the recording to word-level timestamps (`{words:[{word,start,end}]}`) — e.g. OpenAI
   whisper-1. Save as `transcript.json`.
2. **Decide the clips:** read the transcript, pick self-contained advice moments (start/end). Propose to
   the user for approval BEFORE rendering. Author each clip's editing **to match the transcript** —
   circle the KEY phrases as they're spoken, drop a card on each real takeaway. Do NOT sprinkle circles
   on a timer; that looks generic. ~1 meaningful animation per 5-7s.
3. **Find the other person's speech intervals** (to anonymize): prefer **speaker-view detection** (the
   on-screen tile = who's talking; `classify_speakers.py` template-matches the name label). Diarization
   (pyannote) is a fallback but UNRELIABLE for two similar same-mic voices.
4. **List PII** (names, locations, $ figures) and get the user's approval, then bleep (audio mute +
   caption mask).
5. **Run** `pipeline/render_clip.sh <clip>` (cloud) or stop after the base cut and edit elsewhere.
6. **Deliver** the clip + a set of YouTube title options.

## Editing rules that matter (learned in production)
- Captions (running subtitles) go ONLY over the other person's question / B-roll — never over your face.
  Your answer is told with circled phrases + cards.
- Cards/circles only over YOUR face; never two text elements on screen at once; never an overlay card on
  top of the face-hiding branded card.
- Voice: pitch < 1.0 (DEEPER, ~0.82), not higher. Shift on substantial spans where the other person is
  the active tile (>=0.8s); don't shift sub-second flicker tails (that's your voice).
- Silence: cut hesitations/dead air; when merging adjacent segments, ONLY merge if truly adjacent —
  merging across a cut gap re-fills the silence (a real bug we hit).
- Zoom: ONE gentle continuous drift per shot (e.g. 1.0->1.045), never pulsing in/out.
- Run heavy assembly on a server, not the user's laptop (it pegs CPU).

## Privacy
Always have consent to record and publish. Anonymization reduces but doesn't eliminate identifiability
(story details, word choice). Redact specifics and get sign-off before publishing.
