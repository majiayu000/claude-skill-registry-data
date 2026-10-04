---
name: aggregate-roadmap
description: Regenerate the cross-repo roadmap aggregate in your Claude memory directory by walking every curated repo's `docs/specs/**` frontmatter. Run at session start for cross-repo orientation or after any `spec-new`/`spec-ship` in any repo.
type: skill
---

# aggregate-roadmap

Cross-repo TL;DR — one file, every curated repo's active/proposed/recently-shipped specs.

## Usage

```bash
~/.claude/rag-index/venv/bin/python ~/.claude/rag-index/aggregate_roadmap.py
```

Writes to `OUTPUT_PATH` when set, otherwise to the first `~/.claude/projects/*/memory/roadmap-all.md` directory found.
The PostToolUse hook reindexes it automatically; `rag_query "what's in flight across my repos"` finds it top-1.

## When to run

- Start of a session when you need a bird's-eye view of all active work.
- After any `spec-new` or `spec-ship` — keeps the aggregate in sync with per-repo roadmaps.
- Before planning the next sprint.

## Data source

- `CURATED_REPOS` from `~/.claude/rag-index/build.py` — **single source of truth**. Add a repo there to have it appear in aggregates.
- Spec frontmatters (`status:`, `tags:`, `pr:`) drive the buckets. Hand-editing the aggregate file gets overwritten.

## Output shape

```markdown
# Cross-repo roadmap — YYYY-MM-DD

## Lucky

### Active — …

### Proposed — …

### Recently shipped — …

## homelab

…
```

## See also

- `spec-new`, `spec-ship`, `roadmap-refresh` (per-repo).
