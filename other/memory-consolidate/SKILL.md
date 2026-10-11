---
name: memory-consolidate
version: 2.0.0
description: Consolida de forma determinista observations.jsonl, deduplicando, filtrando ruido y archivando entradas antiguas, sin LLM ni cron. Usar cuando se cierra la sesion tras session_close_observations o cuando observations.jsonl ha crecido mucho. No usar para escribir observaciones nuevas (ver session-close-observations).
triggers: [/consolidate, /memory, /dream-cycle]
author: agent
role: shared
stage: memory
cycle_phase: [F7-cierre-sesion]
writes_memory: true
quality_gate: false
tags: [core, system]
---

# Memory Consolidate V1

Deterministic memory consolidation without LLM or cron. Run manually at session close to deduplicate observations, filter noise, and archive old entries.

## Overview

This skill implements the V1 "dream cycle" pattern adapted from gbrain: a manual command that consolidates `.agent/runtime/memory/observations.jsonl` through deduplication, noise filtering, and age-based archiving, then regenerates `MEMORY.md` from the consolidated version.

### When to Invoke

- At session close (after `project-finalize` Paso 9e, which itself requires Paso 9d —
  `session_close_observations.py` — to have run first)
- When `observations.jsonl` has grown significantly
- Before starting a new work cycle to clean up memory
- When requested via `/consolidate`, `/memory`, or `/dream-cycle` triggers

### When NOT to Invoke

- During active WP implementation (agents may be appending)
- If you haven't reviewed the dry-run report first
- When `observations.jsonl` is empty or very small (< 10 entries)

## Workflow

### Paso 1: Dry-run preview

```bash
python scripts/memory_consolidate.py --verbose
```

Review the generated `CONSOLIDATION_REPORT.md` to see:
- Total entries processed
- Entries that would be kept, dropped, deduped, archived
- No files are modified in dry-run mode

### Paso 2: Review report

Check `.agent/runtime/memory/CONSOLIDATION_REPORT.md`:
- Are dropped entries actually noise (Tool X called, <30 chars)?
- Does dedupe count make sense?
- Are archivable entries truly old (>30 days)?

### Paso 3: Apply if OK

```bash
python scripts/memory_consolidate.py --apply --verbose
```

This will:
- Create backup `observations.jsonl.bak.<timestamp>`
- Rewrite `observations.jsonl` with consolidated entries
- Move old entries to `archive/observations.<YYYY-MM>.jsonl`
- Regenerate `MEMORY.md`
- Update `CONSOLIDATION_REPORT.md` with applied stats

### Paso 4: Validate output

1. Check `MEMORY.md` has proper structure with topics
2. Verify `observations.jsonl` line count reduced
3. Confirm backup file exists
4. Run `python scripts/local_audit.py --quick` to ensure compatibility

### Paso 5: Commit (if applicable)

Note: `observations.jsonl` and `MEMORY.md` are gitignored (runtime files). Only the script, tests, and skill definition are committed.

## Arguments

| Flag | Default | Description |
|------|---------|-------------|
| `--apply` | dry-run | Apply changes (default is dry-run) |
| `--since <Nd>` | `30d` | Archive entries older than N days |
| `--verbose` | off | Print detailed output |

## Safety Features

- **Dry-run by default**: Must explicitly use `--apply` to write
- **Backup before write**: `.bak.<timestamp>` created before any modification
- **Append-only preserved**: External agents continue appending; only this script rewrites
- **Archive, never delete**: Old entries moved to archive, never destroyed
- **Idempotent**: Running twice consecutively produces no change on second run

## Pipeline Steps

1. **Read & parse**: Load entries from `observations.jsonl`, skip malformed lines
2. **Drop noise**: Remove "Tool X called" patterns and entries <30 chars
3. **Dedupe**: Remove duplicates within 24h window (keep newest)
4. **Archive**: Move entries older than 30 days to `archive/`
5. **Regenerate**: Create `MEMORY.md` from consolidated entries
6. **Report**: Write `CONSOLIDATION_REPORT.md` with stats

## Output Files

| File | Action | Git |
|------|--------|-----|
| `observations.jsonl` | Rewritten (if --apply) | Ignored |
| `observations.jsonl.bak.*` | Created (backup) | Ignored |
| `MEMORY.md` | Regenerated | Ignored |
| `CONSOLIDATION_REPORT.md` | Created/Updated | Ignored |
| `archive/observations.*.jsonl` | Appended (if archivable) | Ignored |

## Constraints

- **NO LLM**: Fully deterministic, stdlib only
- **NO cron**: Manual invocation only (V2 may add scheduling)
- **NO deletion**: Entries are archived, never deleted
- **Session close only**: Don't run while agents are active

## Troubleshooting

### Too many entries dropped

Review noise criteria in `scripts/memory_consolidate.py`:
- `NOISE_PREFIXES = ("Tool ",)` - patterns starting with "Tool "
- `MIN_SIGNAL_LEN = 30` - minimum signal length

Adjust if your use case requires different thresholds.

### Idempotency broken

If second `--apply` produces changes:
1. Check timestamps are preserved (not rewritten)
2. Verify dedupe window logic
3. Run test `test_idempotency` in test suite

### Race condition

If agents are appending during consolidation:
- Wait for agent activity to stop
- Only invoke at session close
- Document in session brief when consolidation occurred

## References

- Work Plan: `WP-2026-083` (legacy-compat: ticket historico de origen de esta skill; ver glosario WOT-2026-010a en AGENTS.md)
- Origin: Oportunidad #4 from `garrytan/gbrain` repo-compare
- V2 Backlog: LLM-based synthesis + cron scheduling

## Related Skills

- `project-finalize`: Invoke this skill at Paso 9e (optional session close; depends on Paso 9d
  having run first)
- `local-audit`: Run after consolidation to verify compatibility
