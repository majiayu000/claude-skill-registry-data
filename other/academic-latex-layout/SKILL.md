---
name: academic-latex-layout
description: "Use when working on academic paper LaTeX layout, figure/table float placement, draft-to-template LaTeX generation, existing .tex project layout repair, figures piling up, figures far from text, large blank areas, two-column figure/table placement, page-limit layout cleanup, or compiled PDF layout review."
---

# Academic LaTeX Layout

LaTeX layout and float-placement router for academic papers. Optimize figure/table placement by semantic adjacency and compiled PDF evidence, not by source-level hacks.

## Router Protocol

1. Read `manifest.yaml`.
2. Read every file listed under `always_load`.
3. Detect exactly one mode from the manifest.
4. Echo the selected mode before executing.
5. Reach for `references/` only when the manifest condition is satisfied.

## Modes

| Mode | Use when |
|---|---|
| `draft-to-latex-layout` | Draft + template + existing figures/tables must become LaTeX with semantically placed floats |
| `layout-repair` | Existing `.tex` project has float pileups, text/figure drift, blank areas, or two-column layout problems |
| `layout-audit` | User wants diagnosis only, without edits |

## Boundaries

Do not generate data figures; use `academic-figure`. Do not broadly polish prose; use `academic-polishing`. Do not decide which figures the paper should contain.

## Completion Criteria

- Template constraints identified or bounded.
- Figure/table semantic map produced.
- Direct edits follow risk policy.
- Compile and PDF preview loop run when feasible; otherwise bounded assessment explains the blocker.
- Final report follows `references/report-format.md`.
