---
name: recall
description: Query the cross-provider topic-memory corpus by keyword (and optional class) instead of grepping ~180 files. Use when you need to check "what have we learned about X" before solving a problem.
when_to_use:
  - recall what we know about a topic
  - check prior lessons / feedback before implementing
  - "have we hit this before"
  - search memory / topics by keyword
---

# recall — query the topic-memory corpus

One provider-neutral mechanism (Claude / Codex / agy) to query `.claude/memory/topics/`
with identical, deterministic results. Stdlib-only; no dependencies.

## When to use
Before solving a hard or recurring problem, **recall** prior lessons rather than
re-discovering them. Pairs with `.claude/memory/topics/INDEX.md` (the browseable index).

## Usage
```
python3 scripts/memory/recall.py "git worktree race"          # keyword(s)
python3 scripts/memory/recall.py worktree --class feedback --limit 10
python3 scripts/memory/recall.py --kw stash --kw rebase       # repeatable keywords
```
On Linux with uv: prefix `uv run --no-project`.

Output is ranked by match count (desc), then filename (stable) — so every provider
sees the same ordered result set. `--class` filters by problem class
(`feedback` / `project` / `reference` / `user` / ...).

## Related
- Index generator: `scripts/memory/build_topics_index.py` → `topics/INDEX.md`
- Cross-provider memory slices: `scripts/memory/curate_readback_slice.py` (codex/gemini/hermes)
- Bridge: `scripts/memory/bridge-hermes-claude.sh` (regenerates INDEX + slices)
