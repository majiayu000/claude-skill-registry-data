---
name: start
description: Autonomous session launcher — morning briefing, unattended overnight runs, cross-project patrol, auto-research
when_to_use: "start session, morning session, autonomous run, launch agent — NOT for a briefing-only readout (use /brief); /start with no args includes the briefing then offers to launch work"
argument-hint: '[--morning] [--run] [--hours N] [--goal "X"] [--budget N] [--max-iter N] [--patrol] [--research] [--resume] [--stop] [--dry-run]'
user_invocable: true
---

# Start Skill

One command to launch autonomous coding sessions. Morning briefings, targeted goals, overnight runs, cross-project patrols — all from `/start`.

## Architecture

```
/start                     → Morning briefing (safe, read-only)
/start --run               → Full autonomous session (plan → loop → verify → repeat)
/start --goal "fix tests"  → Targeted run (skip orchestrate, go straight to loop)
/start --patrol            → Cross-project scan (report only, no workers)
/start --research          → Auto-research based on project context
```

## Usage

```
/start                           # Morning briefing (default, safe)
/start --run                     # Autonomous session until done/blocked/budget
/start --run --budget 10         # Set cost budget ($5 default)
/start --run --hours 8           # Wall-clock limit
/start --goal goal.md            # Targeted: use goal file directly (skip orchestrate)
/start --goal "fix all tests"    # Targeted: inline goal string
/start --run --max-iter 5        # Limit outer iterations (default: 20)
/start --run --max-workers 2     # Limit parallel workers (default: 4)
/start --run --model opus        # Supervisor model (default: sonnet)
/start --run --worker-model haiku # Worker model (default: sonnet)
/start --patrol                  # Scan all ~/projects/ with CLAUDE.md
/start --research                # Auto-research from TODO/GOALS/BRAINSTORM
/start --resume                  # Resume interrupted session
/start --stop                    # Write stop sentinel
/start --dry-run                 # Show plan and exit
```
