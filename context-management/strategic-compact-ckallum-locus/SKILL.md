---
name: strategic-compact
description: Hook-driven strategic compaction system. Tracks tool call count and suggests /compact at logical intervals (50 calls, then every 25) to preserve context through phase transitions.
user-invocable: false
---

# Strategic Compact

Hook-driven system that suggests manual `/compact` at strategic intervals rather than relying on auto-compact which fires at arbitrary points mid-task.

## How it works

A PreToolUse hook on Edit/Write runs `skills/strategic-compact/scripts/suggest-compact.js` which:

1. **Tracks tool call count** per session via a temp file keyed by `CLAUDE_SESSION_ID`
2. **Suggests `/compact` at threshold** (default 50 tool calls) — signals you're likely transitioning from exploration to execution
3. **Suggests again every 25 calls** after threshold — periodic checkpoints for stale context

## Why manual over auto-compact

- Auto-compact happens at arbitrary points, often mid-task
- Strategic compacting preserves context through logical phases
- Compact after exploration, before execution
- Compact after completing a milestone, before starting the next

## Configuration

Set `COMPACT_THRESHOLD` environment variable to override the default 50-call threshold.

## Files

- `skills/strategic-compact/scripts/suggest-compact.js` — the hook implementation
- Registered in `hooks/hooks.json` as a PreToolUse hook on Edit/Write
- Works with `scripts/hooks/pre-compact.js` which saves state before compaction
