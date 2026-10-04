---
name: full-feature-cycle
description: Complete feature from request to documented and tested
argument-hint: <feature description>
allowed-tools: Read, Write, Edit, Bash, Glob, Grep
effort: high
---

# Full Feature Cycle

Chain: feature-plan → feature-implement → feature-test → feature-review → feature-document

## Process

1. Plan: acceptance criteria, technical design, test plan
2. Implement: code changes across all affected files
3. Test: unit + integration + edge cases
4. Review: self-review for correctness, patterns, security
5. Document: update docs, changelog, API docs if applicable

Ask for user approval after planning before implementing.