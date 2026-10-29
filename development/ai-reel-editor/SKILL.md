---
name: ai-reel-editor
description: Turn raw talking-head footage (a camera video, a separate mic recording, and one line of notes) into a finished vertical reel. It syncs the mic to the camera, cuts dead air and bad takes from the transcript, fact-checks the script, adds word-synced captions, graphics and sound effects, and re-renders until a QA check passes. Use when the user says "edit this video", "make a reel from this footage", "cut the dead air", "auto-edit my talking video", "sync my mic audio", or shares raw footage for a reel.
---

# AI reel editor

The idea is audio-first editing: timing comes from the speaker's voice, not from hand-placed scenes. Remotion (React) and HyperFrames (HTML) are code-first frameworks where you time every scene yourself.

## Pipeline

0. **Inputs.** `camera.mp4`, `mic.wav` (or `.mov`), and one line of notes (topic plus call to action). `ffprobe` both to get durations and audio streams.

1. **Sync the mic to the camera.** Extract both audio tracks as 16 kHz mono WAV. Cross-correlate them (`numpy`/`scipy.signal.correlate`, take the argmax lag). Shift the mic by that offset (`-itsoffset`, or `adelay` for positive lags) and mux it over the camera video. A weak correlation peak means the files don't belong together, so stop and ask.

2. **Transcribe with word timings.** Use faster-whisper with `word_timestamps=True`, or whisper.cpp with `-ml 1`. Save `words.json` as `[{word, start, end}]`.

3. **Cut.**
   - **Retakes:** when a sentence restarts (same opening words within ~20 s), keep the **last** take.
   - **Dead air:** a gap over ~0.35 s between words is a cut. Keep ~0.1 s of padding so it doesn't sound choppy.
   - Build the cut list and render it (ffmpeg `trim`/`atrim` + `concat`), then re-transcribe the cut version so word timings match the new timeline.
   - Quick option for silence only (no retake logic): `auto-editor in.mp4 --margin 0.2sec`. Add `--export resolve` / `premiere` / `final-cut-pro` (also `shotcut`, `kdenlive`) for an editable timeline. On the Mac install it with `brew install auto-editor`; it ships as a standalone binary now, so skip pip (checked against the auto-editor README and auto-editor.com/installing, v29.3, 2026-09-25).

4. **Fact-check the script.** Pull the names, numbers, product claims and logos from the transcript and verify each on the web. Fix typos in on-screen text. Never alter the spoken audio: flag spoken mistakes to the user instead.

5. **Graphics that land on the word.** For each keyword or number, start its visual at that word's `start` time. That's the "lands on the word" effect, and viewers read about 250 ms of drift as off-beat. Draw the graphics in Python (Pillow or pycairo frames, or manim), not from templates. Render them as transparent PNG sequences and composite with ffmpeg `overlay=...:enable='between(t,A,B)'`. For captions, generate word-level ASS subtitles from `words.json` and burn them in with the `subtitles` filter.

6. **Sound effects.** Put a short whoosh or pop on each graphic entrance and keep them about 12 dB under the voice. Only use SFX the user owns (their own packs or a licensed library); never scrape.

7. **Export.** 1080×1920, H.264, AAC, `-movflags +faststart`. Normalize loudness with `loudnorm=I=-14:TP=-1:LRA=11`, a common social-media target.

8. **QA loop.** Re-render until every check passes, up to 3 loops, then report:
   - no dead air: `silencedetect=noise=-35dB:d=0.6` finds nothing
   - nothing frozen: `freezedetect=n=0.003:d=1` finds nothing outside intentional holds
   - no blank frames: `blackdetect=d=0.2` finds nothing
   - captions stay inside the safe area and the length hits the target in the notes

## Honest notes
- This is a clean-room build of a popular "edit with AI" workflow from standard tools.
- Steps 1-3, 7 and 8 are deterministic ffmpeg/Python work. Steps 4-6 are where judgement lives, so show the user a draft before the final render.
