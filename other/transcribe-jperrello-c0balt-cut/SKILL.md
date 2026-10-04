---
name: transcribe
description: Transcribe a video/audio file to a JSON transcript with word-level timestamps using local whisper.cpp + a GGML model. Use when you have a media file and need text + word timing for downstream subtitle burning or segment ranking.
---

# transcribe

Local whisper.cpp transcription. No API calls.

## Inputs
- `input`: path to a video or audio file
- `out` (optional): output JSON path (defaults to `<input>.transcript.json`)
- `language` (optional): ISO code, default `en`

## Output
JSON shaped as:
```json
{
  "source": "<input path>",
  "language": "en",
  "words": [
    {"t0": 0.42, "t1": 0.81, "w": "hello"},
    ...
  ],
  "segments": [
    {"t0": 0.42, "t1": 4.10, "text": "Hello, welcome to the show."},
    ...
  ]
}
```

## How
1. Read `WHISPER_BIN` and `WHISPER_MODEL` from `.env`.
2. If input is video, extract 16kHz mono WAV via `ffmpeg -i <in> -ac 1 -ar 16000 -f wav -`.
3. Pipe to `whisper-cli --model "$WHISPER_MODEL" --output-json-full --no-prints -l <lang>`.
4. Parse whisper-cli's JSON; flatten tokens into `words[]`, group by segment into `segments[]`.

## Run
```
.claude/skills/transcribe/transcribe.sh <input> [out.json] [lang]
```
Idempotent: skips work if `out` is newer than `input`. Uses `--max-len 1 --split-on-word` for word-level segments; groups into sentence segments on `.!?` or every 18 words.
