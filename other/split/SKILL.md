---
name: split
description: >
  Split user stories into smaller, independently deliverable slices using the SPIDR method
  (Spike, Path, Interface, Data, Rules). Use this skill whenever the user asks to split a story,
  break down work, slice a story, asks "can this be split", mentions "SPIDR", says "story splitting",
  or wants to decompose a large ticket into smaller pieces. Also trigger when a user presents a story
  that seems too large for a single sprint and asks for help sizing or scoping it.
---

# Story Splitting with SPIDR

Split user stories into thin, independently valuable vertical slices using the five SPIDR techniques from Mike Cohn (Mountain Goat Software).

## When you have a story to split

If the story comes from a Jira ticket, fetch it first. If it comes from conversation context or text, work with what you have. If the story lacks enough detail to assess splitting options, ask one focused clarifying question before proceeding.

## Process

### 1. Summarize the story

State the story in one sentence. Identify the core user value.

### 2. Apply SPIDR analysis

Evaluate each technique against the story. Present as a table:

```
| Technique | Applicable? | Rationale |
|-----------|-------------|-----------|
| **S**pike | Yes/No | Can we extract research or prototyping? |
| **P**ath  | Yes/No | Are there multiple user flows or alternate paths? |
| **I**nterface | Yes/No | Can we deliver progressively richer interfaces? |
| **D**ata  | Yes/No | Can we restrict data types or subsets initially? |
| **R**ules | Yes/No | Can we temporarily relax business rules? |
```

For each "Yes", include a brief concrete example of how it applies to this specific story.

### 3. Recommend the split

Pick the technique (or combination) that produces the best vertical slices — stories that each deliver value independently and can be shipped separately.

Prefer splits where:
- Each sub-story is independently deployable and testable
- Earlier stories lay groundwork that later stories build on (but aren't just "setup" — they deliver value)
- The split reduces risk by getting feedback earlier
- Sub-stories are roughly similar in size

Avoid splits that produce:
- Horizontal layers (e.g., "build the API" then "build the UI") — these aren't independently valuable
- Stories so small they're just tasks
- Artificial splits that add integration overhead without reducing complexity

### 4. Write the sub-stories

For each recommended sub-story, provide:

**Title** — concise, descriptive
**Why** — 1-2 sentences on the value this slice delivers independently
**Acceptance Criteria** — Given/When/Then scenarios (2-5 per story). Focus on user-observable outcomes, not implementation details.

### 5. Show the dependency order

```
Story 1: [title]
  └─> Story 2: [title] (builds on Story 1)
       └─> Story 3: [title] (builds on Story 2)
```

If stories are independent of each other, show them at the same level.

## SPIDR Reference

**Spike** — Extract a research or prototyping activity. The team learns something that makes the remaining work easier to estimate and split further. Good when there's a build-vs-buy decision, unfamiliar technology, or unclear requirements.

**Path** — Look for alternate paths through the story. If a user can accomplish something in multiple ways (e.g., pay with card vs Apple Pay vs bank transfer), each path is a candidate for its own story.

**Interface** — Deliver a simpler version of the interface first, then enhance it. Start with the minimum viable interaction and progressively add richness. Works for both UI and API surfaces.

**Data** — Restrict the data types, formats, or subsets supported initially. Handle the common case first, add edge cases later. Example: support one file format now, add the other 15 later.

**Rules** — Temporarily relax business rules that add complexity. Implement the core flow without the rule, then add the rule as a follow-up story. The relaxed version often can't ship to production, but it can still be built and tested in that order.

## Output format

Keep it concise. The SPIDR table should fit on one screen. Only write full sub-stories (with AC) for the recommended split — don't write detailed stories for techniques you're not recommending.
