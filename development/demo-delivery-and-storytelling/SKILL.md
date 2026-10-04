---
name: demo-delivery-and-storytelling
description: "Builds and delivers a demo following the Great Demo! methodology (Situation Slide, critical business issue/CBI, \"do the last thing first\"/inverted pyramid): Discovery → Demo Prep → Demo Delivery → Documentation → Debrief. Use when a prototyped solution needs to be presented to a customer or leadership so that it genuinely convinces rather than just showcasing features."
---

# Demo Delivery & Storytelling

## Purpose

Turn a working prototype into a convincing demo. A working prototype and a
good demo are not the same thing — many technically competent prototypes
fail at demo time because they're presented as a feature list ("let's look
at everything this can do") instead of concretely proving the customer's own
critical business issue. This skill applies Peter Cohan's Great Demo!
methodology (an established framework in the sales-engineering literature)
to an AI consultant's demo situation.

## Anchored in research

- Cohan, Peter E. — *Great Demo! How To Create And Execute Stunning
  Software Demonstrations* (third edition) and Paul Pearce's "Great Demo!
  Five Imperatives" application: Discovery, Demo Prep, Demo Delivery,
  Documentation, Debrief. Core concepts: the **Situation Slide** (a concise
  summary of the customer's situation before the demo), the **critical
  business issue (CBI)**, and **"do the last thing first" / the inverted
  pyramid** (show first the thing that produces the "wow" effect — don't
  build the demo chronologically as a product walkthrough).

## Method

Applied Great Demo! Five Imperatives structure:

1. **Discovery — before you build anything for the demo.** Establish the
   customer's **critical business issue (CBI)**: what concrete pain do
   they have today, who owns it, when does it need to be solved, and how
   much value would a solution create. If you can't answer these, you're
   not ready to build a demo yet — go back to
   [`../../../opportunity-recognition/skills/pattern-and-analogy-connector/SKILL.md`](../../../opportunity-recognition/skills/pattern-and-analogy-connector/SKILL.md)
   or
   [`../../../ai-strategy-and-governance/skills/ai-capability-pattern-matching/SKILL.md`](../../../ai-strategy-and-governance/skills/ai-capability-pattern-matching/SKILL.md)
   to sharpen the situation first.
2. **Demo Prep — write the Situation Slide before the demo.** One
   slide/paragraph summarizing: the customer's situation, the CBI, the
   capabilities needed, the value sought, the timeline. Also assemble: the
   demo's outline and agenda, possible side paths in case the customer
   asks something unexpected, demo data that resembles the customer's OWN
   data (generic sample data is noticeably weaker), and reference stories
   from similar situations.
3. **Demo Delivery — apply "do the last thing first."** Don't start with
   an overview or the technical architecture — start with the one thing
   that concretely resolves the CBI and produces a "wow" reaction. The
   inverted pyramid: the most important thing first, background and
   detail only if interest holds up. Ask questions during the demo instead
   of delivering a monologue — this reveals in real time how the audience
   is experiencing the value and what they still need to decide.
4. **Always tie the demo back to the frame** already set in
   [`../demo-framing-and-expectation-setting/SKILL.md`](../demo-framing-and-expectation-setting/SKILL.md):
   remind the audience what this demo proves and what it doesn't, and
   don't let the drama of the demo carry the frame away (an excited
   audience easily over-interprets).
5. **Documentation — share the Situation Slide and a demo summary
   immediately after the demo.** Research (see References) shows that most
   of a demo's content is forgotten within a week — the written summary is
   what the audience actually takes away and shares within their
   organization. Record the CBI, what was proven in the demo, and the
   agreed next steps.
6. **Debrief — review what worked and what didn't right after the demo**,
   while it's still fresh: which questions were surprising, which part of
   the demo produced the most reaction, what should be done differently
   next time. This matters especially for an AI consultant who runs
   several similar demos back-to-back for different customers — learnings
   compound quickly if the debrief is done systematically.
7. **A special note for vibe-coded prototypes:** never improvise, in a live
   demo, paths that haven't been tested in advance — the failure modes of
   an AI-assisted prototype can be unpredictable. Keep the demo strictly to
   the 2-3 tested paths confirmed to work during Demo Prep (see
   [`../rapid-prototype-and-vibe-coding-craft/SKILL.md`](../rapid-prototype-and-vibe-coding-craft/SKILL.md)
   step 4).

## What this skill does NOT do

- Doesn't build the prototype itself — see
  [`../rapid-prototype-and-vibe-coding-craft/SKILL.md`](../rapid-prototype-and-vibe-coding-craft/SKILL.md).
- Doesn't set the demo's frame (the PoC/Pilot/MVP term, the
  proves/doesn't-prove pair) — that's done before this skill in
  [`../demo-framing-and-expectation-setting/SKILL.md`](../demo-framing-and-expectation-setting/SKILL.md).
- Doesn't replace the sales process as a whole — it focuses on one demo
  event following the Great Demo! methodology, not the entire sales cycle.
- Doesn't guarantee that a good demo leads to a deal or advancement — a
  good demo removes obstacles, but the decision is always the customer's.

## Refinement notes

Areas to keep deepening with real practice:

- your own Situation Slide templates (into
  [`../../references/`](../../references/))
- concrete examples of demos that worked especially well — and what made
  them work
- rules of thumb for how to react when a demo goes wrong live (e.g. the AI
  gives a wrong answer mid-demo)

This is an internal working note, not a claim about the skill's current
usability. Track depth privately via the `maturity` field in
`skills_index.json` (see
[`../../../meta/maturity_levels.md`](../../../meta/maturity_levels.md)).
**Don't add new fields to the frontmatter** — `name` and `description` are
the only ones allowed (see
[`../../../meta/frontmatter_schema.md`](../../../meta/frontmatter_schema.md)).

## Continue from here

- Before this (prototyping): [`../rapid-prototype-and-vibe-coding-craft/SKILL.md`](../rapid-prototype-and-vibe-coding-craft/SKILL.md)
- Before this (framing): [`../demo-framing-and-expectation-setting/SKILL.md`](../demo-framing-and-expectation-setting/SKILL.md)
- A deeper narrative for leadership: [`../../../change-and-communication/skills/executive-narrative-and-storyline/SKILL.md`](../../../change-and-communication/skills/executive-narrative-and-storyline/SKILL.md)
- If the demo succeeds: [`../demo-to-business-case-bridge/SKILL.md`](../demo-to-business-case-bridge/SKILL.md)
- A ready-made skill chain for this situation: see [`../../../playbooks/`](../../../playbooks/)
- This pack's shared guardrails: [`../../CLAUDE.md`](../../CLAUDE.md)

## References

- Cohan, Peter E. — *Great Demo! How To Create And Execute Stunning
  Software Demonstrations*
- Pearce, Paul H. — "Great Demo! Five Imperatives" application (Discovery,
  Demo Prep, Demo Delivery, Documentation, Debrief)
- Research on demo content being forgotten without written documentation
  (sales engineering literature)
- [`../../references/`](../../references/) — the pack's shared background material
- [`../../CLAUDE.md`](../../CLAUDE.md) — the pack's shared guardrails
