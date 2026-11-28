---
name: surgical-refactoring
description: Refactor/rename/migration discipline — enumerate every call site before the first edit, separate mechanical from judgment edits, keep the build green, verify by absence and presence. Use when asked to rename, extract, move, split, inline, or deduplicate code; for signature/type reshapes; for codebase-wide pattern swaps (replace a helper, swap a library call); for any change touching 3+ call sites. Not for feature work or bug fixes that merely touch many files.
---

# Surgical Refactoring

Weak refactoring edits the hits the first grep happened to show, fixes a bug it noticed on the way, and calls it done when the build passes. Strong refactoring writes the full touch-point list before editing, changes behavior by exactly zero in the mechanical pass, and proves completion with a grep that returns nothing.

## 0. Baseline before the first edit

Run the project's gate suite (build/typecheck, lint, tests) once before touching anything and note what already fails. Without this you cannot tell a failure you caused from one you inherited.

## 1. Enumerate every touch point BEFORE the first edit

Grep for the symbol/pattern in every casing and form (`fooBar`, `foo_bar`, `FooBar`, `foo-bar`, string literals, dynamic/reflective access, re-exports, tests, docs, config). Record the exact command and the hit count. That list is the definition of done — not a green build, because dead branches, string-keyed lookups, and mock/stub twins compile fine while broken.

Sweeps people skip: test fixtures, mocks that mirror real implementations, serialized/persisted keys, API contract strings, comments/docs, CI and build config, anything reached by string dispatch.

## 2. Separate mechanical from judgment edits

(a) Mechanical: rename, move, signature reshuffle — zero behavior change. (b) Judgment: logic changes, improvements. Do them in separate passes, ideally separate commits, and run the gate suite between them: a green gate after the mechanical pass alone is the proof that pass was behavior-neutral. A diff mixing both is unreviewable, and behavior bugs hide inside "just a rename".

If asked only to refactor, behavior must be bit-identical. Bugs found mid-refactor are noted and reported, not fixed — fixing them silently changes behavior the user did not ask to change.

## 3. Sequence to keep the build green

Introduce the new shape first (new function/type alongside the old), migrate call sites in groups, delete the old shape last. When old and new cannot coexist, do the full sweep in one atomic pass. Never end a session with half the call sites migrated.

## 4. Verify by absence AND presence

- Absence: rerun the step-1 grep → zero hits, or a one-line justification per remaining hit.
- Presence: the full gate suite after the last edit.
- Behavior: exercise the refactored path at runtime — a pure rename that passes tests can still break string-keyed dispatch or serialized data.

## 5. Scope is a contract

Improvements outside the requested scope go in the report as suggestions, not in the diff. The only exception is a change strictly required to complete the refactor (a caller that must adapt).

## Stop and re-plan when

The sweep reveals far more sites than expected (5×), a public API or shared-interface boundary, or persisted-data implications (stored keys, wire formats, migrations). Surface it before continuing; it changes the cost and risk the user approved.

## Report

Include: the grep command with before/after hit counts, justification for any remaining hit, gate results (baseline vs final), what you exercised at runtime, and the bugs and out-of-scope improvements you noticed but did not touch.
