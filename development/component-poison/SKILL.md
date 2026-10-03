---
name: component-poison
description: Deliberately introduce a controlled number of specification/code misalignments ("poisons") into a single Certus component on a throwaway branch, in order to test translation-verification tooling such as `component-check-spec-translation`. Each poison intentionally desynchronizes the component's `spec.md` from its implementation while keeping the code compiling. Use only for red-team / evaluation of the audit skills, never on a branch intended to merge.
argument-hint: "[component-name] [poison-count]"
---

# Poison a Component

The purpose of this skill is to **test the translation-verification mechanisms** (e.g.
`component-check-spec-translation`) by deliberately introducing known, controlled
mismatches between a component's specification (`spec.md`) and its code. The audit skill
should then be able to detect these seeded mismatches.

This is a destructive, adversarial skill. It only ever operates on a dedicated
`poison-<component-name>` branch that is **not** meant to be merged. Do not run it on
`unstable`, a feature branch you intend to ship, or any branch with uncommitted work you
care about.

The component name is `$0` and the number of poisons to introduce is `$1`.

## 1. Resolve parameters

1. If `$0` (component name) was not supplied, interactively ask the user which component to
   poison and stop until provided.
2. Resolve `$0` to exactly one component directory under `components/` (the lower-case,
   hyphen-ized form of the name, or the directory whose `define_component!` block declares
   it). If it does not exist or is ambiguous, return an error and stop.
3. Discover the component's specs with `rg --files <component-dir>` and select files whose
   path ends in `/spec.md` (support `specs/<feature>/spec.md` and
   `.specify/specs/<feature>/spec.md`, and deeper nesting). If **no** `spec.md` exists,
   stop and report the searched path — there is nothing to misalign against.
4. If `$1` (poison-count) was not supplied, interactively ask the user how many poisons to
   introduce and stop until provided. Require a positive integer; reject `0` or negatives.

## 2. Create and check out the poison branch

1. Confirm the working tree is clean enough to proceed. If there are uncommitted changes
   that would be swept onto the new branch, warn the user and ask whether to continue.
2. Record the current branch as the base branch.
3. Create a **new local branch derived from the current branch**, named
   `poison-<component-name>` (using the lower-case, hyphen-ized component name), and check
   it out — e.g. `git checkout -b poison-eviction-policy-lru`. If a branch with that name
   already exists, ask the user whether to delete and recreate it, or to append a numeric
   suffix. Do not push this branch to any remote.

## 3. Introduce `$1` poisons

Build a short inventory of the component's spec claims (requirements, interfaces,
parameters, data types, defaults, constants, errors, semantics, exclusions) so each poison
targets a *specific, testable* claim. Then apply exactly `$1` distinct changes, each of
which purposely mis-aligns `spec.md` and the code. Spread the poisons across different
claims and, where possible, across different poison categories below so the test exercises
several detection paths.

Each poison must fall into one of these categories (mix them; do not use the same category
for every poison):

- **Remove functionality** — delete a function, branch, validation, or behavior that the
  spec requires (spec still promises it; code no longer does it → *Missing*).
- **Add unspecified functionality** — introduce behavior the spec never mentions: an unused
  helper, a hidden "backdoor" code path, or writing state to a file/env that the spec does
  not describe (→ *Extra behavior*).
- **Change syntax / parameters** — alter a function signature, argument order, argument
  count, or name away from what the spec documents (→ *Contradiction*).
- **Change a data type** — change a field/return/parameter type to one that mismatches the
  type explicitly specified (e.g. `u32` where the spec says `u64`, `Option<T>` vs `T`).
- **Change semantics** — keep the signature but change what the function *does*: invert a
  condition, change a default value, change rounding/units, weaken an error into a silent
  success, or change ordering guarantees.
- **Over-specify the spec** — add a new requirement, acceptance scenario, default, or
  use-case to `spec.md` that the code does **not** implement (poisons the spec side rather
  than the code side).

Guidance for each poison:

- Make it a *semantic* mismatch, not a cosmetic one. Renaming a private local or reflowing
  comments will not exercise the audit. Target something the spec states as an observable
  contract.
- Keep each poison small and self-contained, and note the exact `path:line` on both the
  spec side and the code side.
- Prefer targeting distinct requirement IDs / interfaces so the poisons are independently
  detectable.

## 4. Keep the code compiling

**The code must still compile after all poison changes.** After applying the poisons,
build the component and fix any compilation errors introduced by the poisons *without
undoing the intended misalignment*:

```bash
cargo build -p <crate-name>
```

If a component is SPDK-gated and cannot be built in this environment, build with its
default configuration and clearly note in the report that a full `--workspace` build was
not verified. If a poison cannot be made to compile without also removing the misalignment,
back it out and choose a different poison so the final count of applied poisons still
equals `$1` (or, if impossible, stop and report how many were successfully applied).

Do **not** run formatters or linters that would "helpfully" reconcile the mismatch, and do
not run `component-sync-specs` or any spec-sync skill — that would defeat the purpose.

## 5. Summarize the poisons

Write a `POISON.md` file in the component directory summarizing every applied change in a
table, so the poisons can later be compared against whatever the verification skill detects
(the ground-truth key). Use this shape:

```markdown
# Poison Report

Component: <component-dir>
Base branch: <base branch>
Poison branch: poison-<component-name>
Poisons requested: <$1>   Poisons applied: <N>
Build verified: <cargo build -p <crate> result / caveat>

> Generated by the `component-poison` skill to test translation-verification tooling.
> This branch is intentionally broken and must not be merged.

| # | Category | Side poisoned | Spec claim (path:line) | Code location (path:line) | What was changed | Expected audit result |
|---|---|---|---|---|---|---|
| 1 | Change data type | code | specs/001-.../spec.md:88 | src/lib.rs:142 | Return type `u64` → `u32` | Contradiction (High) |
| 2 | Over-specify spec | spec | specs/001-.../spec.md:120 (added) | (none) | Added FR for retry backoff not implemented | Missing (Medium) |
```

Map the "Expected audit result" column to the classifications the audit skill uses
(*Aligned / Partial / Contradiction / Missing / Extra behavior / Unverifiable*) so the
poison report doubles as an answer key.

## 6. Report

Print a concise summary to the user: the poison branch name, the base branch, how many
poisons were applied (vs requested), whether the build passed, and the path to `POISON.md`.
Remind the user this branch is intentionally broken, must not be merged, and that they can
now run `component-check-spec-translation` against the component to see how many poisons it
catches. Do not commit or push unless the user explicitly asks.
