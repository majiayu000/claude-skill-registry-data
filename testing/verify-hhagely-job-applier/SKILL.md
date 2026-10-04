---
name: verify
description: Build, run, and drive this app (FastAPI + SvelteKit) to observe a change at its real surface. Use when verifying a diff/PR by running the app rather than by running tests.
---

# Verify (job-applier)

Runtime observation only. Don't run pytest/vitest/svelte-check here — that's CI.

## Isolate first (mandatory)

`data/jobs.db` is the user's **real** job data. Never run a dev server against it.
`config.py` derives db + resumes + applications from one env var:

```bash
export JOB_APPLIER_DATA_DIR="<scratch>/data"   # relocates DB, resumes, drafts together
uv run job-applier init                        # creates tables, seeds ~1300 slugs
```

Afterwards confirm `ls -la data/jobs.db` mtime is unchanged.

## Launch

```bash
# backend (pick a non-default port so a running instance isn't clobbered)
JOB_APPLIER_DATA_DIR=<scratch>/data \
  uv run uvicorn job_applier.api.app:app --host 127.0.0.1 --port 8010

# frontend (must be told where the backend is)
cd web && JOB_APPLIER_API_BASE=http://127.0.0.1:8010 \
  npm run dev -- --port 5175 --strictPort
```

## Seeding fixtures

- **Job postings**: no create endpoint — insert `JobPosting` rows directly.
  `engine` in `models/db.py` is a **function**, so `Session(engine())`, not `Session(engine)`.
  Set `filter_status=FilterStatus.passed` or the job is invisible to the queue/scoring.
- **Resume + scores**: use the real API, it exercises more of the app —
  `POST /api/resume` (multipart) and `POST /api/jobs/{id}/score`.
- Real PDFs to reuse for upload tests live in `data/resumes/*.pdf` (read-only copy them out).

## Driving the UI (Playwright)

`playwright` is already a dependency; `uv run python your_script.py` works.

Three gotchas, all of which cost time:

1. **Vite binds `localhost`, not `127.0.0.1`.** `curl 127.0.0.1:5175` returns nothing;
   use `http://localhost:5175`.
2. **`wait_until="networkidle"` never settles** — the layout holds an SSE connection
   open for background-task progress. Use `domcontentloaded` + `wait_for_selector`.
3. **Wait ~2s after load before `set_input_files`.** The resume upload auto-submits
   from an `onchange` handler that isn't bound until SvelteKit hydrates; setting files
   too early silently does nothing (no request, no banner). Verify a POST actually
   fired via `page.on("request", ...)` before concluding the app misbehaved.

## Surfaces worth driving

| Change touches | Drive |
| --- | --- |
| scoring / staleness | `/resume` upload → prompt; `/dashboard` Score pending |
| queue + statuses | `/` master-detail, form actions |
| drafts / PDFs | `/jobs/[id]` draft cart (needs an AI provider) |
| pure API | `curl` the endpoint, then still drive the page that calls it |

**Anything AI-backed (scoring, drafting, suggest-roles) needs a configured provider**
and spends the user's real subscription quota. Without one the app returns a clean
409 (`no AI provider selected`). Verify the error path and say plainly that the
success path went unexercised — don't burn quota to complete a happy path.
