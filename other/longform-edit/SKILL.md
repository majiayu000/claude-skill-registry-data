---
name: longform-edit
description: "Edits a raw long-form YouTube recording (screen recording export, camera file, or either plus a separate mic) into a publish-ready video automatically, like Descript on autopilot: transcribes with word timestamps, removes retakes and keeps the last take, tightens dead space while keeping silent on-screen action (speeding up long waits), masters the voice to -14 LUFS / -1.5 dBTP with no music bed, re-transcribes the FINAL render for an every-word SRT (optional burned-in captions), drafts chapters, titles and a description, and fails loudly on QA gates (words, A/V sync, caption sync per chapter, caption coverage, loudness) plus contact sheets you look at. Use when someone says edit this long-form, clean up my recording, cut the retakes and dead space, process the long-form inbox, or descript this. Needs Claude Code with ffmpeg, whisper.cpp and Python 3."
---

# longform-edit

Drop raws in a folder, run one command, get a cut, mastered, captioned video plus a REVIEW.md that
explains every cut. Short-form sibling: `edit-style` (reels). Transcription setup: `use-local-whisper`.
Thumbnails: `thumbnail-generator`. Per-platform captions for clips: `reel-captions`.

## Requirements (check first, install only after the user says yes)

```bash
ffmpeg -version | head -1                       # any 6.x+; libass only needed for --burn-captions
whisper-cli --help >/dev/null && echo WHISPER_OK   # whisper.cpp (brew install whisper-cpp)
ls ~/models/whisper/ggml-small.en.bin           # or set paths.whisper_model
python3 -m pip install -r scripts/requirements.txt  # numpy, pillow, opencv-python-headless
which claude                                     # optional: titles + chapter names
```

Model: `curl -L -o ~/models/whisper/ggml-small.en.bin https://huggingface.co/ggerganov/whisper.cpp/resolve/main/ggml-small.en.bin`
(466 MB; `ggml-base.en` on slow machines, multilingual `ggml-small` for non-English). Another transcriber is
fine too: pass `--words words.json` as `[{"w": "word", "s": 0.12, "e": 0.40, "p": 0.9}]`.
Claude.ai has no ffmpeg: there, take a pasted transcript with timestamps and return the cut list, retake table,
chapters and an SRT only. Say clearly that nothing was rendered.

## Setup (once)

Copy `config.example.json` to `~/longform/config.json`, set `paths.inbox`, `paths.outbox`, `paths.whisper_model`,
your names in `transcribe.prompt` and `publish.word_fixes`, and optionally `publish.cta_line` + `publish.cta_keywords`
(the draft flags a video with no mid-video call to action). Every threshold below lives in that file.

## Run it

```bash
S=~/.claude/skills/longform-edit/scripts/longform_edit.py
python3 $S ~/longform/inbox/<slug>/ --config ~/longform/config.json             # one video
python3 $S --config ~/longform/config.json                                      # every inbox folder with no REVIEW.md yet
python3 $S <folder> --plan-only      # cut plan + REVIEW.md in ~1 min, no render
python3 $S <folder> --mic voice.wav  # separate mic, synced by cross-correlation (clap at the start helps)
python3 $S <folder> --kind camera    # talking head: every silence is idle (auto-detected from motion or file name)
python3 $S <folder> --burn-captions  # also <slug>.captioned.mp4 with 2-5 word captions burned in
python3 $S <folder> --no-llm         # heuristic chapter titles, no claude CLI call
```

Inbox: `<inbox>/<slug>/` holding one video (largest wins) and optionally one audio file (used as the voice) and a
`config.json` with per-video overrides. Output: `<outbox>/<slug>/`. A 15 min raw takes roughly 6-12 min; run it in the
background and tail `<outbox>/<slug>/run.log`. Re-runs are cached: only changed stages redo.

## What it decides (details and every number in references/method.md)

1. **Retakes, keep the last take.** An explicit cue said as its own phrase ("let me say that again", "retake",
   "scratch that", 22 cues in config) cuts the abandoned attempt plus the cue. A line restarted from the top (same
   opening words, similarity >= 0.8, within 45 s) cuts the earlier attempt. Back-to-back repeated phrases lose the
   first copy. um/uh separated by silence are cut. Anything weaker is **flagged, not cut**.
2. **Dead space, strategically.** Every silence >= 0.7 s is checked against the picture (frame diff at 8 fps,
   cursor-sized blobs ignored, webcam bubble masked, net first-to-last change catches slow typing).
   Static screen: tightened to 0.28 s mid-sentence / 0.40 s at a sentence end, breath kept. Cursor only: 0.6 s.
   Real on-screen action: kept, idle trimmed either side; if it runs > 4.5 s it plays at 1.5-3x with the last 0.9 s
   at 1x so the result lands. Cuts only land in measured silence, never mid-word.
3. **Voice master, no music bed.** HPF 75 Hz, FFT denoise from the measured floor, mud cut, presence, air, de-ess,
   2.5:1 compression, gain to -14 LUFS, limiter to <= -1.5 dBTP, filter latency measured and removed.
4. **Captions from the FINAL audio.** The final render is re-transcribed; the SRT is built from that, never from the
   source transcript, with cue starts snapped to speech onsets. Every word is covered (gated).
5. **Publish draft.** Chapters (structural cues like "the first", "next", long pauses, big screen changes; >= 3,
   first at 0:00, each >= 40 s), 3 title options, description, pinned comment, tags and fact-check flags via the
   `claude` CLI when present, heuristic otherwise. 3 thumbnail candidate frames (sharpest, most colourful per third).

## Gates (exit 2 and `<slug>.FAILED-GATES.mp4` if any fails)

| gate | passes when |
|---|---|
| frames | every chunk has exactly the EDL frame count; video and audio length within 1.5 frames |
| words | final re-transcription recalls >= 93% of the kept source words, no lost run >= 6 words |
| av_sync | 10 probes: audio lag <= 25 ms and the frame matches the source better than +-0.5 s |
| captions | per chapter, cue start vs audio onset: median <= 0.12 s, p95 <= 0.25 s |
| caption_coverage | >= 98% of final words sit inside a caption |
| loudness | -14 +-1 LUFS integrated, true peak <= -1 dBTP |

## After it runs (the agent's job, do not skip)

1. **Exit code.** 0 = all gates passed. 2 = never hand the file over as done; REVIEW.md says which gate and why.
2. **Look at `contact-sheet.jpg` and `cuts-sheet.jpg`** (open the images): picture present in every tile, no
   black frames, the before/after of each edit point looks like a continuous state.
3. **Read REVIEW.md**: retakes cut (before/after text), flagged-not-cut list, on-screen actions kept, loudness,
   caption sync per chapter, A/V probes, words check. To change a decision write `<outbox>/<slug>/overrides.json`
   and re-run the same command (times are SOURCE seconds, the `src` column):
   ```json
   {"keep_retakes": ["R03"], "cut_retakes": ["R07"], "keep_ranges": [[312.0, 330.5]],
    "force_cut": [{"s": 100.2, "e": 104.9, "why": "cough"}]}
   ```
4. **PUBLISH.md is a draft.** Rewrite weak titles, fact-check every flagged number (measured, same source, same
   window), fix name spellings in `publish.word_fixes` and re-run so the SRT is right.
5. **Never upload or schedule.** Hand back the paths; the human publishes.

## Report back in this shape

```
LONGFORM EDIT: <slug>
Runtime   14:32 -> 11:05 (24% cut): 6 retakes, 11 fillers, 3 speed-ups, 41 pauses tightened
Gates     6/6 PASS (words 97.8%, max A/V lag 4 ms, captions median 0.05 s, -14.0 LUFS / -1.6 dBTP)
Flags     R04 at 03:12 restart? similarity 0.62, kept; "saves 10 hours" at 07:40 needs a source
Files     <outbox>/<slug>/<slug>.mp4, .srt, chapters.txt, PUBLISH.md, REVIEW.md, thumbs/
Looked at contact-sheet.jpg and cuts-sheet.jpg: clean. Nothing uploaded.
```

## When something is missing

- No whisper model: stop and print the download line above; or accept `--words` from any other transcriber.
- No opencv: runs anyway, but every silence is treated as idle (says so in run.log); install it for screen recordings.
- No `claude` CLI: heuristic chapter titles, flagged in PUBLISH.md as needing a rewrite.
- ffmpeg without libass: `--burn-captions` is skipped with a note; the SRT still ships (upload it as YouTube CC).
- Mic sync confidence below 4: stops and asks for a clap at the start or for the mic to be dropped.

## Recording habits that make the edit better

Say "retake" (or "let me say that again") as its own sentence before redoing a line: it is the only cue trusted to
cut a whole sentence. During a loading wait either stay silent with the cursor still (cut) or narrate (kept).
A silent stare at a static chart gets tightened: say something while showing it. One continuous take per file.

Optional stages (graphics panels, scene switching, style profiles, external camera sync, retake reveals) are
described in `references/optional-stages.md`; they are not in these scripts.
