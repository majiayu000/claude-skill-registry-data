---
name: test-and-lint
description: Run ReVision's test suite and lint/format checks the way CI does. Use before committing non-trivial changes, when tests or ruff fail, or when asked to validate the ReVision backend.
---

# Test, lint, and format ReVision

CI (`.github/workflows/ci.yml`) runs `ruff check`, `ruff format --check`, and
`pytest` on Python 3.11–3.13, plus a Docker build. Match it locally before
committing.

## Commands

```bash
pytest                # test suite (config in pyproject.toml: testpaths=tests, pythonpath=src)
ruff check .          # lint: rules E, F, I, UP, B, SIM, line length 100
ruff format .         # auto-format (CI runs `ruff format --check`)
```

> In some environments `pytest`/`ruff` are standalone binaries, not in the
> interpreter's site-packages. If `python -m pytest` says "No module named
> pytest", call `pytest` / `ruff` directly.

## Test layout

Tests under `tests/` mirror the module they cover (`server.py` → `test_server.py`):

- `test_config.py` — `Config.from_env()` and env-var parsing.
- `test_anthropic_client.py` — mocks `urllib.request.urlopen`; no network.
- `test_ratelimit.py` — limiter with a monkeypatched clock.
- `test_server.py` — runs a live server on port 0 with a fake injected client.

## Key testing seam

`create_server(config, client=...)` accepts an injected `AnthropicClient`, so
`test_server.py` runs a real server against a fake client with **no network**.
Preserve this seam when touching `server.py` — don't hardcode client
construction into the request path.

## Before committing

1. `ruff format .`
2. `ruff check .`
3. `pytest`

Add a test alongside any behavior change, mirroring the module you touched.
Keep the backend dependency-free (stdlib only); `pytest`/`ruff` are dev-only.
