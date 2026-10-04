---
name: manuscript-to-ppt-workflow
description: "Thin stage orchestrator for manuscript, thesis, paper, report, LaTeX project, asset folder, experiment output, or proposal to editable PPTX. Use to route the user through mandatory human-confirmed stages: production brief, material/fact ledger, defense narrative, storyboard, speaker notes/rehearsal, defense Q&A/backup slides, asset/layout plan, optional academic figure prompt, content fidelity QA, deck build, and render QA. This skill must stop after every stage artifact and never auto-advance."
---

# Manuscript To PPT Workflow

## Role

Use this skill only as the workflow router. It does not replace the stage skills and must not run the full deck pipeline in one turn.

Every stage is a hard human-alignment gate. After a stage writes a draft artifact, stop and ask the user to review, revise, or confirm. Continue only after the user explicitly confirms/freeze the prior stage artifact.

## Stage Skills

Run stages in this order:

| Stage | Skill | Required confirmed input | Main output |
|---|---|---|---|
| 1 | `ppt-production-brief` | user request and materials known enough to interview | `align/ppt_production_brief_v*.md` |
| 2 | `ppt-material-fact-ledger` | confirmed production brief | `align/material_inventory_v*.md`, `align/fact_ledger_v*.md` |
| 3 | `ppt-defense-narrative-stage` | confirmed brief and fact ledger | `align/ppt_defense_narrative_v*.md` |
| 4 | `ppt-storyboard-stage` | confirmed brief, fact ledger, and defense narrative | `align/PPT_storyboard_v*.md` |
| 5 | `ppt-speaker-notes-rehearsal-stage` | confirmed brief, fact ledger, defense narrative, storyboard | `align/ppt_speaker_notes_rehearsal_v*.md` |
| 6 | `ppt-defense-qa-backup-stage` | confirmed speaker notes/rehearsal | `align/ppt_defense_qa_backup_v*.md` |
| 7 | `ppt-asset-layout-plan` | confirmed Q&A/backup artifact | template inventory, asset audit, visual plan, layout plan |
| 8 | `academic-figure-prompt` | confirmed asset/layout plan that requires generated academic visuals | `align/academic_figure_prompt_v*.md` |
| 9 | `ppt-content-fidelity-qa-stage` | confirmed upstream artifacts, layout plan, and any required figure prompt | `align/ppt_content_fidelity_qa_v*.md` |
| 10 | `ppt-deck-build` | confirmed content fidelity QA, layout plan, notes, backup plan, and any required figure prompt/assets | deck build work order, page-worker run, editable PPTX draft, and build manifest |
| 11 | `ppt-render-qa-loop` | confirmed deck build manifest | rendered screenshots, QA report, and repair backlog when needed |

Default stage gate:

```yaml
stage_status: draft | confirmed
```

Codex may write `draft`. Only the user may cause `confirmed`.

## Routing Rules

1. If no confirmed production brief exists, route to `ppt-production-brief`.
2. If the brief is confirmed but no confirmed fact ledger exists, route to `ppt-material-fact-ledger`.
3. If facts are confirmed but no confirmed defense narrative exists, route to `ppt-defense-narrative-stage`.
4. If defense narrative is confirmed but no confirmed storyboard exists, route to `ppt-storyboard-stage`.
5. If storyboard is confirmed but no confirmed speaker notes/rehearsal artifact exists, route to `ppt-speaker-notes-rehearsal-stage`.
6. If speaker notes/rehearsal are confirmed but no confirmed Q&A/backup-slide artifact exists, route to `ppt-defense-qa-backup-stage`.
7. If Q&A/backup-slide plan is confirmed but no confirmed asset/layout plan exists, route to `ppt-asset-layout-plan`.
8. If the confirmed asset/layout plan says an AI-generated academic visual or image2/gpt-image academic prompt is required, and no confirmed `align/academic_figure_prompt_v*.md` exists, route to `academic-figure-prompt`.
9. If all required prompt artifacts are confirmed but no confirmed content fidelity QA exists, route to `ppt-content-fidelity-qa-stage`.
10. If content fidelity QA is confirmed and the user asks to generate the image asset, route to `openrouter-icu-image`; do not generate images in the same turn that drafts the prompt or writes content fidelity QA.
11. If content fidelity QA is blocked, route defects back to the responsible earlier stage. Do not generate a deck.
12. If content fidelity QA is confirmed and all required generated assets are approved or explicitly waived, but no deck build work order exists, route to `ppt-deck-build` to draft the work order and then stop for confirmation.
13. If the deck build work order is confirmed but no draft deck build manifest exists, route to `ppt-deck-build` to dispatch page workers in batches and assemble the editable PPTX draft, then stop.
14. If deck build is confirmed but no render QA report exists, route to `ppt-render-qa-loop`.
15. If render QA fails, route defects back to the responsible earlier stage. Do not silently repair in the QA stage.

## Non-Negotiable Stop Rule

Do not execute two stages in one assistant turn. Do not combine production brief, fact extraction, defense narrative, storyboard, speaker notes/rehearsal, Q&A/backup planning, asset planning, academic figure prompt drafting, content fidelity QA, image generation, deck generation, and render QA into a single run.

The only allowed same-turn action after writing a stage artifact is to summarize the artifact path, list open decisions, and ask the user to confirm or revise.

Generated academic visuals have three gates: first confirm `academic-figure-prompt`, then confirm `ppt-content-fidelity-qa-stage`, then run `openrouter-icu-image` only when the user approves image generation. Do not let Codex invent visual content to fill missing research facts.

Deck build has an internal dispatch gate: first draft the deck build work order and stop; only after user confirmation may Codex dispatch `ppt_page_build` workers. After page-worker assembly writes the editable PPTX draft and build manifest, stop again before render QA.

Maintain `align/ppt_workflow_state.json` when practical. It is a resume aid, not a replacement for confirmed artifact checks. Optional Phase 2 artifacts such as `align/rehearsal_evidence_v*.md` and `align/template_design_rules_v*.md` should be recorded there when present.

## Agents

Native custom agents are bounded workers, not stage owners:

- `ppt_storyboard`: used inside `ppt-storyboard-stage`.
- `ppt_page_build`: used inside `ppt-deck-build`; each worker owns exactly one slide/page job.
- `ppt_template_automation`: used inside `ppt-deck-build` only for deck-level assembly/template checks or a user-approved fallback.
- `ppt_render_qa`: used inside `ppt-render-qa-loop`.

Do not create agents for production alignment, fact extraction, defense narrative, speaker notes/rehearsal, defense Q&A/backup planning, content fidelity QA, or default asset audit. Those are human-review stage outputs.

If native subagent tools are unavailable, stop before the affected stage and report the fallback option. Continue locally only after user confirmation.

## Figma Policy

Figma is not part of the default PPT-native lane. Use `figma-context-mcp` only if the user explicitly starts a separate Figma experiment or provides Figma context as a read-only visual reference. Official Figma writes require explicit `figma_write_policy`.

## Hook Guardrail

This repository may include `.codex/hooks.json` and `.codex/hooks/ppt_stage_gate.ps1` to remind and block common stage-skipping write attempts. Treat hooks as guardrails, not as the only source of truth. The stage skills and user confirmation remain mandatory.

## Scripts

- `scripts/update_ppt_workflow_state.py`: scan known stage artifacts, including optional rehearsal evidence and template design rules, then write `align/ppt_workflow_state.json` with latest paths, statuses, SHA-256 hashes, and the next required stage. Use after confirming a stage artifact or when resuming a workflow.

## Prompt Template

```text
Use $manuscript-to-ppt-workflow.

Task:
Route this PPT workflow to the next required stage. Do not execute more than one stage. Stop after writing a draft artifact and ask me to review or confirm before continuing.
```
