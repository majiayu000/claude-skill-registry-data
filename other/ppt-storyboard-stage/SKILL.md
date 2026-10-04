---
name: ppt-storyboard-stage
description: Create, review, or freeze a slide-by-slide storyboard for a manuscript-to-PPT workflow. Use only after confirmed production brief, confirmed fact ledger, and confirmed defense narrative exist, and before speaker notes/rehearsal, defense Q&A/backup planning, asset/layout planning, or PPTX generation.
---

# PPT Storyboard Stage

## Role

Use this stage to expand the confirmed defense narrative into a slide-by-slide storyboard. It is a mandatory stop gate.

Do not proceed unless these confirmed artifacts exist:

- `align/ppt_production_brief_v*.md`
- `align/fact_ledger_v*.md`
- `align/ppt_defense_narrative_v*.md`

Use native agent `ppt_storyboard` when available. The leader must inspect the result before asking the user to confirm it.

## Required Output

Write or update:

- `align/PPT_storyboard_v*.md`

Include:

```yaml
stage: storyboard
stage_status: draft | confirmed
requires_confirmed:
  - ppt_production_brief
  - fact_ledger
  - defense_narrative
allowed_next_stage: ppt-speaker-notes-rehearsal-stage
confirmed_by: <user/date or empty>
```

Use `stage_status: draft` until the user explicitly confirms the storyboard.

## Storyboard Requirements

Each slide must include:

- slide number and title
- action title inherited from or justified against the confirmed narrative spine
- one core point
- source facts or claim IDs
- exhibit discipline fields when `assertion_evidence_policy` is `strict` or `relaxed`:
  - exhibit type: source figure, data chart, table, diagram, quote, comparison, process, or none;
  - exhibit claim: what the exhibit proves;
  - `so_what_annotation`: the short takeaway the audience should read from the exhibit;
  - citation need: in-slide citation, references slide only, user-confirmed source, or not applicable;
- recommended visual form
- asset needs
- speaking points
- estimated time
- QA risk
- backup/merge/split notes when relevant

Avoid mechanical chapter compression. Optimize for the confirmed talk-level argument, not the manuscript chapter order.

If the confirmed brief sets `assertion_evidence_policy: strict`, every evidence-bearing content slide must have one main exhibit and one explicit `so_what_annotation`. If the policy is `relaxed`, record why a slide can be text-led or multi-exhibit. If the policy is `off`, preserve source fact IDs but do not force exhibit structure.

Run a quick ghost-deck check: the slide action titles, read alone, must still tell the confirmed defense story. If they do not, revise the storyboard or route back to `ppt-defense-narrative-stage` for human realignment.

## Stop Rule

After writing a draft storyboard, stop and ask the user to review, reorder, merge, split, or confirm. Do not draft speaker notes, plan Q&A/backup slides, plan assets, or generate PPTX in the same turn.

When the user confirms, update only the storyboard status to `stage_status: confirmed`, record `confirmed_by`, then stop again.
