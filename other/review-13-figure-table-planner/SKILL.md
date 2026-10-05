---
name: review-13-figure-table-planner
description: Plan review figures, tables, graphical abstract, flowcharts, pathway/workflow diagrams, evidence tables, PRISMA flowcharts, and figure legends for a medical review. Mechanism diagrams are disabled by default unless the user explicitly requests one.
---

# Review 13 Figure Table Planner

## Purpose

Design figures and tables that summarize evidence without introducing unsupported mechanisms. For this workbench, the default visual output is flowchart, pathway map, workflow diagram, evidence framework, decision tree, PRISMA-style flow diagram, or graphical abstract. Do not plan molecular/cellular mechanism diagrams unless the user explicitly asks for a mechanism figure in the current turn.

## Required Inputs

- Manuscript outline.
- Evidence matrix.
- Source figure/table permissions status if reusing or adapting images.

## Output

Create `11_figures_tables/figure_table_plan.md` with:

- Figure list and purpose.
- Table list and variables.
- Source evidence for each panel.
- Required redraw/adaptation notes.
- Figure legends in draft form.
- Permission or original-redraw status.
- A diagram-type label for each figure: `flowchart`, `pathway_map`, `workflow`, `evidence_framework`, `decision_tree`, `graphical_abstract`, `table`, or `mechanism_only_if_user_asked`.

## Completion Gate

Pass only when every figure panel and table row has a traceable evidence source.

## Stop Rules

Do not copy published figures directly unless permission and citation requirements are documented.
Do not create mechanism diagrams by default. If a source template suggests a mechanism figure, convert it into a pathway/workflow/evidence framework unless the user explicitly asks for molecular mechanism visualization.
