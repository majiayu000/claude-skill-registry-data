---
name: ppt-production-brief
description: Create, review, or freeze the first human-confirmed production brief for a manuscript-to-PPT workflow. Use when Codex must clarify audience, scene preset, rubric or committee expectations, duration, slide count, materials, template policy, assertion-evidence preference, visual policy, editability, QA thresholds, non-goals, or acceptance criteria before any fact grounding, storyboard, asset planning, PPTX generation, or render QA.
---

# PPT Production Brief

## Role

Use this stage to create the workflow contract. This is a mandatory stop gate.

Start with `codex-deep-interview` unless the user already supplied a current confirmed brief. Ask only high-impact questions, one at a time. Do not inspect sources deeply, build facts, create a storyboard, generate assets, or create a deck in this stage.

## Required Output

Write or update:

- `align/ppt_production_brief_v*.md`

The brief must include a status block:

```yaml
stage: production_brief
stage_status: draft | confirmed
allowed_next_stage: ppt-material-fact-ledger
confirmed_by: <user/date or empty>
```

Use `stage_status: draft` until the user explicitly confirms the brief. Codex must not self-confirm it.

## Brief Contents

Record:

- audience and presentation setting
- scene preset: `defense | conference | seminar | proposal | progress | project_review | custom`
- rubric and committee map: evaluator roles, likely concerns, grading criteria, advisor preferences, and known sensitive claims
- target duration and slide count or range
- language, identity fields, and cover requirements
- material bundle and missing materials
- source priority when files conflict
- template file and whether it is binding or only style inspiration
- output priority: editable PPTX, polish, speaker notes, or rough draft
- assertion-evidence policy: `strict | relaxed | off`, with the user's rationale when not strict
- visual enrichment policy, including OpenRouter ICU Image permission
- visual production routing preference for source figures, data charts, flow/structure diagrams, source-derived concept diagrams, and decorative visuals
- editability policy and whole-slide-image policy
- `python_pptx_policy`
- `powerpoint_com_qa_policy`
- render fallback policy
- workflow state policy: whether to maintain `align/ppt_workflow_state.json` after confirmed stage artifacts
- non-goals
- acceptance criteria and visual QA thresholds
- planned stage sequence and native agent lanes

Default scene preset guidance:

- `defense`: emphasize defendable contribution, methods validity, limitations, Q&A, and backup slides.
- `conference`: emphasize novelty, key result, speed, audience memory, and concise takeaway.
- `seminar`: allow deeper background, method detail, and discussion prompts.
- `proposal`: emphasize gap, plan, feasibility, risks, milestones, and expected contribution.
- `progress`: emphasize completed work, blockers, next decisions, and evidence of progress.
- `project_review`: emphasize stakeholder value, decision points, delivery status, and risks.

## Stop Rule

After writing a draft brief, stop and ask the user to review, edit, or confirm. Do not continue to material inventory or fact grounding in the same turn.

When the user later confirms the brief, update only the brief status to `stage_status: confirmed`, record `confirmed_by`, then stop again. The next user turn must explicitly invoke or allow `ppt-material-fact-ledger`.
