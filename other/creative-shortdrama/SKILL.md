---
name: creative-shortdrama
description: Make a Chinese 短劇 (short drama) scene end to end on the local stack — stills in Flow, edge-tts dialogue, Wan 2.1 i2v + InfiniteTalk lip-sync in ComfyUI, and a measured assembly. Use when the user says "make a short drama", "短劇", or "shoot this dialogue scene", or wants to continue or re-run the short-drama capability test. NOT for music videos (use creative-mv-director, which owns MV lip-sync), NOT for a podcast or slideshow, and NOT for driving Flow itself (use tool-flow-stills).
vault_sync: true
---

# 短劇 generator

The stack works. What decides whether a scene is usable is **framing, line
length and shot type** — settled by measurement on 2026-09-20, see
`{vault}/70_Media/shortdrama-captest-20260919/RESULTS.md`.

## The rules that decide the outcome

1. **Dialogue at close-up.** Face height in the rendered 480×832 frame is the
   single strongest predictor of lip-sync quality: 269 px → LSE-C 8.2,
   123 px → 6.8, 83 px → 2.1. Nothing under ~120 px has passed.
2. **Two-handers are shot as singles.** A wide two-shot cannot carry a line.
   The same line, same audio, same seed: **2.119 in the two-shot, 6.417 as a
   close-up single.** The wide two-shot is for silent establishing and
   reaction shots, where it works fine.
3. **Write dialogue beats longer than ~1 second of speech.** Below that no
   lip-sync verdict is possible (see § Measuring), so the shot can only be
   judged by eye.
4. **Action and speech stay in separate shots.** v2v flattens body motion to
   about a third, and the hand-and-prop shot is the weakest part of the stack
   — an insert asking a hand to slide an object across a counter inverted
   itself (it lifted the object away instead). Expect to re-roll or re-stage.
5. **Hold the 180° line in the prompts.** Name the screen side and the eyeline
   per shot ("positioned left of centre, looking toward screen-right"), and
   keep each character on their side for the whole scene.

## Pipeline

### 1. Script and audio first (cheap, and it sizes everything)

Write the scene, then generate each line with `tts_gate.py` (edge-tts +
Whisper round-trip, gate ≥ 0.70). Chinese voices: `zh-CN-YunxiNeural` (m),
`zh-CN-XiaoxiaoNeural` (f). Two traps:

- The gate sends a simplified-script `initial_prompt`; without it Whisper
  answers in 繁體 for some voices and fails lines it heard correctly.
- edge-tts writes **MP3 data** whatever you name the file. Save `.mp3` and
  convert to real PCM with ffmpeg, or the mux later produces noise.

Measure each line's **speech span**, not its file length — the files carry
up to a second of trailing silence, and every later decision uses the span.

### 2. Stills in Google Flow (free)

Follow `tool-flow-stills`. Specifics for drama:

- Generate one **character reference** per role and one **location
  reference**, then attach all three as ingredients to every shot prompt.
- **The aspect ratio resets to 16:9 between sessions.** Set 9:16 before every
  batch, and confirm the settings chip reads `crop_9_16` before submitting.
- **Verify the ingredient count inside the prompt box**, not on the page — the
  previous generation's info panel also shows ingredient thumbnails, and
  counting those once sent a shot with no references at all (it produced two
  strangers; identity scored 0.03–0.26, which is how it was caught).
- Generate ×2 and pick. Check wardrobe and screen direction on every
  candidate; both were the commonest defects.

### 3. Video in ComfyUI

Harness: `{vault}/70_Media/Music/melodic-bass-album-2026-09/02-one-more-hour/lipsync-test-20260916/harness/infinitetalk_workflow.py`.
Always `steps 6 / start_step 0`.

| Shot | Mode |
|---|---|
| Silent (establishing, reaction, action) | `plain` |
| Dialogue, best quality | `i2v` (still + audio) — scored highest at 8.2 |
| Dialogue over an existing take | `plain` source → `v2v` |
| Two speakers in one frame | `multi` — **masks required**, see below |

**A `multi` run needs explicit `ref_target_masks`** (speaker 1, speaker 2,
background). The wrapper's documented left/right default is dead code:
`nodes_sampler.py:586` reads the masks before `multitalk_loop` creates them,
so without them the run dies with `'NoneType' object has no attribute 'max'`.
Even with masks it works only mechanically — prefer singles (rule 2).

**Output is longer than you ask for.** InfiniteTalk pads to whole windows:
65 → 81, 85 → 153, 181 → 225, 261 → 297 frames. The tail carries no audio, so
trim each dialogue shot to its speech span at assembly.

**Memory.** One InfiniteTalk job needs ~30 GB of commit. Run one job at a
time, unload models between jobs (`POST /free`), and abort above ~94% commit —
`run_guarded.py` in the test folder does all three. `block_swap` is not the
lever; the spike is model loading into RAM.

### 4. Measure before believing

- **Lip-sync:** `measure_syncnet.py` (SyncNet LSE-C/LSE-D). Pass = LSE-C ≥ 4.5
  **and** own-line minus a *different-line decoy* ≥ 2.0 **and** |offset| ≤ 6
  frames. **Needs ≥ 1.0 s of speech**: excerpts of a clip scoring 8.6 score
  2.9–5.3 at 0.44 s, so anything shorter is noise and goes to human judgement,
  never recorded as a failure. For reference, real in-sync video measures
  LSE-C 6.8–8.2.
- **Identity:** `measure_identity.py`. Median cosine ≥ 0.45 vs the character
  reference, only for faces ≥ 90 px; cross-character < 0.30. **Always read the
  jaw crop too** — the embedding passed a face wearing a moustache the
  character does not have.
- **By eye:** dense contact sheets, and measure before reporting motion. A
  "jump" seen at 12-frame spacing was refuted by frame-difference and scale
  measurement; sparse sampling exaggerates gradual drift.

### 5. Assemble

`assemble.py` in the test folder is the reference: ffmpeg only, clip pictures
concatenated through the concat *filter*, clean WAVs laid on the timeline (never
the clip's embedded audio), a quiet room-tone bed, and each dialogue shot
trimmed to its speech span. An L-cut is made by cutting the picture early
while the line continues over the next shot — measure the speech end, or the
overlap silently lands in the trailing silence and carries nothing.

## Record every generation

Log each submission to the MV library (`scripts/mv_library.py record-attempt`,
project 短劇) with the prompt, input hashes, verdict and reason, then
`scripts/check_mv_library.py`. An automated metric alone is `unreviewed`, not
`pass`.

## Direct the scene first

This skill renders; it does not design. **`creative-drama-director` finds the
turn, plans coverage and writes per-shot performance direction** — run it
first and render its shot table, or the output is eight clean shots with no
dramatic shape (which is exactly what run 1 produced).

## Cross-references

- `creative-drama-director` — the scene and performance design this executes
- `{vault}/70_Media/shortdrama-captest-20260919/` — spec, results, scripts, cut
- `tool-flow-stills` — the Flow mechanics this leans on
- `creative-mv-generator` — the music-video pipeline; different stack, do not mix
- `{vault}/30_Resources/EmptyOS/kb/notes/lesson-shortdrama-capability-test.md`
