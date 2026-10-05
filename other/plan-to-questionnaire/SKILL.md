---
name: plan-to-questionnaire
category: meta-orchestration
description: Turn a decision you can't answer alone into a Markdown questionnaire for the one person who can — filled in async, or worked through together in a meeting.
disable-model-invocation: true
codex-short-description: "Turn a decision you can't answer alone into a questionnaire"
related-skills:
  - plan-to-spec
  - grill-me
  - clarity-council
loop-eligible: false
compatibility: claude-code codex opencode
---

# Plan to Questionnaire

Turn something the user can't answer alone into a **questionnaire** — a Markdown document they hand to one person to fill in async, or fill out together over a meeting. The recipient holds knowledge the user lacks; the questionnaire pulls it out of them.

**Grill the send, not the subject.** Interview the user only about the *send*, which they can always answer: who it goes to, and what they need back. Interviewing them about the topic is pointless here — not knowing the topic is why they're writing to someone else. The questions in the document then target the **gap** between what the recipient knows and what the user needs.

## Scope

Three deliberate limits. Say so plainly rather than improvising past them:

- **No ingest phase.** This skill doesn't read a transcript or a file and extract questions from it. What makes it work after a grilling session is running it in the *same conversation*, so that session is already in context and the drafting can draw on it. Invoked fresh, it knows only what the user answers in the two exchanges below — say so and ask for the topic.
- **One recipient per run.** Step 1 asks for *the* recipient, singular; the tone and context of the whole document are pitched at them. Three people holding three parts of the answer means three runs, not one document with per-role sections.
- **No branching.** The output is a static document — themed groups, most-important-first, every question live. Not a tree that skips section D based on the answer to A.

## Process

### 1. Who is it going to?

Ask, in one exchange, the recipient's role, expertise, and relationship to the user. This fixes the questionnaire's tone and how much context it must carry.

**Done when:** you know who the recipient is and what they know that the user doesn't.

### 2. What do you need back?

Ask, in one exchange, the specific decisions or facts the user can't resolve alone and needs from this person.

**Done when:** you have a concrete list of what the user must walk away able to do or decide.

### 3. Write the questionnaire

Draft questions aimed at the gap from steps 1–2, following the document structure below. Write it to `plan-to-questionnaire-<slug>.md` in the current directory (slug from the topic) and report the path.

**Done when:** the file exists and every item the user named in step 2 is covered by a question.

## Document structure

Frame the document as a **discovery questionnaire**: the user lacks context, the recipient holds it. Order questions most-important-first — async means you may only get one pass — and group them under `##` headings by theme once there are more than a handful.

<questionnaire-template>

# <Questionnaire title>

**Purpose:** why this questionnaire exists and the decision riding on it.

**From:** <the user> — **To:** <the recipient> — **How your answers will be used:** <where they go>

## Context

One paragraph orienting a recipient who wasn't in the user's head. Enough to answer well, not a page.

## How to answer

Deadline and rough effort. Partial answers and "I don't know" are useful — flag anything you're unsure of rather than skipping it.

## <Theme heading>

One `##` section per theme. Under each, its questions, most-important-first. Every question is one idea — never compound — with an answer stub directly beneath, and a one-line _why this matters_ only where the question could be misread or invite a throwaway answer.

<question-example>
### What load is the system expected to handle at launch?

_Why this matters: it decides whether we provision for burst traffic now or defer it._

>
</question-example>

## Anything else?

A closing catch-all: anything we didn't ask that we should know?

</questionnaire-template>

## Quality Loop

Before reporting the path, check the document against the send:

1. **Covers the ask** — every item from step 2 maps to at least one question.
2. **Answerable by *this* recipient** — nothing in it requires knowledge only the user has.
3. **One idea per question** — no compound questions the recipient can half-answer.
4. **Ordered by importance** — if they answer only the first three, the user still gets the most valuable thing.
5. **Self-contained** — a recipient with no other context can answer from the document alone.

If two or more fail, revise and re-check. Cap at two passes.

## Delegation Map

| User need | Delegate via | Notes |
| :--- | :--- | :--- |
| The answers came back — now write it up | Invoke `plan-to-spec` | The filled questionnaire is the spec's primary source |
| The user *can* answer it themselves, with pressure | Invoke `grill-me` | Grill the subject, not the send |
| The decision needs perspectives, not facts | Invoke `clarity-council` | A questionnaire pulls knowledge; the council weighs judgement |

**Loop eligibility:** false — one questionnaire per decision.

> **Host portability:** this skill asks the user questions and writes one Markdown file — no host-specific tools. See [PORTABILITY.md](../PORTABILITY.md).

<!-- self-evolve:start -->
## Self-Evolve Loop
Journal `~/.ink-and-agency/learnings/plan-to-questionnaire.md` (or workspace-local `.ink-and-agency/` where the sandbox confines writes). Read it first; append what the run taught — [SELF-EVOLVE.md](../SELF-EVOLVE.md).
<!-- self-evolve:end -->
