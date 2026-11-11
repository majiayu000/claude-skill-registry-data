---
name: technical-presentations
description: "Designs, red-teams and revises technical talks, workshops and decks for mixed business and technical audiences so they have real depth instead of framework cards and AI slop: fixes the narrative contract first, picks slide counts by runtime, builds one case progressively, shows a real failure and recovery, labels every claim's evidence, then verifies timing, notes and rendering. Use when someone says 'this talk is too basic', 'cut my deck to 15 minutes', 'review my AI agents talk', 'make a leave-behind PDF deck', 'prep a workshop from this transcript', or 'write a brief so an agent can edit my deck'. Pairs with a pptx or HTML-deck skill for the actual file."
---

# Technical Presentations

A polished deck is not a substantive talk. Credibility comes from showing where
uncertainty lives, what stays deterministic, how state, tools, permissions and
failures work, and what evidence backs each claim. One system built up across
the talk beats ten shallow examples.

## 1. Fix the narrative contract before any slide

Write these six lines and get them agreed (ask for anything missing):

1. **Audience:** novice, mixed, or deeply technical.
2. **Runtime:** minutes excluding Q&A.
3. **Teaching promise:** what they can distinguish, sketch or decide afterwards.
4. **Central tension:** the misconception or practical problem.
5. **Technical spine:** one architecture, workflow, failure or artifact for the experts.
6. **Evidence boundary:** what is verified, anonymised, illustrative, or hypothesis.

If runtime or audience changes later, redesign from the contract. Never just
squeeze the old deck.

## 2. Structure by runtime

| Runtime | Main slides | Shape |
|---|---|---|
| 10 to 15 min | 7 to 9 (10 to 12 only if each is a sparse visual beat) | cold open or vote, thesis, one framework, one deep case, one failure, one decision test, close |
| 25 to 35 min | 14 to 17 (owner rooms with demos: up to ~20 to 26 short beats) | right problem, precise mechanism, one system, failure and recovery, evidence and controls, decision rule |

Founders speaking naturally run 30 to 60 percent over the slide timings. Sum the
timings, then add room time for demos, questions, QR scans and typing.

## 3. Slide rules

- **Two layers:** projection = one sentence + one visual, about 25 to 35 words
  max. Narration (speaker notes) = nuance, caveats, evidence, depth.
- **Depth ladder:** plain problem, precise mechanism, workflow diagram, state or
  sequence artifact, failure scenario, control and recovery, evaluation evidence.
- **Real artifacts over framework cards:** workflow maps, state machines,
  sequence diagrams, typed tool contracts, failure matrices, short JSON traces,
  eval pipelines, authority matrices.
- **One case spine:** understandable without industry knowledge, recurring,
  cross-system, varied enough to need judgment, measurable without invented numbers.
- **Semantic colours** fixed for the whole deck, for example code = teal, model
  judgment = orange, human authority = green, state = purple, irreversible side
  effect = red.
- **Engagement that teaches judgment:** "chat, automation, agent, or fix the
  process?", "which step is irreversible?", "where does a human stay in charge?"

## 4. Evidence rules

- Every client example, number and outcome gets a label: verified, anonymised,
  composite, illustrative.
- From transcripts or calls: read the source, not a summary; separate what the
  customer said, what you said and what you hypothesise; keep timestamps in notes,
  not on slides; anonymise unless publication is approved.
- Never invent ROI, accuracy, deployment status or client results. Contracted is
  not deployed, deployed is not measured.
- Credit any borrowed framework on the slide.

## 5. Red-team the outline before visuals

Would a technical attendee learn anything after slide 3? Are component
interactions shown, or only named? Is the model treated as the whole system? Is
there one concrete failure with a safe recovery? Are state, permissions, side
effects and stop conditions visible? Is it one system or a stack of frameworks?
Does each slide earn its minutes? If any answer is weak, fix the curriculum first.

## 6. Verify before delivery

1. Slide count and summed runtime fit the slot with buffer.
2. Render and look at every slide; projected text readable from the back row.
3. Every claim has an evidence label; every framework is credited.
4. Speaker notes match final slide order.
5. Appendix slides excluded from the timing.
6. Run at least one fix-and-reverify cycle.

## Output

For a new or revised talk, deliver a slide table, then build the file only after
the user approves it:

```
| # | Role | Projected line (<=35 words) | Visual | Notes gist | Evidence | Time |
|---|------|------------------------------|--------|------------|----------|------|
| 1 | TEACH | Agents aren't the use case. Finding work worth owning is. | room vote: 4 workflows | ... | n/a | 1:30 |
| 5 | DEMONSTRATE | It sent once, knew it sent, and stopped. | retry trace with idempotency key | ... | illustrative | 2:00 |
Total 12:40 of 15:00. Appendix: A1 state machine, A2 prompt-injection boundary.
```

Roles: TEACH, DEMONSTRATE, PROVE, INVITE. If INVITE or promotional beats
dominate, rebalance.

For a review, give a verdict, then a disposition per slide: keep, cut, merge,
move, rewrite, or appendix.

## Special cases (read the reference)

| Situation | Reference |
|---|---|
| Talk about finding real uses for AI agents | `references/agent-systems-talk-pattern.md` |
| Executives, owners, boards; sponsor wants product-heavy content; security for company-wide AI | `references/executive-talks.md` |
| Leave-behind PDF that must work forwarded, without you | `references/forwardable-decks.md` |
| Taking over or continuing a workshop from a transcript or outline | `references/workshop-handoffs.md` |
| Auditing a live HTML deck, or writing a brief an AI agent will implement | `references/deck-audit.md` + `scripts/harvest-deck.js` |

## Handoff brief for an AI deck editor

When someone will give your revision to an agent, write a Markdown brief, not a
critique: source URL or file path, stable slide IDs mapped to actions, exact
projected copy, visual, notes and timing per slide, explicit
insert/move/merge/delete instructions, zero- vs one-based slide routing, phrases
that must disappear, design-system rules, controls to keep (QR targets, keyboard
nav), the QA list from section 6, and a human review gate before publishing.
Keep the source deck untouched until the revision passes QA.

## Pitfalls

- Equating depth with more words or smaller fonts.
- Spending half the talk on definitions.
- Implying full autonomy is the goal, or a happy-path demo is production.
- Building slides before audience, runtime, thesis and spine are settled.
