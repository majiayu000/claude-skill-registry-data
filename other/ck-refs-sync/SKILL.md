---
name: ck-refs-sync
description: "Update reference repos (git pull) and rebuild the condensed contract index. Run: /ck-refs-sync"
disable-model-invocation: true
---

# ck-refs-sync

Keeps the condensed reference index current. Two parts: a script (pull + skeleton) and Claude (extraction).

> If `.claude/contextkit/` is missing (script or `contextkit.config.json` not found) →
> ContextKit is not installed here: stop, and install via `/ck-setup` in the hub.

## Resolve project root

```bash
CK_ROOT="${CLAUDE_PROJECT_DIR:-}"; [ -d "$CK_ROOT/.claude/contextkit" ] || CK_ROOT="$(d="$PWD"; while [ "$d" != "/" ] && [ ! -d "$d/.claude/contextkit" ]; do d="$(dirname "$d")"; done; echo "$d")"; [ -d "$CK_ROOT/.claude/contextkit" ] || { echo "ContextKit not found: no .claude/contextkit in this directory or any parent"; exit 1; }
echo "$CK_ROOT"
```

`{platform}` below is the `platform` value in `$CK_ROOT/.claude/contextkit/contextkit.config.json` (`generic`, `ios`, `android`, or `web`).

## Step 1 — Pull + stub refresh (script)

```bash
CK_ROOT="${CLAUDE_PROJECT_DIR:-}"; [ -d "$CK_ROOT/.claude/contextkit" ] || CK_ROOT="$(d="$PWD"; while [ "$d" != "/" ] && [ ! -d "$d/.claude/contextkit" ]; do d="$(dirname "$d")"; done; echo "$d")"; [ -d "$CK_ROOT/.claude/contextkit" ] || { echo "ContextKit not found: no .claude/contextkit in this directory or any parent"; exit 1; }
python3 "$CK_ROOT/.claude/contextkit/scripts/reindex.py"
```

Runs `git pull --ff-only` on every configured reference repo (dirty or diverged → warning, no pull), compares HEAD SHAs, and writes an index stub at `$CK_ROOT/.claude/contextkit/cache/references/<repo>.md` for **changed** repos. Unchanged repos are skipped.

## Step 2 — Extraction (Claude)

For each stub with `status: needs-extraction`:

1. Read the reference repo at `<referencesPath>/<repo>` **selectively** — only what `indexScope` covers:
   - **Contracts**: public interfaces, public types, DTOs
   - **API specs**: endpoints, routing, OpenAPI
   - **Parity ({platform} <-> {repo})**: counterparts on `{platform}`, and deliberate divergences
   No implementation detail.
2. Fill those sections in the stub. Use the heading `Parity ({platform} <-> {repo})`.
3. In the frontmatter set `status: indexed` and `indexed: <today's date>`.

> **Writing style (optimized for the model; a person does not read the index):**
> - Terse: one fact per line. No prose, filler, or repetition.
> - Point, do not copy: `file:line`, `repo@sha`. Never code blocks.
> - Only the signature, name, or path needed to find it again. No implementation detail.

## Step 3 — Freshness stamp

```bash
CK_ROOT="${CLAUDE_PROJECT_DIR:-}"; [ -d "$CK_ROOT/.claude/contextkit" ] || CK_ROOT="$(d="$PWD"; while [ "$d" != "/" ] && [ ! -d "$d/.claude/contextkit" ]; do d="$(dirname "$d")"; done; echo "$d")"; [ -d "$CK_ROOT/.claude/contextkit" ] || { echo "ContextKit not found: no .claude/contextkit in this directory or any parent"; exit 1; }
mkdir -p "$CK_ROOT/.claude/contextkit/cache" && date > "$CK_ROOT/.claude/contextkit/cache/.last-refresh"
```
