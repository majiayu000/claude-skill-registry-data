---
name: ppt-asset-layout-plan
description: Create, review, or freeze the template inventory, asset decisions, visual enrichment plan, and editable layout plan for a PPT workflow. Use after confirmed brief, fact ledger, defense narrative, storyboard, speaker notes/rehearsal, and defense Q&A/backup-slide plan exist, and before PPTX generation or academic figure prompt/image generation.
---

# PPT Asset Layout Plan

## Role

Use this stage to decide how every confirmed slide will be built. It is a mandatory stop gate before deck generation.

Do not proceed unless confirmed artifacts exist:

- `align/ppt_production_brief_v*.md`
- `align/fact_ledger_v*.md`
- `align/ppt_defense_narrative_v*.md`
- `align/PPT_storyboard_v*.md`
- `align/ppt_speaker_notes_rehearsal_v*.md`
- `align/ppt_defense_qa_backup_v*.md`

Use this stage to decide whether any slide needs a generated academic visual. Do not call `openrouter-icu-image` from this stage. If a source-derived academic diagram prompt is needed, route next to `academic-figure-prompt` and stop for confirmation.

Use `openrouter-icu-image` only after a separate confirmed prompt exists and the confirmed brief allows visual generation or editing. Do not generate fake evidence, charts, screenshots, scientific images, or result visuals.

## Required Outputs

Write or update:

- `align/template_inventory_v*.md`
- optional `align/template_design_rules_v*.md`
- optional `align/template_layout_map_v*.json`
- `align/PPT_asset_audit_v*.md`
- optional `align/PPT_asset_manifest_v*.csv`
- optional `align/visual_enrichment_plan_v*.md`
- `align/ppt_layout_plan_v*.json`

Every Markdown output must include:

```yaml
stage: asset_layout_plan
stage_status: draft | confirmed
requires_confirmed:
  - ppt_production_brief
  - fact_ledger
  - defense_narrative
  - storyboard
  - speaker_notes_rehearsal
  - defense_qa_backup
allowed_next_stage: academic-figure-prompt | ppt-content-fidelity-qa-stage
confirmed_by: <user/date or empty>
```

Use `stage_status: draft` until the user explicitly confirms asset and layout decisions.

## Planning Requirements

For each slide record:

- template layout choice and reason
- editable content structure
- reuse/redraw/generate/omit/confirm asset decision
- source asset paths and licenses/risks when known
- generated visual role: evidence, source-derived diagram, illustration, or decoration
- visual production route: source reuse, local plotting, local editable diagram/ImageGen fallback, academic figure prompt, or no generation
- whether `academic-figure-prompt` is required before any image generation
- source fact IDs and exact slide anchors for every generated academic visual
- editability tradeoffs
- expected QA risks
- speaker-note implications for the PPT notes pane
- backup-only status, appendix placement, and Q&A anchor when relevant

Template inventory should record slide size, masters, layout names, placeholder geometry, theme fonts/colors, logos, headers, footers, and suitable layouts.

Template design rules should record binding typography, color, logo/header/footer rules, forbidden layouts, preferred slide archetypes, and any template-specific QA risks. Keep it compact and reusable for `ppt-deck-build`.

## Visual Production Routing

Use this routing table unless the confirmed production brief says otherwise:

| Visual need | Default route | Required evidence | Notes |
|---|---|---|---|
| Existing paper figure or table | `source_reuse` or `source_redraw` | source file path, caption, fact IDs | Prefer source reuse/redraw for evidence. Do not regenerate evidence with image tools. |
| Data chart from experiment outputs | `local_plotting` / `thesis-figure-pipeline` | data file path, metric definition, plotting script path when created | Use reproducible local plotting for charts. Do not use ImageGen for numeric result charts. |
| Flowchart, pipeline, framework, or structure diagram | `local_editable_diagram` first, `imagegen_fallback` only if approved | source facts, node/edge list, editability policy | Prefer editable PowerPoint shapes, Mermaid, or existing local skills. ImageGen fallback must stay explanatory, not evidence. |
| Source-derived academic concept diagram | `academic_figure_prompt` | slide anchor, fact IDs, allowed visual boundaries | Requires confirmed `align/academic_figure_prompt_v*.md` and later content fidelity QA. |
| Decorative or atmospheric visual | `no_generation` unless explicitly approved | brief permission and purpose | Never use decorative visuals to imply findings. |

Each routed visual must record:

- `visual_route`;
- `route_reason`;
- `source_anchor`;
- `editable_output_expected`;
- `evidence_status`: `source_evidence | source_derived_explanation | illustrative_only | decorative`;
- `generation_allowed`: `yes | no | needs_user_confirmation`;
- fallback if the preferred route fails.

## Template Design Rules

When a template or prior PPT is available, write `align/template_design_rules_v*.md` with:

- slide size and aspect ratio;
- theme fonts, body font minimums, CJK font policy, and equation/code font policy;
- color palette, accent colors, and prohibited color combinations;
- logo, header, footer, page number, school/lab brand, and confidentiality markings;
- master/layout names and suitable use cases;
- placeholder geometry and safe content bounds;
- preferred layouts for title, agenda, section divider, method, result, comparison, backup, and Q&A slides;
- forbidden layout patterns, such as dense screenshots, unreadable axis labels, decorative-only imagery, or nested cards;
- citation/source line placement;
- appendix and backup slide visual rules;
- template-specific render QA risks.

Do not make template design rules decorative. They are build constraints for `ppt-deck-build` and QA criteria for `ppt-render-qa-loop`.

## Stop Rule

If any slide has an asset decision of `generate` or `redraw` for a source-derived academic diagram, write this explicitly in `align/visual_enrichment_plan_v*.md`:

```yaml
requires_academic_figure_prompt: true
required_prompt_artifact: align/academic_figure_prompt_v*.md
```

After writing draft asset/layout plans, stop and ask the user to review or confirm. Do not draft academic figure prompts, run content fidelity QA, generate images, or generate PPTX in the same turn.

When the user confirms, update only the relevant status blocks to `stage_status: confirmed`, record `confirmed_by`, then stop again.
