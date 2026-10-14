---
name: miner-damage
description: "Use when you must evaluate fatigue life with cumulative damage: sum the Palmgren-Miner damage fractions over the load spectrum, check the total against the life limit, and report the percentage of fatigue life consumed. Produces the cumulative damage fraction, the life limit verdict, and the life consumed percentage that gate the fatigue assessment. Trigger: fatigue, cumulative damage, palmgren-miner, load spectrum, fatigue life, damage tolerance."
license: Apache-2.0
compliance: STANDARDS-REF
standards:
  - id: far-25
    reference-only: true
  - id: cs-25
    reference-only: true
gated: false
domain: structures
pack: structures
compatibility: "agentskills.io SKILL.md; any SKILL.md host (Claude Code, Hermes, OpenClaw)"
metadata:
  domain: structures
  subdomain: fatigue
  tags: [fatigue, cumulative-damage, palmgren-miner, load-spectrum, fatigue-life, damage-tolerance]
  version: 0.1.0
  author: Aero Agent Skills
---

# Fatigue Cumulative Damage (structures/fatigue/miner-damage)

Use when the task is fatigue life evaluation with cumulative
damage: Palmgren-Miner fractions, life limit checks, and life
consumed reporting.

## Domain quick reference

- The Palmgren-Miner rule sums n/N for each load level, where n is
  applied cycles and N is cycles to failure.
- Failure is predicted when the accumulated fraction reaches 1.0.
- The load spectrum is the sequence of (cycles, cycles-to-failure)
  blocks from the fatigue analysis.
- Fatigue practice sits in the FAR-25.571 damage tolerance context
  for transport aeroplanes.

## Workflow

1. Collect the load spectrum blocks.
2. Sum the damage with cumulative_damage.
3. Check the total with damage_ok.
4. Report life consumed with life_consumed_pct.
5. Gate the fatigue assessment on the verdict.

## Pitfalls

- Summing damage without the cycles-to-failure at each level.
- Using a zero cycles-to-failure for a load block.
- Treating a damage fraction above 1.0 as acceptable.

## Behavior contract (gate 3)

The damage, limit, and life logic is exercised by the gate 3
contract test: scripts/test_miner_damage.py against
scripts/miner_damage_logic.py (stdlib unittest, offline). Run:
python3 scripts/test_miner_damage.py

## Compliance

- Standards referenced, not reproduced: FAR-25 is US government
  work (public domain) and CS-25 is a free EASA download; the
  damage rule is common fatigue methodology, summary-only per
  standards-map.yaml.
- compliance: STANDARDS-REF, gated: false.
