---
name: plan-mode-spec-lint
description: Find what a spec leaves unstated. Use when auditing an existing spec, PRD, or epic for the gaps that would cause a wrong implementation.
license: MIT
---

# Spec Lint

A spec is a contract; the failures live in what it does not say. Audit an existing spec for the gaps that would cause a wrong implementation.

1. Read the spec and list every behavior it specifies. For each, note the trigger, the expected result, and the stated edge cases.
2. For each specified behavior, ask what happens in the cases the spec does not name: empty input, duplicate input, concurrent input, failure of a dependency, partial completion, and recovery after interruption.
3. Check for contradictions between sections, undefined terms used as if defined, and acceptance criteria that cannot be observed or tested.
4. Report gaps ordered by the cost of getting them wrong, each with the specific question that would close it. Do not fix the spec.

Linting is read-only. Report the gaps; the spec's owner decides what to change.

Record this output in `docs/plans/` per the [doc system](../references/doc-system.md), delegating the write to a subagent.
