---
name: code-review
description: High signal-to-noise code review focused on bugs, security, and logic — not style
triggers: [review, code review, review this PR, review changes, review diff]
audience: engineer
---

# Code Review

## Context
Code review is a critical quality gate, but it creates friction when reviewers surface noise (style, formatting, naming preferences) alongside signal (bugs, logic errors, security issues). This skill focuses the review on what genuinely matters.

Use this skill when:
- Reviewing a PR or diff before merging
- Self-reviewing before requesting review from a teammate
- Reviewing a colleague's work during pairing or async review

## Instructions

### What to Look For (Signal — Always Surface)
1. **Logic errors** — Does the code do what the author intended? Are there off-by-one errors, wrong operator choices, incorrect conditionals?
2. **Security vulnerabilities** — Injection risks, improper auth checks, sensitive data in logs, unvalidated inputs, insecure deserialization.
3. **Data correctness** — Race conditions, missing null/empty checks, incorrect type assumptions, data loss on failure paths.
4. **Error handling gaps** — Uncaught exceptions on critical paths, swallowed errors, missing retry logic where needed.
5. **Breaking changes** — API contract changes, database schema changes without migration, removed behavior.
6. **Missing tests** — New logic without test coverage; changed behavior without updated tests.
7. **Performance risks** — N+1 queries, unbounded loops, synchronous calls on hot paths, missing pagination.
8. **Correctness against requirements** — Does the change actually solve the stated problem?

### What NOT to Comment On (Noise — Skip)
- Formatting, indentation, or whitespace (let the linter handle it)
- Naming style preferences unless the name is actively misleading
- "I would have done it differently" without a specific defect
- Minor stylistic preferences on language features

### How to Write a Review Comment
- **Be specific.** Quote the line, state the issue, explain the risk.
- **Distinguish severity:**
  - `[blocker]` — Must fix before merge. Bug, security issue, breaking change.
  - `[suggestion]` — Worth considering but not required to merge.
  - `[question]` — Seeking clarification, not a defect.
- **Propose a fix when blocking.** Don't just say "this is wrong" — show what right looks like.
- **Praise what's done well.** One specific positive observation per review builds a healthy culture.

### Review Checklist
Before approving, confirm:
- [ ] No blockers remain unresolved
- [ ] New behavior is covered by tests
- [ ] No secrets or credentials in the diff
- [ ] Migration/rollback plan exists for schema or data changes
- [ ] Public API changes are documented or versioned

## Principles
- Source: [LeadDev — Code Review Best Practices](https://leaddev.com)
- Source: [Thoughtful Code Review — Martin Fowler Blog](https://martinfowler.com)
- Key idea: *"The goal of code review is to find real problems, not to show off your knowledge or preferences."*

## Output Format
When applying this skill, the agent should:
- List findings grouped by severity: `[blocker]`, `[suggestion]`, `[question]`
- Quote the relevant code line for each finding
- Provide a specific fix or recommendation for each blocker
- End with a summary: overall assessment and whether it's ready to merge
