---
name: use-local-whisper
description: "Transcribe audio or video on your own machine with Whisper (mlx-whisper, faster-whisper or whisper.cpp) and get word-level timestamps as words.json, a plain .txt and an .srt. No API key, nothing uploaded. This is the transcription step the editing skills (edit-style, longform-edit, reel-captions) depend on. Use when asked to transcribe a take, get word timings, make an SRT, re-transcribe a final render for a caption sync check, or 'run whisper locally'."
author: Johann (@johannships)
version: 2.0.0
---

# Use local Whisper

One script, three backends, one output format. Everything downstream (cut
lists, caption timing, sync gates) reads `<stem>.words.json`:

```json
[
{"w": "Your", "s": 0.02, "e": 0.27},
{"w": "AI", "s": 0.27, "e": 0.4}
]
```

`w` = word as heard, `s`/`e` = start/end in seconds.

## Requirements (Claude Code, on a computer)

- `ffmpeg` (any build): `brew install ffmpeg` / `apt install ffmpeg`
- Python 3.9+
- One backend:

| backend | install | default model | use it when |
|---|---|---|---|
| `mlx` | `pip install mlx-whisper` | `mlx-community/whisper-large-v3-turbo` | Apple Silicon. Best word TIMING of the three |
| `faster-whisper` | `pip install faster-whisper` | `large-v3-turbo` | Linux/Windows, or CUDA |
| `whisper-cpp` | `brew install whisper-cpp` (binary is `whisper-cli`) | none, pass `--model` | no Python ML stack wanted |

whisper.cpp model download (466 MB, English):

```bash
mkdir -p ~/whisper-models
curl -L -o ~/whisper-models/ggml-small.en.bin \
  https://huggingface.co/ggerganov/whisper.cpp/resolve/main/ggml-small.en.bin
```

Install check (prints which backend `auto` would use):

```bash
ffmpeg -version | head -1
python3 -c "import mlx_whisper" 2>/dev/null && echo mlx || \
python3 -c "import faster_whisper" 2>/dev/null && echo faster-whisper || \
command -v whisper-cli || echo "NO BACKEND: install one from the table"
```

Not available on Claude.ai (no shell). There, ask the user to upload an SRT instead.

## Run it

```bash
python3 scripts/transcribe.py take.mov                       # auto backend, English
python3 scripts/transcribe.py take.mov --backend whisper-cpp --model ~/whisper-models/ggml-small.en.bin
python3 scripts/transcribe.py final.mp4 --out qa/ --words-per-cue 2
python3 scripts/transcribe.py interview.m4a --lang auto      # detect language
```

It extracts 16 kHz mono with ffmpeg first, so any container works (mov, mp4, m4a, wav).
Output lands next to the input unless `--out` is given:
`<stem>.words.json`, `<stem>.txt`, `<stem>.srt`.

## Which model for which job

| job | use | why |
|---|---|---|
| Caption cue TIMING, sync gates | large-v3-turbo (mlx or faster-whisper) | small models drift 0.1 to 0.4 s per word on the same audio |
| Transcript text, cut lists, retake detection | small.en or turbo | text quality is close; small.en is fast on CPU |
| Non-English | large-v3-turbo with `--lang <code>` | `.en` models are English only |

## Rules that save a re-do

1. **Text from the script, timing from Whisper.** Whisper mishears names
   ("Cloud" for Claude). For captions, align the script's words to
   `words.json` and keep the script spelling (edit-style `tools/make_cues.py`
   does this). Keep a fix map (`{"cloud code": "Claude Code"}`) for anything
   with no script.
2. **Write numbers as digits in scripts.** Whisper emits `2,000`, not "two
   thousand", so a spelled-out script fails to align.
3. **Re-transcribe the FINAL render** for the published SRT and any sync
   check. Times from the raw take are wrong after every cut.
4. **Whisper stamps the first word near 0.00 even when speech starts later.**
   Find the real onset from audio energy before trimming the head, then
   re-transcribe the first 2 s to prove the first word survived.
5. Long files (over ~30 min): fine with all three backends; expect roughly
   real-time / 10 on Apple Silicon with turbo. Run under `nice -n 15` if
   someone is recording on the same machine.

## Failure handling

| symptom | fix |
|---|---|
| `no local Whisper found` | install one backend from the table |
| `whisper-cpp needs --model` | download a ggml model (above) or set `WHISPER_MODEL` |
| `whisper-cli not found` but it is installed | set `WHISPER_BIN=/path/to/whisper-cli` (launchd/cron PATHs often miss `/opt/homebrew/bin`) |
| empty or 0-word output | check the file has audio: `ffprobe -v error -select_streams a -show_entries stream=codec_name -of csv=p=0 FILE` |
| wrong language / gibberish | pass `--lang <code>` explicitly |
| words glued together ("2,000files") | whisper.cpp quirk on some builds; use mlx or faster-whisper for timing work |

## Output to report

```
whisper-cpp: 17 words, 5.68s -> o/take.words.json / .txt / .srt
```

Then hand the `words.json` path to the next skill (edit-style, longform-edit, reel-captions).
