---
name: context-manager
description: "Keep long tasks accurate by tracking goals, constraints, decisions, evidence, artifacts, unresolved questions, and context budget through progressive disclosure and verified handoffs. Use when a task spans many files, tools, agents, or compactions; never treat a summary as stronger evidence than its sources. Turkish triggers: uzun görevin bağlamını koru, durum özeti ve devir, context kaybını önle."
license: MIT
---

# Context Manager

## Context ledger

Maintain a compact task-owned ledger when complexity warrants it:

```markdown
Goal and acceptance criteria:
In scope / out of scope:
User constraints and authority:
Verified facts with source paths/links:
Decisions and rationale:
Artifacts changed/created:
Commands/tests and results:
Open questions, risks, blockers:
Next dependency-ready actions:
```

Keep this as a navigation layer, not a second copy of all source material.

## Operating rules

1. Load only the project instructions and files needed for the current step.
2. Search and inspect before broad reads; prefer exact ranges, schemas, manifests, and generated summaries with source pointers.
3. Separate user requirements, verified facts, inferences, and proposals.
4. Record decisions when they constrain later work. Remove superseded assumptions and preserve why they changed.
5. Store large raw outputs in artifacts and retain a short pointer plus hash/timestamp.
6. Delegate bulky independent investigation with a bounded contract; integrate its evidence rather than its confidence.
7. Before compaction/handoff, write the ledger and verify critical paths, commands, counts, and unresolved risks against source.
8. After compaction, reopen the ledger and current files; do not assume the working tree or external state is unchanged.

## Budget response

When context grows, first remove duplicates and stale branches, then move reference data behind progressive disclosure, summarize completed evidence, and isolate independent work. Never compress away authority limits, acceptance criteria, user corrections, security constraints, failed attempts, or rollback information.

## Completion gate

The final answer must be reconstructable from source artifacts: outcome, changed files, tests, skipped checks, risks, and next action. Delete temporary context artifacts only when they are task-owned and no longer needed; preserve user files and audit evidence.
