---
name: edl-edit
version: 1.0.0
description: Build a multi-clip edit as an auditable JSON "edit decision list" (EDL) — a list of clips with source/in/out and a written rationale per pick — that one command renders to a finished video. Use whenever you're stitching several cuts/takes/segments into one video and want the edit to be reviewable, diffable, and re-runnable instead of a throwaway ffmpeg filtergraph. Covers the schema, the rationale discipline, multicam cutaways, and verifying the output by re-transcribing it.
---

# The edit is a JSON file

Don't hand-author a one-off `filter_complex` for a multi-cut edit and throw it away. Write the
edit as **`edit.json`** — a list of clips with `src`, `start`, `end`, and a written
`rationale` — and let one command execute it:

```bash
uv run video-agent edl edit.json -o out.mp4
```

Why: the edit becomes **text you can read, diff, and re-render**. A revision is "change two
numbers and re-run," not "reconstruct the filtergraph." The `rationale` field forces you to
write down *why* each cut was made (which take won, why the others lost, why the cut point
sits where it does) — better decisions and an inspectable trail for the user.

## Schema

```jsonc
{
  "fps": 60, "width": 1920, "height": 1080,        // optional (these are the defaults)
  "grade": "luts/warm.png",                         // optional LUT for the whole cut (.cube or HALD .png)
  "audio_fix": "loudnorm=I=-14:TP=-1.5:LRA=11",     // optional filter chain on the speech bus
  "seam_fade": 0.015,                               // optional; click-killing fade at each cut
  "music": { "src": "inputs/bed.mp3", "gain_db": -18, "duck": true,
             "start": 0.0, "fade_in": 0.5, "fade_out": 2.0 },   // optional music bed
  "clips": [
    { "src": "takeA.mp4", "start": 1.89, "end": 60.81,
      "first_words": "Hey everyone",                 // doc only — the cut's first words
      "candidate_takes": ["A001","A004"],            // doc only — what you considered
      "rationale": "A004 cleanest complete take: zero ums, clean ending; A001 had a 5.8s dead pause" },
    { "src": "takeB.mp4", "start": 12.0, "end": 20.0,
      "audio_lead": 0.4,                             // J-cut: sound arrives 0.4s before picture
      "punch": [1.0, 1.06],                          // slow push over the clip (static shot)
      "rationale": "answer starts under the tail of the question so the cut disappears" },
    { "src": "talk.mp4", "start": 70.0, "end": 78.0,
      "vsrc": "roomcam.mp4", "vstart": 161.3, "vend": 169.3,
      "rationale": "audio stays on the mic'd talk; cut the PICTURE to the wide cam while the slide is static" }
  ]
}
```

- `start`/`end` are **seconds (floats) on the source timeline**. Cuts are frame-accurate
  (trim filter, not `-ss` seeking); the renderer quantizes every boundary onto the frame grid
  so times written by `snap`/`tighten` can't drift picture against sound.
- `first_words`, `candidate_takes`, `rationale` are **documentation only** — the renderer
  ignores them; humans read them. Always fill `rationale`.
- Every segment is normalized to `width`×`height` (scale-to-fit + pad) at `fps`, so clips of
  **different resolutions/fps concat cleanly** (e.g. a 4K take next to a 720p one).
- `audio_lead` makes the cut a **split edit** (+ = J-cut, − = L-cut). This is the main thing
  that stops an edit feeling choppy — see the `cutting-rhythm` skill for how much to use.
  Video and audio are concatenated as two independent chains, so a lead never desyncs.
- `punch` is a slow zoom push (`1.06` or `[1.0, 1.06]`) — life for an otherwise static shot.
- `music` mixes the bed **in the same render pass** (looped to cover, ducked under speech by
  default), so a montage doesn't need a second re-encode. `audio_fix` runs on the speech
  before the mix, so ducking triggers on normalized dialogue.
- `seam_fade` (default 15 ms) is applied at every internal audio boundary; it's inaudible as
  a fade but removes the click a butt-splice makes. Set `0` to disable.

## Multicam cutaways (`vsrc`)

A clip can take its **audio from `src`** but its **picture from a different camera** via
`vsrc`/`vstart`/`vend`. The audio timeline stays continuous (one mic); only the video switches
— a clean camera cut, no audio seam. This is how you express "screen recording with cutaways
to the room cam" (see the `editor` skill's multi-camera section for finding the per-cutaway
sync offset by audio cross-correlation).

## Get cut points from the transcript, not by scrubbing

Build the EDL from text: `transcribe src.mp4 --words` (word timestamps) for *what's said* and
`speech-segments src.mp4` for *frame-accurate silence edges*. Grep the transcript for the line
you want and write its start/end into the EDL. Never eyeball a timeline.

Then let `snap` place the cuts exactly, instead of nudging numbers by hand:

```bash
uv run video-agent snap edit.json -o edit.snapped.json --to silence   # onto silence edges
uv run video-agent snap edit.json -o edit.snapped.json \
    --to beats --ref inputs/music.mp3 --tolerance 0.4                 # onto the music grid
```

It prints every move it made and leaves alone any cut with no candidate inside `--tolerance`.

## Check the pacing before you render

```bash
uv run video-agent edl edit.json -o /dev/null --report --dry-run
```

Prints each shot's length as a bar plus warnings for monotone shot lengths, missing split
edits, and a too-short final shot — the three things that make a correct cut list watch
badly. It costs nothing and it catches problems that are invisible in the JSON. Act on it via
the `cutting-rhythm` skill. `--draft` renders a fast 480p version for your own verification.

## Verify by re-transcribing the OUTPUT

The strongest check that the cut is right is to transcribe what you actually rendered and
compare to intent:

```bash
uv run video-agent edl edit.json -o out.mp4
uv run video-agent transcribe out.mp4 --clean -o check.txt   # read it: right words, no fillers, nothing dropped
```

If a take was supposed to be filler-free, grep the re-transcript for `um`/`uh`. If a cut
landed wrong, the output transcript will show a clipped or repeated word that a frame-check
misses. Fix the offending clip's numbers in the EDL and re-run. (Internal verification only —
per the no-partial-previews rule, show the user the finished video, not the checks.)

## Gotchas

- **`grade` / `audio_fix` are raw ffmpeg** applied to the assembled cut — `audio_fix` runs on
  the concatenated audio (good place for `loudnorm`, `acompressor`; see `audio-edit`), `grade`
  is a LUT path, either `.cube` or a HALD `.png` from `grade gen-lut` (see `color-grade`).
- **One re-encode.** The whole EDL renders in a single `filter_complex concat` pass
  (`h264_videotoolbox`, aac 48k) — don't post-process with stream-copy concat afterward.
  That now includes the music bed and the grade, so there's no reason to add a second pass.
- **This LGPL ffmpeg lacks `eq`/`drawtext`** — `audio_fix` and `grade` must use available
  filters (loudnorm/acompressor/curves/colorbalance/lut3d/haldclut), not `eq`.
- **A `vsrc` cutaway must match the length of the audio it covers.** A cutaway swaps the
  picture only; if `vend-vstart` ≠ `end-start` the picture comes apart from the sound for the
  rest of the edit. The renderer rejects a mismatch rather than rendering it.
- **`audio_lead` needs source material to reach into** — a J-cut borrows audio from *before*
  the clip's in-point, so a clip starting near 0 in its source can't take a large lead. The
  renderer errors instead of silently shortening. It's ignored on clip 0 (nothing precedes it).
