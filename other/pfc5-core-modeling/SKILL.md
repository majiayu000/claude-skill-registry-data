---
name: pfc5-core-modeling
description: Build and audit PFC2D/PFC3D 5.0 model foundations for asphalt cases, including lifecycle, domain, balls, walls, clumps, groups, ranges, top-level cmat, staged saves, and source-version purity.
---

# PFC5 Core Modeling

Use this skill for the version-pure foundation of a PFC 5.0 asphalt case. It
replaces the reusable intent of the former general basics/contact workflow
without restoring newer-major command files.

## When To Use

- start or audit a PFC2D/PFC3D 5.0 case;
- create domains, walls, balls, clumps, groups, or ranges;
- plan current-contact versus future-contact model assignment;
- organize build, compaction, contact installation, equilibrium, and save stages;
- classify accepted, restart-only, diagnostic-only, failed, and obsolete states;
- detect unsupported-version syntax in a PFC5 source tree.

Route detailed gradation/void closure to `pfc-asphalt-mixture`, FISH to
`pfc5-fish`, servo/calibration to `pfc5-servo-calibration`, and migration or recovery
of an existing private case to `pfc5-case-handoff`.

## Required Inputs

- PFC2D/PFC3D 5.0, units, sign convention, and runtime route;
- specimen/domain dimensions and boundary behavior;
- particle/clump size and shape abstraction;
- material/contact pair table;
- seed, equilibrium criterion, save/output contract.

## Workflow

1. Freeze version, dimension, units, axes, seed, and object abstractions.
2. Create a clean model and domain before domain-sensitive objects.
3. Define future-contact defaults with PFC5 top-level `cmat`.
4. Create boundaries, particles/clumps, groups, and reusable ranges.
5. Form contacts, then audit counts/types before changing existing contacts.
6. Compact or equilibrate to an explicit criterion.
7. Install final contacts transactionally: save, apply, cycle, audit, solve, save.
8. Initialize measurements before loading. If energy histories are required, enable
   mechanical energy tracking before the measured interval.
9. Run `scripts/audit_pfc5_case.py` and an actual PFC5 syntax probe.

For an existing project, restore and audit the last claimed accepted state before a
full rebuild. A restart-only state may seed a recovery branch only when its object and
geometry invariants are known; re-run the original final gates without weakening them.

Read [stage-gates.md](references/stage-gates.md) for lifecycle checks and
[pfc5-command-boundary.md](references/pfc5-command-boundary.md) when auditing
syntax.

## Non-Negotiable Rules

- Do not infer PFC5 compatibility from an extension or old filename.
- Separate future defaults from existing-contact reassignment.
- Order non-default CMAT slots deliberately: PFC5 selects the first matching range,
  then falls back to the default slot for that contact type.
- Treat multiple `solve` limits as alternatives, not cumulative acceptance gates;
  record which limit terminated the solve.
- Do not delete all contacts as a generic model-switch recipe.
- `cmat apply` replaces the whole selected contact model and discards its prior stored
  state; save and audit before applying it.
- A fixed cycle count does not prove equilibrium.
- Source audit is static evidence only; runtime acceptance remains required.

## Output Contract

Return the PFC5 stage map, object/group/range map, contact assignment table,
equilibrium criteria, save map, audit report, and `runtime_validated` status.

## Local Contents

- `references/stage-gates.md` — build-to-delivery gates.
- `references/pfc5-command-boundary.md` — syntax-family boundary.
- `scripts/audit_pfc5_case.py` — deterministic source-tree audit.
- `agents/openai.yaml` — interface metadata.
