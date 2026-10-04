---
name: ln-consult
description: "Lightweight triage for the ln-* skill set. Use when unsure which ln skill to use next, starting work on something new, or when the user asks for guidance on their development process."
---

# Ln Consult

Assess where the user is, classify the work, and suggest the next `ln-*` skill.

If context is unclear, ask **one** clarifying question — then recommend.

The canonical rule is simple: durable planning state lives only in `memory/SPEC.md` and `memory/PLAN.md`, and new or uncertain work defaults to the canonical flow until a narrow exception is clearly justified.

Do not invent new planning documents, sidecar ledgers, or alternate storage locations without explicit user permission. If a fact matters beyond the current step, reconcile it into `memory/SPEC.md` or `memory/PLAN.md`; if it is temporary transfer state, keep it in `HANDOFF.md`; if it is a temporary multi-card execution queue inside one frontier item, keep it in `memory/CARDS.md`; if it is a temporary refactor execution plan, keep it in `memory/REFACTOR.md`. Derivative files stay live only while they still carry unfinished work.

Orient, then classify.

## Fresh-thread re-entry

If this is a fresh thread or an unfamiliar area, reload the live context before routing:

1. `memory/SPEC.md`
2. `memory/PLAN.md`
3. `HANDOFF.md` if present
4. `docs/archive/PLAN_HISTORY.md` only if the current frontier or touched area is still unclear

Start the assessment with 2-4 bullets naming:

- the containing seam or subsystem
- the active frontier item or nearby priority
- volatile state or manual follow-up from handoff
- the main open risk

## Work-type classification

Classify the request before routing.

| Work type | Signals | Default handling |
| --- | --- | --- |
| **Structural** | New seam, new boundary, durable architectural choice, invalidates assumptions | `ln-spec` / `ln-plan` / `ln-scope` as needed |
| **Bounded feature** | New capability inside settled seams | `ln-scope` with a light scope card, then `ln-build` |
| **Hardening** | Dependency audit, fixture work, perf, tooling upkeep | direct `ln-build` only if the seam is already settled and scope is obvious; otherwise `ln-scope` |
| **Bugfix** | Regression or incorrect behavior inside known seams | direct `ln-build` only if the seam is settled and reconciliation is likely to be a no-op |
| **Refactor** | Rename, extract, restructure without changing behavior | `ln-refactor` |

If the work crosses more than two seams, changes a requirement, or would change future planning if it went differently, promote it to **structural**.

If you cannot name the containing seam from the live docs, treat the work as **structural** until proven otherwise.

Presume **structural** on a fresh thread when the work touches workflow closure, routed layout ownership, persistence schema, knowledge-graph behavior, observer sync, or transport contracts.

## Canonical flow

Default rule:

`ln-grill` or `ln-disambiguate` → `ln-spec` → `ln-plan` → optional `ln-design` / `ln-oracles` → `ln-scope` → optional `ln-spike` → `ln-build` → `ln-review` → optional `ln-refactor` / `ln-sync`

Bounded exception:

`ln-scope → ln-build`

Bounded serial exception:

`ln-scope → ln-build → commit → ln-build ...` inside one already-settled frontier item, optionally with the prepared queue persisted in `memory/CARDS.md`

Direct-build exception:

`ln-build`

Only recommend the bounded or direct-build exceptions when all of these are true:

- the containing seam is already named in the live docs
- no durable requirement / assumption / decision / invariant change is expected
- post-build reconciliation can plausibly be a no-op

Only recommend the bounded serial exception when those same conditions hold and the next several commit-sized steps are obvious enough to queue without fresh planning.

## Routing table

| Situation | Work type | Suggest |
| --- | --- | --- |
| Idea is vague, needs fleshing out | structural | `ln-grill` |
| Plausible interpretations diverge; examples would clarify faster than open-ended questioning | structural | `ln-disambiguate` |
| Understanding exists, needs a written spec | structural | `ln-spec` |
| Spec exists, needs work sequencing | structural | `ln-plan` |
| Verification strategy is the main uncertainty | structural | `ln-oracles` |
| Next work item needs precise boundaries | structural or bounded | `ln-scope` |
| One settled frontier item needs several small verified commits in sequence | bounded, hardening | `ln-scope` then serial `ln-build` loop, optionally via `memory/CARDS.md` |
| Module interface needs exploration | structural | `ln-design` |
| Full or light scope card exists, ready to code | bounded, hardening, bugfix | `ln-build` |
| Technical uncertainty blocks progress | any | `ln-spike` |
| Code works but needs restructuring | refactor | `ln-refactor` |
| Code works but quality / architecture needs audit | any | `ln-review` |
| Docs are stale, overweight, or milestone context needs cleanup | structural / maintenance | `ln-sync` |
| Session is ending or context is getting fragile | any | `ln-handoff` |

## Output

```md
## Assessment
- [orientation bullet]
- [orientation bullet]
- [1-2 sentences on current state and work classification]
```

## Routing

After assessment, present the top 2–3 relevant options from the routing table to the user (use `tool-ask-question`). Mark the best fit as recommended. If two skills are clearly sequential (for example `ln-scope` then `ln-build`), note the sequence in the recommended option's description.
