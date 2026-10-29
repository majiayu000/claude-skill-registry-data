---
name: yangdim-campaign-workflow
description: YangDim research-campaign workflow and hygiene. Use for ledger cleanup, source-of-truth synchronization, status boxes, subagent packet design, consolidation pauses, promotion/demotion of route material, exploration inventory updates, and deciding what belongs in main.tex, prescribed_dual_bridge_realization.tex, drafts, ledgers, scripts, or skills.
---

# YangDim campaign workflow

Use this skill with `honest-conjecture-resolution` for long proof campaigns and cleanup passes.

## Required packet

Read `references/workflow-discipline.md`.

## Source-of-truth rule

- `main.tex`: theorem-level paper results and polished exposition.
- `prescribed_dual_bridge_realization.tex`: self-contained active open-problem formulation and proof-route draft material.
- `drafts/`: route syntheses, finite certificates, and arguments not ready for the paper.
- `ledgers/`: active-only targets, reduced cruxes, blockers, and next actions.
- `scripts/`: diagnostics, verifiers, and regression checks.
- `EXPLORATION_INVENTORY.md`: navigation map.
- Skills: reusable methodology and stable project memory, not route diaries.

## Cleanup rule

Replace stale blocks rather than appending chronology. A clean ledger starts with the current theorem/question, definitions, assumptions, route IDs, status labels, and the next one to three concrete actions. Closed proofs leave the active list once promoted to `main.tex`, `prescribed_dual_bridge_realization.tex`, or a stable side draft.

## Proof/disproof alternation rule

Counterexample search and proof reduction should be run as a feedback loop. A search round should end with a proof-facing structural lesson or candidate lemma, and a proof round should end with a disproof-facing diagnostic that could falsify or sharpen the new crux.

## Promotion rule

Promote to TeX only after there is a proof-level statement with explicit hypotheses and dependency labels. After significant TeX changes, compile with SyncTeX enabled, then commit and push source plus generated PDF artifacts when the standing project rule applies.
