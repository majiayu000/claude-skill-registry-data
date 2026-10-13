---
name: dept-resume
description: Read dept-state.md and spawn a Dept Head with a lean briefing. Department-operations parallel of /pd-resume.
category: dept-ops
version: 1.0.0
---

# dept-resume

Spawns a Dept Head agent for the given department with a pre-built briefing from `dept-state.md`. Lean context, fast start.

## Usage

```
/dept-resume [dept-slug]
/dept-resume content-creation
/dept-resume engineering
/dept-resume all
```

## Argument Resolution

| Argument | Action |
|---|---|
| `[dept-slug]` | Resume exactly one department |
| `all` | Resume all active departments (spawns in parallel) |
| no arg | Fail with usage hint |

## What It Does

1. Reads `~/.agency/agents/{dept}/state/dept-state.md`
2. Checks `~/.agency/agents/{dept}/state/incoming/` for pending inter-spawn tasks
3. Checks `~/.claude/agents/{dept}/state/dev-plan.md` for existence (dev-plan-absent check)
4. Spawns the Dept Head with dept-state.md inline — no extra reads on spawn
5. Dept Head boots per `core/runbooks/dept-boot-sequence.md` Mode 1

## Dev-Plan-Absent Check

After reading dept-state.md (Step 1), check whether `~/.claude/agents/{dept}/state/dev-plan.md` exists.

- **If absent** (and the initiative has 3+ D3 tracks): inject into the Dept Head spawn prompt:
  "DEV-PLAN ABSENT — generate ~/.claude/agents/{dept}/state/dev-plan.md before dispatching
  any Dept-Coords. Apply the two-condition parallel rule (see task-decomposition-methodology.md)
  to assign layers. After generating the dev-plan, run /save-state and respawn to enter
  the deployment phase with a clean context."
- **If absent** (simple initiative, <3 D3 tracks): skip dev-plan generation — not required
  for single-track or dual-track initiatives.
- **If present**: inject a one-line note: "Dev-plan: ~/.claude/agents/{dept}/state/dev-plan.md
  (present — read before dispatching Dept-Coords)"

This mirrors the pd-resume dev-plan-absent trigger, applied to department operations.

## Dept Head Boot Context

The spawn prompt includes:
- dept-state.md content (inline, no file read needed)
- incoming task count and any HIGH-priority items
- The dept head's agent definition path

**Target context on spawn: ~400 tokens.** Everything else is lazy-loaded per Mode 2 (Route).

## Output

```
dept-resume done — {dept}
  Head: {head-agent-name}
  Priority: {current-priority from dept-state}
  Active coords: {n or "none"}
  Incoming tasks: {n or "none"}
```

## Notes

- If `dept-state.md` doesn't exist, output: `No dept-state found for {dept}. Run /dept-wrap to initialize.`
- Dept Heads do NOT start their session by reading every pipeline and protocol file — that is lazy-loaded
- The incoming check is part of the boot sequence and runs before any other dept work

## References

- Dept boot sequence: `core/runbooks/dept-boot-sequence.md`
- Dept-Coord protocol: `core/runbooks/dept-coord-protocol.md`
- Parallel: `/pd-resume` for project directors, `/dept-status` for read-only check
