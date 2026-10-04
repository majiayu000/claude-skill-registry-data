---
name: ppt-deck-build
description: Generate an editable PPTX draft from confirmed PPT workflow artifacts. Use only after confirmed production brief, fact ledger, defense narrative, storyboard, speaker notes/rehearsal, defense Q&A/backup-slide plan, template inventory, asset decisions, layout plan, content fidelity QA, and any required academic figure prompt/generated visual assets exist; stop before render QA.
---

# PPT Deck Build

## Role

Use this stage to build an editable draft deck. It is a mandatory stop gate before render QA.

Do not proceed unless confirmed artifacts exist:

- `align/ppt_production_brief_v*.md`
- `align/fact_ledger_v*.md`
- `align/ppt_defense_narrative_v*.md`
- `align/PPT_storyboard_v*.md`
- `align/ppt_speaker_notes_rehearsal_v*.md`
- `align/ppt_defense_qa_backup_v*.md`
- `align/PPT_asset_audit_v*.md`
- `align/ppt_layout_plan_v*.json`
- `align/ppt_content_fidelity_qa_v*.md`
- template inventory or equivalent confirmed template policy
- template design rules when the asset/layout stage produced them

If `align/visual_enrichment_plan_v*.md` marks `requires_academic_figure_prompt: true`, also require a confirmed `align/academic_figure_prompt_v*.md` and either approved generated image files or an explicit user decision to build without them.

Default to page-worker build mode. First create a deck build work order and page job list, then stop for human confirmation before dispatching any slide worker. After the work order is confirmed, the main thread schedules one `ppt_page_build` worker per slide and batches workers according to local native-agent capacity.

Use native agent `ppt_template_automation` only for deck-level assembly/template checks or for a user-approved fallback. This stage must not accept the deck as final.

## Scripts

- `scripts/inspect_pptx_template.py`: inspect template PPTX OOXML metadata without modifying the file.
- `scripts/prepare_deck_build_run.py`: create a resumable deck-build run directory and one page request per slide from a confirmed work order JSON.
- `scripts/page_job_status.py`: summarize queued/running/done/blocked/failed slide jobs for a run directory.
- `scripts/record_page_result.py`: record one page worker result and update the run-level job status and repair backlog.
- `scripts/finalize_deck_build.py`: summarize page outputs into a draft deck build summary after page workers finish.

Load `references/page-worker-contract.md` before preparing page jobs or instructing `ppt_page_build`. Load `references/deck-build-run-manifest.md` when creating, resuming, or finalizing a deck-build run directory.

## Required Outputs

Write or update:

- `generated_pptx_test/<deck>_v*.pptx`
- `align/ppt_deck_build_manifest_v*.md`
- `align/ppt_deck_build_work_order_v*.md` before page workers run
- `exp/ppt_deck_build/<run_id>/` with page requests, status files, page results, assembly logs, and repair backlog
- optional generation scripts or logs under `exp/`

The build manifest must include:

```yaml
stage: deck_build
stage_status: draft | confirmed
requires_confirmed:
  - ppt_production_brief
  - fact_ledger
  - defense_narrative
  - storyboard
  - speaker_notes_rehearsal
  - defense_qa_backup
  - asset_layout_plan
  - academic_figure_prompt_when_required
  - content_fidelity_qa
allowed_next_stage: ppt-render-qa-loop
confirmed_by: <user/date or empty>
deck_build_mode: page_worker | approved_monolithic_fallback
work_order_path: <path>
run_dir: <path>
page_worker_agent: ppt_page_build
```

Use `stage_status: draft` until the user explicitly confirms the draft is ready for render QA.

## Build Requirements

Prefer native editable PowerPoint objects: placeholders, text boxes, shapes, tables, charts, and inserted source or approved generated images. Avoid whole-page screenshots unless the confirmed brief accepts that tradeoff.

Follow confirmed `align/template_design_rules_v*.md` when present: slide bounds, typography, palette, citation/source line placement, logo/header/footer rules, appendix/backup conventions, and forbidden patterns.

Follow the visual production route from the asset/layout plan. Do not convert numeric result charts, evidence figures, or source tables into generated decorative images. If the preferred visual route fails, record the failure and use the confirmed fallback or stop for user confirmation.

Add confirmed speaker notes to the PowerPoint notes pane when the generation engine supports it. If notes-pane writing is not available, preserve the confirmed notes artifact path in the manifest and mark the limitation explicitly.

Build confirmed backup slides according to the Q&A/backup artifact and asset/layout plan. Keep backup-only slides separate from the main timed talk, using the confirmed placement policy: hidden, appendix, or after a Q&A separator.

Record slide count, main-slide count, backup-slide count, notes insertion status, content fidelity QA artifact path/status, template design rules path/status, visual route outcomes, template mapping, assets used, generated image provenance, workflow state hash when available, known pre-render risks, and the exact PPTX path.

## Page Worker Build Mode

The normal build path has two stops inside this stage:

1. Draft the deck build work order and machine-readable page jobs, then stop. Do not dispatch page workers while the work order is still draft.
2. After explicit user confirmation, dispatch page workers in batches, assemble the editable deck draft, write the build manifest, then stop before render QA.

The main thread owns scheduling, integration, and final evidence. Page workers own exactly one slide each. A page worker receives a single page request with exact source, claim, asset, layout, note, and backup indices. It must not rediscover the manuscript, redesign the narrative, change slide count, or perform whole-deck assembly.

If native subagents are unavailable, stop with a clear blocker and ask whether the user wants a manually confirmed fallback. Do not silently return to whole-deck generation.

## Stop Rule

After generating the work order, stop and ask the user to inspect or confirm worker dispatch. After generating the draft PPTX and manifest, stop and ask the user to inspect or confirm readiness for render QA. Do not run PowerPoint COM render QA in the same turn.

When the user confirms, update only the deck build manifest to `stage_status: confirmed`, record `confirmed_by`, then stop again.
