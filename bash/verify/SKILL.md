---
name: verify
description: Run kajet-turbo locally against a temp DB and a fake embedding endpoint, then drive the REST surface (login, notes, jobs, reindex) to observe changes end-to-end.
---

# Verifying kajet-turbo at runtime

## Launch recipe (temp everything, no prod deps)

```bash
SCRATCH=$(mktemp -d)
# Fake OpenAI-compatible embeddings endpoint (returns deterministic vectors,
# ~150ms artificial delay). Any script serving POST /v1/embeddings with
# {"data":[{"index":i,"embedding":[...]}]} works; dim is probed automatically.
python3 fake_embed.py &   # port 8899

DB_PATH=$SCRATCH/kajet.db WORKSPACES_DIR=$SCRATCH/ws \
SECRET_KEY=verify-secret-key-0123456789abcdef \
KAJET_ADMIN_EMAIL=admin@test.local KAJET_ADMIN_PASSWORD=verify-pass \
MCP_BASE_URL=http://localhost:8801 MCP_PORT=8801 \
KAJET_WORKER_POLL_INTERVAL=0.25 \
uv run kajet-turbo > $SCRATCH/app.log 2>&1 &
# readiness: curl localhost:8801/readyz
```

Role `all` runs an in-process worker thread (job queue drains without a
separate worker process). `KAJET_WORKER_POLL_INTERVAL=0.25` makes deferred
jobs observable within ~1s.

## Driving the REST surface

```bash
curl -c cookies.txt -X POST :8801/api/login -d '{"email":...,"password":...}'
curl -b cookies.txt -X POST :8801/api/workspaces -d '{"name":"notes"}'
# keyless profile → probes the endpoint, captures dim, activates:
curl -b cookies.txt -X POST :8801/api/me/embedding-profiles \
  -d '{"name":"fake","base_url":"http://127.0.0.1:8899/v1","model":"fake-8"}'
curl -b cookies.txt -X POST :8801/api/workspaces/notes/notes \
  -d '{"title":"T","content":"# T\n\nbody\n"}'
```

Gotchas:
- PATCH/DELETE on notes require `expected_sha`; get it from
  `GET /api/workspaces/{ws}/notes/{id}/history` → `entries[0].sha`.
- Jobs API: `GET /api/me/jobs?kind=embed_note&status=pending`.
- There is NO REST search — search is MCP-only (`search_notes` tool), behind
  OAuth. Verifying search at runtime needs an MCP client with the OAuth dance.
- `sqlite3` CLI cannot read `note_chunks_vec_*` (vec0 virtual table); use
  `uv run python` with `sqlite_vec.load(conn)` to count vectors. Plain columns
  (`notes.index_state`, `note_chunks.dim`) read fine from sqlite3.
- Logs are JSONL in `$SCRATCH/app.log`; grep `worker_start`, `job_failed`,
  `vectors_attached`, `search_performed`.
