---
name: experiment-governance
description: Maintain or extend the advisory governance layer that classifies experiment usefulness, concentration, noise, and scoped-candidate status from existing paper-research metrics. Use when changing experiment status rules, governance summaries, or operator-facing decision support. Never use for auto-enabling experiments or changing scorer behavior directly.
---

# Experiment Governance

## Binding sources

- **`docs/FINAL_SYSTEM_VISION.md`** — research/experiment interpretation supports **L6** learning inputs and **L9–10** transparency; not a substitute for **L5** (AI) or **L7** (risk).
- **`AGENTS.md`** — governance remains advisory; **bounded** autonomous *review* actions only; no promotion of live trading.

## Purpose

Use this skill to manage the advisory decision layer around experiments.

This layer should standardize interpretation of existing summary data, not change runtime behavior. It turns metrics such as executable deltas, block deltas, stability, and concentration into readable governance statuses and rule triggers.

## Use When

Use this skill when:
- changing experiment status categories
- changing rule-based governance summaries
- changing scoped-candidate analysis or supporting evidence
- extending operator-panel decision-support widgets that interpret experiment outcomes
- adding passive promotion review summaries from existing evidence
- adding passive operator approval checklists or promotion history summaries
- adding switchable manual vs bounded-autonomous governance review flows
- extending shared governance audit history for operator and autonomous decisions
- capturing explicit manual final actions, notes, and defer/reject reasons in the shared audit trail
- incorporating passive learning-readiness or AI-readiness signals into approval checklists without changing runtime behavior

## Do Not Use When

Do not use this skill for:
- changing scorer math or strategy math
- changing hard risk rules
- auto-enabling experiments
- auto-applying tuning or learning

## Safety Contract

- Governance remains advisory only.
- Repo defaults remain unchanged.
- Rule triggers stay explicit and operator-readable.
- Summary text must not imply an experiment was activated automatically.
- Governance must not hide safety failures or increased risk blocks.
- Promotion-review outputs may label a mode as not_ready, hold, review, or promotable, but they must never switch modes automatically.
- Autonomous governance may record bounded review actions such as keep_observing, collect_more_sample, defer, review_regime_pockets, or manual_review_candidate, but it must never switch runtime mode or promote behavior automatically.
- Manual governance may record bounded final actions plus optional operator note or defer/reject reason, but it must stay within the same shared audit model as autonomous governance.
- Learning-readiness and AI-readiness inputs may strengthen review discipline, but they must remain passive checklist evidence rather than runtime gating.

## Primary Workflow

1. Read `AGENTS.md`.
2. Inspect current summary inputs before adding new interpretation rules.
3. Reuse existing comparison data where possible.
4. Keep rule logic explicit, simple, and traceable.
5. Expose the reasons behind the classification, not just the label.

## Required Checks

- Status labels remain descriptive rather than prescriptive.
- Sample size, block deltas, and concentration remain visible alongside the verdict.
- Unsafe or noisy cases are surfaced clearly.
- Scoped-candidate analysis includes both supporting evidence and a caution.
- Approval checklists and promotion history remain passive review artifacts only.
- Manual and autonomous governance paths must share the same audit model and remain traceable.
- Explicit final action, decision source, operator note, and defer/reject reasons must remain visible in the audit trail when present.
- Learning-readiness and AI auditability signals must stay readable as review inputs, not as automatic promotion authority.

## Expected Output

- `Governance Statuses:` what labels exist now.
- `Rule Triggers:` what evidence drives the current classification.
- `Advisory Scope:` explicit note that no behavior changed.
