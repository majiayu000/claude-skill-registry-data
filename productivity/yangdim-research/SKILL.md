---
name: yangdim-research
description: Lightweight project overview for the YangDim paper. Use when a task needs repo-level routing, baseline notation, terminology, paper/build conventions, or computational guardrails, or when no narrower yangdim-* skill fits. Prefer specialized YangDim skills for topological dictionary, minimal non-ample structure, prescribed-dual bridge realization, or campaign workflow tasks.
---

# YangDim overview router

Use this skill as a repo-level navigation layer. It owns stable baseline packets only: shared notation, terminology, paper conventions, and computation guardrails. It must not carry proof-route diaries or active theorem status.

## First choose the topic owner

- Use `yangdim-topological-dictionary` for Yang complexes, cubical complexes, CM/SCM/VD/shellability, local-CM/Buchsbaum, Alexander duality, teaching, h-vectors, and dictionary cleanup.
- Use `yangdim-minimal-nonample` for minimal non-ample structure, VC-radius, sphere law, Claim-X status, maximum fibers, and closed frontier audits.
- Use `yangdim-bridge-realization` for the active prescribed-dual bridge realization problem, antipodal suspensions, split-lift repair variables, endpoint separation, wall/provenance descent, row-torsor routes, and finite signature diagnostics.
- Use `yangdim-campaign-workflow` for ledger hygiene, source-of-truth synchronization, subagent packet design, consolidation pauses, and promotion from exploration to TeX.

If the task has a clear topic owner, switch to that skill after this overview and load only that skill's required packet.

## Baseline packets owned here

- For object definitions and notation, read `references/core-objects.md`.
- For terminology guardrails, read `references/terminology.md`.
- For paper-writing and LaTeX conventions, read `references/paper-conventions.md`.
- For computational command conventions and reusable helpers, read `references/computational-toolkit.md`.
- For known computational pitfalls and false shortcuts, read `references/computational-pitfalls.md`.

## Packet ownership boundaries

- Topological and algebraic dictionary packets live in `yangdim-topological-dictionary/references/`.
- Minimal-nonample, VC-radius, sphere-law, and Claim-X frontier packets live in `yangdim-minimal-nonample/references/`.
- Prescribed-dual bridge, split-lift, row-torsor, and finite-signature packets live in `yangdim-bridge-realization/references/`.
- Workflow-discipline packets live in `yangdim-campaign-workflow/references/`.

## Source-of-truth routing

- For current route state, prefer `prescribed_dual_bridge_realization.tex` plus `ledgers/proof_route_topological_dictionary.md` over memory files. References are stable background and guardrails; the ledger is the active source of truth.
- For theorem-level results, use `main.tex` or `prescribed_dual_bridge_realization.tex` with explicit hypotheses and labels.
- For active-only status, use `ledgers/proof_route_topological_dictionary.md` by replacement, not chronology.
- For navigation-only status, use `EXPLORATION_INVENTORY.md`.
- For reusable methodology, update the relevant skill; do not use skills as chronological logs.

## Reference hygiene

- Keep overview references short. If a reference accumulates multiple proof routes, split it into topic packets and leave only routing/status in the overview. Prefer one-level reference packets linked directly from `SKILL.md` or a named overview; avoid reviving monolithic route diaries.
- Split reference packets by job: objects/notation, terminology, paper conventions, computation, pitfalls, or a named topic skill. Do not mix proof-route status into this overview skill.
- Update this skill only for stable project facts, recurring pitfalls, routing changes, or reusable workflow lessons.
- After significant TeX changes, compile with SyncTeX enabled, then commit and push the source and
  generated PDF artifacts as requested by the user.
