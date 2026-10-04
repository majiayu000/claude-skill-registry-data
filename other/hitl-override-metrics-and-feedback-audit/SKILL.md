---
name: hitl-override-metrics-and-feedback-audit
description: "Audits a human-AI partnership's health with override-rate and override-accuracy metrics (catching both automation bias and an under-performing model), and designs the feedback loop that turns human corrections into structured model-improvement input — the AI Flywheel and bidirectional learning."
---

# HITL Override Metrics & Feedback Audit

## Purpose

Turns "we have human oversight" from a design claim into a measured,
ongoing fact. A HITL process that was well-designed at launch can quietly
degrade into rubber-stamping, or can reveal a model that was never
actually fit for the task, and neither failure mode is visible without
tracking the right metrics over time. This skill defines those metrics and
the audit cadence, and designs the loop that captures human corrections as
an asset rather than letting them evaporate after each individual decision.

## Anchored in research

- Su Belagodu — the override-rate diagnostic (below ~5% signals automation
  bias risk; the team should investigate whether that reflects genuine
  model accuracy or reviewers disengaging from real judgment) — see the
  sourcing caveat in `../hitl-maturity-and-confidence-routing/SKILL.md`'s
  "Anchored in research" section, which applies here too.
- Joshua Ebner (AI engineering & AI integration strategy practitioner) —
  the "AI Flywheel" framing: cumulative human feedback compounds into a
  competitive advantage that can't be replicated just by buying the same
  underlying model. He is a real, identifiable practitioner in this field;
  the specific quotes and framing attributed to him in the source material
  for this skill could not be independently verified word-for-word — treat
  the AI Flywheel concept as a reasonably well-grounded practitioner
  framing, and any specific quote as unconfirmed paraphrase.
- The general "data flywheel" mechanism already used elsewhere in this
  repo (Collins, Jim — *Good to Great*, 2001, applied to data in
  `../../../data-strategy-and-literacy/skills/data-role-diagnosis/SKILL.md`)
  — this skill applies the same self-reinforcing-loop logic specifically
  to human correction data rather than to data assets generally.

## Method

1. **Track the override rate as an ongoing metric, not a launch-time
   check.** Override rate = the share of AI outputs or recommendations
   that a human reviewer changes, rejects, or overrules. Calculate it on a
   rolling basis (e.g. weekly), broken down by task type — an aggregate
   number across dissimilar tasks hides which specific task type is
   actually the problem.
2. **Read the override rate against both failure directions, not just
   one:**
   - **Below roughly 5%** — investigate before treating this as good news.
     It can mean the model is genuinely excellent, or it can mean
     reviewers have stopped exercising real judgment and are approving by
     default (automation bias). Check a random sample of "approved"
     decisions by hand against the actual right answer to tell the two
     apart — don't infer from the rate alone.
   - **Above roughly 30%** — the model is very likely not yet fit for the
     task at its current confidence threshold. Either the confidence-score
     routing in
     `../hitl-maturity-and-confidence-routing/SKILL.md` needs
     re-calibrating (more cases should escalate before this point), or the
     underlying model/prompt needs improvement before this task is a good
     automation candidate at all.
3. **Measure override accuracy, not just override rate.** An override
   being frequent doesn't tell you whether the human's correction was
   actually better — spot-check a sample of overridden decisions against
   an independent ground truth or a senior reviewer's judgment. A high
   override rate paired with low override accuracy points to a confused or
   under-trained review process, not (only) a weak model.
4. **Design the feedback-capture mechanism before assuming corrections
   feed back into anything.** A correction that lives only in the
   individual reviewer's head or an unstructured comment field doesn't
   compound. Structure what's captured: what was wrong, what the correct
   answer was, and (where possible) a category tag for the type of error —
   this structured record is the raw input to prompt refinement or
   fine-tuning, i.e. the AI Flywheel.
5. **Close the loop deliberately** — schedule a recurring review (not just
   an inbox of corrections) where structured feedback is actually
   triaged into: a prompt/guardrail change (see
   `../ai-accuracy-guardrails-and-grounding-design/SKILL.md`), a
   fine-tuning or retrieval-corpus update (an engineering task, out of
   this skill's scope), or a routing-threshold change (see
   `../hitl-maturity-and-confidence-routing/SKILL.md`). A flywheel that
   only accumulates feedback without ever acting on it isn't actually
   turning.
6. **Feed the audit results into prioritization** — for a product manager
   deciding where to invest next, task types with the strongest AI
   Flywheel effect (feedback clearly and repeatably improves the model)
   and reasonably clean data deserve more investment than task types where
   feedback doesn't seem to move the needle; use an ROI-vs-Difficulty view
   similar to
   `../../../ai-strategy-and-governance/skills/ai-opportunity-portfolio/SKILL.md`'s
   scoring logic to make this trade-off explicit rather than intuitive.
7. **Produce a structured audit output**: override rate by task type and
   trend over time, override accuracy from the spot-check sample, flagged
   automation-bias or under-performance risks, and the specific actions
   the triage in step 5 produced.
8. **Re-run this audit on a fixed cadence**, not only when something has
   already gone wrong — a healthy human-AI partnership at launch can drift
   in either direction (toward complacent rubber-stamping or toward
   reviewer distrust that quietly re-inflates cost) without a single
   dramatic failure to trigger a review.

## What this skill does NOT do

- Doesn't design the routing rule itself — see
  `../hitl-maturity-and-confidence-routing/SKILL.md`; this skill audits
  whether that design is actually working.
- Doesn't implement the technical fine-tuning or retrieval-corpus update
  that structured feedback might justify — that's an engineering task;
  this skill produces the structured input for it.
- Doesn't confirm figures or performance data from memory — uses the
  organization's own logged override data, or marks an assumption clearly
  (`[assumption — verify]`) if that data doesn't exist yet, in which case
  building the logging capability is the actual first step.
- Doesn't replace
  `../../../ai-strategy-and-governance/skills/ai-output-curation-and-quality-control/SKILL.md`'s
  step 7 ("track quality over time") — this skill is the deeper, fuller
  audit methodology that step points to.

## Refinement notes

Areas to keep deepening with real practice:

- your own calibrated override-rate bands by industry/task risk profile —
  the 5%/30% figures above are starting heuristics, not validated
  universal thresholds
- a concrete feedback-triage template (into `../../references/`)
- real before/after examples of a flywheel effect that measurably improved
  a model's usefulness over a defined period

Once this section is filled in and validated in practice, update the
`maturity` field in `skills_index.json` to `draft`, `validated`, or
`canonical` (see `../../../meta/maturity_levels.md`). **Don't add new
fields to the frontmatter** — `name` and `description` are the only ones
allowed (see `../../../meta/frontmatter_schema.md`).

## Continue from here

- Before this in this pack: `../hitl-maturity-and-confidence-routing/SKILL.md`,
  `../ai-accuracy-guardrails-and-grounding-design/SKILL.md`
- Related skill in this pack: `../expert-agency-and-apprenticeship-protection/SKILL.md`
  — a healthy override rate depends on reviewers who still have the
  expertise to override well; that skill protects the pipeline that
  produces them.
- Related skill in another pack:
  `../../../ai-strategy-and-governance/skills/ai-output-curation-and-quality-control/SKILL.md`
  — deepens that skill's step 7.
- Related skill in another pack:
  `../../../ai-strategy-and-governance/skills/ai-opportunity-portfolio/SKILL.md`
  — for prioritizing which task types deserve continued AI investment
  based on this audit's findings.
- This pack's shared guardrails: `../../CLAUDE.md`

## References

- `../../references/hitl-partnership-heuristics-research.md` — full
  sourcing and grounding-strength notes for this pack
- `../../references/` — the pack's shared background material
- `../../CLAUDE.md` — the pack's shared guardrails
