---
name: ppt-defense-narrative-stage
description: "Create, review, or freeze the defense narrative and action-title spine for a manuscript-to-PPT workflow. Use after confirmed production brief and fact ledger exist, and before slide-by-slide storyboard, asset planning, PPTX generation, or render QA. This stage focuses on how to tell the defense story: central claim, argument arc, audience strategy, what to emphasize or omit, anticipated committee objections, and a ghost-deck-tested sequence of action titles. It must stop for human confirmation before storyboard work begins."
---

# PPT Defense Narrative Stage

## Role

Use this stage to decide how the defense should be told before deciding individual slide layouts.

This is not the storyboard. It is the talk-level argument plan that the storyboard must follow. It should answer:

- What is the one sentence the committee should remember?
- What does the audience need to believe first, second, and last?
- What parts of the paper should be emphasized, compressed, moved to backup, or omitted?
- Where should likely objections be pre-answered?
- Do the action titles alone tell a coherent argument?

## Required Inputs

Do not proceed unless these confirmed artifacts exist:

- `align/ppt_production_brief_v*.md`
- `align/fact_ledger_v*.md`

Use `codex-deep-interview` if any of these are still unclear:

- defense scenario, audience, time limit, slide count, or evaluation criteria;
- the main contribution claim the user wants to defend;
- advisor or committee preferences;
- rubric or committee map from the confirmed production brief;
- whether to optimize for passing defense, publication-style persuasion, demo impact, or technical rigor;
- which claims are risky, controversial, or not yet safe to emphasize.

Ask only high-impact questions. Do not deep-read sources again unless the fact ledger is visibly insufficient.

## Required Output

Write or update:

- `align/ppt_defense_narrative_v*.md`

Include this metadata:

```yaml
stage: defense_narrative
stage_status: draft | confirmed
requires_confirmed:
  - ppt_production_brief
  - fact_ledger
allowed_next_stage: ppt-storyboard-stage
confirmed_by: <user/date or empty>
source_inspirations:
  - https://github.com/Gabberflast/academic-pptx-skill
  - https://github.com/PHY041/claude-skill-academic-ppt
```

Use `stage_status: draft` until the user explicitly confirms the narrative. Codex must not self-confirm it.

## Narrative Requirements

The artifact must include:

- defense thesis: one sentence that captures the core defendable claim;
- audience contract: what the committee likely cares about and how the talk will satisfy it;
- rubric/committee strategy: how the story addresses known evaluator concerns and grading criteria;
- argument arc: situation -> gap/problem -> approach -> evidence -> contribution -> limitation/answer;
- emphasis map: must-say, can-compress, backup-only, and omit decisions;
- risk map: likely committee questions, weak spots, and where to pre-answer them;
- action-title spine: a sequence of complete-sentence slide titles, not topic labels;
- ghost deck test: a short check of whether the action titles alone tell the full story;
- storyboard handoff notes: slide count/timing implications and constraints for `ppt-storyboard-stage`;
- open decisions for the user.

Action titles should be claims or takeaways. Avoid labels like `Background`, `Method`, `Experiments`, or `Conclusion` unless paired with an actual statement.

## Guardrails

- Do not invent facts, results, baselines, datasets, or limitations.
- Do not replace the fact ledger as source of truth.
- Do not create the slide-by-slide storyboard in this stage.
- Do not plan assets, generate images, generate PPTX, or run render QA.
- Do not force the paper chapter order if a more persuasive defense order is needed.
- Keep backup content explicit so the main talk can stay focused.

## Stop Rule

After writing a draft defense narrative, stop and ask the user to review the story, emphasis choices, and action-title spine.

When the user confirms, update only `align/ppt_defense_narrative_v*.md` to `stage_status: confirmed`, record `confirmed_by`, then stop again. The next user turn must explicitly invoke or allow `ppt-storyboard-stage`.
