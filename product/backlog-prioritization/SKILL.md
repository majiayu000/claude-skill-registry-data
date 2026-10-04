---
name: backlog-prioritization
category: pm
description: Use when ordering board tasks - set priority/blocked_by/deploy_depends_on by severity and dependency, split MoSCoW within a feature, and use RICE/ICE only for a genuine "what next" call across several features
source: phuryn/pm-skills prioritization-frameworks (MIT), adapted
---
# Backlog Prioritization

## Overview

Prioritization decides what agents pick up next. TaskTrooper is a local, single-user product with no usage data, so a scored framework with invented numbers (fake "Reach 200") is theatre. Order by the levers the board actually enforces, and fall back to an explicit estimate only when several same-level features genuinely need ranking.

**Core principle:** `priority`, `blocked_by`, `deploy_depends_on` and backlog/todo are the real order. Score only when they tie.

## The real levers

| Lever | What it controls |
|---|---|
| `priority` (critical / high / medium / low) | The only persisted order field; sorts `list_ready_tasks` critical-first, then by age. |
| `blocked_by` | The enforced START order — a task parks in `blocked` while any listed task is open, and is picked up automatically when the last one lands. |
| `deploy_depends_on` | The enforced SHIP order — this task is not released until the listed ones are live. |
| backlog vs todo | The human gate — nothing in backlog is picked up; moving to todo starts it. |

## Priority ladder

- **critical** — data loss or corruption, a security exposure, the product unusable, a broken release.
- **high** — a core flow broken, a regression of shipped behaviour, an analiz that unblocks two or more tasks, a stated deadline.
- **medium** — default for a requested feature.
- **low** — cosmetic, nice-to-have, a Should/Could split-off from MoSCoW.

**Within a level:** the stakeholder's stated order, then unblockers (an analiz or a backend task other work depends on), then smaller work first.

## MoSCoW inside a feature

When scoping one feature or task:
- **Must** → this task's `acceptance_criteria`.
- **Should / Could** → separate backlog tasks, not folded into this one's criteria.
- **Won't** → the `description`'s Out of Scope line, with the reason.

## RICE/ICE — only for an explicit "what's next" call

Use a lightweight score only when the stakeholder asks "what should we do next" across three or more same-priority-level features, and label every factor as an estimate with its basis — never invent a reach number with no usage data behind it.

`score = (Impact × Confidence) ÷ Effort` (ICE; drop Reach — there's no multi-user traffic to count). Impact and Confidence are 1–3 with a one-line reason each; Effort is developer-days from the architect's estimate if one exists, otherwise your own rough guess labelled as such.

## Worked Example

Three candidates in `backlog`:
- A data-loss bug on task delete → `priority: critical`, `todo` immediately — ladder override, no scoring needed.
- An analiz for reporting that unblocks three planned tasks → `priority: high` (unblocker), `todo`.
- A new dark-mode toggle the stakeholder mentioned once → `priority: medium`, stays in `backlog` until they confirm it's next.

If the stakeholder then asks "dark mode, bulk delete, or CSV export — what first?": ICE each in one line (dark mode: Impact 1/low because cosmetic, Confidence 3, Effort 2 → ICE 1.5; bulk delete: Impact 2, Confidence 3, Effort 1 → ICE 6; export: Impact 2, Confidence 2, Effort 3 → ICE 1.3) and recommend bulk delete first, with the basis stated, not just the number.

## Common Mistakes

- Scoring every backlog item with RICE instead of using `priority`/`blocked_by` directly.
- Inventing a reach/impact number with no basis and presenting it as data.
- A Should/Could item folded into a Must task's criteria instead of split off.
- Holding work in `backlog` to fake an order that `blocked_by` should enforce.

## Red Flags

- A known data-loss bug sitting below a feature in `priority`.
- An unblocking analiz left at `medium` or in `backlog`.
- A RICE score with a "Reach" number nobody can source.
