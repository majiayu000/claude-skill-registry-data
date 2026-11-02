---
name: agent-state-checkpointing
description: Design resumable agent checkpoints that preserve task state, evidence, changed files, and idempotent next actions after interruption.
---

# Agent State Checkpointing

## Goal

Allow interrupted workflows to resume without repeating destructive actions or losing what has already been verified.

## Inputs to inspect

Workflow phases, session artifacts, repository state, external side effects, retry behavior, and current branch/revision.

## Workflow

1. Identify safe checkpoint boundaries and the minimum state required to resume: task objective, decisions, inputs, outputs, current revision, pending actions, and verification evidence.
2. Record completed steps separately from intended steps; attach tool result references and hashes or versions to artifacts that may change.
3. Classify in-flight actions as safe to retry, requiring status reconciliation, or unsafe to repeat without explicit approval.
4. On resume, verify the current branch/revision and revalidate checkpoints that depend on external state before continuing.
5. Test interruption after reads, file writes, external mutation, partial batch operations, and during final verification; ensure repeated resume is safe.

## Validation checklist

- [ ] Checkpoint records clearly distinguish done, pending, and uncertain side effects.
- [ ] Resume verifies that dependent files and external state have not changed unexpectedly.
- [ ] Retries are idempotent or preceded by reconciliation.
- [ ] Secrets and unnecessary personal data are excluded from checkpoint artifacts.
- [ ] A second resume does not duplicate completed mutations.

## Required output

Deliver a checkpoint schema, safe-resume decision table, validation/reconciliation protocol, and interruption test matrix.

## Boundaries and failure handling

Do not resume blindly from a text summary after the repository or remote state has changed; do not repeat ambiguous external actions without checking their result.

When repository evidence is incomplete, label the gap explicitly and request only the missing information that changes the decision. Do not claim commands, benchmarks, tests, or runtime checks passed unless their outputs were observed.
