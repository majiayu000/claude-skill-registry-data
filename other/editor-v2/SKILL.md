---
name: editor-v2
description: "Editor V2: a storytelling edit that opens on a fast picture-montage hook (12.5 images a second, the same pictures returning blurred and solarized, a camera shutter click roll, slowing down to land), then the speaker talking with real B-roll, huge red captions behind the speaker, and a massive end title they stand in front of. Always 16:9. Runs free on this computer. Use whenever someone says Editor V2 or asks for this style."
---

## Video Studio (read first; overrides the rest of this file)

This skill is installed in Video Studio (`Edits/.claude/skills/`), from the NextPhase / creator packs
Bryan downloaded on 2026-10-31. Video Studio's `CLAUDE.md` wins wherever the two disagree.

- **Start from the studio job, never an intake.** Jobs come from the studio page (`jobs/<id>/job.json`).
  This skill runs when the job's `style` is `story-montage`. Never ask "short or long?" or "which style?":
  the page already asked. (`nextphase-studio`'s intake is not used here.)
- **One transcript:** `projects/<id>/transcript/words.json` (WhisperX). Don't run this skill's own transcriber.
- **Brand:** `styles/brand.json` (purple `#8B5CF6` / `#C4B5FD` / `#4C1D95`, Inter + Playfair Display)
  replaces this skill's default colours. Generate its theme/tokens from it.
- **Show the motion graphics before rendering (Bryan's rule):** design first, show stills of each graphic over
  the real frame in batches (the `design` → `graphics` stages, `graphics.json`), wait for approval, then render.
- **Sounds and music:** the studio's library (`styles/sfx.json`, `node studio/sfx.mjs place`) on the locked
  picture; music only from tracks Bryan owns or licensed.
- **Windows Git Bash, not macOS/WSL:** `python` not `python3`; a venv's Python is `Scripts/python.exe`;
  long paths fail, so map a short drive (`cmd //c "subst R: <winpath>"`). Run this skill's setup/doctor script
  only the first time the style is used, and ask before any download over ~500 MB.
- **Where work goes:** editing work in `projects/<id>/`, deliverables in `jobs/<id>/`.
- The pack's bundled song (`music/song.m4a`) was removed: use a track Bryan owns or licensed. The huge captions behind the speaker need the matte (PyTorch, ~1 GB): ask before installing.


# Editor V2

**Format: always 16:9, 1920x1080.** The reference reel is square, but only its timing and sound carry over. Make the montage pictures at 16:9, never crop square ones or use vertical.

Read `reference/study.md` first. It holds the section map, the timing and the sound.

## What you need from them

A talking-head recording and, ideally, some B-roll of them working. Their own face, desk and hands go in the montage. If they have no B-roll, ask for it, or build the montage from free archive material plus frames of their recording. Everything here is free, so nothing is generated unless a look can't be had any other way, and then you show the cost and ask first.

## How to run it

Start a folder with `bash ~/.claude/skills/editor-v2/scripts/new_project.sh <name>`. It copies the working code from `examples/raw-footage/` to `~/editor-v2/videos/<name>/`. That code is one real video, so rewrite its timings, words and picture lists for theirs. Run the scripts from inside the project folder. Run Python with `~/.claude/skills/editor-v2/scripts/py`.

1. **Voice first.** Transcribe (`scripts/transcribe.py raw/take.mp4 --out work/take_tx.json`), write `cut.json` (the format is at the top of `scripts/voicecut.py`) and cut with `scripts/voicecut.py <project>`. Then re-transcribe the cut stretch by stretch with `--from` and `--to`. A whisper pass over a whole take can hide a line said twice, and it only shows up when the voice cut is transcribed on its own.
2. **Find outside material for free.** Wikimedia Commons API and Prelinger on archive.org (`pull.py`). Look at every shot: a time read off a contact sheet is often a few seconds out. Keep a credits list with each file's licence.
3. **Hook** (`hook.py`): keep the reel's cut points, swap the pictures. Use the speaker's own face, desk and hands among them. **The voice starts on frame 0 and runs over the hook.** A silent montage has no context.
4. **Then the voice is the clock** (`edit.py`). Shots follow the words. Rushes at the reel's speed on the key words, holds of 1 to 2.6 s between. Nothing over 3 s. **No zooms on talking shots: no punch-ins, no slow push.** They look strange here. Change the picture with B-roll and outside clips instead.
5. **Sound** (`mix.py`): the hook bed 5 LU under the voice, the click roll on rushes, single clicks on other cuts. The song in the kit (`music/song.m4a`) starts after the hook with its drop on a line, 5.5 LU under the voice measured where they overlap, cutting out for punchlines. Never pick music yourself: use the kit's song or the one they give you. It repeats every 58 s with a drop at 43.5 s. `scripts/song_drop.py <song>` finds the drop in another song.
6. **End card** (`endcard.py`, `matte_seg.py`): the name massive, heavy (Impact) and red on the wall, in a black and white room. It lands while the speaker is still well inside the frame, so they visibly stand in front of it, then they walk out. A thinner title that appears as they're already leaving doesn't work. Build the empty room from a locked-off clip. Cut the person out with the matte plus the difference from the empty room, but only count that difference right beside the body, or light shifts on the wall chew the letters. Keep the type above the desk objects and trace what crosses it. If the clip ends with them still at the edge, slide the cut-out off the frame with motion blur. Hold about 2.3 s.
7. **Captions behind the speaker** (`cap()` in `edit.py`, `word_mask()` in `endcard.py`): huge red Impact on the wall above the shoulders, word by word on the voice, the person cut out in front, like a magazine cover. Put them on the first talking line after the hook. Short words spread wide so the head hides less, a long phrase keeps one fixed layout as its words arrive, and each new word gets a click. These need the matte: run `setup.sh --matte` once, then `scripts/matte_all.py <project>` for the talking take. Its frame numbers assume 30 fps.
8. **Measure against the reel** on the same 25 fps grid, then fix what's short. A first render can look right on a sheet and still measure 11 changes a second against 17.7, because frames inside a picture barely move. A small push on sharp frames and a thrown frame on blurred ones closes it. `scripts/study_reel.py <video> <outdir>` gives the same numbers for any video.
9. **Check before you show it.** Look at frames either side of every cut, and transcribe every section with the music on. You can't hear the audio, so say that levels are measured only.

Render with the spawn context: forked workers hang on OpenCV on macOS and produce nothing, silently.

## Files

- `reference/study.md`: what the reel does, second by second
- `examples/raw-footage/`: working code from one real video. `pull.py` fetches and cuts material, `lib.py` holds the looks, `hook.py` the montage, `edit.py` the timeline, `endcard.py` and `matte_seg.py` the end title, `mix.py` the sound
- `sfx/`: shutter clicks, the click roll, the hook bed, a boom and a sweep, all made in code by `scripts/synth_sfx.py`. To use your own sound, drop a WAV with the same name into `sfx/`. It won't be overwritten
- `music/song.m4a`: the song, 5 minutes
- `scripts/`: `setup.sh`, `demo.py`, `new_project.sh`, `transcribe.py`, `voicecut.py`, `bed-mix.py`, `matte_all.py`, `song_drop.py`, `study_reel.py`, `synth_sfx.py`, `py`
