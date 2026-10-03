---
name: add-subtitles
description: Add burned-in subtitles to a video the user uploads or points to on disk. Use when the user provides a local video file (mp4/mov/etc.) and wants captions/subtitles added to it. Transcribes the audio with Whisper and burns styled captions directly into the video.
allowed-tools: Bash,Read,Write,Glob
---

# Add Subtitles to a Video

Take a video the user uploads (or a path to a local file) and produce a new video
with styled, burned-in subtitles — ready for social media. Audio is transcribed
automatically with Whisper, so no transcript or YouTube source is required.

This skill reuses `burn_subtitles.py` from the `get-y2b-clips` skill, but is scoped
to the single task of subtitling an already-provided video file.

## When to Use This Skill

Activate when the user:
- Uploads or references a local video file and asks to "add subtitles" / "add captions"
- Wants a subtitled / captioned version of an existing clip for social media
- Has a video (not a YouTube URL) and wants burned-in text

If the user provides a **YouTube URL** and wants clips extracted, use `get-y2b-clips`
instead. This skill is for a video the user already has.

## Dependencies Check

**ALWAYS check dependencies first:**

```bash
# ffmpeg is required to burn subtitles
command -v ffmpeg || echo "MISSING: ffmpeg"

# stable-ts (Whisper) is required to transcribe the audio
python3 -c "import stable_whisper" 2>/dev/null && echo "stable-ts OK" || echo "MISSING: stable-ts"
```

### Install Missing Dependencies

**ffmpeg:**
```bash
# macOS
brew install ffmpeg
# Linux
sudo apt update && sudo apt install -y ffmpeg
```

**stable-ts (Whisper):**
```bash
pip3 install stable-ts
```

## Input Requirements

- **Required**: Path to a local video file (e.g. `./videos/my-clip.mp4`)
- **Optional** (ask only if relevant):
  - Font size (default: 24)
  - Whisper model size — `tiny`/`base`/`small`/`medium`/`large` (default: `base`).
    Suggest `small` or `medium` for higher accuracy on longer or harder audio.
  - Output path (default: same folder, `<name> Subtitled.mp4`)
  - Whether to keep the generated `.srt` file (default: no)

### Locating the uploaded video

If the user uploaded a file but didn't give a path, look for it:

```bash
# Common locations for an uploaded/provided video
ls -la ./videos/ 2>/dev/null
find . -maxdepth 3 -type f \( -iname "*.mp4" -o -iname "*.mov" -o -iname "*.mkv" -o -iname "*.webm" \) -mmin -120 2>/dev/null
```

If multiple candidates exist, confirm which file with the user before proceeding.

## Workflow

### Step 1: Confirm the input

```bash
VIDEO="./videos/my-clip.mp4"   # path the user provided / you located

# Verify it exists and inspect basic info
test -f "$VIDEO" && echo "Found: $VIDEO" || echo "NOT FOUND: $VIDEO"
ffprobe -v error -show_entries format=duration,size -of default=noprint_wrappers=1 "$VIDEO"
```

### Step 2: Choose the output path

```bash
DIR=$(dirname "$VIDEO")
BASE=$(basename "$VIDEO")
NAME="${BASE%.*}"
OUTPUT="$DIR/${NAME} Subtitled.mp4"
echo "Output: $OUTPUT"
```

### Step 3: Transcribe + burn subtitles (one command)

`burn_subtitles.py` defaults to Whisper mode: it transcribes the video's audio for
accurate word-level timing, then burns the captions in with ffmpeg.

```bash
python3 .claude/skills/add-subtitles/burn_subtitles.py \
    --video "$VIDEO" \
    --output "$OUTPUT" \
    --whisper-model base \
    --font-size 24
```

Useful flags:
```bash
--whisper-model small   # higher accuracy (slower); also: tiny/base/medium/large
--font-size 28          # larger captions
--keep-srt              # also write the .srt next to the output (for editing/reuse)
```

**What it does:**
1. Transcribes the audio with Whisper (stable-ts) for accurate word-level timestamps
2. Groups words into readable subtitle blocks with sensible display durations
3. Burns them into the video with styling:
   - Large readable font (default 24pt)
   - White text, black outline, semi-transparent background box
   - Bottom-center positioning

### Step 4: Report the result

Show the user:
- Output file path and size
- Whisper model used
- Number of subtitle blocks created (printed by the script)

## Console Progress Reporting

Provide clear progress updates:

```
[SETUP] Checking dependencies...
  ✓ ffmpeg found
  ✓ stable-ts found

[INPUT] Video: ./videos/my-clip.mp4 (1m 18s, 14.1 MB)

[SUBTITLES] Creating subtitled video
  Transcribing with Whisper (base model)...
  ✓ Transcribed 24 subtitle blocks (Whisper)
  ✓ Created: my-clip Subtitled.mp4 (13.8 MB)

[DONE] Subtitled video ready: ./videos/my-clip Subtitled.mp4
```

## Editing Subtitles Before Burning (optional)

If the user wants to review/fix the transcription before it's burned in:

```bash
# 1. Generate and keep the SRT, but transcription + burn happen together,
#    so to edit first, run with --keep-srt, then re-burn from the edited SRT.
python3 .claude/skills/add-subtitles/burn_subtitles.py \
    --video "$VIDEO" --output "$OUTPUT" --keep-srt
# 2. Edit the resulting "<name> Subtitled.srt"
# 3. Re-burn using ffmpeg directly with the corrected SRT:
ffmpeg -i "$VIDEO" \
  -vf "subtitles='<edited>.srt':force_style='FontSize=24,FontName=Arial,PrimaryColour=&HFFFFFF,OutlineColour=&H000000,BorderStyle=4,Outline=2,Shadow=1,MarginV=30,Alignment=2'" \
  -c:a copy -y "$OUTPUT"
```

For most requests this is unnecessary — the one-command Whisper flow is enough.

## Error Handling

| Issue | Solution |
|-------|----------|
| `MISSING: ffmpeg` | Provide install command, then retry |
| `MISSING: stable-ts` | `pip3 install stable-ts`, then retry |
| Video file not found | Ask the user for the exact path / re-locate the upload |
| Transcription inaccurate | Re-run with a larger `--whisper-model` (small/medium) |
| Subtitles out of sync | Use `--keep-srt`, adjust timings, re-burn (see section above) |
| No audio in video | Inform user — subtitles require an audio track |

## Example Session

**User**: Here's a video, can you add subtitles? `./videos/founder-take.mp4`

**Claude**:
1. Checks ffmpeg + stable-ts are installed
2. Confirms the file exists (`./videos/founder-take.mp4`, 1m 18s)
3. Runs `burn_subtitles.py` in Whisper mode → `./videos/founder-take Subtitled.mp4`
4. Reports output path, size, and subtitle block count
