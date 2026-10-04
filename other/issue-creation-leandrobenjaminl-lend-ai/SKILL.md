---
name: issue-creation
description: >
  Professional GitHub issues — bug reports, feature requests, and tasks
  with enough context to act on immediately. Templates and clear criteria.
  Trigger: When filing an issue, reporting a bug, or requesting a feature.
license: MIT
metadata:
  author: Leandro Benjamin L.
  version: "3.0"
  model_tier: T2-fast
---

# Skill: issue-creation

Professional issues. Clear enough that anyone can pick them up.

## Trigger

- You found a bug and need to report it
- You want to propose a new feature
- A large project needs to be broken down into tasks
- You were assigned an issue and need to understand it

## Workflow LEND

1. ANALYZE
   ├── Type: bug, feature, chore, improvement
   ├── Severity: critical, major, minor, suggestion
   ├── Context: where does it happen? how to reproduce?
   └── Priority: now, this week, this month, backlog

2. OFFER (Senior Menu)
   ├── A) Bug report — reproduction steps + expected vs actual + environment
   ├── B) Feature request — description + motivation + acceptance criteria
   └── C) Technical task — context + definition of done + subtasks

3. CHOOSE → user confirms

4. EXECUTE
   ├── Bug: clear title, steps to reproduce, expected vs actual, logs/screenshots, environment
   ├── Feature: title, description, motivation, acceptance criteria (Given/When/Then)
   ├── Labels: bug, feature, enhancement, good-first-issue, needs-discussion
   ├── Assignee: who will resolve it
   ├── Milestone: if applicable (sprint, version)
   ├── Priority label: P0 (critical), P1 (high), P2 (medium), P3 (low)
   └── Templates: use issue template if the repo has one

5. VERIFY
   ├── The issue has all the information needed to start
   ├── Reproduction steps are clear (for bugs)
   └── Acceptance criteria are measurable (for features)

- [ ] Save decisions and changes to Engram (mem_save)
- [ ] Check if README, AGENTS.md, or ARCHITECTURE.md need updating
- [ ] If docs changed → update them in the same PR/commit
