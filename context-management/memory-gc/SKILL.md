---
name: memory-gc
description: Session-end memory garbage collector. Promotes valuable L2 session facts to L1 atomic memory, wipes L2, and rotates oversized audit logs. Run at end of session to prevent context inflation and storage bloat.
origin: yana-ai (custom)
license: Apache-2.0
version: 1.0.0
compatibility: yana-ai >= 1.3.34
---

# /memory-gc — Memory Garbage Collector

## When to Use

- End of session: "dọn bộ nhớ", "gc", "memory cleanup", "session end"
- After a long session (10+ facts in L2)
- Before switching to a new task domain
- When context window feels inflated
- Scheduled: run automatically via Stop hook

## Do NOT use for

- Mid-session cleanup (you'll lose in-progress facts)
- Replacing `/l1-promote` for interactive, selective promotion
- Replacing `/session-wrap` (that handles docs + learning + followup)

---

## What it does

```
Phase 1: Score all L2 facts (5-point rubric)
  → Promote facts scoring ≥ 2/5 to L1_atomic
  → Wipe entire L2 regardless

Phase 2: Check audit log size
  → If > 5MB: compress to releases/logs/, keep last 500 lines
  → If ≤ 5MB: skip rotation

Phase 3: Report summary
```

## Promotion Rubric (L2 → L1)

| Criterion | Points |
|---|---|
| Has at least 1 tag | +1 |
| Statement length > 20 chars | +1 |
| Has evidence field | +1 |
| Not session-state-only (not "currently..." / "right now...") | +1 |
| No duplicate ID in L1 already | +1 |

Threshold: **≥ 2/5** → promoted. Below → wiped without promotion.

---

## Usage

```bash
# Full GC (promote + wipe L2 + rotate logs)
bash core/scripts/memory-gc.sh
bash core/scripts/log-rotate.sh

# Dry run — see what would happen
bash core/scripts/memory-gc.sh --dry-run
bash core/scripts/log-rotate.sh --dry-run

# Wipe L2 only (discard session, no promotion)
bash core/scripts/memory-gc.sh --wipe-only

# Force log rotation regardless of size
bash core/scripts/log-rotate.sh --force
```

## Anti-Fake-Pass Checklist

```
□ memory-gc.sh exited 0
□ L2 directory is empty after run (or --dry-run was used)
□ Promoted facts appear in memory/L1_atomic/
□ audit log size checked (log-rotate.sh ran if > 5MB)
□ secure-logger.sh recorded memory_gc_complete event
```

## Integration: Stop Hook

Add to `core/hooks/hooks.json` under `Stop` event to auto-GC every session:

```json
{
  "matcher": "true",
  "hooks": [{
    "type": "command",
    "command": "bash core/scripts/memory-gc.sh && bash core/scripts/log-rotate.sh"
  }]
}
```
