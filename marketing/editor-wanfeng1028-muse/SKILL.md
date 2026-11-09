---
name: editor
version: 1.0.0
description: |
  Turn raw footage into a finished edit in a specific genre/format — montage, documentary, tutorial, news, workshop, vlog, trailer, explainer. Use whenever the user wants the video "edited into a X", asks "what style should this be / what would make a good X", or hands over raw footage without spelling out every cut. This is the director: it understands the footage first, picks a treatment, then composes the other skills (edl-edit, cutting-rhythm, filler-removal, captions, reframe-social, video-transitions, video-overlay, audio-edit, color-grade, remotion-graphics, grok-video-edit) to execute it.
---

# Editor — understand the footage, then edit it to a style

This is a **director/orchestrator** skill, not a single ffmpeg move. It does three things in
order: (1) **understand** what the footage is, (2) **pick a treatment** (genre/format), and
(3) **compose the other skills** into a plan and execute it. Every "signature move" below is
just a call into an existing skill or CLI command — this skill decides *which*, in *what
order*, and *why*.

## Is there a video-understanding API key?

**No separate one — and you don't need it.** `XAI_API_KEY` drives Grok's *generative editing*
only (`grok-video-edit`). The understanding model here is **you (Claude) — you are
multimodal**. Sample the footage with the local, key-free tools and read it yourself. (Grok's
vision chat *could* caption frames if you were ever running fully headless with no ability to
read images, but that's the fallback, not the path — reading the frames directly is better and
free.)

## Step 0 — Scan `inputs/` for ALL assets

**Before anything else**, run `ls inputs/` (or whatever directory holds the footage). Look for:
- Multiple video files (multicam, cutaways, B-roll)
- **Music / audio files** (`.mp3`, `.wav`, `.aac`, `.m4a`) — if one exists, it is almost
  certainly the intended soundtrack bed; use it in the edit instead of inventing a music choice
- LUT files (`.cube`, `.png` HALD) — pre-supplied color grade
- SRT/VTT files — pre-supplied captions

Do not proceed to Step 1 until you know every asset available. Missing a music file means the
whole audio direction is wrong before you start.

## Step 1 — Understand the footage (local, no key)

Gather three signals and form one paragraph "read" of the source before deciding anything:

1. **Metadata** — `uv run video-agent info src.mp4` → duration, fps, resolution, codec.
   (AV1 is fine; primitives route through PyAV automatically. Note raw length — it sets how
   aggressively you cut.)
2. **WHAT is said** — `uv run video-agent transcribe src.mp4 -o /tmp/t.txt` (add `--clean`
   unless you'll also be removing filler). Read it for: topic, **structure** (a narrative
   arc? numbered steps? Q&A? a single pitch?), tone, energy, named people/titles, and the
   punchiest lines (these become montage/trailer beats and pull-quotes).
3. **What it LOOKS like** — `uv run video-agent detect src.mp4 --start 0.0 --end <dur> -o /tmp/grid/`
   then Read the grid PNGs. Classify: single talking head · screen-recording/slides ·
   multi-scene + b-roll · action/motion · existing on-screen text. This drives crop-vs-pad,
   transition choice, and whether there's visual variety to cut on.
   - Per the **detect sanity check** habit: before trusting a moment, re-extract a couple of
     full-res `frame`s at ±0.2s to confirm what's actually there (grid cells are downscaled).

**Read output** (state it back to the user briefly): content · structure · visual type ·
pace · raw length · audio quality. This justifies the treatment you pick next.

## Step 2 — Pick the treatment

If the user named a style, use it. If not, recommend one from the read and **confirm before a
long render** (`AskUserQuestion`) — inferring wrong is cheap to ask, expensive to redo. Natural
fits:

| Source read | Likely style |
|---|---|
| One person pitching/telling a story, good lines | Documentary · Trailer · Explainer-short |
| Step-by-step, screen/slides | Tutorial · Workshop |
| Lots of motion, varied shots, music-friendly | Montage · Vlog |
| Authoritative single subject, factual | News |

## Step 3 — The recipes (each = a composition of other skills)

**Universal order of operations** — do not reorder; getting it wrong forces re-renders:

> **content cuts** (trim · filler-removal · highlight-select) → **rhythm** (tighten · split
> edits · beat-snap) → **structure** (transitions) → **reframe** → **audio** (normalize ·
> music bed) → **overlays/captions LAST** → **single final encode**.

Why last-things-last: captions must be burned at final resolution (font size/wrapping follow
the output frame), and audio music-bed ducking needs the final speech track. Re-encode any
join *after a filtered segment* with `filter_complex concat` (CLAUDE.md: stream-copy concat
freezes at non-keyframe seams; re-encode audio to kill drift).

**Rhythm is a step, not a side effect.** Picking the right moments gets you an accurate edit;
it does not get you a watchable one. After the content cuts and before anything visual, run
the `cutting-rhythm` skill: collapse dead air (`tighten`), add `audio_lead` split edits so the
cuts stop slamming, vary the shot lengths, and snap to the music grid if there's a bed. Check
it with `edl --report --dry-run` before you render — it names the three failure modes for you.

### Montage — fast, kinetic, music-driven (~20–60s)
- **Select beats**: from the transcript pull the punchiest 4–10 lines; from `detect` pull
  high-motion / expressive frames. `trim` each beat short (1–3s).
- **Join** with hard cuts, or quick `video-transitions` (slide/pixelize) for energy.
- **Music bed** in the EDL's `music` field (looped, ducked, same render pass). Then actually
  cut on the beat: `beats` → `snap --to beats` (see `cutting-rhythm`), don't eyeball it.
- **Shot lengths must shorten toward the climax** — an all-1.5s montage is monotone.
- Optional **speed ramps** (`setpts=0.5*PTS` + `atempo`), per-clip `punch`, and big kinetic
  `overlay-text` hits.

### Documentary — narrative, slower, cinematic
- **Keep the arc**; clean disfluencies with `filler-removal` (don't gut content).
- **L-cuts carry the narration over the pictures** — set `audio_lead` negative on B-roll
  clips so the voice continues across the visual change. This is what makes doc cutting feel
  seamless; hard butt cuts make it feel like a slideshow.
- **Crossfades/dissolves** between sections (`video-transitions` xfade, or `splice` for a soft
  seam).
- **Lower-thirds**: name + title via `video-overlay`; section/chapter title cards.
- **Music bed ducked** under voice + `loudnorm`. Optional cinematic grade. Clean `captions`
  optional. `tighten --target-gap 0.7` — let it breathe.

### Tutorial — clarity first
- `filler-removal` (tight), then `tighten --target-gap 0.35` to kill dead air. Keep screen
  content readable: reframe with `--mode pad` (never crop UI off).
- **Step/section title cards** (`overlay-text`, numbered). **Zoom/punch-in** on the region
  that matters — use `position-grid` to find it, then crop + scale there.
- **Clean captions** (`captions --clean`) + `loudnorm`.

### News — authoritative, factual
- Tight filler cut, `loudnorm`, neutral grade. Standard **16:9**.
- **Lower-third** name/title + a headline **chyron** (`video-overlay`). Intro/outro card.
- Clean `captions`.

### Workshop — long-form teaching, keep most content
- **Light** filler trim only (don't lose substance). Minimal reframe (`pad` for slides).
- **Chapter/section cards** (`overlay-text`); consider exporting an `.srt` (`transcribe --srt`)
  as chapter source. `loudnorm`.
- Accessibility `captions --clean` — for a very long video, **split → caption each part →
  concat** (captions skill gotcha: one encode pass, but huge segment counts bloat the command).

### Other styles — same method, just a different composition
The point of this skill is the *method* (read → map → compose), so new genres are easy:
- **Vlog** — personable: jump-cuts, light music, `captions`, occasional `overlay-text` asides.
- **Trailer** — dramatic: music-driven, escalating fast cuts, big `overlay-text`, `xfade`
  transitions (`fade`/`pixelize`) between beats, fade-from-black in / fade-to-black out. Hook in
  the first 2s. Structure: **hook (≤2s) → build → turn → climax (fastest cutting) → button
  (one held shot + title)**; shot lengths shorten through the build and the button holds. For
  the bed: profile a music track's energy (RMS per second) and take a segment whose **build
  peaks at your climax beat** (the payoff/button); put it in the EDL's `music` field and
  `snap --to beats` so the cuts land on it. Keep the key spoken lines, not full sentences.
- **Explainer-short** — `reframe 9:16`, hook line as `overlay-text` in first 2s, `captions`
  (clean, karaoke-style if time allows), ruthless tightening to <60s.

## Multi-camera / multi-source footage (cutaways)

When you're handed two+ recordings of the *same* event (e.g. a room/wide camera + a
screen-capture, two phones, broadcast + slides), cut between them for energy — but they're
rarely frame-aligned, especially if one was trimmed (de-sensitized, ad breaks, etc.).

- **Sync by audio cross-correlation, not by eye.** Decode each to mono ~8 kHz, take a smoothed
  amplitude envelope (`abs` then a ~20 ms moving average), and `scipy.signal.correlate` a short
  window of source A against a wider search window of source B → the lag is the offset. The
  correlation peak doubles as a confidence score.
- **The offset can be piecewise-constant.** If one source had sections removed, the offset
  **jumps at each removal**, so measure it **locally per cutaway window**, not once globally. A
  window that straddles a removed cut gets a low correlation score — use that to **auto-drop**
  bad windows.
- **Keep ONE audio track continuous; switch only the video.** Take audio from the primary
  source for the whole timeline and replace just the *picture* during a cutaway (room cam video
  + primary audio). No audio seam, sync is automatic, and any sensitive audio that was removed
  from the primary never re-airs.
- **Never cut to a frame with no subject in it.** A fixed wide cam often has the speaker dark at
  the very edge — which fools brightness/diff detectors — so *verify presence* (background-
  subtract the side zones, or just look at a frame per window) and drop the genuinely empty
  ("everyone walked off") windows.
- **Assemble in one pass.** Generate a single `filter_complex` that `trim`s each segment
  (screen spans from the primary, room spans from the other input at `t+offset`) and `concat`s
  them — re-encodes once, and every boundary lands on exact source-time so audio stays gapless.
  A center-out montage tool (`detect`) or per-window frame grabs make the presence check cheap.

## Pacing cleanup (remove dead air)

"Lightly cleaned" usually means collapsing long pauses, not cutting content — that's the
`tighten` command, which writes an EDL rather than a video so the pacing stays reviewable:

```bash
uv run video-agent tighten talk.mp4 -o edit.json --target-gap 0.5 --min-gap 1.0
uv run video-agent edl edit.json -o out.mp4 --report
```

It removes time from the *middle* of each long pause so breaths survive at both ends.
Conservative `--min-gap` (≥1 s) avoids clipping them; verify a couple of cuts don't truncate a
burned-in caption. This is distinct from `filler-removal` (which cuts spoken um/uh) — silence
collapse leaves the words, just tightens the gaps. **Then widen back out the pauses that are
doing work** (after a punchline or reveal) — uniform pacing is what makes an edit sound
machine-made. See `cutting-rhythm` for the per-genre gap targets.

## Step 4 — Assemble and deliver ONE finished video

- **Author the cut as an `edit.json` (EDL), not a throwaway filtergraph** — for any multi-clip
  stitch, list the clips with in/out + a written rationale and render with `edl-edit` (`uv run
  video-agent edl edit.json -o out.mp4`). It's auditable, diffable, re-runnable, and handles
  multicam cutaways (`vsrc`) and a final `grade`/`audio_fix`. **Verify by re-transcribing the
  output.** Reach for a hand-built `filter_complex` only for one-offs the EDL can't express.
- Optional polish in the same pass: a **color grade** (`color-grade` skill / EDL `grade`) and
  **animated graphics** (`remotion-graphics`, optional — kinetic captions / animated lower-
  thirds, composited as a layer); static labels stay in `video-overlay`.
- Final join (when not using the EDL): `filter_complex concat` with `-c:a aac -ar 44100`
  (re-encode) after any filtered/Grok/overlay segment.
- Write the result to `outputs/`.
- **Show only the finished video — never a partial render.** Build the whole pipeline through
  to the last encode, then present the single final file. (No half-painted previews; the
  per-cut preview loop inside `filler-removal` is internal verification, not a deliverable.)

## Gotchas

- **Order of operations** (Step 3 banner) is the #1 source of wasted renders — caption before
  reframe = wrong font size; music duck before final speech = wrong levels.
- **transcribe verbatim vs `--clean`**: `filler-removal` needs verbatim (um/uh kept);
  captions and every other style want `--clean`. If a recipe both removes filler *and*
  captions, transcribe verbatim for the cut, then `--clean` for the captions.
- **Don't mis-cut for the genre**: a montage that isn't tight drags; a documentary/workshop
  cut too hard loses its point. The raw length + structure from Step 1 sets the budget.
- **Confirm an inferred style before a long render** — `AskUserQuestion`, then commit.
- **Generative looks are optional and non-deterministic** — only reach for `grok-video-edit`
  when a style needs a reimagined look (recolor, smoke, restyle) that ffmpeg/overlays can't do;
  prefer the deterministic skills.
- **Verify long concatenated renders with float timestamps + fps-dumps.** A bare integer to
  `frame --at` is a *frame number*, not seconds — pass floats/`HH:MM:SS`. For auditing a 60-min
  concat, `ffmpeg -ss T -i out.mp4 -t W -vf fps=N out_%03d.png` (a short window dump) is more
  reliable than a single seeked frame; confirm cutaway/seam content this way before the final pass.
- **Leave exactly one clearly-named final per deliverable; delete intermediates.** Multi-pass
  edits spawn look-alike WIP files — if you leave `switched.mp4`/`raw.mp4` next to the final, the
  user will open the wrong one and report "you didn't do X." Clean `outputs/` down to the finals.
