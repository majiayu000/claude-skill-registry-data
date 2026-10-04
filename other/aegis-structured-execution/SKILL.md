---
name: aegis-structured-execution
description: 'Use when substantial project work needs execution control. USE FOR: "proof-heavy execution pass", "multi-phase drift control", "scope-proof-checkpoint coordination". DO NOT USE FOR: "tiny one-shot edit", "general brainstorming", "simple formatting".'
disable-model-invocation: true
---

# Aegis Structured Execution

Use this skill for broad, risky, multi-phase, or proof-heavy work where execution state can drift.

## Contract

1. Identify the deliverable, scope, non-goals, truth sources, and proof requirements.
2. Split work into phases only when trust boundaries, proof modes, or execution surfaces differ.
3. Keep final synthesis in the coordinator; helper agents may gather evidence but do not define final truth.
4. Separate current state, target state, validated proof, unresolved gaps, and drift.
5. Update the active checkpoint surface after meaningful state changes.
6. Report completion only at the strongest proven level: `implemented`, `code_proven`, `test_proven`, `runtime_proven`, or `end_to_end_proven`.

## Completion Criteria

The execution pass is complete only when the deliverable, proof level, unresolved gaps, and next safe action are explicit and do not contradict repo truth.

## Red Flags

- The plan becomes generic ceremony.
- Helper output is treated as final authority.
- Proof is inflated by docs, HTML, or tracker status.
- A contradiction is smoothed over instead of marked as `drift` or `gated`.

## Boundary

Do not use this as a heavy wrapper for tiny one-shot tasks. Prefer `aegis-communication-discipline` plus `aegis-html-ledger` for ordinary project execution.
