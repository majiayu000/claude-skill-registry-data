---
name: verify-financial-development
description: >-
  Drive FinancialDevelopment the way a user does: FastAPI Quant Console
  dashboard (HTTP) plus pytest unit suite. Use when proving a dashboard,
  widget, orchestrator, or shared-module change in this repo.
---

# verify-financial-development

Primary surface: **local FastAPI dashboard** (`dashboard/app.py`) on
`http://127.0.0.1:8000`. Secondary: **pytest** (`pytest -m unit`) for
no-network proof. Do not use Playwright unless the change is pure CSS/layout
and HTTP JSON is not enough.

Windows paths below assume the checkout
`C:\Users\bottl\FinancialDevelopment` and the shared root `.venv`.

## Launch

From repo root (PowerShell):

```powershell
# once per machine
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt

# start dashboard (no --reload during verification — reload kills in-flight work)
cd dashboard
..\.venv\Scripts\python.exe -m uvicorn app:app --host 127.0.0.1 --port 8000
```

Ready when `GET http://127.0.0.1:8000/health` returns HTTP 200 (or `/` returns HTML).
Keep that process for the whole verify session.

Teardown: stop only the uvicorn PID you started (Ctrl+C in that terminal, or
kill that PID). Never `taskkill /IM python.exe`.

Isolate: bind stays on `127.0.0.1:8000`. Do not start a second instance on the
same port. If port busy, doctor fails — do not steal another user's session.

## Doctor

Read-only checks before driving:

1. `.venv\Scripts\python.exe -c "import fastapi,uvicorn; print('ok')"` exits 0.
2. `GET http://127.0.0.1:8000/health` (or `/`) is 200.
3. `GET http://127.0.0.1:8000/api/widgets/catalog` is 200 JSON (widget-native console).
4. Optional: `pytest -m unit --collect-only -q` collects without import errors.

If doctor fails, fix env / start the app before Drive.

## Drive

Prefer **HTTP** against the live app. Stable handles are route paths, not
coordinates.

Examples (PowerShell / curl):

```powershell
# liveness
curl -s -o NUL -w "%{http_code}" http://127.0.0.1:8000/health

# overview page
curl -s -o evidence\overview.html -w "%{http_code}" http://127.0.0.1:8000/

# widget catalog (Phase 7 surface)
curl -s -o evidence\widgets-catalog.json http://127.0.0.1:8000/api/widgets/catalog

# unit tests (no network) — secondary harness
..\.venv\Scripts\python.exe -m pytest -m unit -q --tb=short
```

Do **not** fire billed suite runs (`POST /run/...` or long orchestrator jobs)
unless the user explicitly asked to prove a full suite path. Prefer read-only
routes and `pytest -m unit`.

For a widget run proof (only when the change touches widgets):

```powershell
# inspect catalog for a safe slug first, then:
curl -s -X POST "http://127.0.0.1:8000/api/widgets/<slug>/run" `
  -H "Content-Type: application/json" `
  -d "{}" -o evidence\widget-run.json
```

Use a dry / unit-safe widget when possible. Capture request + response bodies.

## Evidence

Store under `.cursor/skills/verify-financial-development/evidence/` (gitignored
if needed; keep proofs local):

- `overview.html` or status codes for `GET /` and `GET /health`
- `widgets-catalog.json` for catalog
- `pytest-unit.txt` stdout/stderr for unit run
- For a feature drive: request, response body, and any side effect (DB row,
  file under a run dir) — not just “200”.

Proof standards: exercise the real user path; capture action + resulting
state; mocks only at production boundaries already isolated.

## Cleanup

1. Stop the uvicorn process you started.
2. Leave `evidence/` intact — cleanup never deletes proofs.
3. Do not delete `.venv`, `swaps.db`, or user run history.

## Helpers

No custom helper script yet. Use `curl` / `Invoke-WebRequest` and
`.\.venv\Scripts\python.exe -m pytest`.

## Feature map

See `features/README.md`. Drive at least one mapped feature per verify pass.
