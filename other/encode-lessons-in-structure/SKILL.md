---
name: encode-lessons-in-structure
description: Turn an evidenced recurring mistake into a focused structural safeguard such as a type, test, lint rule, or existing check. Consult when the same correction repeats; avoid generalizing a one-off preference.
license: MIT
---

# Encode Lessons in Structure

When a correction repeats, ask which mechanism could prevent the actual
failure. This is a shared improvement principle, not permission to expand the
current task or rewrite global instructions.

## Establish the pattern

Identify the repeated failure, its triggers, and the requirement it violates.
Separate a real invariant from a context-dependent preference or one-off event.
Locate where the invalid state enters and which existing mechanism owns it.

## Choose the smallest effective safeguard

Prefer a mechanism close to that owner: a representation that excludes the
invalid state, boundary validation, a behavior test, an existing lint/check, or
a narrow shared helper. Choose based on what actually enforces the requirement
without duplicating another source of truth or prohibiting valid behavior.

A new framework, dependency, hook, or global policy is rarely the first step.
When judgment cannot be automated reliably, retain concise guidance with the
failure example instead of creating a noisy mechanical rule.

## Apply within scope and verify

Implement the safeguard only when the current request authorizes changes to
that area. Otherwise return a concrete proposal with its location, cost, and
verification method; do not auto-file an issue or modify another repository.

Show that the observed bad case is rejected and representative valid cases still
work. Use [prove-it-works](../prove-it-works/SKILL.md). A rule that passes without
detecting the recurring failure has not closed the loop.

Remove redundant instruction text only after the mechanism covers the same
requirement and editing that text is authorized. Preserve rationale, externally
imposed constraints, and guidance still needed for judgment. Do not delete
comments or rewrite skills simply because a structural fix exists.

Return the pattern, chosen mechanism, evidence, and remaining judgment calls.
Promote stable knowledge to the project's established documentation only when
appropriate; do not update user memory or global rules without a request.

## Source

Adapted from Lauren Tan's [pstack Encode Lessons in Structure](https://github.com/cursor/plugins/blob/12d587dfb20741cafc376c42c696c5f6e2a64487/pstack/skills/principle-encode-lessons-in-structure/SKILL.md).
Local changes: evidence of recurrence, local enforcement, scope-aware application,
and no automatic memory, issue, or instruction edits. See [LICENSE](LICENSE).
