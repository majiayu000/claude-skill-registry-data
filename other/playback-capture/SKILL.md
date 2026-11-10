---
name: playback-capture
description: Build one continuous playback video from raw screen recordings, so the creator plays it fullscreen and films their screen in a single phone take instead of start-stopping through a live product demo. Black head and tail act as sync markers, every beat is padded so a long voiceover still has screen under it, and a beatmap gives exact timestamps for the edit. Use when someone wants to film their screen with a phone, record a "phone pointed at laptop" demo, or turn screen recordings into footage for a reel. Usage - /playback-capture <folder-of-screen-recordings> [approved-script.md]
argument-hint: <folder-of-screen-recordings> [approved-script.md]
---

# Playback Capture

You are turning raw screen recordings into **one video the creator plays fullscreen and films in a
single take**. This replaces driving a live product on camera.

**Input**: $ARGUMENTS

## Requirements

- `ffmpeg` and `ffprobe` on PATH
- Python 3.9+ with `numpy` and `Pillow` (`pip3 install numpy pillow`), used by `find_offset.py`
- A phone and a tripod for the filmed take

Bundled scripts live in `${CLAUDE_SKILL_DIR}/lib/`.

---

## Why this exists

Filming a live product means hitting record, doing a step, checking it worked, stopping, redoing it.
That easily produces 5+ minutes of footage for 30 seconds of usable screen, plus beats where the
screen does not show what the voiceover claims.

With a playback video the product work is already done and verified. The creator films a screen for
about 35 seconds, once. The edit gets clean beats at known timestamps instead of a haystack.

It also sidesteps bot protection. Some sites hard-block scripted browsers, so Claude cannot drive
them, but Claude can still assemble footage of them from ordinary screen recordings.

---

## The five things that make it work

1. **Black at the head and tail.** 1.5 seconds each. The creator hits record before pressing play
   and stops after the black returns, and those two black stretches are how you find the sync offset
   later. This is the whole trick. Do not skip it (`build_playback.py` adds them if you forget).
2. **Every beat held ~50% longer than its voiceover line needs.** If a line runs long when it is
   recorded, there is still screen footage covering it. Nothing gets reshot for timing.
3. **Native screen resolution.** Export at the same pixel size as the screen recording so it plays
   back 1:1 fullscreen with no upscaling softness.
4. **One beat per voiceover line, hard cuts between them.** The cuts land where you will cut anyway.
5. **Write a beatmap.** Save the exact in/out of every beat to JSON while building. That file is what
   makes the edit trivial.

---

## Phase 1: plan the beats from the approved script

One beat per line that needs screen. For each, note what must be **visibly true** at that moment
(e.g. "prompt text visible in the box, not empty", "the result has actually rendered").

Then find those moments in the raw recordings. Grid each recording at intervals, read the frames, and
pick windows by content. Verify the window is stable across its whole duration, not just at the
frame you sampled. A page that is mid-scroll at the in-point will clip when punched in later.

**Watch for gaps.** Recordings often start with the site already open while the script says "open
the site" or "type the URL". When a beat has no footage that shows it, say so plainly and ask for a
short pickup recording rather than papering over it.

## Phase 2: build the playback video

Write a beat config (copy `${CLAUDE_SKILL_DIR}/lib/beats_example.json` into the recordings folder and
edit it), then run:

```
python3 ${CLAUDE_SKILL_DIR}/lib/build_playback.py <folder>/beats.json
```

Beat durations: take the expected voiceover length for that line and add roughly half again. A 3
second line gets a 4.5 second beat.

Leave `width`/`height` as `null` to use the native size of the first recording. It writes the video
and `beatmap.json` next to the config. Keep the beatmap.

## Phase 3: write filming instructions

Write a short `HOW_TO_FILM.md` alongside the video. It needs:

- Play fullscreen, pause on the first black frame, start the phone recording, wait ~2 seconds, press
  play, do not touch anything until the black returns
- **Room lights off, one warm lamp behind or beside you, screen the brightest thing in frame.** This
  is the single biggest quality factor: it alone can take a shot from unusable to good
- Phone on a tripod, **rear camera not front** (the front camera mirrors on-screen text)
- Screen filling roughly 60 percent of frame height
- Do not move the phone during the take
- On a fumble, redo the whole take, it is only about 35 seconds

## Phase 4: find the sync offset from the black markers

Do not hunt for it frame by frame. Measure the screen band only, so the lit room does not skew the
average, and find the dark stretches:

```
python3 ${CLAUDE_SKILL_DIR}/lib/find_offset.py <filmed.mov> <beatmap.json> "crop=2160:1300:0:1100"
```

The crop is the laptop-screen band in the filmed frame (adjust per framing; omit it to measure the
whole frame). The script samples every 0.1s, thresholds the band brightness at the 20th percentile,
takes the first long dark run as the lead-in and the last as the tail, then computes:

```
OFFSET = filmed_lead_in_end - playback_lead_in_end
filmed_time = playback_time + OFFSET
```

**Verify it at both ends.** The script compares the filmed content duration against the playback
content duration. A drift like 0.07s over 32 seconds is sampling noise and a single constant offset is
safe. If the two differ by more than about 0.15s, derive the offset per beat instead.

Then spot-check every beat at its predicted timestamp and actually look at the grid before cutting.

## Phase 5: hand off

You now have beat-accurate timestamps in the filmed footage. Cut against the voiceover as usual, then
hand off to your captioning and SFX pass (for example the `edit-reel` skill in this plugin).

---

## What not to do

- Do not skip the black head and tail. Without them the sync is guesswork
- Do not pad beats by a fixed 1 second. Pad proportionally, long lines need more slack
- Do not export at 1080p if the screen recording is 3024 wide. It plays back soft
- Do not burn any guide text, countdowns or markers into the playback video. The phone films the
  whole frame, so anything you overlay ends up in the footage
- Do not fill a missing beat with unrelated footage and hope. Ask for the pickup
