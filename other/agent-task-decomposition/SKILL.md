---
name: agent-task-decomposition
description: Break a multi-step engineering request into bounded agent tasks with dependencies, acceptance tests, and safe parallel work.
---

# Agent Task Decomposition

## Goal

Improve throughput without creating overlapping edits, hidden dependencies, or ambiguous final validation.

## Inputs to inspect

User goal, repo structure, definition of done, permissions, likely file ownership, and validation commands.

## Workflow

1. Translate the goal into observable outcomes and explicit out-of-scope changes. Identify decisions that require user approval before implementation.
2. Map the dependency graph: discovery, design, independent implementation units, integration, and verification. Keep early uncertainty as a task, not a hidden assumption.
3. Give each task a named owner, disjoint file scope where possible, specific inputs, expected artifacts, test requirements, and stop conditions.
4. Parallelize only work whose contracts are independent. Serialize shared manifests, lockfiles, migrations, generated outputs, and branch/ref updates.
5. Integrate by reviewing diffs and artifacts, then run cross-task tests against the combined state. Reconcile contradictory findings before claiming completion.

## Validation checklist

- [ ] Every task maps to a user-visible acceptance criterion.
- [ ] Shared mutable files have an explicit single owner or merge protocol.
- [ ] Agents cannot expand scope merely because a dependency is unavailable.
- [ ] Integration tests cover interaction between tasks, not just isolated unit success.
- [ ] The final report distinguishes implemented, verified, blocked, and untested work.

## Required output

Produce a dependency graph, task cards, file ownership map, verification matrix, and a final integration checklist.

## Boundaries and failure handling

Do not split work by arbitrary file counts if that breaks functional boundaries; do not treat parallel completion as proof the integrated result works.

When repository evidence is incomplete, label the gap explicitly and request only the missing information that changes the decision. Do not claim commands, benchmarks, tests, or runtime checks passed unless their outputs were observed.
