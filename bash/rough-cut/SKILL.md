---
name: rough-cut
description: >
  Step 2 of the content pipeline, and the default entry point for "rough
  cut this" / "cut this clip" / "give me a rough cut". Transcribes the
  raw footage once with WhisperX, kills filler words and dead air,
  measures real cut boundaries against the audio (never trusts transcript
  timestamps), snaps everything to the video frame grid, and produces
  BOTH the cut list and the canonical transcript. Default finish hands
  off to an editing app (Premiere/CapCut) as trimmable edit points in
  seconds — it does NOT render a flattened video unless the job is
  headed for a full HyperFrames graphics build.
---

# Rough cut

This is the one slow step in the pipeline (transcription). Everything
else here and downstream is fast. Time-to-timeline is the metric — don't
render a flattened video by default; hand off a cut list instead.

If `projects/<job>/` doesn't exist yet or `raw/` is empty, run
`/intake` first.

## 1. Transcribe once

```bash
uv run .claude/skills/rough-cut/scripts/transcribe.py <job-name>
```

Writes `projects/<job>/transcript/words.json` — WhisperX large-v3,
word-level alignment. **This file is written once and never touched
again.** The script refuses to overwrite it if it already exists. If a
word is misspelled, that's a job for `transcript/corrections.json`
(single whole-word swaps, text only), not a re-transcribe — see step 3.

## 2. Build the cut list

```bash
uv run .claude/skills/rough-cut/scripts/build_cutlist.py <job-name>
```

This is where the two hardest locks in this pipeline live, both already
implemented in `lib/`:

- **Filler/dead-air detection** (`lib/filler_detect.py`) works off the
  transcript's own timestamps to find *candidate* cut spans — filler
  words (um, uh, erm...) and pauses longer than 0.7s (trimmed to a
  natural 0.2s beat, not butted together).
- **Boundary measurement** (`lib/audio_boundaries.py`) then throws the
  transcript timestamps away for anything that will actually become a
  cut, and re-measures the real acoustic edge from an RMS envelope of
  the raw audio — word starts in WhisperX output run 50-100ms late
  versus the real attack. Each measured edge is padded slightly outward
  into silence, then snapped to the video frame grid, so every kept
  segment's video and audio duration match exactly (no drift in concat
  later).

Writes `projects/<job>/cutlist.json`. Read the printed kept/dropped
summary — if it dropped far more or less than expected, look at
`cutlist.json` directly before trusting it.

## 3. Write the canonical transcript

If `transcript/corrections.json` needs entries (misspellings WhisperX
made), add them now — single-token whole-word swaps only, e.g.:

```json
{ "corrections": [ { "from": "teh", "to": "the" }, { "from": "gonna", "to": "going to" } ] }
```

Then:

```bash
uv run .claude/skills/rough-cut/scripts/write_canonical_transcript.py <job-name>
```

Writes `projects/<job>/outputs/.transcript.json` — corrected text,
remapped onto the OUTPUT timeline (post-cut). **Every downstream
consumer** (captions, the editing-app handoff, second-pass review) reads
this file and only this file. Nothing downstream ever goes back to
`words.json` or re-transcribes.

## 4. Default finish: hand off to the editing app

```
/editing-handoff <job-name>
```

This replays `cutlist.json` against the raw footage as individually
trimmable edit points in Premiere or CapCut — not a flattened render.
This is the default finish for "rough cut this." Stop here unless the
job is explicitly going to a full graphics build.

## 5. Only if this job is going to a full HyperFrames render

Skip step 4 (or do it in parallel for review) and instead assemble the
flattened, polish-passed rough cut that graphics render on top of:

```bash
bash .claude/skills/rough-cut/scripts/assemble_rough_cut.sh <job-name>
```

This runs the other two hard locks:

- **One lossless filtergraph** (`lib/build_filtergraph.py`): video is
  hard-cut at frame-snapped boundaries and concatenated with no
  crossfade; audio is trimmed with a small handle of *real* room tone
  borrowed from just outside each kept boundary and joined with short
  equal-power `acrossfade`s — never a fade to zero, which trades a click
  for an audible hole. The crossfade math is symmetric so the audio
  timeline still totals exactly the same length as the video timeline.
- **One audio polish pass** (`lib/polish_audio.sh`): static +10dB gain,
  then a -6dBFS limiter, then AAC 256k. Never dynamic loudnorm (it
  pumps), never per-segment FX. Any later re-encode of this audio must
  match or exceed 256k.
- **Mandatory QA** (`lib/audio_qa.py`) runs automatically and prints
  warnings for joint clicks, silence gaps, and limiter pressure — it
  never silently passes. Read its output even on exit 0.

Writes `projects/<job>/outputs/.roughcut.mp4` — the base video the
graphics-plan skill builds on top of.

Continue to `/graphics-plan`.
