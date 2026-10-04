---
name: thalarch-refactor
description: >
  Behavior-preserving refactoring protocol for simplifying, restructuring, modularizing, or
  modernizing existing code without silently changing externally observable behavior. Use for
  non-trivial cleanup, decomposition, abstraction changes, package/module moves, or legacy
  modernization where regression risk matters.
---

# Thalarch Refactor

A refactor changes structure without intentionally changing observable behavior. Bug fixes,
feature changes, and refactors are separate operations unless the user explicitly combines them.

## 1. Freeze the behavior contract

Before editing, identify the behaviors that must remain stable:

- public inputs/outputs;
- exceptions/error semantics;
- side effects and ordering;
- persisted/wire formats;
- timing/concurrency guarantees that callers depend on;
- ABI/API/binary compatibility where relevant.

If tests are weak, create or locate characterization evidence before broad restructuring when
feasible.

## 2. Identify the actual pressure

Name the reason for the refactor: duplicated knowledge, ownership confusion, excessive coupling,
unsafe state, difficult testing, dependency direction, obsolete platform pattern, or another
specific maintenance cost.

Do not refactor merely because a different style is aesthetically preferred.

## 3. Small semantic steps

Prefer a sequence where each step is independently understandable and verifiable:

- rename;
- extract/move;
- replace data shape;
- invert dependency;
- remove duplication;
- delete old path.

Avoid simultaneous formatting, renaming, behavioral changes, and architecture movement in the
same diff unless unavoidable.

## 4. Abstraction test

Before creating an abstraction ask:

- what repeated knowledge or dependency boundary does it own?
- are there real consumers today?
- does it reduce coupling or merely relocate complexity?
- does the name express a stable domain concept?

If a shared abstraction has accumulated caller-specific flags/branches, consider re-inlining the
behavior, simplifying each caller, and re-abstracting only the truly shared rule.

## 5. Compatibility

For public or persisted contracts, explicitly review:

- source/binary compatibility;
- serialization/schema changes;
- migration order;
- config/environment compatibility;
- client/server rollout sequencing.

## 6. Verification

Use before/after proof:

1. establish baseline tests/behavior;
2. make one bounded structural change;
3. rerun the smallest invalidated checks;
4. inspect the semantic diff;
5. repeat;
6. run broader relevant verification at the end.

If a test must change because behavior changed, that part is not a pure refactor. Surface it.

## Completion

Report structural improvement separately from any intentionally changed behavior. Never hide a
bug fix inside a cleanup commit/diff.
