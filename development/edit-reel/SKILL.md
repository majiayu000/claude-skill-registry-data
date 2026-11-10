---
name: edit-reel
description: Edit a raw talking-head video into a polished short-form reel (Instagram Reels, TikTok, YouTube Shorts) with word-by-word karaoke subtitles in any language, including English and Greek. Trims silence and retakes, crops to 9:16, adds subtle zooms, sound effects and image overlays. Use when someone wants to edit a reel, add subtitles to a talking-head video, or turn raw footage into a short. Usage - /edit-reel <path-to-video> [options]
argument-hint: <path-to-video.MOV> [--lang en] [--crop-top 20] [--no-images] [--manual-text "your script here"]
---

# Reel Editor

You are a senior short-form video editor. You will take a raw talking-head video and produce a polished reel ready for Instagram/TikTok.

**Input**: $ARGUMENTS

## Pipeline Overview

The editing pipeline has 3 passes:
1. **Trim + Crop + Scale**: Cut silence, remove retakes, crop to 9:16 (object-cover, never stretch)
2. **Subtitles + Zoom + Image Overlays**: Burn karaoke-style subs, add subtle zooms and logo/image overlays
3. **Mix SFX**: Layer sound effects on key moments

## Step 1: Analyze the Video

1. Run `ffprobe` to get resolution, duration, rotation, codec info
2. Check orientation: if rotation is 90/270, the video is portrait (swap w/h)
3. Detect silence gaps with: `ffmpeg -i <input> -vn -af "silencedetect=noise=-30dB:d=0.5" -f null -`

## Step 2: Transcribe

### 2a. Determine Language

If the user provided `--lang <code>` (e.g., `--lang en`, `--lang el`, `--lang es`), use that language code directly.

Otherwise, **ask the user** which language the video is in before transcribing. Common options:
- `en`: English
- `el`: Greek
- `es`: Spanish
- `fr`: French
- `de`: German

The user can also type any [Whisper language code](https://github.com/openai/whisper#available-models-and-languages).

### 2b. Download Whisper Model (if needed)

The Whisper medium model (~1.5 GB) must be downloaded before first use. **Download it as a separate step** before transcribing, so the user can see progress and it doesn't timeout during transcription:

```python
import whisper
print("Downloading Whisper medium model (this may take a few minutes on first run)...")
model = whisper.load_model("medium")
print("Model ready.")
```

Run this in a script with a generous timeout (5+ minutes). If the download fails or times out, retry, the download resumes from where it left off.

### 2c. Transcribe

```python
result = model.transcribe(audio_path, language=LANG_CODE, word_timestamps=True, condition_on_previous_text=True)
```

Save transcript to `transcript.json` in the same directory. Print the full transcript and word timestamps for review.

## Step 3: Proofread the Transcription

**CRITICAL**: Whisper makes mistakes, especially with:
- Brand/tool names in any language (e.g., "Cloud Code" → "Claude Code", "CacheSource" → "Cursor", "Super Base" → "Supabase")
- Homophones and near-misses (e.g., "lucky" → "lowkey", "dragon" → "dragging")
- Spelling errors in the target language
- Merged or split words

Review the transcript yourself and fix obvious errors. If you're unsure about a specific word (especially a tool/brand name), **ask the user** before proceeding.

If the user provides `--manual-text`, use their exact text instead of Whisper's output, but still use Whisper's word timestamps for timing alignment.

## Step 4: Build Segments & Timed Words

Based on the silence detection and word timestamps:

1. Define `KEEP_SEGMENTS`: list of `(start, end)` tuples of audio to keep
   - Cut silence gaps > 0.5s between sentences
   - When the speaker repeats themselves, keep only the LAST take
   - Use tight boundaries: end segments right when speech ends, don't include trailing silence
   - Start segments just before speech begins (~0.05s padding)

2. Define `TIMED_WORDS`: list of `(word, start, end)` with the CORRECTED text mapped to Whisper timestamps

3. Recalculate all timestamps relative to the trimmed output

## Step 5: Configure Effects

### Subtitles (Karaoke Style)
- Font: Manrope Bold (search for `Manrope-Bold.otf` or `Manrope-Bold.ttf` in system/user font directories, or download from Google Fonts if not installed)
- Font size: 72px (at 1080 width)
- Style: **Sentence case** (never ALL CAPS)
- Colors: White (inactive) + Gold/Yellow `(255, 200, 0)` (active word highlight)
- Outline: 5px black outline, no background pill
- Extra bold: Double-draw technique (9 passes with 1px offsets)
- Position: 72% from top
- Words per group: 2 (keeps text fitting on one line)

### Zoom Effects (Subtle)
- Maximum 5 zoom triggers per video
- Zoom factor: 1.08–1.10x (never more than 1.12x: avoid making viewer dizzy)
- Duration: 0.35–0.45s per zoom
- Easing: Ease-in (sqrt) to peak at 30%, ease-out (quadratic) to end
- Trigger on: Key reveals, surprising numbers, strong statements, CTAs

### Sound Effects
- **NEVER repeat the same SFX file twice in one video**
- This skill ships with SFX in `${CLAUDE_SKILL_DIR}/audios/` (the `audios/` folder next to this SKILL.md). Pick by meaning:
  - `trimmed_whoosh.mp3`: transitions, reveals
  - `trimmed_cash.mp3`: money, prices
  - `trimmed_fah.mp3`: emphasis, strong statements (comedic, skip on serious videos)
  - `trimmed_click.mp3`: tool mentions
  - `trimmed_bubble_pop.mp3`: light reveals
  - `trimmed_riser.mp3`: builds, anticipation
  - `sfx_pop.mp3`, `sfx_thock.mp3`: small soft accents under a word
  - `sfx_swish.mp3`: soft transition
  - `sfx_thud.mp3`, `sfx_subdrop.mp3`: weight on a big statement or a number
  - `sfx_shimmer.mp3`: something new, magical, "look at this"
  - `sfx_rise.mp3`: build before a reveal (starts 1.4s before the word)
  - `sfx_ding.mp3`, `sfx_success.mp3`, `sfx_fanfare.mp3`: correct, done, a win
  - `sfx_buzzer.mp3`, `sfx_alert.mp3`, `sfx_undo.mp3`: wrong, warning, a mistake
  - `sfx_tick.mp3`: countdowns, deadlines
  - `sfx_swoop_up.mp3`: something going up (growth, a level up)
  The `sfx_*` files are generated by `${CLAUDE_SKILL_DIR}/scripts/make-sfx.py` (CC0). If the folder is ever missing them, run that script.
- **Locating SFX**, in this order:
  1. `${CLAUDE_SKILL_DIR}/audios/` (bundled)
  2. An `audios/` folder next to the video (the user's own SFX win when they match the moment)
- If new untrimmed audio files exist, trim leading silence first:
  ```
  ffmpeg -i input.mp3 -ss <silence_end> -acodec libmp3lame -q:a 2 trimmed_output.mp3
  ```
- Volume: 0.15–0.20 (subtle, never overpower voice)
- Trigger on: Tool names, key numbers, strong moments, transitions

### Image Overlays
- Image sources, in this order:
  1. A folder the user names in the command, plus its `images/` subfolder.
  2. An `images/` folder next to the video.
  3. An asset library the user keeps for all their reels, if they mention one (for example `~/Movies/assets/`). Ask for its path once; use it when the user says "find an asset that fits" or mentions a tool that has a matching file (e.g. `cursor.png`).
- Prefer the user's folder over the library when both have a match.
- List the images you plan to use before burning them in, so the user can confirm or swap.
- Display above the speaker's head area (centered, ~15% from top)
- Logo size: 200px max
- Meme/screenshot size: 500px max
- Animation: Pop-in (ease-out over first 15%) and pop-out (over last 15%)
- Duration: 1.8–2.5s per image
- Trigger on: When the speaker mentions the tool/concept the image represents
- Each image triggers only once
- Convert SVGs to PNG first if needed (use `cairosvg`)

## Step 6: Video Processing

### Crop (Object-Cover, Never Stretch)
- Target: 1080x1920 (9:16)
- If `--crop-top N` is specified, remove N% from the top before fitting
- Always crop to fit the target ratio (like CSS `object-fit: cover`), never scale-to-fit (which would stretch/distort)
- Center the crop horizontally; for vertical, bias toward bottom-center (keep the speaker's face)

### Processing Pipeline (Python + ffmpeg + Pillow)

**Pass 1: Trim + Crop + Scale (ffmpeg)**
- Build a complex filter: trim each segment, concat, crop to 9:16, scale to 1080x1920
- Concat uses interleaved stream ordering: `[v0][a0][v1][a1]...concat=n=N:v=1:a=1`
- Output: temp_trimmed.mp4 (libx264, crf 18, aac 192k, 30fps)

**Pass 2: Subtitles + Zoom + Images (Pillow frame-by-frame)**
- Decode trimmed video to raw RGBA frames via ffmpeg pipe
- For each frame:
  1. Apply zoom effect if active (center-crop + resize)
  2. Composite image overlay if active (with pop animation)
  3. Composite subtitle overlay
- Encode back to mp4 via ffmpeg pipe

**Pass 3: Mix SFX (ffmpeg)**
- Overlay all SFX using `adelay` + `amix` filter
- Use `normalize=0` to prevent volume pumping
- Copy video stream, re-encode audio only

### Output
- Save as `final_<name>.mp4` in the same directory as the input
- Print summary: original duration → final duration, number of effects applied
- Clean up temp files

## Important Rules

1. **Never stretch video**: always crop to fit (object-cover behavior)
2. **Proofread before burning subtitles**: Whisper WILL get tool names wrong
3. **Ask the user** if unsure about a word, especially brand/tool names
4. **Sentence case only**: never ALL CAPS subtitles
5. **No background pill** behind subtitles: outline only
6. **Unique SFX**: never use the same sound file twice in one video
7. **Subtle zooms**: 1.08-1.10x max, 5 per video max
8. **Tight cuts**: trim silence aggressively, the reel should feel fast-paced
9. **Cache transcript**: if `transcript.json` exists, reuse it (skip re-transcription)
10. **Keep the last take**: when the speaker repeats, always keep the final version
