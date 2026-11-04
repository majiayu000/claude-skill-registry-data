---
name: code-review
description: "Use when completing a coding task to perform senior-level code review. Triggers on: code review, post-task review, review changes, check code quality, review my code."
argument-hint: "Optional: the files or plan section to scope the review to"
user-invocable: true
context: fork
agent: code-review
allowed-tools: Read, Grep, Glob, Bash(git diff:*), Bash(git status:*), Bash(git log:*)
---

Before acting, load and follow @../../../.agents/skills/code-review/SKILL.md in full.
