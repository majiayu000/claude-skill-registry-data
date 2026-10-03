---
name: engineering-figure-table
description: Plan, revise, audit, or polish figures, tables, captions, table notes, and visual evidence flow for English engineering conference or journal papers. Use when the user asks about figure responsibility, multi-panel layout, main-result tables, ablation tables, captions, table formatting, object/category naming consistency, page budget for visuals, or whether visuals support manuscript claims.
---

# Engineering Figure Table

Use this skill to make figures and tables serve the manuscript argument.

## Core Stance

- Define visual responsibility before visual styling.
- A figure or table should carry a specific claim, setup fact, evidence axis, or
  reader action.
- Do not let captions claim what the visual does not show.
- Visuals can illustrate mechanisms, but they cannot prove hidden mechanisms
  without direct visual, tabular, or experimental evidence.
- Do not use tables as unstructured parameter dumps unless the table's job is
  setup compression.
- Keep category names, metric names, captions, and prose consistent.

## Boundaries

- Use `engineering-writing` when the user needs section prose around the visual
  evidence.
- Use `engineering-polishing` for prose-only clarity or style work.
- Use `engineering-response` when visual changes are driven by reviewer or
  advisor comments.
- Use `engineering-validation` for final label/reference/build consistency
  before claiming submission readiness.

## When to Open Extra Files

| File | Open when |
|---|---|
| [references/visual-contract.md](references/visual-contract.md) | Planning figure/table responsibility or deciding which visuals are needed |
| [references/figure-roles.md](references/figure-roles.md) | Deciding what motivation, framework, workflow, gallery, or evidence figures should do |
| [references/captions.md](references/captions.md) | Writing or auditing captions and table notes |
| [references/tables.md](references/tables.md) | Designing setup, main results, ablation, or stress-test tables |
| [references/panel-claim-map.md](references/panel-claim-map.md) | Mapping every panel, row, or column to a manuscript claim |
| [references/figure-source-data-consistency.md](references/figure-source-data-consistency.md) | Checking that plotted values, source data, captions, and prose agree |
| [references/venue-figure-standards.md](references/venue-figure-standards.md) | Target venue family changes figure resolution, source data, or caption expectations |
| [references/consistency.md](references/consistency.md) | Checking category names, metrics, labels, caption style, and prose alignment |
| [references/page-budget.md](references/page-budget.md) | Cutting visual space, caption length, or table detail without damaging evidence |
| [references/examples.md](references/examples.md) | Needing concrete figure/table role examples and caption behavior |
| [references/failure-modes.md](references/failure-modes.md) | Handling captions or tables that claim more than the visual supports |
| [../_shared/evidence-boundary.md](../_shared/evidence-boundary.md) | Visual claims may exceed visible or tabulated evidence |
| [../_shared/claim-strength.md](../_shared/claim-strength.md) | Caption or table note verbs may overstate what is visible |
| [../_shared/output-mode.md](../_shared/output-mode.md) | The user asks for caption/table output only |
| [../_shared/terminology-ledger.md](../_shared/terminology-ledger.md) | Category, metric, object, or method names change across visuals and prose |

## Workflow

1. State the paper claim the visual supports.
2. Assign one responsibility to each figure/table.
3. Map each panel, row, or column to a piece of evidence.
4. Check source-data and caption consistency when values, metrics, or panels
   are provided.
5. Check whether the caption states only visible or tabulated information.
6. Check consistency across prose, caption, labels, and notes.
7. Check whether any category/metric rename needs coordinated changes.
8. Remove or redesign a visual if it has no claim, setup fact, evidence axis, or
   reader action.
9. If editing LaTeX, preserve labels and references unless there is a direct
   reason to change them.

## Default Output

```text
Visual audit
| Item | Responsibility | Visible/tabulated evidence | Claim supported | Must not claim | Placement | Related prose action | Risk | Action |

Panel-claim map
| Panel/row/column | Claim served | Evidence shown | Source-data check | Caption boundary |

Caption/table revision
[English caption or table plan]

Consistency actions
- labels:
- category names:
- metric names:
- prose references:
```
