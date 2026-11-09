---
name: audio-stems
description: >-
  Generate and place a video/animation's audio as SEPARATE stems — voiceover, background music,
  and a time-synced sound-effects track — and optionally a ducked master mix. Use when adding
  music and SFX to an animation or explainer, when iterating on audio WITHOUT re-rendering the
  video, when you need whooshes/clicks/typing/risers placed on exact timeline moments, or when
  the user wants the music/SFX/VO delivered as separate files. Generates music + SFX via
  ElevenLabs and mixes with sidechain ducking. Triggers: "add music and sound effects", "give
  me the stems separately", "place a whoosh on each transition", "typing/generating sounds",
  "background music track", "ducked mix so the voice leads", "SFX synced to the animation".
---

# Audio Stems

Produce a piece's audio as **independent stems** — `voiceover.mp3`, `music.mp3`, `sfx.mp3` — placed on a known timeline, plus an optional ducked `master.mp3`. Delivering stems separately lets you (or the user) iterate on audio **without touching the rendered video**, and drop tracks onto any editor.

## Generate (ElevenLabs — `scripts/elevenlabs.py`)
- **Music bed:** `python3 scripts/elevenlabs.py music "upbeat but understated corporate tech, instrumental, ~120 BPM" music.mp3 --ms 150000`  (caps ~150s; for longer, `acrossfade`-loop). Keep it understated so VO leads.
- **SFX palette:** `python3 scripts/elevenlabs.py sfx "soft cinematic whoosh" sfx_clips/whoosh.mp3 --seconds 0.9` — build a small palette (e.g. `whoosh/swish`, `pop`, `type`, `generate`, `shimmer`, `ding`, `logo`, `crack`). Min duration 0.5s. **Always check level** (`ffmpeg -af volumedetect`); regenerate if `max < -30 dB` (ElevenLabs occasionally returns near-silent clips).
- **Voiceover:** see the `vo-sync` skill (`elevenlabs.py tts` with word timestamps).

## Place SFX on the timeline (`scripts/build_sfx.py`)
Write an events file `{ "total": <sec>, "events": [ {"t":12.34,"clip":"whoosh","gain":0.6}, … ] }` (one silent base + each clip delayed to its time), then:
```bash
python3 scripts/build_sfx.py sfx_events.json sfx_clips sfx.mp3
```
Place events at **known choreography moments** — derive them from a scene model or from `vo-sync`'s `timing.json` (`t = scene.start + cue.at`) so a sound lands exactly on the spoken word / the card raise. Same tool builds the VO track if you put per-scene clips in a folder named by id.

## Tasteful placement (learned defaults)
- One **transition** sound (swish/whoosh) per push/scene-change; a softer/low one is less fatiguing than a bright hissy whoosh — offer a few options and let the user pick.
- **pop** on each card raise; **type** while text types, **generate** during a "processing/generating" beat; **shimmer** on a decrypt/sparkle; **ding** on success; **logo** sting on intro/outro; **crack** synced to a fracture.
- Keep per-interaction SFX **quiet** (gains ~0.3–0.5); the SFX track should be mostly silence.
- Don't put events in the 0→first-motion intro; verify every `t ≤ total`.

## Mix (optional master — `scripts/mix.sh`)
```bash
./scripts/mix.sh music.mp3 voiceover.mp3 sfx.mp3 master.mp3
```
Side-chains the music **under** the voiceover (ducks when the voice is present), sums VO + SFX, and limits. Pad/trim every stem to the exact timeline length first (`afade`/`apad`). Target mean ≈ −20 dB, peak < −1 dB.

## Deliver
Hand over the **stems separately** by default (`voiceover.mp3`, `music.mp3`, `sfx.mp3`) — only mux into the video when the user confirms. To mux onto a silent render: `ffmpeg -i video.mp4 -i master.mp3 -c:v copy -c:a aac -b:a 192k -shortest out.mp4`.
