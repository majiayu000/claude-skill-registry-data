---
name: self-review
description: Independently review the current implementation for one Issue before external review.
argument-hint: "[issue-number]"
disable-model-invocation: true
context: fork
agent: general-purpose
background: false
disallowed-tools: Write Edit NotebookEdit
---

Independently review the current branch implementation for GitHub Issue $0.

Read `AGENTS.md`, the Issue, and the branch diff against `main`. Do not modify files, commit, push, or change GitHub state.

Prioritize:
- unmet acceptance criteria
- correctness defects and regressions
- existing contract violations
- repository ownership, dependency, and information-flow boundary violations
- concrete changed behavior that lacks necessary regression coverage

Do not make speculative extensibility, unrelated cleanup, or style already enforced by tooling blocking.

Classify findings as `blocking` or `non-blocking`. If no blocking finding remains, explicitly conclude `blockingなし / merge可能`.
