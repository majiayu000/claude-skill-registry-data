---
name: review
description: Structured code review that reports correctness, security, performance, and maintainability findings before any fix. Use when you need concrete review findings, not implementation.
origin: Betopia
slash: /review
order: 40
---

# Code Review

Review first. Fix only if the user explicitly asks.

## When to Activate

- User asks for a review or second opinion
- A patch or PR needs findings before merge
- You need a structured audit of correctness or risk

## Inputs to Collect

- The exact diff or changed files
- The intent behind the change
- Any known constraints, expectations, or rollout risks

## Workflow

### 1. Read the scope

- Understand what changed and why
- Check the intent before judging the implementation

### 2. Inspect the diff

- Read the actual files and line ranges that changed
- Keep the review grounded in concrete code

### 3. Review systematically

- Correctness: logic errors, edge cases, broken behavior
- Security: injection, auth, secrets, unsafe flows
- Performance: repeated work, extra renders, large loads
- Maintainability: unclear names, duplication, tangled logic

### 4. Rank findings

- Critical: must fix
- Warning: should fix
- Suggestion: nice to have

### 5. Report clearly

- Cite file and line numbers for each finding
- Separate facts from inference
- If there are no blockers, say so and note any residual risk

## Quality Rules

- Do not turn a review into an implementation unless asked
- Do not hide uncertainty
- Do not use vague comments when a concrete finding is available
- Prefer precise findings over broad commentary

## Examples

- "review this PR for regressions"
- "review the patch before merge"
- "review the code for security issues"

## Output Standard

Findings first, summary second.

Use a ranked list like:

- Critical: must fix
- Warning: should fix
- Suggestion: nice to have
