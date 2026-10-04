---
name: custodian
description: Infrastructure custody pass — dispatches infra-custodian over a scope (TEND) or the working diff (REVIEW, the bare default); returns its typed receipt. Use after landing edits to constitutions, RULINGS, routers, laws, standards, or .claude/ definitions, and on "check the infra", "did we miss a ruling".
argument-hint: [paths = tend | ref = review that diff | memory = audit the memory estate | empty = review the working diff]
context: fork
agent: infra-custodian
---

TARGET: $ARGUMENTS

- Paths: TEND those surfaces — a target resolving on disk is a path; one resolving only as a committish is a ref.
- Ref: REVIEW that diff (`git diff <ref>` with `git status --porcelain`).
- `memory`: MEMORY audit over the project memory directory — resolve it as `~/.claude/projects/<slug>/memory/`, `<slug>` the absolute repo-root path with every `/` and `.` replaced by `-`; the audit is read-only, its `MEMORY:` rows land through the dispatcher.
- Empty: REVIEW the working diff — `git status --porcelain` with `git diff HEAD`, falling to the last commit's own diff (`git show HEAD`) when the tree is clean.

Return the receipt whole — the dispatcher owns `OWED:`, `ROUTED:`, and `MEMORY:` row implementation.
