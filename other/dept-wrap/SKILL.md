---
name: dept-wrap
description: Freeze department state at session end. Writes dept-state.md, updates member-roster.md, archives scratch files. Department-operations parallel of /save-state and semantic pair of /dept-resume.
category: dept-ops
version: 1.0.0
---

# dept-wrap

Freezes department state at session end. Full implementation in `skills/dept-wrap/SKILL.md`.

Renamed from `/dept-save-state` to pair semantically with `/dept-resume`.

## Usage

```
/dept-wrap [dept-slug]
/dept-wrap engineering
/dept-wrap all
```

## What It Does

1. Reads current `dept-state.md` and any active scratch files
2. Overwrites `dept-state.md` with current session state (max 20 lines)
3. Updates `member-roster.md` utilization columns
4. Archives or clears completed coord scratch files
5. Promotes session lessons to `dept-path/memory/lessons.md`

## Argument Resolution

| Argument | Action |
|---|---|
| `all` | Save all 14 departments in parallel |
| `[dept-slug]` | Save exactly one department |
| no arg | Fail with usage hint |

## References

- Full spec: `skills/dept-wrap/SKILL.md`
- Dept boot sequence: `core/runbooks/dept-boot-sequence.md`
- Dept-Coord protocol: `core/runbooks/dept-coord-protocol.md`
- Parallel: `/save-state` for projects, `/dept-resume` for session start, `/dept-status` for read-only check
