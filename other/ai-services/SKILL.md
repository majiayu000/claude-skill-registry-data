---
name: ai-services
description: Use when the user asks to OCR an image or PDF (including tables, forms and complex layouts), transcribe an audio file, or turn text into speech, through the shared Stardust AI Services endpoint, or asks to connect an agent to the ai-services MCP server. One service covers OCR (RapidOCR or Qwen vision), ASR (Qwen3-ASR) and TTS (Qwen3-TTS).
metadata:
  requires:
    bins:
      - python3
---

# AI Services

One Access-protected service for three jobs:

| Job | Backend | Tool / command |
| --- | --- | --- |
| OCR, plain text | RapidOCR (zh + en) | `ocr_document` / `ai_services.py ocr` |
| OCR, tables and complex layouts | Qwen vision, returns Markdown | `ocr_document` with `engine="qwen"` |
| Speech to text | Qwen3-ASR | `transcribe_audio` / `ai_services.py asr` |
| Text to speech | Qwen3-TTS CustomVoice | `synthesize_speech` / `ai_services.py tts` |

- Base URL: `https://ai-services.preseen.ai`
- MCP endpoint: `https://ai-services.preseen.ai/mcp`
- REST: `GET /health`, `POST /ocr`, `POST /asr`, `POST /tts`

## Pick the path

1. If the `ai-services` MCP server is connected in this agent, call its tools
   directly (`health`, `ocr_document`, `transcribe_audio`, `synthesize_speech`).
   Binary inputs and outputs are base64, so for large files prefer the script.
2. Otherwise use the bundled client, which uploads local files directly and
   writes results to disk:

```bash
python3 "$HOME/.agents/skills/ai-services/scripts/ai_services.py" health
```

To connect an agent to the MCP server, use the endpoint above, for example in
Codex `config.toml`:

```toml
[mcp_servers.ai_services]
enabled = true
url = "https://ai-services.preseen.ai/mcp"
```

For ChatGPT, add a custom MCP plugin with the same URL and OAuth. Never put a
credential in the URL.

## OCR

Choose the engine from the document, not by habit:

- `rapidocr` (default): screenshots, receipts, scans and ordinary text. Fast,
  returns plain text with a confidence score.
- `qwen`: tables, forms, multi-column or otherwise complex layouts. A vision
  model reads each page and returns Markdown, with tables as Markdown or HTML.
  Slower; it ignores `--languages` and reads at most 20 pages per call, so pass
  `--pages` for longer PDFs.

```bash
S="$HOME/.agents/skills/ai-services/scripts/ai_services.py"
python3 "$S" ocr /abs/path/receipt.png                       # rapidocr, markdown report
python3 "$S" ocr /abs/path/report.pdf --engine qwen --pages 1-3 --format text
python3 "$S" ocr /abs/path/scan.png --format json --output /abs/path/ocr.json
```

Formats: `text` (text only), `markdown` (headings, engine, confidence, warnings;
the default), `json` (the service response). Treat low confidence and
`warnings` as uncertainty: never silently correct names, amounts, dates or
identifiers. If a table matters and rapidocr flattened it, rerun with
`--engine qwen`.

## ASR

```bash
python3 "$S" asr /abs/path/meeting.mp3 --language zh --format text
python3 "$S" asr /abs/path/call.m4a --format json --output /abs/path/call.json
```

`--language` is optional (auto-detected). `json` includes timestamped segments.
Long audio can take minutes; the service re-encodes files over 24 MB itself.

## TTS

Output is always MP3 and each request is limited to 3000 characters.

```bash
python3 "$S" tts "欢迎使用星尘智能服务。" --voice Vivian \
  --instructions "温暖、自然、语速稍慢" --output /abs/path/welcome.mp3
python3 "$S" tts --input-file /abs/path/script.txt --voice Serena --output /abs/path/narration.mp3
```

Voices: `Vivian` (default), `Serena`, `Uncle_Fu`, `Dylan`, `Eric`, `Ryan`,
`Aiden`, `Ono_Anna`, `Sohee`. `--instructions` steers tone, emotion and pacing
in plain language. For text over 3000 characters, split it at sentence
boundaries yourself, with the user's agreement, and synthesize in pieces.

The Qwen3-TTS model unloads after about five idle minutes. The first call after
that can take 2-3 minutes; the client retries once on Cloudflare's 524, so
if it still fails, wait a minute and run it again.

## Authentication

The service sits behind Cloudflare Access. The bundled client uses the shared
Stardust Access client: the first request opens a browser for company login
(an authorized `@stardust.ai` identity). The refresh token is kept in the local
owner-only store, isolated by service origin.

```bash
python3 "$S" --auth-status     # check without starting a job
python3 "$S" --logout          # remove only this service's session
```

Approved headless workloads set both `CF_ACCESS_CLIENT_ID` and
`CF_ACCESS_CLIENT_SECRET` from their secret manager. Never set only one, and
never paste either value into chat, source, logs or reports.

## Data handling

Files and text are sent to the Stardust service and its GPU backends. Do not
send material the user has not agreed to share. The service itself writes
nothing to disk beyond a temporary file that is deleted after the request
(audio re-encoding); it does not control logging on the shared GPU gateway.

## Troubleshooting

- `HTTP 401` / login loop: run `--auth-status`; sign in again if required.
- `HTTP 403 ... 1010`: Cloudflare's browser-integrity check, not a login
  failure. See `lib/stardust_access/README.md`.
- `HTTP 502 ... backend`: the GPU backend is busy or cold. Retry shortly;
  qwen OCR and TTS share GPUs with other models.
- Wrong or empty OCR: try the other engine; check `warnings` in `--format json`.
