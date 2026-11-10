---
name: sponsored-reel
description: Edit a paid sponsored or brand-deal reel to a client-ready standard. Recuts the picture without touching the voiceover, burns pill captions with a glowing hook title, picks clips by measurement, and mixes SFX at measured levels. Optional bilingual captions (native-language line with English underneath). Use for sponsored posts, UGC deliverables, brand collabs, client revisions or timestamped client notes. Usage - /sponsored-reel <path-to-cut-or-raw-video>
argument-hint: <path-to-video.mp4> [--greek] [--bilingual] [--vo <voiceover.mp3>]
---

# Sponsored Reel Editor

You are editing a **paid deliverable for a brand**. The bar is higher than an organic post: the client will review it frame by frame and send timestamped notes. Everything here comes from revisions that got signed off.

**Input**: $ARGUMENTS

---

## Requirements

- **ffmpeg** and **ffprobe** on the PATH
- **Python 3** with `Pillow` (captions), `openai-whisper` (word timestamps) and `numpy` (clip scoring): `pip install pillow openai-whisper numpy`
- **Fonts**: Manrope Bold (body captions, covers Greek), Inter Display Black and Inter Display Black Italic (hook title), and a serif italic for the hook's tail line (Georgia Italic, or Noto Serif Italic, which also covers Greek). The scripts find them in `<project>/fonts/`, then the usual system and user font folders on macOS, Linux and Windows. Override any of them with `FONT_SUB`, `FONT_HOOK`, `FONT_HOOK_ITALIC` or `FONT_SERIF` set to a file path.
- **SFX**: the shared pack at `${CLAUDE_SKILL_DIR}/../edit-reel/audios/`, or your own `audios/` folder next to the video (that one wins when present).

---

## The rule that governs everything

**Never re-time the voiceover.** Recut the picture only and re-attach the original audio untouched. Every caption timing, SFX cue and overlay is anchored to VO word timestamps, so the moment the audio shifts, every one of them breaks.

Concretely: build a new video-only track, then `-map 0:v -map 1:a` from the original. Total duration must match to the frame.

---

## Pipeline

All scripts take the project folder (the video's folder) as their first argument and read and write `work/` and `edited/` inside it.

### 1. Transcribe for timings

```python
model = whisper.load_model("medium")
r = model.transcribe(path, language="en", word_timestamps=True)   # or "el"
```

Cache to `work/vo.json`. Every downstream timing comes from these word stamps.

**Proofread the transcript.** Whisper reliably mangles brand and tool names: `clod` for Claude, `lightning` for lighting, a lowercase brand heard as a common word, and a domain like `brand.ai` split into two tokens. Apply a fixes map that replaces text **without touching timings**, and glue tokens starting with `.` onto the previous word.

### 2. Recut the picture

`python3 ${CLAUDE_SKILL_DIR}/lib/recut.py <project>`. Lay segments end to end with ffmpeg concat. Each segment is `(source, in, out, optional filter)`.

- Swapping in a reshot clip: trim it to **exactly** the slot duration it replaces.
- Need a closer view but no reshoot? Digital zoom is fine when the source is 4K and the output is 1080p, because a 1.45x crop of a 2160-wide frame is still above target resolution. Say so rather than pretending it was reshot.
- Lifting a dark shot: `eq=brightness=0.06:contrast=1.04:saturation=1.05`. Measure before and after and report the actual change. A grade is not the same as adding a light, and if the client asked for ambience lighting, tell them it is an approximation.

Print each segment's realised duration and confirm the sum.

### 3. Captions

Two named styles ship with this skill.

**Pill captions with a glowing hook title** (`lib/render_reel.py`)

Body captions:
- White text on a **translucent black rounded pill** (alpha ~150, radius ~22), never a hard outline
- Manrope Bold ~58px at 1080 wide
- High in frame, around `y = 0.20`, because the bottom third is usually a lit keyboard or busy UI
- Grouped 5 words max, split on sentence ends, no orphan tail of 1-2 words

Hook title:
- Pairs of lines per screen: **white upright caps on top, gold italic caps underneath**
- Gold is `(245, 192, 19)`, sampled from the reference look, not guessed
- Inter Display Black and Inter Display Black Italic; the tail line switches to a serif italic
- **No outline.** Each word carries a tight glow in its own colour: draw the text to a layer, blur ~9px, composite at ~85%
- **A word does not exist before it is spoken.** It appears at its timestamp, resolving from a ~14px blur over ~0.13s. Do not pre-render upcoming words at low opacity, that reads as a mistake

**Bilingual: native-language line with English underneath** (`lib/render_bilingual.py`)

- Native line (for example Greek) Manrope Bold ~60px, English translation ~40px in light grey `(214, 214, 214)` underneath, both with a thin black stroke
- The hook is carried by the subtitle itself, set in a heavier face (Inter Display Black ~70px) for the first few seconds, not by a second block of text saying the same thing
- On sections where a UI fills the frame, drop the English so the product stays visible
- The same script also does static punch-ins, pop-in image overlays, styled chat bubbles and the measured SFX mix

### 4. Zooms

Use **static punch-ins**, not animated ramps: hard cut into a tighter framing, hold, hard cut out. Values 1.08 to 1.12.

Align every cut in and out to a caption boundary or a real scene cut. A reframe landing mid-sentence looks like an error.

Find real cuts with:
```
ffmpeg -i in.mp4 -vf "select='gt(scene,0.30)',metadata=print" -an -f null -
```

### 5. SFX

This is where guessing fails. **Measure, never assume.**

Sounds come from `${CLAUDE_SKILL_DIR}/../edit-reel/audios/` (the shared pack) or an `audios/` folder next to the video. The shared pack has `trimmed_whoosh`, `trimmed_cash`, `trimmed_fah`, `trimmed_click`, `trimmed_bubble_pop`, `trimmed_riser` and generated `sfx_pop`, `sfx_swish`, `sfx_thock`, `sfx_thud`, `sfx_subdrop`, `sfx_shimmer`, `sfx_ding`, `sfx_buzzer`, `sfx_fanfare`, `sfx_tick` (all `.mp3`).

1. Find where the sound actually starts. Stock clips often have a second of silence first. One clip had its click at 1.02s, so the naive first-half-second trim was pure silence at -91 dB.
   ```
   ffmpeg -i sfx.mp3 -af "silencedetect=noise=-45dB:d=0.08" -f null -
   ```
2. Measure the trimmed slice with `volumedetect` and compute the gain needed to hit a target relative to the voice. With a VO around -18 dB RMS, transients want about -22 dB, beds about -28 dB, and an opening riser about -26 dB.
3. Apply `volume={gain}dB`, then `alimiter=limit=0.97` on the final mix.

Rules: **never the same sound twice** in one video, place them on real scene cuts, and cap at four or five. Verify by comparing RMS of the final against the source over each SFX window; a cue that adds less than ~0.5 dB is inaudible.

### 6. Blur patches

For a notification, a face or a logo you cannot show. Crop the region, Gaussian blur it, and composite through a **feathered mask** so there is no visible rectangle.

Prefer this over recropping. A crop tight enough to lose a notification can also clip the client's own headline mid-word, which looks worse than the notification did.

For photos with bystanders, a **graduated blur across the whole upper band** hides every distant face and any screen content in one move and reads as depth of field rather than censorship.

---

## Choosing clips by measurement

When handed long footage, do not eyeball it. Score every candidate window on motion and colour, drop anything too dark, and take the winner:

```python
motion = np.abs(np.diff(frames, axis=0)).mean(axis=(1,2,3))
sat    = (frames.max(axis=3) - frames.min(axis=3)).mean(axis=(1,2))
score  = 0.6 * motion/motion.max() + 0.4 * sat/sat.max()
```

On 93 seconds of game footage this picked the one stretch that opened on a neon map and cut into a colour change. Tell the client how it was chosen; it reads as craft, not luck.

---

## Filming conventions these edits assume

- Phone pointed at the laptop screen, not a clean screen capture. It reads as someone showing you a thing rather than an ad
- **Browser zoom at 150% minimum.** The single most common client note is that on-screen text is unreadable
- Hide the bookmarks bar, close unrelated tabs, dismiss notifications
- Dark room, screen as the brightest thing in frame, one warm lamp on the wall behind
- Film 2 to 3x the seconds you need

---

## Verify before you deliver

Never claim something is fixed without checking it:

- **Frame grids** at 1s intervals to review structure: `fps=1,scale=180:-1,tile=10x3`
- **Tight crops** upscaled with lanczos to judge text rendering
- **Brightness** before and after any grade, as numbers
- **Audio RMS** of final vs source per SFX window
- **Duration** matches the source to the frame

---

## What ships with this skill

```
lib/recut.py              picture-only recut, audio re-attached untouched
lib/render_reel.py        pill captions + glowing hook title
lib/render_bilingual.py   native-language captions with English underneath, punch-ins, overlays, SFX mix
lib/fonts.py              font lookup (project fonts/, system folders, env overrides)
```

Run each as `python3 ${CLAUDE_SKILL_DIR}/lib/<script>.py <project-dir>`. The timings, hook words and segment lists at the top of each file are a worked example; replace them with the values for your video before running. They are working code, not pseudocode.

---

## Options

- `--greek` transcribe with `language="el"` (any Whisper language code works the same way)
- `--bilingual` English translation under the native-language line, ~40px in light grey, with the native line at ~60px above it. On sections where a UI fills the frame, drop the English so the product stays visible
- `--vo <file>` when the voiceover was recorded separately

---

## What not to do

- Do not re-time or re-record the VO to fit the picture
- Do not use animated zoom ramps
- Do not put a black outline on the hook title
- Do not show words before they are spoken
- Do not repeat an SFX file
- Do not guess SFX volumes as bare multipliers
- Do not publish real DM screenshots or anything that fabricates evidence; use styled text bubbles instead
