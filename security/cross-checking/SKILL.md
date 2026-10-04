---
name: cross-checking
description: >-
  Cross-references a specific topic, concept, or rule across all files to verify
  it is used consistently. Use when checking if a term or claim matches its
  authoritative definition everywhere, or when user says "cross-check", "is this
  consistent", "verify this term", or "does this match everywhere". Does NOT audit
  entire directories — use /auditing-physics or /auditing-canon for that.
model: sonnet
effort: medium
context: fork
---

# Cross-Checking

Verify that a specific topic or rule is used consistently across the repo.

## Process

1. Find the authoritative source for the term/rule
2. `grep -r` to find all mentions across the repo
3. Compare each mention against the authoritative definition
4. Report matches, additions, and contradictions

## Rules

- Cross-civilization differences are NOT contradictions
- In-universe documents may intentionally differ from science documents
- Different eras may have different understandings

## Out of Scope

Does NOT audit entire directories (use /auditing-physics or /auditing-canon).
Does NOT write or modify files. Report only.
