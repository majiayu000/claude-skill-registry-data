---
name: vo-sync
description: >-
  Sync an animation, captions, or cues to a voiceover so visuals land on the spoken words, and
  pace the timeline tightly to the narration (no dead air). Use when you have (or will generate)
  a voiceover and want cards/elements/captions to appear exactly when they're mentioned, when
  card raises feel out of sync with the narration, or when there are long voice-less gaps to
  tighten. Generates VO with word-level timestamps (ElevenLabs) and computes per-scene durations
  + cue times from them. Triggers: "sync the voiceover with the animation", "make the cards
  appear when the voice says it", "the VO is out of sync", "tighten the pacing / remove silent
  gaps", "land captions on the spoken word", "word-timestamp sync".
---

# VO Sync

Make the visuals follow the voice: each cue (a card raising, a caption, a sound) lands **on the word that names it**, and each scene lasts about as long as its narration — so the piece is **tight** with no silent stretches.

## How it works
1. **Write VO that names things in appear-order**, then generate it **with word timestamps**:
   `python3 scripts/elevenlabs.py tts script.json vo --voice <id>` → clips + `vo/durations.json` + `vo/alignments.json` (per-character start times). (`script.json` = `[{"id":"scene1","text":"…"}, …]`.)
2. **Compute timing:** edit the `CONFIG` (scene order + cue→keyword) in `scripts/compute_timing.js` and run it → `timing.json` = `{ total, head, scenes:[{id,start,dur,cues:[{key,at}]}] }`. `dur` follows the VO length; `at` is `head + word time`.
3. **Feed your engine** `timing.json` (read it at boot via a `timing.js` `window.__TIMING=…`, or `fetch`): use `dur` for scene length and `at` for when each cue fires.
4. **Build audio to the same timeline** so SFX hit on the words (see the `audio-stems` skill: place each event at `scene.start + at`).

## Key moves
- **VO-driven durations** (`dur = head + voLen + tail`, clamped to fit the last cue/animation) → continuous narration, no dead air.
- **Anchor on words**: a word spoken `w` seconds into a clip → cue `at = head + w`.
- **Spread** when you can't name every item: anchor named ones, interpolate the rest between anchors.
- **Snap-to-instant**: to make a whole list turn green the moment the VO says "auto-mapped," set those cues to the trigger word + tiny increments.
- Recompute + rebuild audio freely (cheap); only **re-render the video once the visuals are locked** — a one-word VO change shifts every downstream scene start.

See `reference/VO_SYNC.md` for the full workflow, the `alignments.json` lookup, lead/hero timing, and gotchas (spelled-out acronyms, regeneration). Other providers: any TTS works if you can get word/segment times; without timestamps, estimate `at` from word counts.
