---
name: cross-validation
description: Use when user says "validate this", "get feedback", "cross-validate", "what are we missing", when seeking external review before committing to major decisions, when stress-testing a design with senior reviewers, or when reviewer responses need to be synthesized into actionable changes.
---

# Cross-Validation

## Overview

Two-phase skill with a human step in the middle. Phase 1: compile a self-contained prompt that any reviewer can assess without prior context. Phase 2: synthesize responses into consensus levels and actionable changes. The prompt must stand alone — a reviewer should need zero prior context.

## When to Use

- Major architectural or product decisions need external validation
- User wants to check blind spots before committing to a direction
- Multiple reviewers (human or AI) will assess the same document
- High-stakes decisions where being wrong is expensive

## When NOT to Use

- Quick sanity check on a small decision — just ask directly
- Code review — use `code-review-and-quality`
- No `.forge/prd.md` or `.forge/architecture.md` exists yet — produce artifacts first

## Common Rationalizations

| Thought | Reality |
|---------|---------|
| "We've already thought about this enough" | Internal teams develop blind spots. External eyes catch what you've normalized |
| "The prompt doesn't need full context" | If a reviewer has to ask clarifying questions, the prompt failed |
| "Three reviewers said it's fine, so it's fine" | Unanimous approval is less valuable than one specific objection |
| "Disagreements mean someone is wrong" | Disagreements reveal hidden assumptions — both sides may be partially right |
| "We can synthesize informally" | Informal synthesis loses minority opinions. Structured synthesis surfaces them |

## Red Flags

- Prompt requires prior context to understand (not self-contained)
- Questions are generic ("is this good?") instead of specific ("does the auth model handle session revocation within 5 seconds?")
- Synthesis ignores dissenting opinions
- All reviewers agree on everything (questions were too soft)
- Synthesis doesn't distinguish consensus levels

## Core Process — Phase 1: Generate Prompt

**Re-entry check**: If `.forge/cross-validation-prompt.md` already exists and the user provides reviewer responses, skip to Phase 2.

### Step 1: Identify what to validate

Read available `.forge/` artifacts. With the user, identify:
- Which decisions are highest-risk (most expensive if wrong)
- Which assumptions have the least evidence
- What specific aspects need external eyes

### Step 2: Compile self-contained context

Extract from `.forge/` artifacts into a single document that a reviewer can read cold:
- Problem statement (from PRD)
- Key architectural decisions (from architecture.md)
- Trade-offs made and alternatives rejected (from ADRs)
- Current approach summary

**Self-containment test**: can someone who has never seen this project understand the context and give useful feedback? If not, add more context.

### Step 3: Structure questions

Write 10+ specific questions across categories:
- Architecture decisions and trade-offs
- Security and data handling
- Scalability and performance assumptions
- Business model and pricing
- Missing requirements or edge cases
- Risk assessment
- Technical debt implications

Each question must be specific and answerable. Not "is the architecture good?" but "given the multi-tenant requirement, is schema-per-tenant or RLS the better isolation strategy for <specific constraints>?"

### Step 4: Define output format

Tell reviewers exactly how to structure their response: numbered answers matching the questions, confidence level per answer, and a "what did we miss?" section.

### Step 5: Write the prompt

Write `.forge/cross-validation-prompt.md` with: context, questions, and response format. Prepend a `forge:meta` header (`generated_by: cross-validation`, `generated_at: <ISO 8601 UTC with Z>`, `depends_on: [.forge/prd.md, .forge/architecture.md, …any other artifacts embedded in the prompt]` — paths only, never hashes, `generated_from: {<each path>: <upstream content_hash AT generation time>}`, `content_hash: <sha256 first 8 of THIS file's body>`). See [forge-dependency-graph](../../references/forge-dependency-graph.md).

**Pause**: "Prompt written to `.forge/cross-validation-prompt.md`. Send this to your reviewers. When you have responses, run `/validate` again with the responses to generate the synthesis."

## Core Process — Phase 2: Synthesize Responses

### Step 6: Categorize consensus

For each question, classify the responses:
- **Unanimous**: all reviewers agree — high confidence in this direction
- **Strong consensus**: most agree, minor variations — proceed with noted caveats
- **Split**: roughly even disagreement — requires deeper analysis
- **Dissent**: one reviewer disagrees strongly — investigate their reasoning

### Step 7: Extract actionable changes

From disagreements and suggestions, produce:
- **Must change**: issues multiple reviewers flagged independently
- **Should consider**: good ideas from at least one reviewer with strong reasoning
- **Monitor**: concerns that don't require immediate action but should be tracked

### Step 8: Write synthesis

Write `.forge/cross-validation-synthesis.md` with: consensus summary per question, actionable changes list, and a "best ideas we hadn't considered" section. Prepend a `forge:meta` header (`generated_by: cross-validation`, `generated_at: <ISO 8601 UTC with Z>`, `depends_on: [.forge/cross-validation-prompt.md, …reviewer-response files]` — paths only, never hashes, `generated_from: {<each path>: <upstream content_hash AT generation time>}`, `content_hash: <sha256 first 8 of THIS file's body>`).

## Verification

- [ ] Prompt is self-contained — reviewer needs zero prior context
- [ ] Questions are specific, not generic
- [ ] At least 10 questions across multiple categories
- [ ] Synthesis distinguishes consensus levels (unanimous / strong / split / dissent)
- [ ] Dissenting opinions are investigated, not dismissed
- [ ] Actionable changes are categorized (must / should / monitor)
- [ ] `.forge/cross-validation-prompt.md` written (Phase 1)
- [ ] `.forge/cross-validation-synthesis.md` written (Phase 2, after responses received)
