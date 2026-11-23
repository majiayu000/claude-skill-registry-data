---
name: ck-doctor
description: "Knowledge-base hygiene: setup doctor, schema lint, rebuild the index, freshness stamp. Run: /ck-doctor"
disable-model-invocation: true
---

# ck-doctor

Keeps the "second brain" consistent. Deterministic checks run in a script; then report the findings.

> If `.claude/contextkit/` is missing (script or `contextkit.config.json` not found) →
> ContextKit is not installed here: stop, and install via `/ck-setup` in the hub.

## Resolve project root

```bash
CK_ROOT="${CLAUDE_PROJECT_DIR:-}"; [ -d "$CK_ROOT/.claude/contextkit" ] || CK_ROOT="$(d="$PWD"; while [ "$d" != "/" ] && [ ! -d "$d/.claude/contextkit" ]; do d="$(dirname "$d")"; done; echo "$d")"; [ -d "$CK_ROOT/.claude/contextkit" ] || { echo "ContextKit not found: no .claude/contextkit in this directory or any parent"; exit 1; }
echo "$CK_ROOT"
```

1. **Check the setup:**
   ```bash
   CK_ROOT="${CLAUDE_PROJECT_DIR:-}"; [ -d "$CK_ROOT/.claude/contextkit" ] || CK_ROOT="$(d="$PWD"; while [ "$d" != "/" ] && [ ! -d "$d/.claude/contextkit" ]; do d="$(dirname "$d")"; done; echo "$d")"; [ -d "$CK_ROOT/.claude/contextkit" ] || { echo "ContextKit not found: no .claude/contextkit in this directory or any parent"; exit 1; }
   python3 "$CK_ROOT/.claude/contextkit/scripts/doctor.py"
   ```
2. **Lint + index** (lint first — required fields `id` / `type` / `summary`, a valid `status`, `id` equal to the filename, dangling or one-sided `related` edges; rebuilds `INDEX.md` when the schema is clean, otherwise stops with the errors):
   ```bash
   CK_ROOT="${CLAUDE_PROJECT_DIR:-}"; [ -d "$CK_ROOT/.claude/contextkit" ] || CK_ROOT="$(d="$PWD"; while [ "$d" != "/" ] && [ ! -d "$d/.claude/contextkit" ]; do d="$(dirname "$d")"; done; echo "$d")"; [ -d "$CK_ROOT/.claude/contextkit" ] || { echo "ContextKit not found: no .claude/contextkit in this directory or any parent"; exit 1; }
   python3 "$CK_ROOT/.claude/contextkit/scripts/knowledge.py"
   ```
3. **Content** (model judgment, report only — do not rewrite in bulk without approval).
   Use this fixed rubric every session:
   - **Missing Definition of Done**: a `ticket` without a `## Definition of Done` section → add it on the next edit (see `ck-create-note`).
   - **Duplicate / overlap**: same `type` and the same topic or a similar `summary` → propose a merge. Do not merge automatically.
   - **Contradiction**: two `related` entries, or two entries on the same topic (especially `decision`s), assert opposite facts, or a decision that is not `superseded` contradicts a newer one → mark it in the findings and ask for a resolution.
   - **LOG.md as a trace**: read the last 20 `## [` headings of `<knowledgePath>/LOG.md`. The same `id` several times in a short span is a signal that the entry was created too early or is still half-formed, beyond the audit trail itself.
   (Stale `proposed` / `open`, and dangling or one-sided `related` edges, are already caught deterministically in step 2 — only sharpen the content here.)
4. **Freshness stamp + log:**
   ```bash
   CK_ROOT="${CLAUDE_PROJECT_DIR:-}"; [ -d "$CK_ROOT/.claude/contextkit" ] || CK_ROOT="$(d="$PWD"; while [ "$d" != "/" ] && [ ! -d "$d/.claude/contextkit" ]; do d="$(dirname "$d")"; done; echo "$d")"; [ -d "$CK_ROOT/.claude/contextkit" ] || { echo "ContextKit not found: no .claude/contextkit in this directory or any parent"; exit 1; }
   mkdir -p "$CK_ROOT/.claude/contextkit/cache" && date > "$CK_ROOT/.claude/contextkit/cache/.last-knowledge-check"
   python3 "$CK_ROOT/.claude/contextkit/scripts/knowledge.py" --log lint "<n> entries · <m> warnings"
   ```
