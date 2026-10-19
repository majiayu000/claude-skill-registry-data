---
name: pstack-architect
description: "Compare concrete module and type designs for a nontrivial boundary or ownership change. Use for architectural design requests or changes where choosing the wrong data shape would cause rework."
license: MIT
metadata:
  upstream: https://github.com/cursor/plugins/tree/ccb5507cec1546dc88135c1139c811e6c59115ba/pstack/skills/architect
  upstream-commit: ccb5507cec1546dc88135c1139c811e6c59115ba
  adaptation: portable-chat-inherited
---

# Architect

Design from the caller's use and the system's invariants. Architectural design alone does not authorize implementation.

## Environment contract

Use the active chat model and its current reasoning settings. Delegate only when supported and authorized; omit model and effort overrides when omission inherits the chat settings. If the host cannot guarantee that inheritance, do the work in the current chat. Sequential passes are a fallback, not independent reviewers.

Use available file, search, terminal, browser, history, and connector tools. Follow the user's scope, authorization, repository instructions, and local resource controls. A skill invocation does not authorize publication, unrelated changes, or external messages.

## Ground

Trace the affected subsystem, its callers, existing boundaries, shared primitives, data ownership, and constraints. Inspect historical rationale when changing an established boundary. Reuse a design-system component before designing another one for an equivalent UI need.

## Sketch alternatives

For a consequential choice with multiple viable shapes, produce at least two structurally distinct candidates. Skip the bakeoff when requirements and existing patterns dictate one clear shape.

Keep sketches outside product source until implementation is authorized. Sketch the caller's usage first, then types, signatures, ownership, and lifecycle. Do not commit placeholder bodies or temporary broken code merely to satisfy the design phase.

Compare candidates on:

- Interface depth: a small public contract that hides meaningful complexity.
- Encapsulation: transport, storage, and framework details stay with their owner.
- One owner per mutable state and one source for repeated invariants.
- Clear domain boundaries rather than modules divided only by execution stages.
- Compatibility with actual external consumers and independent deployments.
- Reader effort, implementation cost, and real extension needs.

Parallel candidates may use inherited-model agents when authorized. Otherwise compare alternatives directly. Neither approach supplies multi-model diversity.

## Choose and follow through

State the preferred design, rejected alternatives, and the evidence that decided. Preserve API, behavior, and visual appearance of existing consumers unless a breaking change is authorized. Unknown business or product decisions remain open; continue independent authorized work.

If implementation is requested, fill in the chosen design and verify its observable contract. Repeated new casts, special cases, shared-writer locks, or caller coordination are evidence to revisit the design. Revise only within the authorized scope, preserving the user's work.

## Deliver

A concrete usage/type sketch or module map, rationale, compatibility implications, remaining decisions, and verification plan. Use an existing architecture skill when it already expresses the task; this procedure does not require another installed skill.
