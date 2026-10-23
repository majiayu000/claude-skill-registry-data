---
name: video-check
description: >-
  Runs the quality gates and an independent review on any video before anyone sees it: grounding
  read of every claim, voice gate, hyperframes check, reading time per line, stills at
  mid-transitions and at phone width, 1:1 zoom on images, render and encode settings, loudness
  and true peak, sound against picture, frozen and black frames, one-frame glitches at every cut
  (ghost, black or held frames, late cuts), the poster frame, a transcript of the finished file,
  and a review by fresh subagents that grade defects P0/P1/P2. An executor under video-studio.
  Use when a film is rendered and before it is shown, or when video-studio reaches its gates.
  Triggers: "check the video", "QA the film", "review the film", "what is wrong with this
  video", "check the render", "seam scan".
---

# video-check

The eyes and ears on a film. video-studio decides that every film passes these gates
before the user sees it; this skill holds the gates, the tools and the review protocol.
What counts as a defect is defined by `../video-studio/references/laws.md`; what the film must say
and show, by its `brief.md` (`../video-studio/references/brief.md`) - the gates and the review check
the film against both.

## The gates

`references/qa.md`, in order: private data listed → grounding read → voice gate →
`hyperframes check` → reading time → stills incl. mid-transitions and phone width → 1:1 zoom on
images → render (master `--crf 10`, encode once) → sound on the file (loudness, true peak, effects
heard, sound on its picture) → black and frozen frames → cut seams → poster → transcript of the
file → independent review → watch once with sound.

## Setup

- `ffmpeg` / `ffprobe` on PATH; Node 18+ and the HyperFrames CLI for `readcheck.mjs` and `check`.
- `soundqa.py` and `seamscan.py` need numpy (+ scipy for soundqa): run them with the sound
  library's venv, `PY="${VIDEO_LIBRARY:-$HOME/.local/share/marketing-agent-kit/video-library}/tools/.venv/bin/python"`
  (made by `python3 ../video-sound/scripts/library.py venv`), or any Python with those packages.
- Transcripts: a Whisper CLI - `mlx-whisper` on Apple Silicon (`pip install mlx-whisper`),
  `openai-whisper` elsewhere (`pip install openai-whisper`).

## Tools

| Job | Command |
|---|---|
| Stills at chosen times, contact sheets, phone width | `python3 ${CLAUDE_SKILL_DIR}/scripts/stills.py <project> t1 t2 ... [--every 0.5] [--per-sheet 12] [--width 390 --cols 2]` |
| Reading time of every on-screen line | `node ${CLAUDE_SKILL_DIR}/scripts/readcheck.mjs <project> [--norm strict]` |
| Sheets cut from a rendered file | select frames by number (`select='not(mod(n\,15))'`), never `fps=N` - it labels tiles early |
| Effects heard | `$PY ../video-sound/scripts/sfxcheck.py timeline.json` |
| Sound against picture, on the encoded file | `$PY ${CLAUDE_SKILL_DIR}/scripts/soundqa.py film.mp4 --placed audio/track.placed.json --track audio/track.wav [--cues more.json] [--silence-ok a-b]`: each cue's `visual` (cut / move / land / appear, optional `roi`) against the frame motion, the effect's peak on its cue, the film's audio vs the mix (≤ 1 ms), loudness and true peak, unplanned silence. Exit 1 on a FAIL |
| One-frame glitches at every cut, on the encoded file | `$PY ${CLAUDE_SKILL_DIR}/scripts/seamscan.py film.mp4 --scenes scenes.json [--scene-in dip:3] [--seams more.json]` or `--cuts 12.9,f387,62.0:dissolve:1.0`, or nothing to detect the cuts: GHOST / BLACK / FLASH / HELD / DISPLACED / DEAD per seam, declared dips, dissolves, wipes, whips and fades checked against their own shape; `report.txt` + labelled sheets in `<film>.seams/`. Exit 1 on a defect (qa.md gate 10) |
| Transcript of the finished file | Apple Silicon: `mlx_whisper <file> --model mlx-community/whisper-large-v3-turbo --word-timestamps True --condition-on-previous-text False --language <first spoken language>`; elsewhere: `whisper <file> --model turbo --word_timestamps True --condition_on_previous_text False --language <lang>` (why each flag, and why not parakeet: `references/qa.md` gate 12) |

## Independent review

`references/review.md`: every film gets a review by fresh subagents (two split by time plus
one for consistency when the film is over ~60 s), who write `REVIEW.md` with P0/P1/P2
defects. Fix every P0 and P1, show the film with the P2 list, ask before another round.

## /watch - a model that sees AND hears the film (optional)

A third-party plugin, Watch (github.com/bradautomates/claude-video, MIT). In Claude Code:

    /plugin marketplace add bradautomates/claude-video
    /plugin install watch@claude-video

Then ask with the `/watch` skill (`/watch:watch <file-or-URL>` plus the question with
timestamps). Its Gemini engine needs `GEMINI_API_KEY` in the plugin's own config,
`~/.config/watch/.env` (a free Google AI Studio key works) - not in the kit's keys file.

**It uploads the film to Google.** With the Gemini engine a local file goes to Google's Files API
and is deleted after the answer (an upload that cannot be deleted expires within 48 hours). Whether
an unreleased film may go there is the user's call - ask before the first upload of a project.
`--engine local` never contacts Google (frames + transcript on this machine) and is the choice
for anything private.

- **Reference teardown** (format-reference-copy): ask for every technique in order with start/end
  times, what the camera or the edit does and what is heard. Tested on a camera-moves showreel:
  the timings matched our own frames, it read the on-screen readouts (16 → 52 mm on the dolly
  zoom) and named the sounds (a ratchet on the dutch angle, a rising hum on the crane, a click per
  jump cut, ticking on the time-lapse).
- **A "listen" pass in review**: ask for moments where sound and picture are out of sync, an effect
  that does not match its picture, a voice under music, a clipped word. It complements soundqa.py's
  measurements; its findings are observations to verify, not facts.
- **Free key limits** (2026-10): Flash models only (Pro models have 0 quota on the free tier);
  Flash answered 503 "high demand" five times before working - retry every ~2 minutes; a 30 s
  film cost ~268k tokens. The answer includes the model's thinking; the useful part is its
  timestamped list.

## Adapt it

- **Your laws**: the gates judge against `../video-studio/references/laws.md` - fill in its
  "Brand laws (yours)" section, or the review has no brand to hold the film to.
- **Your reading norm**: `readcheck.mjs` uses 0.3 s per word; switch to `--norm strict` for an
  audience that reads slowly or in a second language.
- **Your loudness target**: the gates assume -14 LUFS and ≤ -1 dBTP (YouTube, LinkedIn, ads);
  pass `soundqa.py --target` for a channel that wants another.
- **Your private data**: list in gate 0 what counts as private in your company (customer names,
  internal hostnames, key formats) so the grep finds it.
- **Your review rounds**: the default is one round, then show; set how many rounds you want and
  who sees the P2 list.
