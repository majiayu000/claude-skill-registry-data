---
name: ppt-material-fact-ledger
description: Build the human-reviewable material inventory, source priority map, fact ledger, and claim-source map for a PPT workflow. Use after a confirmed `align/ppt_production_brief_v*.md` exists, and before defense narrative, storyboard, asset planning, PPTX generation, or render QA.
---

# PPT Material Fact Ledger

## Role

Use this stage to ground the deck in source material. It is a mandatory stop gate after the production brief.

Do not proceed unless a current `align/ppt_production_brief_v*.md` has `stage_status: confirmed`. Use `research-fact-source-sync` when it helps align claims, metrics, terminology, figures, and limitations.

## Required Outputs

Write or update:

- `align/material_inventory_v*.md`
- `align/fact_ledger_v*.md`
- optional `align/material_manifest_v*.csv`
- optional `align/claim_source_map_v*.md`

Each Markdown output must include:

```yaml
stage: material_fact_ledger
stage_status: draft | confirmed
requires_confirmed: ppt_production_brief
allowed_next_stage: ppt-defense-narrative-stage
confirmed_by: <user/date or empty>
```

Use `stage_status: draft` until the user explicitly confirms the facts. Codex must not self-confirm them.

## Inventory Requirements

Record every available or missing material:

- manuscript PDF, DOCX, Markdown, LaTeX, BibTeX, compiled PDF
- figures, tables, experiment outputs, notebooks, logs, screenshots
- prior slides, posters, advisor notes, comments
- brand/school assets, logos, fonts, template PPTX

For each item record path, type, authority level, likely slide use, extraction method, and risk.

## Fact Ledger Requirements

Ground:

- one-line thesis or project claim
- contributions and safe wording
- method/system components
- datasets, baselines, metrics, results, and limitations
- figure/table use decisions
- terminology
- high-risk claims and safer answers

Do not invent baselines, metrics, figures, identities, or conclusions.

## Stop Rule

After writing draft inventory/facts, stop and ask the user to review, correct, or confirm. Do not create defense narrative, storyboard, asset plan, or PPTX in the same turn.

When the user confirms, update only the relevant status blocks to `stage_status: confirmed`, record `confirmed_by`, then stop again.
