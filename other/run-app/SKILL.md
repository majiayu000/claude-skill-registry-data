---
name: run-app
description: Run the ReVision server locally and smoke-test it. Use when asked to start, serve, run, or manually verify the ReVision web app, or to reproduce behavior of the / UI, /healthz, or /api/messages endpoints.
---

# Run the ReVision app

ReVision is a stdlib-only Python web server (`src/revision/`) that serves the
single-page UI and proxies `/api/messages` to the Anthropic API. Requires
Python `>=3.11`.

## Start the server

With an editable install:

```bash
python -m venv .venv && source .venv/bin/activate
pip install -e ".[dev]"
ANTHROPIC_API_KEY=sk-ant-... revision            # http://127.0.0.1:8000
```

Without installing (src layout is on the path via `PYTHONPATH`):

```bash
ANTHROPIC_API_KEY=sk-ant-... PYTHONPATH=src python -m revision.cli
```

Useful flags / env vars (see `src/revision/config.py`):

- `revision --host H --port P --model M`
- `REVISION_MODEL` (default `claude-sonnet-5`), `REVISION_HOST`, `REVISION_PORT`
- `REVISION_API_TOKEN` (bearer auth on `/api/messages`), `REVISION_RATE_LIMIT`,
  `REVISION_RATE_WINDOW`, `REVISION_TRUST_PROXY`

The server prints a warning but still starts if `ANTHROPIC_API_KEY` is unset —
`/api/messages` then returns a graceful `502` error.

## Smoke test

```bash
curl localhost:8000/                     # UI (index.html)
curl localhost:8000/healthz              # {"status": "ok"} — never calls Anthropic
curl -X POST localhost:8000/api/messages -d '{"prompt":"hi"}'
```

Errors come back as `{"error": {"message": ...}}` with status `400` (bad input),
`401` (auth), `429` (rate limit, includes `Retry-After`), or `502` (Anthropic).

## Docker

```bash
docker build -t revision . && docker run -p 8000:8000 -e ANTHROPIC_API_KEY=sk-ant-... revision
```

The image binds `0.0.0.0:8000` and has a `HEALTHCHECK` against `/healthz`.

## Notes

- Never move the API key or a direct `api.anthropic.com` call into the browser —
  the key is server-side only (`anthropic_client.py`).
- The model id is server-controlled (`config.py`), not chosen by the frontend.
