---
name: bmc-client-language-translation
description: "Interprets typical client statements about BMC work ('we need to update our business model', 'we've already done a BMC') as strategic signals, and corrects three of the most common conceptual misunderstandings: value proposition as a feature list, customer segment as demographics, revenue stream as pricing."
---

# BMC Client Language Translation

## Purpose

Provides a vocabulary for what a client MEANS when they say typical
BMC-related phrases — and what to ask next. Also corrects three of the
most common conceptual misunderstandings (value proposition, customer
segment, revenue stream vs. pricing), which show up directly in how the
client FILLS IN the canvas, not just in how they talk about it.

## Anchored in research

Based on the owner's private research layer (an April 2026 expert
interview)
(`03_domain_model/vocabulary/client_language_translation.md` and
`concept_misunderstandings.md`, `status: template`, `confidence: low/medium`),
a synthesis drawing on observations from van der Linden and Jeffries.
Note: these are TWO DIFFERENT files from
`../bmc-antipattern-and-misunderstanding-correction/SKILL.md`'s source
files (`bmc_client_misunderstandings.md`,
`bmc_antipatterns_expert.md`) — this skill covers VOCABULARY and
CONCEPTS, that skill covers misunderstandings about the BMC's ROLE. Use
both alongside each other; they don't overlap.

## Method

### A. Interpreting client statements

1. **"We need to update our business model."** Interpretation: the
   client feels the model has become outdated, often triggered by
   competitive pressure or shrinking margins. They haven't yet
   identified what specifically needs to change. Ask next: what
   concretely made this feel outdated right now?
2. **"We've already done a BMC."** Interpretation: the classic "one and
   done" pattern (Jeffries) — the team filled in the blocks and
   considers the work finished. The canvas has become a poster. Ask
   next: can I see it? (This often reveals a single static canvas with
   no variants or iteration — see
   `../bmc-canvas-clarity-and-iteration/SKILL.md`.)
3. **"We need to find our value proposition."** Interpretation:
   usually signals feature-driven thinking. The team can describe WHAT
   they do, not what the customer GETS out of it.
4. **"We want to validate our model."** Interpretation: almost always
   means "we talked to a few people and they liked it" — not real
   hypothesis testing. See `../bmc-tool-switching-decisions/SKILL.md`
   for hypothesis quality criteria before calling something validated.
5. **"Our customers are [a very broad segment]."** Interpretation: the
   single most commonly cited mistake (van der Linden, Jeffries).
   Demographics without jobs, pains, or buying logic. See DR-03 and the
   segment validity decision in
   `../bmc-tool-switching-decisions/SKILL.md`.

### B. Three conceptual misunderstandings

6. **Value proposition.** Typical client usage: a feature list ("We
   offer high-quality X with excellent service and competitive
   pricing"). What it actually is: a specific, testable statement of
   value, built for a particular segment in terms of jobs done, pains
   relieved, or gains created. Tell: if it could apply to any
   competitor in the category, it isn't a value proposition — it's a
   category description.
7. **Customer segments.** Typical client usage: broad demographics
   ("SMEs," "enterprise customers," "consumers 25-45"). What it
   actually is: a group that shares the same jobs, pains, and gains —
   requiring a meaningfully different value proposition or channel.
   Defined by WHAT they need, not WHO they are.
8. **Revenue streams vs. pricing.** Misunderstanding: filled in with a
   price ("we charge €500/project") instead of a revenue logic
   ("transaction-based, billed per project"). The distinction: the
   revenue model (how value is captured) vs. pricing (how much is
   charged) — these are two different questions.

## What this skill does NOT do

- Doesn't contain the owner's own answer to what they ask next after
  these statements, or which phrases are most common in THEIR OWN
  client base — these remain open as `[EXPERT INPUT]` sections in the
  source files.
- Isn't an exhaustive vocabulary — it covers only the five phrases and
  three concepts documented in the research layer, not every possible
  form of client language.
- Doesn't replace
  `../bmc-antipattern-and-misunderstanding-correction/SKILL.md` — that
  skill covers broader misunderstandings about the BMC's ROLE (e.g.
  "the BMC defines everything at once"), this skill covers the content
  of INDIVIDUAL CONCEPTS (value proposition, segment, revenue stream).

## Refinement notes

- What does a "business model update" request usually mean in your
  experience? Is it usually a genuine strategic need or a symptom of
  something else? What do you ask next?
- How do you respond to "we've already done a BMC"? Do you ask to see
  it? What does "already done" usually reveal?
- What's your instinct when you hear "we want to find our value
  proposition"? What's the real problem behind it, in your experience?
- How do you handle the use of the word "validation"? How do you reset
  expectations about what validation requires?
- How do you handle a very broad segment definition in the room? Do you
  push back immediately or let it develop first? What's your opening
  question?
- How do you see the value-proposition misunderstanding show up in your
  own clients? What's your own corrective move?
- What's the worst segment definition you've seen? What did you do?
- Do you distinguish the revenue model from pricing? How do you handle
  the pricing conversation within a BMC context?
- Which phrases do you translate most often in YOUR OWN client base?
- Which misunderstandings are most common in your specific client
  context?

## Continue from here

- Related skill in the same pack:
  `../bmc-antipattern-and-misunderstanding-correction/SKILL.md` —
  broader misunderstandings about the BMC's ROLE (owner-validated,
  `validated`-level — use as the primary source when the question is
  about the BMC's ROLE rather than an individual concept).
- Related skill in the same pack:
  `../bmc-tool-switching-decisions/SKILL.md` — the segment and
  hypothesis validity criteria that this skill's concept explanations
  support.
- This pack's shared guardrails: `../../CLAUDE.md`

## References

- `../../references/bmc-source-material-notes.md` — source material background
- `../../CLAUDE.md` — this pack's shared guardrails
