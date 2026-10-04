---
name: dsh-ingest
description: "Rebuild the DSH node's persistent knowledge state. Runs register-claude.py to (re)create the dome.db schema and upsert agents/skills/tools/stack rows, then runs ingest.py to re-index kb/, logs/, docs, and agent core source into ChromaDB's dome-kb collection, then runs pre-spore-verify.py to confirm all 7 skill modules load and the akashic write+query roundtrip works. Idempotent — safe to run any time."
---

You are restoring or refreshing the DSH node's knowledge graph and agent registry. This skill is the recovery path when `db/dome.db` gets corrupted, when new KB content is added, or after an ingest-breaking dependency upgrade.

## 1. Preflight

```bash
cd "$DOME_ROOT"
test -f .venv/bin/activate || { echo "no venv — run dsh-setup first"; exit 1; }
source .venv/bin/activate
python3 -c "import sqlite3, chromadb, sentence_transformers, hashlib" || { echo "deps missing — pip install -r compute/requirements.txt"; exit 1; }
```

If the venv doesn't exist or deps are missing, stop and point the user at the `dsh-setup` skill first.

## 2. Register Claude + skills + tools in dome.db

```bash
python3 scripts/register-claude.py
```

What it does:

- Creates (if missing) tables: `sessions`, `stack`, `agents`, `skills`, `tools`
- UPSERTs the Claude agent row into `agents`
- UPSERTs 8 skill rows into `skills` (docx, pdf, pptx, xlsx, schedule, setup-cowork, skill-creator, consolidate-memory)
- UPSERTs 26 tool rows into `tools`
- Mirrors everything into `stack` as category-tagged entries

Keyed on `(category, name)` so it's safe to re-run; only the `updated_at` and descriptions change.

Verify:

```bash
sqlite3 db/dome.db "SELECT name FROM sqlite_master WHERE type='table'"    # 5+ tables
sqlite3 db/dome.db "SELECT COUNT(*) FROM agents"                          # 1
sqlite3 db/dome.db "SELECT COUNT(*) FROM skills"                          # ≥ 8
sqlite3 db/dome.db "SELECT COUNT(*) FROM tools"                           # ≥ 26
sqlite3 db/dome.db "SELECT COUNT(*) FROM stack"                           # ≥ 35
```

If the skill count is higher than 8, new skills were registered elsewhere — that's fine, the upsert doesn't delete anything.

## 3. Re-index the knowledge base

```bash
python3 scripts/ingest.py
```

What it does:

- Walks `kb/`, `logs/`, `README.md`, `INDEX.md`, `MANUAL.md`, `agents/core/`
- Accepted extensions: `.md`, `.txt`, `.py`, `.ts`, `.json`
- Skips `.venv/` and `__pycache__/`
- Chunks each file and embeds via sentence-transformers (all-MiniLM-L6-v2)
- Writes to ChromaDB namespace `dome-kb` at `db/chroma/`

The script prints a per-file chunk count and a final total. Typical fresh-install expectation: 1,800–3,700 chunks depending on how many session logs are present.

Verify:

```bash
python3 -c "
import chromadb
c = chromadb.PersistentClient('db/chroma')
print(f'dome-kb: {c.get_collection(\"dome-kb\").count()} chunks')
"
```

## 4. Akashic collection hygiene

The akashic namespace uses a specific sentence-transformer embedding function. If it was previously created with a different embedder, the `akashic:write+query` roundtrip in pre-spore-verify will fail with `Embedding function conflict`.

Check:

```bash
python3 -c "
import chromadb
c = chromadb.PersistentClient('db/chroma')
names = [col.name for col in c.list_collections()]
print('collections:', names)
"
```

If `akashic` is in the list but empty (0 chunks) AND pre-spore-verify fails on it, drop and recreate:

```bash
python3 -c "
import chromadb
c = chromadb.PersistentClient('db/chroma')
if 'akashic' in [col.name for col in c.list_collections()]:
    c.delete_collection('akashic')
    print('dropped stale akashic collection — will recreate on first write')
"
```

The next `pre-spore-verify.py` run will seed the first akashic record (test write) cleanly.

## 5. Verify everything loads

```bash
python3 scripts/pre-spore-verify.py
```

Expected output ends with:

```
═══════════════════════════════════════
  27/27 checks passed

  ✅ ALL SYSTEMS GO — READY FOR SPORE.SH
═══════════════════════════════════════
```

The 27 checks:

- 12 dependency imports (numpy, scipy, sympy, numba, torch, qiskit, pennylane, cirq, matplotlib, networkx, mpmath, pandas)
- 7 skill-module `verify()` roundtrips
- 1 akashic write+query roundtrip

## 6. Report

```
✅ dome.db: <agents>/<skills>/<tools> rows
✅ chroma/dome-kb: <N> chunks
✅ chroma/akashic: <M> chunks
✅ pre-spore-verify: 27/27
```

## Non-negotiables

- **Never run `ingest.py` from outside `$DOME_ROOT`.** It uses repo-relative paths; wrong cwd = wrong source set.
- **Never drop `dome.db`.** The schema migrations are forward-only; there's no rollback. If the file is suspected corrupt, back it up (`cp db/dome.db db/dome.db.bak.$(date +%s)`) before deleting.
- **Never drop `dome-kb` blindly.** Re-ingest takes 30+ seconds and you lose any manual records. Only delete when a schema or embedder change forces it.
- **Never commit `db/chroma/` or `db/*.db`.** Both are in `.gitignore`; they are per-node state, not code.
