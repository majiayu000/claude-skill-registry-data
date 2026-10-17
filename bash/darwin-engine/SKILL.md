---
name: darwin-engine
description: Use for the self-evolving civilization - skills, memories, swarm agents, energy economy, grid duels, metacognition. Run `python scripts/autonomous_loop.py --loop` from the repo root (or `darwin_engine.py --full` for skill evolution only).
---

# Darwin Engine — Self-Evolving Civilization (25 Phases)

The skill population, memories, and swarm agents evolve autonomously:
fitness from real usage signals, live trials in production cron jobs,
speciation from harvested knowledge, energy economy, cross-machine grid
duels, metacognitive gap analysis, and a 30-minute autonomous loop that
runs everything without human input.

## Quick reference (repo root)

```bash
# THE one command - full autonomous cycle (also runs via cron every 30 min)
python scripts/autonomous_loop.py --loop

# skill evolution only
python scripts/darwin_engine.py --autopilot
python scripts/darwin_engine.py --full

# trials & tournaments
python scripts/darwin_engine.py --trial skillA skillA__mutX
python scripts/darwin_engine.py --trials
python scripts/darwin_engine.py --compete

# predation & quarantine
python scripts/darwin_engine.py --predate            # dry-run
python scripts/darwin_engine.py --predate-apply      # real duels
python scripts/darwin_engine.py --quarantine         # dry-run
python scripts/darwin_engine.py --rollback N

# metacognition & species
python scripts/darwin_metacognition.py --introspect
python scripts/darwin_metacognition.py --evolve-gaps --apply
python scripts/darwin_engine.py --explain <skill>
python scripts/darwin_engine.py --status

# memory darwinism
python scripts/memory_darwinism.py --scan --duel --cull --stats

# swarm os
python scripts/swarm_os.py --status
python scripts/swarm_os.py --tick
python scripts/swarm_migration.py --emigrate worker target

# grid (cross-machine natural selection)
python scripts/darwin_grid_github.py --publish <machine-id>
python scripts/darwin_grid_github.py --list
python scripts/darwin_grid_github.py --duel <machine-id>

# reporting
python scripts/darwin_engine.py --report
python scripts/darwin_weekly_report.py --post
python scripts/darwin_dashboard.py --port 8910   # live dashboard
```

## Exit codes

`0` = ok, `1` = error, `2` = evolution made changes (SUCCESS for cron).

## Full chronicle

See [PHASES.md](PHASES.md) — all 25 phases with live evidence.

## Pitfalls

- Exit code 2 is success-with-changes, not failure.
- Starvation: workers with energy <= 0 die in tick (last worker never dies).
- Predation tie-break: fitness rank decides when both duel participants
  exit 0 — only a *functional* prey win saves it.
- Harvested blueprint slugs come from `_pretty_slug` (readable names).
- Memory duels need opposite polarity texts to count as contradictions.
- Grid genome is only as fresh as the last `--publish` (cron runs every 6h).
