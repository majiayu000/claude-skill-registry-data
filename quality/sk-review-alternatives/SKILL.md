---
name: sk-review-alternatives
description: Independent review of proposed alternatives before they are presented to the user. Use when the sk-alternatives skill has generated options, or when the user passes alternatives and asks for a review.
---

# Review Alternatives

Evaluate up to 3 proposed alternatives and flag low-quality options. Read-only unless the user explicitly asks the reviewer to rewrite.

## When to use

- After `sk-alternatives` generates options.
- When a user pastes alternatives and asks for a review.
- Before presenting alternatives to a stakeholder.

## Input

For each option:

- **Idea**: short description
- **Snippet** (if present): minimal code or design example
- **Pros / Cons**: brief, balanced assessment
- **Recommendation** (if present): author's preferred option and why

## Output contract

Return ONLY this block. No prose intro.

```text
### Alternatives Review Findings

option:<n>: <tag>: <problem>. <fix>
totals: N irrelevant N duplicate N weak N strawman N missing-context N unjustified | verdict: pass / needs-revision
```

Or, when no findings:

```text
### Alternatives Review Findings

Lean & valid. Ship.
```

## Tags

- `irrelevant`: does not solve the actual problem or constraints
- `duplicate`: overlaps another option without a distinct trade-off
- `weak`: viable but worse in every meaningful dimension
- `strawman`: intentionally bad or only included to make another look good
- `missing-context`: omits a critical cost, risk, or constraint
- `unjustified`: recommendation not supported by pros/cons

## Review criteria

1. **Relevance**: every option addresses the user's actual constraints.
2. **Distinctness**: options differ on at least one meaningful trade-off.
3. **Fairness**: pros and cons are balanced.
4. **Completeness**: each option mentions the main cost/risk/limitation.
5. **Recommendation support**: the recommendation follows from the comparisons.

## Triage

Label each finding `valid`, `false_positive`, or `unvalidated` with a one-line reason. If zero `valid` findings remain, output exactly `Lean & valid. Ship.` and `verdict: pass`.

## Rules

- One finding per line; problem then fix, separated by ". ".
- Sort findings by `option:<n>` ascending.
- Repeat issues per option if they span multiple options.
- Do not add new options; only review what is provided.
- Minor wording or disagreements are not findings unless they mislead.
