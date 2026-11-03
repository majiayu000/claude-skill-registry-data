---
name: narrated-video
description: Make a narrated product video (a launch video, product demo, or tutorial) from real screenshots of the product and the person's own webcam narration. Captures the product, builds a storyboard to record against, edits the recorded take (restarts, dead air, optionally fillers), times every scene, click, and keystroke to the spoken words, then renders and verifies a 1080p mp4 with a round webcam bubble. Use when someone wants a demo, walkthrough, tutorial, or launch video they will narrate themselves, or has recorded a new take to cut.
---

# Narrated video

The person records one take of themselves talking over a storyboard. The agent edits the take and animates real
screenshots of the product to it: every scene starts, every click lands, and every search is typed on the word that
names it. The whole video is code (a HyperFrames composition plus an edit list), so a new take, a changed screen, or a
different order is a re-run, not a re-edit.

The video bends to the narration, never the other way around. The person directs taste; the agent produces cuts,
shows frames, and asks.

## Setup

- `ffmpeg` on PATH, `uv`, Node 20+ with `npx` (HyperFrames 0.8.62 runs through npx), and Playwright with Chromium
  for captures. Works on macOS, Linux, and Windows.
- Whisper runs locally: mlx-whisper on Apple Silicon, faster-whisper elsewhere. `uv run` installs the right one.
- `SK=<this skill's directory>/scripts`. Every tool runs as `uv run $SK/<tool>.py`; each declares its own
  dependencies.
- Work in a folder outside any repository's tracked files (a gitignored `.logs/<video>/`, or a scratch folder):

```
<work>/
  assets/            captures, backdrop, end card
  storyboard.json    the scenes -> storyboard/index.html
  takes/<name>/      one folder per recorded take: probe output, transcripts, edit.json, the cut narration and webcam
  video.py           the composition script -> comp/ (index.html, renders/)
  NOTES.md           every decision: cuts and why, scene starts, rebuild commands
```

## 1. Brief

Confirm in one short exchange, offering defaults:

- Format: launch video, feature demo, or tutorial ([references/formats.md](references/formats.md)). A launch video
  stays under 2:00 including the end card.
- Audience, the three or four beats the video must land, and the call to action.
- Example data that demos well: an example business or search that reads at a glance for this audience.
- Brand: a backdrop image (or the default gradient), an end card (the product's OG image works well), the URL shown in
  the window's title bar.

## 2. Capture

Real screenshots of the running product at 1440x900, 2x, from a Playwright script built on `$SK/capture.mjs`:
per-keystroke frames for anything typed on screen, before and after states for anything clicked, tall shots for
anything scrolled, and measured click targets for the pointer. If the app needs a sign-in, pass `login` and the first
run opens a browser window for the person to sign in once. Never draw UI or edit pixels. Look at every capture before
using it. Details and the privacy pass: [references/capture.md](references/capture.md).

## 3. Storyboard

Write `storyboard.json`, one card per scene: the screenshot, what is on screen, three to six bullets of what to say
(short notes, not sentences), and rough seconds. Build it and show it:

```sh
uv run $SK/storyboard.py storyboard.json storyboard/
```

It is a plain page, one section per scene. Publish `storyboard/` (index.html plus `frames/`) when the harness can
publish a page, otherwise open it locally. Iterate until the person is ready to record, then hand over the recording
notes in [references/storyboard-and-recording.md](references/storyboard-and-recording.md). Once they are recording
from it, do not change the storyboard without asking.

## 4. Record

The person records one take, webcam and voice in one file (any webcam recorder: QuickTime, Photo Booth, Windows
Camera, OBS), talking through the scenes. Flubs are fine: they restart the sentence and keep going. Several takes are
fine; each gets a take folder.

## 5. Edit the take

```sh
uv run $SK/probe.py <recording> takes/<name>       # take.wav, cam.mp4, take.json; check still.jpg, re-run with --crop if needed
uv run $SK/transcribe.py takes/<name>              # two passes: plain, and one that writes fillers out
uv run $SK/analyze.py takes/<name>                 # candidates: long pauses (with cuts), fillers, restarts, stray sounds
uv run $SK/trace.py takes/<name> <a>:<b>           # place each cut on the energy trace (--fine for 5 ms rows)
uv run $SK/splicetest.py takes/<name> c1=<a>:<cut start>,<cut end>:<b>   # hear a cut: it must read as the intended sentence
uv run $SK/jump.py takes/<name> <cut start>:<cut end> --slide 0.3        # how visible the cut is in the webcam bubble
# write takes/<name>/edit.json, then:
uv run $SK/edit.py takes/<name>                    # edl.json; prints the edited narration and the fillers kept: read it all
uv run $SK/build.py takes/<name>                   # narration-edit.wav, cam-edit.mp4 (crossfades and webcam dissolves at every cut)
uv run $SK/master.py takes/<name>                  # narration.wav at -16 LUFS
```

Two levels of edit ([references/editing.md](references/editing.md)):

- Light, the default: cut restarts and false starts, and trim dead air (a pause over ~1.1 s keeps 0.7 s, 0.9 s at a
  scene change). Every um and short hesitation stays.
- Fewer fillers, when asked: also remove most ums that stand alone between phrases, and trim pauses over ~0.8 s to
  about 0.55 s. Leave any filler glued to a neighbouring word.
- Each cut sits in room tone on the trace and passes a splice test before it goes in. Restart cuts go on scene
  changes where possible, so the picture cut hides the jump in the bubble.

## 6. Compose to the words

```sh
uv run $SK/cues.py takes/<name>       # words.json, the cue sheet (clip-level transcripts of the final narration)
NV_SCRIPTS=$SK ASSETS=assets uv run --with numpy python video.py   # the composition script -> comp/; prints every cue in context
uv run $SK/render.py comp lint
uv run $SK/render.py comp snapshot 1,14.2,22.5,40.1
```

Write `video.py` from the worked example, [examples/openseo-launch/video.py](examples/openseo-launch/video.py): scene
starts and cue times from the cue sheet, camera layers over the captures, and a choreography keyed to words. The
example's cue positions fit its own edit only: re-anchor every one, and read the cue table it prints after every
change to the edit. The timing rules are in [references/composition.md](references/composition.md); the ones that
matter most:

- A scene starts 0.3 s before its first word, or exactly on a cut in the pause before it.
- Each action lands on the word that names it: the click on "copy", the typing as the search is spoken, the zoom on a
  number as it is said, the pointer on each item as it is named.
- The first frame is the poster: the whole app, no fade-in. Something moves in every frame.
- One short label per beat. Snapshot every scene start, click, and label, and look at them before rendering.

## 7. Render and verify

```sh
uv run $SK/render.py comp render
uv run $SK/composite.py comp takes/<name> comp/renders/<video>-1080p.mp4
uv run $SK/check.py comp/renders/<video>-1080p.mp4 comp takes/<name>
uv run $SK/filmstrip.py comp/renders/<video>-1080p.mp4 comp/renders/filmstrip.png
```

Nothing goes to the person until the check shows the window in every frame, every webcam point at frame offset 0, an
audio median of 0 ms, and about -16 LUFS, and you have read the transcript and looked at the filmstrip
([references/verification.md](references/verification.md)).

## 8. Review and iterate

- Give the person the mp4 path, what was cut, and anything to listen for.
- Keep `NOTES.md` current: every cut with its reason, scene starts, rebuild commands. Expect several rounds.
- Variants are cheap: another take, a light and a fewer-fillers edit, a different scene order. Each is a take folder
  or a composition script; with subagents, build them in parallel under separate file names so they never collide.

## Hard rules

- Real screens only. Hide what is not part of the story (a banner, a cookie notice); never paint over pixels.
- Check captures and recordings for secrets and personal data (API keys, other people's emails and names, customer
  data, localhost URLs) before rendering; frame around them or recapture, and have any key that appeared on screen
  revoked. The person's own name or email in the app is fine once they confirm it.
- The person's recordings and sign-in session stay on their machine. Publish nothing without being asked.

What still trips people up: [references/gotchas.md](references/gotchas.md).
