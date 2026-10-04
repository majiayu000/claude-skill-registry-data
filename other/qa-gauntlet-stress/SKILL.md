---
name: qa-gauntlet-stress
description: >
  Orthogonal stress axes for QA Gauntlet: weapons, ew, logistics layered onto any tier.
  Plans pairwise matrix, derives stressed/control policies, runs proof gate
  (differential-token / differential-aggregate / config-only). Use when /qa-gauntlet-stress,
  /team-qa-gauntlet --mode stress, or axes are claimed in a ladder/forge run.
argument-hint: "[--run-id <id>] [--tiers 1,2,3,4,5] [--max-configs 24] [--evidence PATH]"
user-invocable: true
allowed-tools: Read, Glob, Grep, Write, Bash, Task
---

# QA Gauntlet Stress — Orthogonal Axes

**Authority runbook:** [`tools/qa-gauntlet/README-stress-axes.md`](../../../tools/qa-gauntlet/README-stress-axes.md)  
**Catalog:** `production/qa/gauntlet/corpus/stress-axes.yaml`

Tiers own mission/platform complexity. **Axes own pressure** and compose with any tier.

## Axes (do not invent modes)

| Axis | Proof | Control sibling | Notes |
|------|-------|-----------------|-------|
| `weapons` | `differential-token` (`NO_AMMO`) | **Required** | Proven only on **strict increase** vs control (baseline already has many `NO_AMMO`) |
| `ew` | `differential-aggregate` (`Detected`) | **Required** | Aggregate across seeds; never per-seed alone |
| `logistics` | `config-only` (GAP-13) | — | **Never** report as proven |

## Procedure

1. **Plan** (report `estimatedRuns` / `dropped` before execute):

```bash
python3 - <<'PY'
import sys, json
from pathlib import Path
sys.path.insert(0, "tools/qa-gauntlet")
from stress_axes import load_axes
from plan_stress_matrix import plan_matrix
axes = load_axes(Path("production/qa/gauntlet/corpus/stress-axes.yaml"))
plan = plan_matrix(axes, tiers=[1,2,3,4,5], seeds=3, max_configs=24)
print(json.dumps(plan, indent=2))
PY
```

Budget anchors (do not conflate): default ladder **60** runs; corpus regression ~**117–126**; matrix at max_configs=24 ≈ **105**. Ceiling = corpus cost; lower `max_configs` if exceeded.

2. **Derive** stressed + control policies via `apply_stress_axes` (see runbook). Batch at **tier ticks** (T1=6 … T5=40), never CI 10-tick smoke as authority.

3. **Proof gate** (hard-fail non-config-only unproven). **Scope to claimed axes only**
   via repeatable `--axis` (default without flags verifies the full catalog and will
   hard-fail missing EW/weapons evidence even for a weapons-only candidate):

```bash
# Full catalog (all non-config-only must be proven)
python3 tools/qa-gauntlet/gate_stress_proof.py --evidence path/to/evidence.json \
  --out production/qa/gauntlet/<RUN_ID>/stress-proof-report.json

# Claimed-axis only (forge / single-recipe candidates)
python3 tools/qa-gauntlet/gate_stress_proof.py --evidence path/to/evidence.json \
  --axis weapons --out production/qa/gauntlet/<RUN_ID>/stress-proof-report.json
# multi-claim: --axis weapons --axis ew
# or STRESS_PROOF_EVIDENCE=… tools/qa-gauntlet/run-gauntlet.sh --run-id <id>
```

## Forge integration

When forge candidates claim stress dims, recipes `stress-weapons-*`, `stress-ew-*`,
`stress-logistics-config-only` in `corpus/recipes/recipe-catalog.yaml` apply.
**post-oracle:** if axes claimed, require stress-proof report path in `forge/promote-log.md`.
Logistics promote must state `config-only / unproven`.

## Never

- Downgrade `weapons` to presence-only check.
- Claim `logistics` proven.
- Silent EW without detection targets (raise, do not derive inert scenarios).

## See also

- `/team-qa-gauntlet --mode stress`
- `/qa-gauntlet-forge` — `stress-*` recipes
- `/qa-gauntlet-mission-thread` — concurrent threads (not an axis)
- `/qa-gauntlet-agentic-resilience` — quarantine contract (not an axis)
- `/qa-gauntlet-combat-ui` — combat presentation (not an axis)
