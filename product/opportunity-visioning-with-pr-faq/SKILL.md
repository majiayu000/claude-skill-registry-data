---
name: opportunity-visioning-with-pr-faq
description: "Communicates and shows an AI opportunity using Amazon's Working Backwards method before anything has been built: writes a short future-dated press release (PR) and a question-and-answer section (FAQ) describing what the finished solution would look like from the customer's perspective. Use when an opportunity needs to be made concrete and discussable before prototyping, or when a prototype isn't yet feasible/worthwhile but the vision still needs to be communicated convincingly."
---

# Opportunity Visioning with PR-FAQ

## Purpose

Make an AI opportunity concrete and evaluable **without anything having been
built yet.** Many AI opportunities stay abstract ("we could use AI for X")
because no one has forced themselves to describe precisely what the finished
solution would look like from the customer's/user's perspective. This skill
applies Amazon's Working Backwards method and its PR-FAQ document: first
write a short, future-dated press release as if the solution had already
shipped, then a question-and-answer section that works through the customer
benefits, risks, and metrics. This is faster and cheaper than prototyping,
and it often reveals that the vision isn't actually clear yet — before a more
expensive prototyping round begins.

## Anchored in research

- Amazon's "Working Backwards" method and PR-FAQ document (Bryar &
  Carr, *Working Backwards*, 2021): start from the customer and the
  finished experience, and work backwards to what needs to be built.
  The PR-FAQ is a short (roughly 6-page) narrative document in two parts:
  a one-page mock press release dated at a future launch, and a
  question-and-answer section that works through the customer problem,
  the solution, the risks, and the success metrics.

## Method

1. **Write a one-page mock press release**, dated in the future
   (e.g. "released [date], when the solution is in use"), as if
   the solution already existed and had succeeded:
   - Headline and a one-sentence summary.
   - The customer problem that was solved (concrete, not generic).
   - How the solution works from the customer's perspective (no
     technical detail — what the customer EXPERIENCES).
   - One quote from a hypothetical customer describing the benefit
     concretely.
   - How the customer gets started.
2. **Write an FAQ section that works through the hard questions honestly:**
   - Customer questions: what does this cost, how is this different from
     the current way of doing the same thing, what if the solution is wrong.
   - Internal questions: what data/capability is needed that doesn't yet
     exist, what are the biggest technical and organizational risks, how
     will success be measured, what does THIS solution deliberately NOT do
     (scope it consciously).
   Honesty on the hard questions is the whole point of the method — the
   PR-FAQ isn't meant to sell the idea to yourself, but to expose its
   weaknesses before anyone invests in it.
3. **Use the PR-FAQ as a basis for discussion, not as an end product.**
   Take the document to stakeholders and ask specifically: is the customer
   problem right, is the solution credible from their perspective, is there
   an important obstacle missing from the FAQ. Update the document based on
   the feedback before moving on to prototyping.
4. **Use the PR-FAQ even when prototyping isn't yet sensible** — e.g. when
   technical feasibility is highly uncertain or the cost of building
   anything is high. The PR-FAQ gives you a way to communicate and
   cheaply test the vision before committing.
5. **Once the PR-FAQ is stable and stakeholders agree on the vision**, feed
   it into [`../rapid-prototype-and-vibe-coding-craft/SKILL.md`](../rapid-prototype-and-vibe-coding-craft/SKILL.md):
   the PR-FAQ's "how the customer experiences the solution" description
   becomes the prototype's hypothesis (that skill's step 1).
6. **Don't conflate the PR-FAQ with a business case** — the PR-FAQ tests
   the clarity and appeal of the VISION, not its financial viability. Once
   the vision is clear, build the economic case separately with
   [`../../../business-case-and-analysis/skills/business-case-builder/SKILL.md`](../../../business-case-and-analysis/skills/business-case-builder/SKILL.md).

## What this skill does NOT do

- Doesn't build a prototype or write code — produces a written vision
  ahead of prototyping, not a substitute for it.
- Doesn't calculate ROI or costs — the PR-FAQ's FAQ section may mention a
  rough cost estimate, but precise financial calculation is done with
  [`../../../business-case-and-analysis/skills/business-case-builder/SKILL.md`](../../../business-case-and-analysis/skills/business-case-builder/SKILL.md).
- Isn't marketing material for the customer — the PR-FAQ is an internal
  thinking and discussion tool, not a document meant for publication (even
  though its form resembles a press release).
- Doesn't guarantee a vision is right just because it's written
  convincingly — the point of the FAQ section's honest, hard questions is
  precisely to stress-test the vision, not to dress it up.

## Refinement notes

Areas to keep deepening with real practice:

- your own PR-FAQ template with an exact structure (into
  [`../../references/`](../../references/))
- concrete examples of a PR-FAQ that exposed a weakness in the vision
  before a more expensive prototyping round
- rules of thumb for when a PR-FAQ is enough and when you need to move
  straight to prototyping

This is an internal working note, not a claim about the skill's current
usability. Track depth privately via the `maturity` field in
`skills_index.json` (see
[`../../../meta/maturity_levels.md`](../../../meta/maturity_levels.md)).
**Don't add new fields to the frontmatter** — `name` and `description` are
the only ones allowed (see
[`../../../meta/frontmatter_schema.md`](../../../meta/frontmatter_schema.md)).

## Continue from here

- Before this (if a fitting industry pattern is still missing):
  [`../../../ai-strategy-and-governance/skills/ai-capability-pattern-matching/SKILL.md`](../../../ai-strategy-and-governance/skills/ai-capability-pattern-matching/SKILL.md)
- Next in this pack: [`../rapid-prototype-and-vibe-coding-craft/SKILL.md`](../rapid-prototype-and-vibe-coding-craft/SKILL.md)
- A deeper narrative for leadership: [`../../../change-and-communication/skills/executive-narrative-and-storyline/SKILL.md`](../../../change-and-communication/skills/executive-narrative-and-storyline/SKILL.md)
- Economic case once the vision is stable: [`../../../business-case-and-analysis/skills/business-case-builder/SKILL.md`](../../../business-case-and-analysis/skills/business-case-builder/SKILL.md)
- A ready-made skill chain for this situation: see [`../../../playbooks/`](../../../playbooks/)
- This pack's shared guardrails: [`../../CLAUDE.md`](../../CLAUDE.md)

## References

- Bryar, Colin & Carr, Bill — *Working Backwards: Insights, Stories, and
  Secrets from Inside Amazon* (2021) — the Working Backwards method and
  the PR-FAQ document
- [`../../references/`](../../references/) — the pack's shared background material
- [`../../CLAUDE.md`](../../CLAUDE.md) — the pack's shared guardrails
