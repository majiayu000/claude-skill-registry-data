---
name: engineering-paper-router
description: Route ambiguous or mixed English engineering paper tasks to the correct engineering paper skill. Use when the user asks broadly to improve my paper, check my manuscript, revise this draft, prepare submission, respond to comments, or combine drafting, polishing, figure/table work, response drafting, and validation.
---

# Engineering Paper Router

Use this skill only to choose the right workflow and required inputs. Do not
write final manuscript prose unless the user explicitly asks to continue after
routing.

## Core Stance

- Route first; do not draft first.
- Preserve evidence boundaries in the recommended next prompt.
- For mixed tasks, name a primary skill, secondary skills, and workflow order.
- If readiness or completion is requested, include `engineering-validation`.
- Explain why plausible but non-primary skills should not run first.
- Stop routing at the first missing input that would make the next step invent
  facts, citations, line numbers, experiment results, or readiness status.

## Boundaries

- Use this skill when the correct engineering paper skill is unclear.
- Do not use it when the user explicitly names one of the five task skills and
  the request matches that skill.

## When to Open Extra Files

| File | Open when |
|---|---|
| [references/examples.md](references/examples.md) | Needing routing examples |
| [references/failure-modes.md](references/failure-modes.md) | Avoiding router overreach or single-skill bias |
| [../_shared/evidence-boundary.md](../_shared/evidence-boundary.md) | Routing tasks that request strong claims, citations, validation, or missing-evidence work |
| [../_shared/story-spine.md](../_shared/story-spine.md) | Full-paper, abstract, introduction, or major revision tasks need story-first ordering |
| [../_shared/ai-assisted-writing-policy.md](../_shared/ai-assisted-writing-policy.md) | User requests AI-polished or venue-ready prose where author responsibility or disclosure may matter |
| [../_shared/output-mode.md](../_shared/output-mode.md) | User asks for a short route only |

## Routing Table

| User task | Route |
|---|---|
| draft/rebuild title, abstract, Introduction, Methods, Experiments, Discussion, or Conclusion | `engineering-writing` |
| polish existing prose, improve flow, downgrade claims, translate source notes into English prose | `engineering-polishing` |
| plan or revise figures, tables, captions, visual roles, page budget, or visual consistency | `engineering-figure-table` |
| classify reviewer/advisor/editor comments, build revision tracker, draft response letter | `engineering-response` |
| compile/check manuscript, inspect citations, claim-evidence anchors, figures/tables, readiness | `engineering-validation` |

## Input-State Routing

| Input state | Primary route | Secondary route | Stop condition |
|---|---|---|---|
| Thin idea, no method/evidence/boundary | `engineering-writing` scaffold only | none | Do not draft final Abstract/Conclusion |
| Notes plus result tables, no figure responsibilities | `engineering-writing` | `engineering-figure-table` | Do not write strong claims before evidence map |
| Existing paragraph with stable claim/evidence | `engineering-polishing` | `engineering-writing` only if structure fails | Stop if claim, evidence, and boundary are unclear |
| Caption, table, category names, or visual claims | `engineering-figure-table` | `engineering-polishing` for caption wording only | Stop if visual evidence cannot support the requested claim |
| Reviewer/advisor/editor comments | `engineering-response` | writing/figure-table/validation as needed | Stop before final response if edits are not verified |
| Ready/complete/submittable request | `engineering-validation` | writing/figure-table/response for blocking fixes | Stop if build, references, or source files are missing |

## Mixed Workflow Order

For full-paper work, use this order unless the user gives a narrower task:

1. `engineering-paper-auditor`: story-spine and blocker audit if the draft is
   already written or the task is broad.
2. `engineering-writing`: one-sentence thesis, story spine, and
   contribution-evidence map.
3. `engineering-figure-table`: visual responsibility and evidence roles.
4. `engineering-writing`: Methods and Experiments before Introduction.
5. `engineering-writing`: Introduction, Abstract, Conclusion.
6. `engineering-polishing`: paragraph flow, terminology, and claim strength.
7. `engineering-response`: only if comments exist.
8. `engineering-validation`: before claiming complete, fixed, or ready.

## Default Output

```text
Recommended route
- Primary skill:
- Secondary skill:
- Reason:

Task decomposition
- User request contains:
- Primary operation:
- Secondary operations:

Do not use first
| Skill | Why not primary |

Workflow order
| Step | Skill | Required input | Stop condition |

Required inputs
- ...

Evidence boundary
- Do not invent:
- Must verify before claiming ready:

Next prompt to use
[copyable prompt]
```
