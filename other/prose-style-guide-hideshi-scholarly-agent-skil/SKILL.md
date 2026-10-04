---
name: prose-style-guide
version: 1.1.0
description: Before and during chapter writing, autonomously maintain a readable academic style for reviewers and general readers. Prevents exposure of internal identifiers, ensures first-use definitions of technical terms, keeps sentences concise, and applies other writing principles proactively
---

# Prose Style Guide Skill

## Purpose

This skill provides principles for AI to autonomously maintain readable academic prose when writing manuscript chapters (`docs/<paper-id>/chapters/`). Unlike post-hoc checks (`reviewer-readability-check`), this skill activates before and during writing to prevent problems from occurring.

**Target readers**: Both reviewers (specialists) and general readers (those unfamiliar with academic papers).

## Trigger Timings

- Before starting to write a chapter file (confirm principles)
- During writing when uncertain about style (reference as needed)
- When the author points out "hard to understand" or "readers won't follow" (record as friction signal)

## Principles

- **Readers do not know internal identifiers**: Do not expose design-memo IDs (`D2`, `T-4`, `CA-10`) or research-program numbers (`種①`, `seed 4`) in the manuscript. Replace with language readers can understand
- **Define technical terms at first use**: Make the text understandable even to readers unfamiliar with the field
- **Keep sentences short**: Place subjects and predicates close together; avoid chains of modifying clauses
- **Avoid chains of abstract nouns**: Write with concrete verbs and nouns
- **Separate quotation from interpretation**: After a quotation, explain its meaning in the author's own words
- **State the conclusion at the start of paragraphs**: Allow readers to anticipate the paragraph's purpose

## Style Checklist

### 1. Eliminating Internal Identifiers

**Bad example**:
> However, D2 is a secondary review, and this paper does not rely on it as a sole foundation.
>
> Timing of removal is deferred to seed 4.

**Good example**:
> However, the source referenced here is a secondary review, and this paper does not rely on it as a sole foundation.
>
> When to remove the scaffold is outside the scope of this paper.

**Targets**: Literature IDs (A1–F6), task IDs (T-1 to T-6), counter-argument IDs (CA-1 to CA-13), research-program seed numbers (種①, 種④, seed 1, etc.), program-map component numbers, and other design-memo or research-program identifiers. Do not treat them as ordinary nouns. Do not introduce them with a definition in the manuscript; remove them from prose.

### 2. Defining Technical Terms at First Use

**Bad example**:
> This is a coupling-constitution fallacy.

**Good example**:
> The fact that a person uses a tool (coupling) does not mean the tool constitutes part of the mind (constitution) — these are separate claims.

**Targets**: Philosophical terms (coupling, constitution, internalism, externalism, etc.), cognitive science terms (offloading, scaffolding, etc.), and other terms readers may not know

### 3. Sentence Conciseness

**Bad example**:
> Adams and Aizawa (2001) argue that from the fact that tools and people are coupled, it does not follow that tools are part of the mind.

**Good example**:
> Adams and Aizawa (2001) argue that the mere fact that a person uses a tool does not mean the tool is part of the mind.

**Targets**: Sentences over 40 words, sentences with two or more consecutive modifying clauses

### 4. Concretizing Abstract Nouns

**Bad example**:
> The philosophical formalization of the legitimacy of externalization

**Good example**:
> The philosophical grounds for recognizing externalization as legitimate

**Targets**: Expressions with consecutive abstract nouns ("-ity", "-tion", "-ism", etc.)

### 5. Separating Quotation from Interpretation

**Bad example**:
> "The brevity of our life and the multitude of things we are now obliged to know do not permit us to do all of ourselves" — this is an explicit formulation of the necessity of externalization.

**Good example**:
> "The brevity of our life and the multitude of things we are now obliged to know do not permit us to do all of ourselves." This sentence explicitly states that externalization is necessary.

**Targets**: Expressions connecting quotations to interpretations with dashes (——)

### 6. Stating Conclusions at Paragraph Start

**Bad example**:
> What Blair shows is that responses to anxiety turned not only to memory enhancement but to external devices.

**Good example**:
> Responses to anxiety turned not only to memory enhancement but to external devices.

**Targets**: Paragraphs beginning with "What X shows is..." (delays the subject)

## Procedure

```text
[Step 1: Confirm principles before writing] → [Step 2: Reference as needed during writing] → [Step 3: Revise when author points out issues] → [Step 4: Record friction signals]
```

### Step 1: Confirm Principles Before Writing

Before starting to write a chapter, review the Style Checklist in this skill.

### Step 2: Reference as Needed During Writing

When uncertain about style during writing, reference the relevant principle.

### Step 3: Revise When Author Points Out Issues

When the author points out "hard to understand" or "readers won't follow", revise the relevant passage according to the principles.

### Step 4: Record Friction Signals

Record the author's feedback as a friction signal following the `friction-driven-skill-improvement` skill.

## Related Skills

- **Post-hoc check**: `reviewer-readability-check` (mechanical detection of internal identifiers)
- **Terminology consistency**: `terminology-consistency` (standardizing term usage)
- **Sensitive expressions**: `sensitive-expression-guard` (detecting absolute quantifiers, deficit model vocabulary)
- **Friction signals**: `friction-driven-skill-improvement` (filing improvement proposals)

## Outputs

- Revised manuscript (`docs/<paper-id>/chapters/`)
- Friction signal log (`docs/<paper-id>/design/logs/friction-log.md`)
