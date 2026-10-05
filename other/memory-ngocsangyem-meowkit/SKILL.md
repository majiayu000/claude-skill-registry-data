---
name: mk:memory
description: JSON-canonical session memory. Use when capturing session learnings, extracting patterns, or tracking costs — persists to .meowkit/memory JSON stores; matching Markdown files are generated views. Activates during Phase 0 (Orient) to load context and Phase 6 (Reflect) to persist it. NOT for weekly-cadence engineering retrospectives (see mk:retro); NOT for arbitrary file storage.
keywords:
  - memory
  - topic-files
  - fixes-log
  - architecture-decisions
  - review-patterns
  - persistence
when_to_use: Use when reading or updating canonical .meowkit/memory JSON stores (fixes, review-patterns, architecture-decisions, cost-log).
user-invocable: true
owner: memory
criticality: high
status: active
runtime: claude-code
---

# Memory System Toolkit

Reference guides for the memory system: session capture, pattern extraction, and cost tracking.

## When to Use

- During Phase 0 (Orient) to load previous session context
- During Phase 6 (Reflect) to capture learnings and patterns
- When the `analyst` agent tracks costs or extracts patterns

## Workflow Integration

Operates in **Phase 0 (Orient)** and **Phase 6 (Reflect)**. Output supports the `analyst` agent.

## References

| Reference | When to load | Content |
|-----------|-------------|---------|
| **[capture-architecture.md](./references/capture-architecture.md)** | Before any agent-side memory write | The 2-path contract — `##prefix:` is user-typed only; agents write via direct `Edit` |
| **[session-capture.md](./references/session-capture.md)** | Phase 6 | Capturing session learnings in 3 categories (patterns/decisions/failures) |
| **[pattern-extraction.md](./references/pattern-extraction.md)** | Phase 6 | Extracting high-frequency patterns for instruction-file promotion |
| **[cost-tracking.md](./references/cost-tracking.md)** | Phase 0, 6 | Token usage tracking, cost reporting, budget alerts |
| **[consolidation.md](./references/consolidation.md)** | Manual | Prune stale entries, merge duplicates, archive cost data (run when memory grows large) |

## How session-capture is invoked

`session-capture` is **not** a CLI subcommand. At Phase 6 (Reflect) the agent reads `references/session-capture.md` and follows its 4 steps using `Read` / `Write` / `Edit` directly. There is no `mewkit memory session-capture` script — content extraction requires LLM analysis that a static CLI cannot produce.

## Subcommands

### `--prune`

Prune old standard-severity entries from canonical JSON stores, then regenerate Markdown views.

**Stores subject to pruning:** `fixes.json`, `review-patterns.json`, and
`architecture-decisions.json`.

**What gets pruned:**
- `## headings` with a date `(YYYY-MM-DD, severity: standard)` older than threshold (default: 90 days)

**What is exempt:**
- `severity: critical` or `severity: security` entries — never pruned
- Entries without a parseable date — kept as-is (safe default)

**How to run:**
```
/mk:memory --prune              # default 90-day threshold
/mk:memory --prune --days 180   # custom threshold
/mk:memory --prune --dry-run    # show what would be archived without moving
```

**Mechanism:** prune schema entries in JSON by `lastSeen` and severity, then run
`mewkit memory render-views`. Report the affected stores and entries.

**Recovery:** Copy entries from `lessons-archive.md` back to the appropriate topic file.

## Schema Notes

Split JSON files (`fixes.json`, `review-patterns.json`, `architecture-decisions.json`) all use v2.0.0 schema with fields: `version`, `scope`, `consumer`, `patterns[]`, `metadata`. Each pattern entry supports: `id`, `type`, `category`, `severity`, `domain`, `applicable_when`, `context`, `pattern`, `frequency`, `lastSeen`.

## Gotchas

- **Stale patterns applied to changed codebase**: Memory suggests patterns from old architecture → Run consolidation when patterns exceed 50 entries; flag patterns with lastSeen > 6 months
- **cost-log.json growing unbounded**: Every session appends without pruning → Run consolidation to archive entries older than 90 days
- **Generated views are not writable**: Do not write `lessons.md` or Markdown topic files. Update the canonical JSON store, then render views.
