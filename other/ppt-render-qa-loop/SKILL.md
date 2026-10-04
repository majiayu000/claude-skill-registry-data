---
name: ppt-render-qa-loop
description: Render a generated PPTX through PowerPoint COM or an approved fallback, inspect screenshots, write a QA report, and stop for human acceptance or repair routing. Use only after a confirmed deck build manifest exists.
---

# PPT Render QA Loop

## Role

Use this stage to render-check a generated deck. It is the acceptance gate, not an automatic repair stage.

Do not proceed unless a confirmed `align/ppt_deck_build_manifest_v*.md` exists and points to a generated PPTX. Use native agent `ppt_render_qa` when available.

## Scripts

- `scripts/render_pptx_powerpoint_com.ps1`: open a PPTX with PowerPoint COM and export slide PNGs and optional PDF.

## Required Outputs

Write or update:

- `qa/rendered_pages/*`
- optional `qa/deck_render.pdf`
- optional contact sheet
- `qa/ppt_render_qa_v*.md`
- `qa/ppt_repair_backlog_v*.md` when defects are found or human repair routing is needed

The QA report must include:

```yaml
stage: render_qa
stage_status: pass | fail | needs_human_acceptance
requires_confirmed:
  - deck_build
allowed_next_stage: human_acceptance_or_repair
accepted_by: <user/date or empty>
```

Codex must not mark `accepted_by` unless the user explicitly accepts the rendered deck.

Also inspect the confirmed deck build manifest for speaker-note and backup-slide evidence. Render QA cannot fully judge notes-pane content visually, but it must report whether the manifest claims notes were inserted, omitted, or preserved as an external artifact.

## Academic QA Checklist

Report pass/fail/needs-human-review for:

- every content slide has an action title, not only a topic label;
- ghost-deck sequence still tells the argument;
- borrowed figures, data points, and external claims have visible slide citations or a documented citation policy;
- result slides expose one main exhibit and a clear "so what" takeaway when the production brief requires assertion-evidence discipline;
- a references or source slide exists when borrowed sources are used;
- the final non-appendix slide is a conclusion, decision, or Q&A handoff rather than a blank or generic thank-you slide;
- body text and chart labels are readable under the confirmed presentation setting;
- backup slides and appendix/Q&A separator match the confirmed Q&A/backup artifact;
- no decorative generated visuals are presented as evidence.
- template design rules are followed for fonts, safe bounds, logo/header/footer, citation placement, backup slide treatment, and forbidden patterns when the artifact exists.

## Blocking Failures

Fail the run for:

- title/subtitle overlap
- clipped text
- unreadable charts, tables, formulas, or figures
- severe crowding
- missing CJK glyphs or wrong font substitution
- blank pages
- content outside slide bounds
- missing images/assets
- missing required backup slides or appendix/Q&A separator
- obvious template/logo/header/footer misuse
- academic QA blocker such as unsupported evidence visual, missing required citations, or unreadable results exhibit
- violation of confirmed template design rules that changes readability, branding, citation visibility, or backup/appendix interpretation

When failing or requiring human repair, write `qa/ppt_repair_backlog_v*.md`. Each repair item must include severity, evidence screenshot/page, owner stage, suggested repair path, and whether human confirmation is required.

## Stop Rule

After writing QA evidence, stop and ask the user to accept the deck or route defects back to the correct earlier stage. Do not silently repair or generate a replacement PPTX in the same turn.
