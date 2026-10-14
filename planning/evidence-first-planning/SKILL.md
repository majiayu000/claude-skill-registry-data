---
name: evidence-first-planning
description: "Trigger: deep plan, evidence-first plan, planificar a fondo, planificacion basada en evidencia, discovery plan. Discover decisions and plan executable work from repository evidence."
license: MIT
metadata:
  author: andresnator
  status: in-progress
  version: "5.0.0"
---

## Contract

Plan before implementation. Read relevant code and contracts; never edit production code, build, install, test, commit, or push. Planning artifacts are the only writes.

## Method

1. **Evidence first.** Verify implementations, callers, tests, tool versions, and reusable `path:symbol` elements. Cite `path:line` or mark `hypothesis`.
2. **Ask only decisions.** Explore repository facts. Ask each unresolved open-ended scope, product, acceptance, or risk choice directly in normal chat and wait. Add `Recommendation: ...` only when useful; reserve the `question` tool for closed choices.
3. **Validate edges.** Every edge is handled, out of scope, or an open question. Use `references/edge-validation.md`.
4. **Stay proportional.** Keep only information that changes execution; record meaningful rejected alternatives briefly.
5. **Prove the flow.** End with executable commands or an observable end-to-end check and its expected result.

## Wayfinder discovery

Use `assets/discovery-template.md`. Write one `.ai/deep-planner/discoveries/<slug>.md`. Do not add status, phase, or readiness markers. Keep evidence, decisions, and unresolved questions current. When the destination is clear, suggest converting the discovery into a plan.

## Deep Plan

Load `execution-plan` and write one `.ai/deep-planner/plans/<slug>.md`. Large efforts remain one plan with work groups and explicit dependencies. Do not create roadmaps, slices, readiness markers, or companion phase documents.

## Outputs

- Wayfinder: one discovery file and no plan.
- Deep Plan: one plan file and no discovery, roadmap, or change file.

Before returning, check evidence, edges, proportionality, exact paths, and end-to-end verification. Report only the artifact path and next route.

## Resources

- `assets/discovery-template.md`
- `references/edge-validation.md`
- `references/question-economy.md`
