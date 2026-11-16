---
name: spec-writing
description: Turn an agreed conversation or request into a testable product or engineering specification. Use when a durable spec is needed before implementation or ticketing.
---

# Specification Writing

Synthesize the agreed goal into a specification that engineers and reviewers can verify. Do not invent decisions that were not made.

Include:

- **Problem and outcome:** who experiences the problem and what should improve.
- **Scope:** required behavior, explicit non-goals, and supported environments.
- **User flows and contracts:** inputs, outputs, state transitions, errors, permissions, and observable behavior.
- **Constraints:** compatibility, performance, privacy, security, accessibility, and operational requirements where relevant.
- **Acceptance criteria:** concrete, observable conditions, including important edge cases.
- **Open decisions:** assumptions, unresolved questions, and risks, each clearly labeled.

Keep implementation details out unless they are necessary constraints or agreed design decisions. Link claims to source files or discussion context when available. Ask for review of material assumptions; do not publish to an issue tracker or external system without authorization.
