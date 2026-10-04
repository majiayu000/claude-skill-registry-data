---
name: ppt-defense-qa-backup-stage
description: "Create, review, or freeze a defense Q&A plan and backup slide artifact for a manuscript-to-PPT workflow. Use after confirmed production brief, fact ledger, defense narrative, storyboard, and speaker notes/rehearsal exist, and before asset/layout planning, PPTX generation, or render QA. This stage designs anticipated questions, answer strategy, evidence anchors, and backup-only slides; it must stop for human confirmation."
---

# PPT Defense QA Backup Stage

## Role

Use this stage to prepare the defense conversation after the main talk is already storyboarded and rehearsable. It is a mandatory stop gate before asset/layout planning.

Do not proceed unless these confirmed artifacts exist:

- `align/ppt_production_brief_v*.md`
- `align/fact_ledger_v*.md`
- `align/ppt_defense_narrative_v*.md`
- `align/PPT_storyboard_v*.md`
- `align/ppt_speaker_notes_rehearsal_v*.md`

Use `codex-deep-interview` if any of these are still unclear:

- who may ask difficult questions and what they care about;
- which rubric or committee-map concerns should be covered;
- which claims, methods, metrics, baselines, experiments, or limitations feel risky;
- whether backup slides should be hidden, appendix-only, or included after a Q&A separator;
- how direct, defensive, cautious, or exploratory the answer style should be.

Ask only high-impact questions. Do not invent evidence or promise experiments that do not exist.

## Required Output

Write or update:

- `align/ppt_defense_qa_backup_v*.md`

Include this metadata:

```yaml
stage: defense_qa_backup
stage_status: draft | confirmed
requires_confirmed:
  - ppt_production_brief
  - fact_ledger
  - defense_narrative
  - storyboard
  - speaker_notes_rehearsal
allowed_next_stage: ppt-asset-layout-plan
confirmed_by: <user/date or empty>
```

Use `stage_status: draft` until the user explicitly confirms the Q&A and backup-slide plan. Codex must not self-confirm it.

## Q&A Requirements

Create a question matrix with:

- question ID;
- likely question or objection;
- concern behind the question;
- answer thesis in one sentence;
- concise answer draft;
- source fact, claim, figure, experiment, or limitation anchors;
- rubric or committee concern covered when applicable;
- main slide anchor and backup slide anchor when relevant;
- risk level;
- safe fallback if the answer is unknown, out of scope, or needs follow-up.

Cover at least:

- contribution novelty;
- method validity;
- data, baseline, metric, or experimental design choices;
- failure cases and limitations;
- practical significance;
- relation to prior work;
- threats to validity or generalization.

## Backup Slide Requirements

Define every backup-only slide with:

- backup slide ID and action title;
- question(s) it answers;
- evidence source and fact IDs;
- visual or table needed;
- asset source or generation/redraw requirement;
- placement policy: hidden, appendix, or after Q&A separator;
- whether it should be counted in the main talk duration;
- editability and QA risks.

Backup slides must defend real questions. Do not add decorative or speculative slides.

## Guardrails

- Do not change confirmed speaker notes or storyboard unless routing back to the responsible stage.
- Do not plan detailed layout geometry; leave that to `ppt-asset-layout-plan`.
- Do not generate images, generate PPTX, or run render QA.
- Do not over-answer by adding unsupported claims.
- Mark weak evidence, missing comparisons, and unsafe answers as open decisions.

## Stop Rule

After writing a draft Q&A and backup-slide artifact, stop and ask the user to review, challenge, revise, or confirm.

When the user confirms, update only `align/ppt_defense_qa_backup_v*.md` to `stage_status: confirmed`, record `confirmed_by`, then stop again. The next user turn must explicitly invoke or allow `ppt-asset-layout-plan`.
