---
name: trim-raw-video
description: Turn super-raw talking-head footage (retakes, crew chatter, false starts, stumbles, dead air) into one clean trimmed cut. Transcribes with Whisper, separates the real script from chatter, keeps the clearest take of every line and splices them with matched loudness. Works in any language Whisper supports, including English and Greek. Keeps the original frame by default or re-crops to 9:16, 1:1 or 16:9 on request. Use when someone wants to trim, clean up, cut retakes from, or "make a clean cut of" a raw video. Usage - /trim-raw-video <path-to-video> [more clips...]
argument-hint: <path-to-video.MOV> [extra-clips...] [--aspect keep|9:16|1:1|16:9] [--lang en|el|...]
---

# Trim Raw Video: raw footage to a clean cut

You are a senior video editor. The input is **super-raw** talking-head footage:
the speaker says things multiple times, the crew talks over them, there are false
starts, fumbled sentences, "okay okay let's go", jokes, long dead air. Your job is
to find the *real* message buried in it and splice the best takes into one clean,
watchable video. This is a pure trim, no effects.

**Input**: `$ARGUMENTS`, one or more raw video files (later files often hold the
parts the speaker recorded separately, e.g. the ending). Treat them as one project.

If the user wants karaoke or animated subtitles instead of a plain trim, use the
`edit-reel` skill in this plugin. This skill is trim-only.

## Requirements

- `ffmpeg` and `ffprobe` on PATH (`brew install ffmpeg`, `apt install ffmpeg`, or `choco install ffmpeg`)
- Python 3.9+ with `openai-whisper` and `numpy`: `pip3 install openai-whisper numpy`
- The first Whisper run downloads the model (`medium`, about 1.5 GB). A GPU helps but is not required.

## Tools that ship with this skill

In `${CLAUDE_SKILL_DIR}/scripts/`:
- **`analyze.py`**: probe + silence + volume + Whisper transcript. Default mode
  analyses whole files; `--regions` mode re-transcribes exact windows for precise cuts.
- **`render.py`**: renders a finished video from a cut-list JSON (splice +
  loudness-match + optional re-crop + fades + concat).

All work goes in `./_trim_work/` in the current directory.

## Read this first: the rotation gotcha

Phone footage is almost always **stored landscape with a rotation flag**. `ffprobe`
stream `width`/`height` reports the *stored* size (e.g. 3840x2160) but the video
actually *displays* rotated (e.g. 2160x3840 portrait). ffmpeg auto-rotates on
decode, so your filters see the **display** size.

Consequences:
- Always use the **display** dimensions for crop math. `analyze.py` prints both.
- If the source already is the aspect the user asked for (e.g. a 9:16 phone video
  and they ask for a "9:16 reel"), **do not crop**. Cropping into it just zooms
  and re-frames. Tell the user it is already that aspect and keep the full frame.
- `render.py` handles this automatically; just don't fight it.

## Pipeline

### Step 1: Scope it with the user
Before any work, confirm (one `AskUserQuestion` round):
1. **Output frame**: keep the original frame (default), or re-crop to 9:16 / 1:1 /
   16:9. First check the source's real aspect (Step 2) so you don't offer a crop
   that is a no-op.
2. **Language** spoken (drives the Whisper model). Pass it as an ISO code: `en`, `el`, `es`, ...
3. **Pacing**: pure trim (cut retakes and chatter, keep natural delivery) vs also
   tighten internal pauses.
4. If multiple files: confirm they are one project and the intended order.

Tell the user you will show a proposed cut list for approval before rendering.

### Step 2: Analyze
```
python3 ${CLAUDE_SKILL_DIR}/scripts/analyze.py <video> [<video2> ...] --lang <lang>
```
This writes `_trim_work/report.txt` (read it) and `<tag>.transcript.json` per file.
The report gives: stored vs **display** size + rotation, fps, duration, the
**voiced median level and loud spikes**, silence gaps, and the full transcript with
each segment's `avg_logprob`.

The model defaults to `medium.en` for English and `medium` for every other language.
Override with `--model large-v3` (or any Whisper model name) when the language is
less common or the audio is noisy.

### Step 3: Classify every segment
Read the transcript and label each segment:
- **SCRIPT**: a real line of the intended message.
- **CHATTER**: not the script. Tells: greetings, names, direction ("come here",
  "let's go", "from the top"), jokes, "okay / okay okay / it's okay", counting in,
  reactions. On messy or non-English audio Whisper often emits **garbled nonsense
  or repeated filler** ("blah blah blah", "oh oh oh"). That is almost always chatter
  or a blown take. Loud spikes from the report frequently line up with crew banter.
- **RETAKE**: the same script line again. Group all takes of each line.
- **FLUB**: a script line started then abandoned: incomplete, incoherent, a visible
  stumble, or a sentence whose words don't parse.

### Step 4: Reconstruct the script
Write out the intended message as an ordered list of **beats** (lines). Under each
beat list every take with its timecode and source file. Material is often spread
across files: one clip has the intro, another the ending.

### Step 5: Pick the best take per beat
You usually cannot hear the audio, so judge from signals:
- **Completeness and coherence**: the take that says the whole line, grammatically.
- **`avg_logprob`**: closer to 0 = clearer; very negative = mumbled or noisy.
- **Volume**: avoid takes overlapping loud spikes (often frustration or a crew
  reaction); avoid takes right next to a flub.
- **Continuity**: prefer a take that flows cleanly into the next beat; if two
  consecutive beats sit in one unbroken take, keep them as one segment.
- **Later and last**: when the speaker repeats a line, later takes are usually
  warmer; the *last* clean take is the usual keeper.
- Do **not** "fix" a non-native speaker's phrasing. Their natural wording in the
  best take is authentic; surface it, don't mangle the cut to paper over it.

### Step 6: Nail precise boundaries
Full-file timestamps drift. For each chosen take, re-transcribe its window:
```
python3 ${CLAUDE_SKILL_DIR}/scripts/analyze.py --regions "<video>@<start>-<end>" --lang <lang>
```
Use the printed word timings to set cuts: start ~0.12-0.18s before the first word,
end ~0.12-0.18s after the last word. If a boundary is ambiguous (is that first blip
real speech or a breath or noise?), extract a tiny clip and transcribe just that to
settle it. Keep natural sentence pauses inside a beat; only split a beat if there is
a flub mid-beat. For "tighten pauses", trim internal silences over ~0.6s down to ~0.3s
at sentence boundaries, never mid-word.

### Step 7: Build the cut list
Write `_trim_work/cutlist.json` (schema in `render.py`'s header). `segments` is the
ordered keep-list of `{src, start, end}`. Set `aspect` ("keep" unless re-cropping),
`fps`/`scale` only if changing them, and `loudness` (-16, important: it matches
levels across source files recorded at different gains).

### Step 8: Get approval
Show the user the reconstructed script, the segment list with timecodes, and the
estimated final length. The clean assembly is **however long it is**. Never
promise a target length you can only hit by cutting real content. Get a yes (and
any take swaps or order changes) before rendering.

### Step 9: Render
```
python3 ${CLAUDE_SKILL_DIR}/scripts/render.py _trim_work/cutlist.json
```
It frame-accurately seeks each segment, loudness-matches, applies any crop or scale,
adds gentle in/out fades, and concatenates into the `output` file.

### Step 10: Verify
- Re-run `analyze.py` on the finished file (or transcribe its audio) and confirm it
  reads as the intended script with **no chatter** leaked in.
- Extract frames at the cut points and view them. Check framing and that no bad
  take bled through.
- Report: raw duration to final duration, number of segments, what was cut.

## Hard-won rules
1. **Rotation**: use display dimensions; never crop a video into the aspect it
   already is.
2. **`condition_on_previous_text=False`** in Whisper stops hallucinations bleeding
   across the messy retake regions (`analyze.py` already does this).
3. **Loudness-match every segment**: clips from different source files (or different
   recording sessions) have different gain; `loudnorm` per segment fixes it.
4. **Re-transcribe chosen takes in isolation** for boundaries. Full-file timestamps
   are loose, especially on the first word of a clip.
5. **Keep the last clean take** when a line is repeated.
6. **Hard cuts at silence**: splice where speech has stopped and the joins disappear.
7. **Always get cut-list approval** before rendering. Take choices are judgement
   calls; let the user veto.
8. **Pure trim**: no zooms, SFX, music, or overlays. Cut, match levels, fade in/out.
9. **Don't over-promise length**: report the real assembled duration honestly.
