---
name: eng-tech-debt
version: 1.0.0
description: Identify, categorize, and prioritize technical debt into a ranked, defensible backlog that ties each remediation to impact and effort — a register, not a wish list.
author: matrixx0070
tags: [tech-debt, refactoring, prioritization, backlog, maintainability, risk]
capabilities: []
---

## When to use

When planning maintenance work, justifying refactor time to stakeholders, or auditing a codebase or service for accumulated risk. The aim is a ranked, honest list.

**Not for:** greenfield design, or renaming "any code I'd write differently" as debt. Debt is deferred cost that actively hurts — aesthetic disagreement isn't debt.

## Method

1. **Inventory concretely.** Gather from code smells, TODO/FIXME markers, incident postmortems, slow tests, flaky deploys, and team pain points. Name each item as *what is wrong and where* — a vague "the code is messy" gets dropped.
2. **Categorize each item:** Design (bad abstractions), Code (duplication, complexity), Test (gaps, flakiness), Infra/Ops (manual toil, fragile deploys), Dependency (outdated/unsupported), or Documentation.
3. **Assess impact and cost.** Impact = how often it hurts × how badly (velocity drag, incident risk, security exposure, onboarding friction). Cost = effort to fix. Estimate both, even roughly.
4. **Score and rank.** High-impact/low-cost first. If an item is high-impact but high-cost, don't jam it into a sprint — flag it as a project needing planning. If impact is low, park it explicitly (recording it counts as done).
5. **Separate deliberate from accidental debt.** Deliberate debt (a conscious shortcut) needs a written payoff trigger; accidental debt (neglect) needs a root-cause note so it stops recurring.
6. **Recommend a next-cycle slice** — the small set with the best impact-to-effort ratio.

## Example

```
Debt register (excerpt):
  | Item                              | Cat   | Location        | Impact | Cost | Pri |
  | Auth check duplicated in 6 routes | Code  | api/routes/*    | High   | Low  | P1  |
  | Payment tests mock the ledger     | Test  | test/pay/*      | High   | Med  | P1  |
  | Node 16 EOL runtime               | Dep   | Dockerfile      | High   | Med  | P2  |
  | 400-line God controller           | Design| orders.ctrl.ts  | Med    | High | P3  |
Quick win: extract shared auth middleware (High impact, Low cost).
Deferred: God controller — real but high-cost; schedule as a project.
```

## Pitfalls

- **A wish list, not a register** — every dislike logged with no impact/cost, so nothing is actually prioritizable.
- **Chasing low-impact, satisfying refactors** while high-impact debt festers.
- **No effort estimate**, so stakeholders can't weigh the trade and nothing gets funded.
- **Ignoring deliberate debt's payoff trigger** — the shortcut quietly becomes permanent.

## Output format

```
Debt register (table): item | category | location | impact | est. cost | priority
Top priorities: <ranked, one-line justification each>
Quick wins: <high impact, low effort>
Deferred / accept: <item + reason it's parked>
Recommended next-cycle slice: <the best impact-to-effort set>
```
