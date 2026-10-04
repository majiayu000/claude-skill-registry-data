---
name: media-transcription-report
description: Use when transcribing audio or video into timestamped Markdown with optional WhisperX speaker diarization, selecting large-v2 or medium fallback models, and turning transcripts or chat/source notes into neutral third-person Markdown, LaTeX, and PDF reports without exposing private source context.
triggers:
  - transcribe audio
  - transcribe video
  - latest audio to markdown
  - latest video to markdown
  - WhisperX diarization
  - speaker info transcript
  - transcript to report
  - chat notes to report
  - neutral third-person report
  - markdown tex pdf report
---

# Media Transcription Report

Use this skill when local audio/video needs to become a clean transcript, or when transcripts and source notes need to become a neutral report in Markdown, TeX, and PDF.

## Core Rules

- Preserve original media. Copy external files into the project when needed, but do not delete or overwrite originals.
- Prefer the user's requested model and language. Default to Whisper/WhisperX `large-v2` and Chinese (`zh`) when requested; fall back to `medium` and `int8` compute if GPU memory fails.
- Treat speaker labels as optional. If the user asks for speaker info, use WhisperX diarization when credentials and models are available; otherwise produce the transcript immediately and record the speaker-info blocker in the work notes.
- Write public reports as independent third-person documents. Do not mention the chat, recording, transcript, prompt, user request, AI generation, or private working context unless the user explicitly asks for that disclosure.
- Keep raw transcripts, private notes, TeX, figures, and PDFs separated so public artifacts can be shared without leaking source material.
- Validate with actual files: transcript exists, timestamps render, TeX compiles, PDF opens, and generated figures or diagrams do not overlap.

## Recommended Layout

Use the project layout when it already exists. Otherwise create a compact structure:

```text
audio/                         # copied or extracted audio
video/                         # copied videos when needed
text/                          # timestamped transcript Markdown/TXT/JSON
reports/<slug>/                # public report package
reports/<slug>/figures/        # PNG/SVG/PDF figures
reports/<slug>/private/        # source notes not meant for publication
```

Do not commit large media by default. Commit reusable scripts, Markdown, TeX, figures, PDFs, and private handoff notes only when the user or repo convention asks for them.

## Media Intake

Find the newest local media file when the user says "latest" or "new":

```bash
find . -path ./.git -prune -o -type f \( \
  -iname '*.m4a' -o -iname '*.mp3' -o -iname '*.wav' -o -iname '*.flac' -o \
  -iname '*.mp4' -o -iname '*.mov' -o -iname '*.mkv' -o -iname '*.webm' \
\) -printf '%T@ %p\n' | sort -nr | head -1
```

Inspect before processing:

```bash
ffprobe -hide_banner "$MEDIA"
nvidia-smi || true
git status --short
```

For video, extract mono 16 kHz audio for transcription:

```bash
mkdir -p audio
ffmpeg -y -i "$MEDIA" -vn -ac 1 -ar 16000 "audio/${STEM}.wav"
```

For audio, copy into `audio/` when it comes from another folder:

```bash
mkdir -p audio
cp -n "$MEDIA" "audio/${STEM}${EXT}"
```

## Transcription

Prefer existing project scripts if they already implement the local conventions. Otherwise use WhisperX first because it supports alignment and diarization.

Without speaker labels:

```bash
mkdir -p "text/${STEM}.whisperx"
conda run -n whisperx whisperx "$AUDIO" \
  --model large-v2 \
  --language zh \
  --task transcribe \
  --output_dir "text/${STEM}.whisperx" \
  --output_format json
```

With speaker labels:

```bash
mkdir -p "text/${STEM}.whisperx"
conda run -n whisperx whisperx "$AUDIO" \
  --model large-v2 \
  --language zh \
  --task transcribe \
  --diarize \
  --hf_token "$HF_TOKEN" \
  --output_dir "text/${STEM}.whisperx" \
  --output_format json
```

If GPU memory fails, retry with a smaller model or lower precision:

```bash
conda run -n whisperx whisperx "$AUDIO" \
  --model medium \
  --language zh \
  --task transcribe \
  --compute_type int8 \
  --output_dir "text/${STEM}.whisperx" \
  --output_format json
```

Fallback to Whisper when WhisperX is unavailable:

```bash
conda run -n whisper whisper "$AUDIO" \
  --model large-v2 \
  --language Chinese \
  --task transcribe \
  --output_dir "text/${STEM}.whisper" \
  --output_format json
```

Long jobs should run in tmux or another observable session. Record the exact command and poll logs until output files are written.

## Timestamped Markdown

Convert JSON with a real JSON parser, not ad hoc text splitting. Prefer segment start/end timestamps. Speaker labels should appear only when diarization was requested and verified.

Transcript header:

```markdown
# <Clean Title>

- Source file: `<filename>`
- Language: Chinese
- Model: `large-v2`
- Speaker labels: yes/no

## Transcript
```

Without speakers:

```markdown
[00:01:12-00:01:20] The transcribed sentence goes here.
```

With speakers:

```markdown
[00:01:12-00:01:20] Speaker 1: The transcribed sentence goes here.
```

For Chinese transcripts, keep readable paragraph grouping. Merge very short adjacent segments from the same speaker only when the timestamp range remains accurate.

## Neutral Report From Transcript Or Chat Notes

Use transcripts, chat messages, and private briefs only as source material. The published report must read like a standalone third-person document.

Write:

- "The proposed system..."
- "The project introduces..."
- "The workflow can be implemented by..."
- "A feasible first demonstration is..."

Do not write:

- "The user said..."
- "In the recording..."
- "This chat discusses..."
- "We talked about..."
- "I generated..."
- "As an AI..."

Recommended report structure:

```markdown
# <Title>

## Abstract
## Background
## Core Proposal
## System Architecture
## Implementation Plan
## MVP Scenario
## Feasibility And Risks
## Market Or Research Context
## Next Actions
## References
```

When the report needs research, gather current sources, store citations separately, and cite them in the report. For unstable facts such as market size, prices, laws, standards, company claims, or current model/tool capabilities, verify against current primary or authoritative sources.

## TeX And PDF

Use the repo's existing TeX style if present. Otherwise create a clean TeX file with stable sectioning, readable tables, and figures that fit within margins.

Compile English-only reports with `pdflatex` or `latexmk`:

```bash
pdflatex -interaction=nonstopmode -halt-on-error report.tex
pdflatex -interaction=nonstopmode -halt-on-error report.tex
```

Compile Chinese or bilingual reports with XeLaTeX:

```bash
xelatex -interaction=nonstopmode -halt-on-error report.tex
xelatex -interaction=nonstopmode -halt-on-error report.tex
```

For figures:

- Use TikZ, Mermaid-exported SVG/PDF, Matplotlib plots, or generated PNGs when they clarify the idea.
- Keep captions neutral and publication-facing.
- Do not mention generation tools or private prompt text in the public report.
- Check figure dimensions and page previews so labels do not overlap.

## Validation Checklist

- Latest media file selection is correct and documented.
- Audio extraction or copy succeeded without overwriting originals.
- Transcript Markdown exists in `text/` and includes timestamps.
- Speaker diarization is either present, or the blocker is documented.
- Public report has no private chat, recording, prompt, or AI-process disclosure.
- Markdown, TeX, PDF, and figures are all in the expected output folder.
- TeX compiles cleanly enough for delivery; serious overfull boxes, missing references, and missing figures are fixed.
- PDF first page, key figures, and tables were visually checked.
- Git status is reviewed; only intended text/report/skill artifacts are committed.
