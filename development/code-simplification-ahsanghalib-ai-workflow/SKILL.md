---
name: code-simplification
description: Use when working code is harder to read, maintain, or extend than necessary and can be made clearer without changing observable behavior. Do not use for speculative rewrites, performance work, or code that is not understood yet.
license: MIT
---

# Code Simplification

Reduce accidental complexity while preserving exact observable behavior. The
goal is faster comprehension and safer maintenance, not fewer lines.

## When to use

- A working implementation is deeply nested, duplicated, indirect, or unclear.
- A review identifies unnecessary abstractions or misleading names.
- Recently changed code needs a focused readability pass.
- Related logic can be made consistent without changing its contract.

Do not simplify code that is not understood, throwaway code about to be
rewritten, or performance-critical code without a measurement. Use
`performance-optimization` for measured performance work and
`systematic-debugging` for unexplained failures.

## Preserve behavior exactly

Before every change, check that inputs, outputs, public interfaces, error types
and messages where observable, side effects, ordering, retries, timing
assumptions, concurrency, logging, and edge cases remain compatible. Do not
modify tests merely to make a changed behavior pass.

## Understand the fence first

Read repository instructions, neighboring code, callers, callees, tests,
configuration, and relevant history. Answer:

- What responsibility does this code have?
- Which callers and external consumers depend on it?
- Which edge and error paths are specified by tests or documentation?
- Why might the existing abstraction or branch exist? Consider performance,
  platform, compatibility, or a historical constraint.

If those answers are unknown, gather context before simplifying. A fence with
an unclear purpose is a reason to investigate, not remove.

## Simplification signals

Use judgment; these are prompts, not automatic transformations:

- Deep nesting → guard clauses or a named predicate when control flow remains
  equivalent.
- Long functions → separate responsibilities behind focused, well-named
  helpers.
- Nested ternaries or dense expressions → explicit branches or a small lookup.
- Repeated logic → a shared function only when the abstraction has one clear
  responsibility and stable semantics.
- Generic, abbreviated, or misleading names → names that describe the domain
  and actual side effects.
- Comments describing obvious mechanics → remove; comments explaining intent,
  constraints, or "why" → preserve.
- Dead code or unused imports → remove only after confirming it is unreachable
  or unused across relevant consumers.

Avoid inlining a useful concept, merging unrelated responsibilities, removing
test seams, or replacing a deliberate abstraction with a clever expression.
Line count is not a simplicity metric.

## Incremental workflow

1. Capture a baseline with the narrowest relevant tests and checks.
2. Limit the scope to the requested or recently changed area.
3. Make one coherent simplification at a time.
4. Run the relevant checks after each meaningful change.
5. Inspect the diff for behavior, project-convention, and scope regressions.
6. Keep only changes that are easier to understand and still fully verified.

If a simplification fails a check or makes the code harder to review, restore
that attempt and reassess. Large mechanical rewrites require an approved,
reviewable automation plan; do not hand-edit a broad refactor casually.

## Verification

- [ ] Existing tests pass without weakening their assertions.
- [ ] Build, type, lint, or format checks pass where applicable.
- [ ] Public contracts, error handling, side effects, and edge cases are
      preserved.
- [ ] The result follows local conventions and is more comprehensible than the
      original.
- [ ] No unrelated files or speculative cleanup entered the diff.
- [ ] The final diff is small enough to review, or the automation and scope
      were explicitly approved.

## Upstream basis

Adapted for this harness-agnostic repository from
[addyosmani/agent-skills code-simplification](https://github.com/addyosmani/agent-skills/tree/6ca0cd7db39b41b1c37e26d335c507ee92382c6d/skills/code-simplification),
licensed under MIT.
