---
name: openapi-sync
description: Regenerate and verify docs/openapi/openapi.json, the FastAPI schema snapshot behind the docs site's API reference. Use after changing backend routes, parameters, request or response models, tags or endpoint summaries, when CI reports a stale OpenAPI snapshot, or when asked to refresh the API reference. Backend implementation itself belongs to backend-change.
---

# openapi-sync

The docs site renders `/docs/referencia/api` from `docs/openapi/openapi.json`
with `fumadocs-openapi`; no MDX is generated or committed. The snapshot is
exported by `backend/scripts/export_openapi.py`, which imports the app without
starting services. CI runs the exporter with `--check` in the backend job.

## Steps

1. Regenerate from the Git root:
   ```bash
   just backend openapi
   ```
   Without Docker, from `backend/`:
   `uv run --locked python scripts/export_openapi.py > ../docs/openapi/openapi.json`.
2. Review `git diff docs/openapi/openapi.json`. Every hunk must come from the
   intended contract change; an unrelated hunk means another change is already
   stale or a dependency changed schema output, so report it instead of
   committing it silently.
3. Verify:
   ```bash
   just backend openapi-check   # or: uv run --locked python scripts/export_openapi.py --check ../docs/openapi/openapi.json
   just docs build              # generated pages compile and prerender
   ```
4. Commit the snapshot with the backend change that caused it, and report the
   commands and results.

## Output

Report the operations added, removed or changed (method and path), the check
results and any unrelated drift found.

## Gotchas

- Never edit `openapi.json` by hand; improve `summary`, `description`,
  docstrings or Pydantic models in the backend and regenerate.
- Page URLs derive from method and path
  (`/docs/referencia/api/<tag>/<method>-<path>`), so renaming a route or its tag
  changes the URL; update links in `docs/content/docs` that point to it.
- The exporter de-duplicates tags repeated by `APIRouter(tags=...)` plus
  `include_router(tags=...)` and adds the local server for the playground; do not
  "fix" those differences against `/api/py/openapi.json`.
- Business rules the schema cannot express (permissions, side effects) belong
  in `docs/content/docs/referencia/` pages such as `miembros-e-invitaciones.md`.
- `openapi-check` needs Docker; a Docker error is not a stale snapshot. Use the
  `uv` variant when Docker is unavailable.
