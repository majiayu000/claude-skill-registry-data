---
name: parallel-code-review
description: Launches three parallel code-reviewer subagents to review code from different angles — correctness, architecture, and security/performance. Only use when the user explicitly requests a code review or parallel review, never proactively.
---

# Parallel Code Review

Launch three `code-reviewer` subagents in parallel, each focused on a distinct review angle. Combine their results into a unified summary.

## When to Use

Only when the user explicitly asks for a code review (e.g., "review my code", "run a code review", "parallel review"). **Never trigger proactively.**

## Workflow

### Step 1: Identify the diff

Run `git diff` (or `git diff --cached` if the user has staged changes) to capture what changed. If the user specifies files or a branch, scope accordingly.

### Step 2: Launch three subagents in parallel

Use the Task tool to launch all three in a **single message** so they run concurrently. Each subagent should use `subagent_type: "staff-code-reviewer"`. Pass the full diff and any relevant file contents in the prompt.

**Agent 1 — Correctness & Robustness**
Focus: bugs, edge cases, error handling, logic errors, test coverage.
Prompt should instruct: "Focus exclusively on correctness, robustness, and testing. Look for bugs, unhandled edge cases, logic errors, missing error handling, and whether tests adequately cover the changes. Ignore architecture and security concerns — other reviewers will handle those."

**Agent 2 — Design & Maintainability**
Focus: architecture, abstractions, readability, naming, separation of concerns, tech debt.
Prompt should instruct: "Focus exclusively on design, architecture, and maintainability. Evaluate abstractions, naming, separation of concerns, readability, and whether the change fits the existing codebase patterns. Ignore correctness bugs and security — other reviewers will handle those."

**Agent 3 — Security & Performance**
Focus: vulnerabilities, data integrity, PII handling, performance pitfalls, scalability.
Prompt should instruct: "Focus exclusively on security and performance. Look for vulnerabilities, PII exposure, missing authorization, input validation gaps, performance pitfalls (N+1 queries, unnecessary allocations, blocking calls), and scalability concerns. Ignore architecture and correctness — other reviewers will handle those."

### Step 3: Synthesize results

Once all three agents return, combine their findings into a single unified review:

```
## Code Review Summary

### Critical (must fix)
[Deduplicated critical findings from all three agents]

### Warnings (strongly recommend)
[Deduplicated warnings from all three agents]

### Suggestions
[Deduplicated suggestions from all three agents]

### Positive Callouts
[Notable good patterns observed across reviews]
```

Rules for synthesis:
- Deduplicate overlapping findings — if two agents flag the same issue, merge into one entry and note which angles caught it.
- Preserve the most specific and actionable version of each finding.
- Tag each finding with its source angle: `[correctness]`, `[design]`, or `[security/perf]`.
- If agents disagree, present both perspectives and note the tension.
