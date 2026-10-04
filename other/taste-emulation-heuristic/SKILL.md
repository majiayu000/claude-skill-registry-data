---
name: taste-emulation-heuristic
description: "Predicts how a specific, narrowly-defined in-group will emotionally and aesthetically react to a concept, without slow or misleading market research — by deliberately building 'exposure hours' to world-class examples, running a mental simulation before asking anyone, and validating the prediction against real feedback in a backpropagation-style loop. Use when a concept, design direction, or positioning needs a fast, defensible taste judgment before committing to build or test it."
---

# Taste Emulation Heuristic

## Purpose

When building costs approach zero, an AI system can produce "good enough"
for almost any brief — the differentiator shifts to who can reliably tell
"good enough" apart from "genuinely excellent" for a specific audience,
before spending weeks validating it the slow way. This skill treats
*taste* not as an innate, mystical trait but as a learnable, trainable
judgment capability: running a mental simulation of a defined group's
reaction, built the same way a model is trained — through deliberate
exposure, repeated prediction attempts, and correction against real
feedback.

## Anchored in

Notion product lead Max Schoening's account of taste as a trainable
prediction skill, supplied by the user from a source video transcript:
*"Taste actually means you're able to run a virtual machine in your head
where, given an idea, you can predict for a certain in-group whether
they're going to like it or not. You just have to do reps — it's almost
like training a model."* And on scope: *"the extremes are — if you are
the only person on the planet that thinks something is good, is it good?
No. But maybe you also don't need to build a product for 8 billion
people. You decide what your in-group is, and then how good do you get
at emulating how they will react to it."*

## Method

1. **Define the in-group narrowly, before anything else.** Not "our
   customers" or "users" — a specific, bounded group (often 100-500
   people in the source framing) whose reaction actually matters for this
   decision. A taste judgment made for "everyone" collapses into the
   lowest common denominator; a taste judgment made for a named,
   specific in-group can be sharp and confident. If the in-group can't be
   named concretely (by role, context, and what they already value), the
   prediction that follows won't be trustworthy — go back and narrow it
   first.
2. **Build exposure hours deliberately, before you need them.** Taste
   emulation depends on having internalized what "world-class" actually
   looks like for the relevant category — not generic good taste, but
   fluency in the specific tradition the in-group judges against (e.g.
   Japanese craftsmanship precision, Apple's unibody restraint, Bauhaus
   functional minimalism, glassmorphism's specific visual grammar).
   This is a standing practice, not a one-time prep step: the quality of
   every later prediction depends on how much deliberate, analytical
   (not passive) exposure has already accumulated. A side effect worth
   naming: this vocabulary is also what lets you brief an AI system
   precisely — "make it feel more Bauhaus" only works as an instruction
   if both you and the model have a shared, specific referent for it.
3. **Run the mental simulation before asking anyone — AI or human.**
   Before consulting a stakeholder, running a survey, or prompting an AI
   for feedback, close the loop yourself first: walk through the concept
   as a member of the defined in-group would experience it, and write
   down the predicted reaction (like/dislike, and specifically why) as an
   explicit, falsifiable claim. Skipping this step and going straight to
   external validation is the single biggest reason taste never actually
   develops as a skill — there's no prediction to be right or wrong
   about.
4. **Validate against real signal and correct the internal model
   (the "backpropagation" loop).** Compare the prediction from step 3
   against actual reactions — real user feedback, a small test, a
   trusted in-group member's honest response. Where the prediction was
   wrong, don't just note the outcome; name specifically what about the
   internal model of the in-group was off (wrong assumption about what
   they value, wrong read on the specific detail that mattered). This
   correction step, repeated, is what turns a guess into a trained
   judgment — treat every miss as a labeled training example, not a
   one-off surprise.
5. **State the confidence level and scope honestly in the output.** A
   taste prediction is a considered judgment, not a fact — present it as
   "predicted in-group reaction: [x], confidence: [low/medium/high based
   on exposure depth and prior track record for this in-group]," and
   name explicitly which in-group it's scoped to. A taste call presented
   as universal truth, or made for an in-group the predictor doesn't
   actually have exposure hours in, should be flagged as low-confidence
   rather than stated with false authority.

## What this skill does NOT do

- Doesn't replace real user research or testing where the decision's
  stakes justify it — this skill is for fast, early-stage judgment
  calls (should we even build this, which of two directions is worth
  prototyping), not a substitute for validating a launch-ready product.
- Doesn't work without genuine, deliberate exposure to the category —
  applying this heuristic to an unfamiliar domain the predictor hasn't
  actually studied produces a confident-sounding guess, not a trained
  prediction; say so explicitly rather than presenting low-exposure
  guesswork as taste.
- Doesn't determine who the in-group should be — that's a strategic
  positioning choice for the business, not something this skill resolves
  (see `category-definition-and-modeling` for that broader question).

## Refinement notes

The exposure-hours and backpropagation-loop framing is a direct
generalization of one practitioner's account, not a broader synthesized
literature — if the owner develops their own track record and concrete
in-group examples applying this heuristic, they belong here as validated
worked examples rather than the current single-source grounding.

## Continue from here

- Before positioning or building on a taste call: `../category-definition-and-modeling/SKILL.md`
- Predicting reaction before a demo/prototype is built:
  `../../../prototyping-and-demonstration/skills/opportunity-visioning-with-pr-faq/SKILL.md`
- A related, more structural read of an opportunity's attractiveness:
  `../../../opportunity-recognition/skills/opportunity-value-assessment/SKILL.md`
  — that skill scores commercial viability; this skill predicts emotional/
  aesthetic reaction, a different and complementary question.
- Once a concept has been through this heuristic, sharpening how it's
  explained to others: `../../../change-and-communication/skills/whiteboard-clarity-and-jargon-stripping/SKILL.md`
- This pack's shared guardrails: `../../CLAUDE.md`

## References

- `../../CLAUDE.md` — the pack's shared guardrails

---
**Reminder:** frontmatter has only `name` and `description`. Everything
else goes into `skills_index.json` (run `scripts/generate_index.py`).
