---
name: architect
description: Design caller usage, data shapes, interfaces, and module responsibilities before implementing a substantial change. Use when the shape is uncertain; implementation follows the original request's scope.
license: MIT
---

# Architect

Produce a design that callers can use and maintainers can verify. Determine
whether the original request authorizes design only or also implementation.

## Ground the design

Read relevant repository instructions, contracts, CONTEXT.md, and ADRs. Reuse a
current traced model when one exists; otherwise use [how](../how/SKILL.md).
Use [why](../why/SKILL.md) when changing existing ownership or constraints whose
rationale is unclear.

Read the available `codebase-design` skill for shared design vocabulary and
criteria. If it is unavailable, favor a small interface that hides substantial
behavior and can be tested through that interface. Do not install a dependency
to obtain guidance.

Respect decisions already settled with the user. Use `design-preflight` only
when explicitly requested. Otherwise ask only about unresolved product choices
or hard-to-change constraints that inspection cannot settle.

## Shape the contract

Write the caller's usage first. Derive:

- the domain state and transitions, including invalid states to exclude;
- inputs, outputs, failure semantics, and public signatures;
- module responsibilities, state ownership, and side effects;
- testable observable behavior, compatibility obligations, and migration needs.

Keep sketches in the response or a temporary artifact unless a durable document
or source scaffold is requested. Avoid adding placeholder production code to
express a design-only answer.

Compare alternatives directly when there is a real choice. Use
[arena](../arena/SKILL.md) only when the user explicitly invokes it for
independent attempts. A design request or this reference alone does not
activate arena. A function boundary alone does not justify fan-out.
For an obvious local extension, one grounded design with its rationale suffices.

Evaluate candidates against the user's requirements, interface depth, ownership,
failure behavior, verification cost, and migration burden. Choose a coherent
shape rather than combining incompatible designs.

## Hand off and revise

Return the usage sketch, chosen shape, significant rejected alternatives,
constraints, and how the behavior will be verified. Mark assumptions and
unresolved decisions.

For a design-only request, stop with the design. For an implementation request,
continue within that authorization using the agreed shape; this skill does not
authorize commits, publishing, dependency changes, or broader rewrites.

During implementation, repeated escape hatches, ownership leaks, or incompatible
state assumptions are evidence that the sketch needs revision. Revisit the
specific assumption before adding another workaround. Surface consequential
changes without reopening settled minor choices.

## Source

Adapted from Lauren Tan's [pstack architect](https://github.com/cursor/plugins/blob/12d587dfb20741cafc376c42c696c5f6e2a64487/pstack/skills/architect/SKILL.md).
Local changes: existing design vocabulary, conditional comparisons, and an
explicit boundary between design and authorized implementation. See [LICENSE](LICENSE).
