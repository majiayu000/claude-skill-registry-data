---
name: whatsapp-voice
description: "Transcribe WhatsApp voice messages using local Whisper CLI. Use when: owner or contact sends an audio/ogg voice message. Combines Whisper transcription + CRM update + task creation. Works offline for short clips, uses OpenAI API for long clips. Hebrew and English supported."
---

# WhatsApp Voice — Use-Case Skill

This is a **use-case** skill, not a standalone integration. It combines:
- **openai-whisper CLI** — transcription
- **personal-crm** — update contact's Last Topic if a person is mentioned
- **monday / task tracker** — save task if needed

---

## Transcription Strategy (Auto-Select by Duration)

Select model based on audio length:

| Tier | Model | When | Est. Time |
|---|---|---|---|
| 1 — Fast | `tiny` (local) | ≤ 15 seconds | 5-15s |
| 2 — Balanced | `small` (local) | 15-60 seconds | 30-90s |
| 3 — Accurate | OpenAI Whisper API | > 60 seconds | 2-5s |

### Auto-Select Script

```bash
#!/bin/bash
FILE="$1"

# Get duration
DURATION=$(ffprobe -v quiet -show_entries format=duration -of csv=p=0 "$FILE" 2>/dev/null | cut -d. -f1)
DURATION=${DURATION:-0}

if [ "$DURATION" -le 15 ]; then
  MODEL="tiny"; TIMEOUT=30
elif [ "$DURATION" -le 60 ]; then
  MODEL="small"; TIMEOUT=120
else
  USE_API=true
fi

if [ "${USE_API:-false}" = true ]; then
  RESULT=$(curl -s https://api.openai.com/v1/audio/transcriptions \
    -H "Authorization: Bearer $OPENAI_API_KEY" \
    -F file="@$FILE" \
    -F model="whisper-1" \
    -F language="he" \
    | jq -r '.text')
else
  OUTDIR="/tmp/whisper-$$"
  mkdir -p "$OUTDIR"
  whisper "$FILE" --model "$MODEL" --language he --output_format txt --output_dir "$OUTDIR" 2>/dev/null
  RESULT=$(cat "$OUTDIR/"*.txt 2>/dev/null)

  # If tiny returned too few words, retry with small
  WORD_COUNT=$(echo "$RESULT" | wc -w)
  if [ "$MODEL" = "tiny" ] && [ "$WORD_COUNT" -le 1 ]; then
    whisper "$FILE" --model small --language he --output_format txt --output_dir "$OUTDIR" 2>/dev/null
    RESULT=$(cat "$OUTDIR/"*.txt 2>/dev/null)
  fi
fi

echo "$RESULT"
```

---

## Installation

```bash
# Install Whisper CLI (local)
pip install openai-whisper

# ffprobe for duration detection
apt install ffmpeg   # Linux
brew install ffmpeg  # macOS
```

Models download automatically to `~/.cache/whisper/` on first run.

---

## Full Use-Case Flow: Voice → CRM → monday

When owner sends a voice message:

1. **Transcribe** (Whisper) — convert OGG to text
2. **Identify intent** — read the text, understand what's needed
3. **If a person is mentioned** (personal-crm) — search CRM board, update Last Topic
4. **If a task is needed** — create item in monday Task Tracker
5. **Execute** — do what was asked

```
Voice OGG → [Whisper] → Text → [Intent] → [CRM update] + [monday task] + [execute]
```

---

## Hebrew-Specific Notes

- Always pass `--language he` — auto-detect often defaults to English
- Names and technical terms may be transcribed phonetically
- `small` model handles natural Hebrew speech well

---

## Known Issues

- FP16 warning on CPU = expected, not an error
- Clips < 2 seconds may hallucinate — ask to re-record
- No GPU = slow. OpenAI API is the fast path for long clips (~$0.006/min)

---

## File Location (OpenClaw)

WhatsApp inbound media:
```
/path/to/openclaw/media/inbound/<uuid>.ogg
```
File path is in system metadata for each inbound media attachment.
