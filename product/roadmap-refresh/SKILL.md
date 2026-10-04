---
name: roadmap-refresh
description: Regenerate `docs/roadmap.md` for a repo from all specs under `docs/specs/` + their frontmatter (status, tags, pr). Produces Now/Next/Recently-shipped sections. Run after creating / shipping a spec, or at the start of a new session for orientation.
type: skill
---

# roadmap-refresh

Agent-OS-style roadmap, generated — not hand-edited.

## Usage
```bash
~/.claude/rag-index/venv/bin/python ~/.claude/rag-index/specs.py roadmap --repo <path>
```

Reads every `docs/specs/*/spec.md`, buckets by `status:` frontmatter:
- **Now** = `status: active`
- **Next** = `status: proposed`
- **Recently shipped** = last 10 under `docs/specs/archived/`

Writes to `docs/roadmap.md`. Idempotent; safe to re-run.

## When to run
- After `spec-new` or `spec-ship` (automatic future: wrap via git hook).
- At session start in an unfamiliar repo — immediately shows what's live/queued/just shipped.
- Before opening a PR that references "per the roadmap".

## Why not hand-edited
Hand-curated roadmaps rot within 2 weeks. This one is **derived state** — the spec frontmatter is the source of truth.

## Editing conventions
- To move a spec from Next → Now: edit frontmatter `status: proposed → active`, re-run.
- To retire a proposed spec: `rm -rf docs/specs/<folder>` (or archive manually), re-run.
- Tags appear next to entries when set: `tags: rag,platform`.

## See also
- `spec-new`, `spec-ship`
- `backlog-mapper` — different: that scans git/PRs, this reads spec files.
