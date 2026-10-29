---
name: yangdim-topological-dictionary
description: YangDim topological and algebraic dictionary router. Use for Yang complexes, cubical complexes, CM/SCM/constructible/shellable/vertex-decomposable/Buchsbaum/local-CM properties, Alexander duality, teaching/Scarf/h-vectors, hd/VC/ample correspondences, or dictionary cleanup in main.tex/prescribed_dual_bridge_realization.tex.
---

# YangDim topological dictionary

Use this skill for topology/algebra/dictionary tasks. Keep `SKILL.md` as a router, not a theorem diary.

## Required first packet

Read `references/topological-dictionary.md`, then load only the one or two child packets it names for the task.

## Common child packets

- Raw Yang CM/SCM/constructible, purity, balancing, connectivity, and teaching guardrails: `references/topology-raw-yang-core.md`.
- Alexander-dual componentwise-linear, shellable, linear-quotient, and VC-one strata: `references/topology-alexander-dual-vc1.md`.
- Local-CM/Buchsbaum and profile-kernel questions: start with `references/topology-local-cm.md`.
- Cubical complexes, collapsibility, dimension/purity, CAT(0)/median, and VC-one graphs: `references/topology-cubical-complexes.md`.
- Derived complexes, teaching, Scarf refinements, h-vectors, and no-general-corner guardrails: `references/topology-derived-teaching-hvector.md`.

## Guardrails

- `CM(Delta_H) <=> ample` is proved; do not treat it as conjectural.
- Do not transfer raw-Yang topological adjectives to derived, Alexander-dual, or cubical objects without checking the relevant packet.
- Put theorem-level results in `main.tex` or `prescribed_dual_bridge_realization.tex`; keep active-only status in ledgers.
- After significant TeX changes, compile with SyncTeX enabled, then commit and push the source plus
  generated PDF artifacts when the standing project rule applies.
