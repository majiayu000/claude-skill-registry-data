---
name: ck-refs-lookup
description: "Look up reference repos (read-only) through the condensed contract index instead of reading the whole repo. Run: /ck-refs-lookup <topic/type/endpoint>"
disable-model-invocation: false
---

# ck-refs-lookup

Answers questions about the **reference repos** from the condensed index at `$CK_ROOT/.claude/contextkit/cache/references/<repo>.md` — without reading the whole repo.

> If `.claude/contextkit/` is missing (script or `contextkit.config.json` not found) →
> ContextKit is not installed here: stop, and install via `/ck-setup` in the hub.

## Resolve project root

```bash
CK_ROOT="${CLAUDE_PROJECT_DIR:-}"; [ -d "$CK_ROOT/.claude/contextkit" ] || CK_ROOT="$(d="$PWD"; while [ "$d" != "/" ] && [ ! -d "$d/.claude/contextkit" ]; do d="$(dirname "$d")"; done; echo "$d")"; [ -d "$CK_ROOT/.claude/contextkit" ] || { echo "ContextKit not found: no .claude/contextkit in this directory or any parent"; exit 1; }
echo "$CK_ROOT"
```

Paths in the config are relative to `$CK_ROOT`.

## Flow

1. Read the index files: `$CK_ROOT/.claude/contextkit/cache/references/*.md`.
2. Find the matching entry (sections: Contracts / API-Specs / Parity ({platform} <-> {repo})).
3. **Check freshness** from the frontmatter (`sha`, `indexed`, `status`). Compare with the repo:
   ```bash
   CK_ROOT="${CLAUDE_PROJECT_DIR:-}"; [ -d "$CK_ROOT/.claude/contextkit" ] || CK_ROOT="$(d="$PWD"; while [ "$d" != "/" ] && [ ! -d "$d/.claude/contextkit" ]; do d="$(dirname "$d")"; done; echo "$d")"; [ -d "$CK_ROOT/.claude/contextkit" ] || { echo "ContextKit not found: no .claude/contextkit in this directory or any parent"; exit 1; }
   git -C "$CK_ROOT/<references.path>/<repo>" rev-parse --short HEAD
   ```
   - SHA **matches** and `status: indexed` → answer from the index, and cite the source as `repo@sha`.
   - SHA **differs** or `status: needs-extraction` → the index is stale: recommend `/ck-refs-sync` AND, for this question, read **only the relevant files** in the reference repo (not the whole repo). If the live fact goes beyond the question itself (a new contract signature, endpoint, or parity note) → add it to the matching section of the existing stub (a `file:line` reference, terse, as in `ck-refs-sync`). Leave `status` at `needs-extraction`, so the finding is kept.
4. A question outside contracts / API / parity → say so: not indexed. Read it live.

Paths come from `.claude/contextkit/contextkit.config.json` (`references.path` + `repos`). Keep answers short, with a `file:line` reference into the reference repo when you can. Reference repos are **read-only** — write only in the project. The cache stub under `$CK_ROOT/.claude/contextkit/cache/` belongs to the project and may be patched.
