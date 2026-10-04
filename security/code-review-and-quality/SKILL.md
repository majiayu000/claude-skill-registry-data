---
name: code-review-and-quality
description: >
  Two-stage code review: spec compliance first, then code quality.
  Use when reviewing code changes, conducting PR reviews, or when
  subagents complete implementation tasks. Ensures code matches
  spec AND meets quality standards.
version: 1.0.0
permissions:
  - fs.read
  - shell.exec
triggers:
  - context: "reviewing code"
  - context: "PR review"
  - context: "subagent completed a task"
  - command: "/review"
platforms:
  - claude-code
  - cursor
  - gemini-cli
  - copilot
  - codex
  - opencode
  - windsurf
  - kiro
dependencies:
  - test-driven-development@^1.0.0
model_variants:
  claude:
    enforcement_style: "human-partner collaborative"
  gemini:
    enforcement_style: "structured-checklist"
  gpt:
    enforcement_style: "directive-imperative"
author: codehands-core
signed: true
tier: 1
---

## Overview

Code review has two jobs: verify the code does what it should (spec compliance) and verify it does it well (quality). These are separate stages — don't mix them. Spec issues block quality review. Quality issues block merge.

## When to Use

- When reviewing any code changes before merge
- When a subagent completes an implementation task
- During PR review
- During `/review` phase
- NOT for reviewing specs or plans (use brainstorming/planning skills)

## Process

### Stage 1: Spec Compliance Review

> Complete this stage BEFORE starting Stage 2. If spec issues exist, they must be fixed first.

1. **Read the spec/plan task.** What was the implementation supposed to do?
2. **Read the code changes.** `git diff` or review the changed files.
3. **Check completeness:**
   - ✅ Every requirement from the spec implemented?
   - ✅ All acceptance criteria satisfied?
   - ❌ Nothing EXTRA added (no scope creep)?
   - ❌ Nothing MISSING from requirements?
4. **Verdict:**
   - **PASS** → Proceed to Stage 2
   - **FAIL** → List specific issues. Implementer fixes. Re-review.

### Stage 2: Code Quality Review

5. **Correctness:** Does the code actually work? Are edge cases handled?
6. **Tests:** Do tests cover the new behavior? Are they meaningful (not just "passes")?
7. **Readability:** Can someone understand this code without explanation?
8. **Security:** Any of the `codehands:security-and-hardening` red flags present?
9. **Performance:** Any obvious performance issues (N+1 queries, unnecessary allocations)?
10. **Consistency:** Does the code follow existing patterns? (`codehands:source-driven-development`)
11. **Simplicity:** Is there a simpler way to achieve the same result?

### Output Format

```markdown
## Code Review

### Spec Compliance: [PASS / FAIL]
- [List of spec issues if FAIL]

### Quality Review: [APPROVED / CHANGES REQUESTED]

**Strengths:**
- [What was done well]

**Issues:**
| Severity | File:Line | Issue | Suggestion |
|---|---|---|---|
| Important | src/auth.ts:45 | SQL concatenation | Use parameterized query |
| Suggestion | src/auth.ts:12 | Magic number | Extract as constant |
| Nit | src/auth.ts:3 | Unused import | Remove |

**Verdict:** [APPROVED / CHANGES REQUESTED (with priority)]
```

### Severity Levels

| Severity | Meaning | Action |
|---|---|---|
| **Blocker** | Security vulnerability, data loss risk, or spec violation | Must fix before merge |
| **Important** | Bug, logic error, or significant quality issue | Must fix before merge |
| **Suggestion** | Better approach exists but current works | Fix if easy, otherwise note for future |
| **Nit** | Style, naming, formatting | Fix if easy, don't block on it |

## Common Rationalizations

| Rationalization | Reality |
|---|---|
| "The code works, that's good enough" | Working code that's unreadable, insecure, or untested is technical debt. Review exists to catch what "works" misses. |
| "I don't want to be too picky" | Specific, actionable feedback is not picky — it's professional. Vague "looks good" reviews are worthless. |
| "Spec compliance and quality are the same thing" | No. Code can perfectly match the spec but be poorly written. Code can be beautifully written but miss requirements. Two stages. |
| "Self-review is sufficient" | Self-review catches 40% of issues. External review catches 80%. The 40% gap is where bugs live. |

## Red Flags

- Reviewing quality before spec compliance (wrong order)
- "LGTM" without reading the code
- No review comments at all (either everything is perfect or nothing was reviewed)
- Blocking on nits while ignoring important issues
- Accepting "close enough" on spec compliance

## Verification

- [ ] Spec compliance reviewed BEFORE code quality
- [ ] All spec requirements verified as implemented
- [ ] No extra features beyond spec (no scope creep)
- [ ] Quality review covers: correctness, tests, readability, security, performance, consistency
- [ ] Issues categorized by severity
- [ ] Strengths acknowledged (positive reinforcement matters)

## See Also

- `codehands:security-and-hardening` — Security checks during review
- `codehands:performance-optimization` — Performance checks during review
- `codehands:code-simplification` — Simplification during review
- `codehands:multi-agent-orchestration` — Review pipeline for subagent output
