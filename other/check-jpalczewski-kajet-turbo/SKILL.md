---
name: check
description: Run the full verification suite for kajet-turbo (backend ruff + ty + pytest, frontend prettier + eslint + svelte-check). Use before committing, after finishing a feature, or when asked to verify the codebase is healthy.
---

Run all checks from the repo root and report results. Run backend and frontend groups in parallel where possible.

Backend:
1. `uv run ruff check .`
2. `uv run ruff format --check .`
3. `uv run ty check`
4. `uv run pytest`

Frontend (in `frontend/`):
5. `bun run lint` (prettier --check + eslint)
6. `bun run check` (svelte-check)

Rules:
- Do not auto-fix anything during this skill — it is a verification pass. Report every failure with file:line.
- If a check fails, summarize the failures grouped by tool and ask whether to fix them, unless the user already asked for fixes.
- All six checks must pass to declare the codebase healthy. Never report success with skipped checks.
