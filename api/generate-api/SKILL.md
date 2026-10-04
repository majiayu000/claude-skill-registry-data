---
name: generate-api
description: Regenerate the frontend TypeScript API client after backend API changes (FastAPI endpoints, request/response models). Exports the OpenAPI schema and runs orval.
---

After any change to backend REST endpoints or their request/response models:

1. Run `bash scripts/generate-api.sh` from the repo root (exports `openapi.json` via `scripts/export_openapi.py`, then runs orval → `frontend/src/lib/api/index.ts`).
2. Check `git diff frontend/src/lib/api/` — confirm the generated changes match the backend change you made.
3. Run `cd frontend && bun run check` to catch type breakage in frontend code that consumes the regenerated client.
4. Fix any frontend call sites broken by the API change.

Note: `frontend/src/lib/api/index.ts` is generated — never edit it by hand (it is also excluded from eslint/prettier). The custom fetch wrapper lives in `frontend/src/lib/api/fetcher.ts` and is hand-maintained.
