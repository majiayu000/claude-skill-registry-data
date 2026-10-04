---
name: question-forge
description: Take a surface question and forge the question actually worth asking — diagnose what's broken in the asked question (smuggled answers, wrong level, false binary, self-protection), transform it, and return a better question WITHOUT answering it. Use when a question feels stuck, loaded, or too easy, or as a preprocessor before other reasoning skills.
---

# Question Forge

Use this skill to reformulate a question rather than answer it. The premise, borrowed from fiction: a great novel doesn't answer "is revenge justified?" — it constructs the version of that question that becomes concrete, costly, and unavoidable. The illumination is in the formulation. Accordingly, this skill's contract inverts the usual one: **the output is a question, not an answer.**

## Purpose

Most questions arrive broken in predictable ways. Answering a broken question efficiently just delivers the asker to the wrong destination faster. This skill diagnoses the break, applies transformations, tests candidates against the standards a dramatist would use, and hands back the forged question — explicitly refusing to answer it.

## Procedure

### 1. Dispatch check (mandatory, first)

If the question is genuinely operational — factual, technical, well-posed ("why is the build failing?", "what's the capital gains rate?") — say the question is fine and answer it normally. Being preciously Socratic about factual questions is this skill's primary failure mode.

### 2. Diagnose the asked question

Common breaks:

- **Smuggled answer** — the question presupposes its conclusion ("isn't it time we...")
- **Wrong level** — asks tactics when the problem is values, or values when the problem is tactics
- **False binary** — two options presented where the space is wider
- **Displaced subject** — asks about the world when it's really about the asker ("should I quit?" is rarely about the job)
- **Wish in question syntax** — a complaint or longing wearing a question mark
- **Shield question** — a safe question standing guard in front of a harder one nearby

### 3. Generate reformulations along transformation axes

- **Subject shift** — world → self: "should I quit?" → "what am I hoping quitting will fix?"
- **Level shift** — up or down the ladder of abstraction
- **Time shift** — this decision → the shape of a life; prospective → retrospective ("what will I wish I had asked?")
- **Inversion** — "why can't I X?" → "what is not-X-ing accomplishing for me?"
- **Value excavation** — "what would have to be true for this to matter?"
- **Dramatization** — embody it in a concrete scene with stakes: not "is loyalty owed to institutions?" but "the whistleblower's sister works on the same floor"

### 4. Test candidates against the dramatist's criteria

A forged question should:

- **Sustain a novel** — resist one-line resolution
- **Have live opposition** — opposing answers both carry real weight; if one side is obviously right it's a quiz, not a question
- **Implicate the asker** — not stay safely third-person
- **Cost something** — answering it honestly requires giving something up
- **Stay generative** — keep producing thought after you stop looking at it

### 5. Deliver — and hold the line

Present the forged question. Do not answer it.

## Output format

```markdown
## The question you asked
...

## What it's doing
<the diagnosis: what the question smuggles, protects, or displaces>

## The forged question
**...**

## What changed
<which transformation(s), and why this version has more torque>

## Living with it
<one short paragraph: what it would look like to carry this question for a while, rather than resolve it>
```

## Guardrails

- **One pass.** Forge once; do not reformulate the reformulation. No infinite regress.
- **Livable, not a koan.** The forged question must be one a person can actually carry and act under — not mystical wordplay.
- **The original deserves respect.** Diagnose without condescension; the asked question is the raw material, not an error.
- **Never answer the forged question.** If the user wants it answered, they can ask — or pipe it into another skill.

## Composition

Works as a preprocessor for the rest of this package: forge the question, then feed the result to `dp-solve`, `decision-matrix`, `assumption-audit`, or `parable`.

## Canonical questions

- "Should I quit my job?"
- "Is AI going to take our jobs?"
- "Was I right to end the relationship?"
- "What should our company's mission be?"
- "Why is engagement dropping?" (often forges into: "what did we build this for?")

Poor fits: operational questions (the dispatch check handles these), and questions the user has already carefully formulated — sometimes the question arrives correct.
