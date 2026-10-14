---
name: plan-mode-to-spec
description: Write a technical specification for a defined product change or system behavior. Use when the user needs interfaces, data flow, edge cases, migration, and verification made concrete before implementation.
license: MIT
---

# To Spec

Turn an agreed behavior into an **implementation contract** another engineer can build and verify.

1. Read the requirement and relevant code, interfaces, tests, architecture notes, and platform documentation. Record current behavior and constraints with source references. Ask about a missing decision only if answers would materially change the design.
2. Define the intended behavior and its boundaries. Specify the components involved, interface and data contracts, state transitions, error handling, permissions, compatibility, and migration or rollout where applicable. Distinguish existing behavior from proposed behavior.
3. Make significant choices explicit: design, credible alternative, reason, and risk. Describe testable behavior at the highest useful seam, including normal, failure, and recovery cases. Trace each requirement to its design and verification.
4. Review the spec for gaps, conflicts with the existing system, invented APIs, and requirements with no verification path. Label assumptions instead of presenting them as decisions.

Deliver concrete contracts, not a file-by-file task list. Include paths or signatures only when verified and useful. Do not change code or create tracker items unless requested.

Record this output in `docs/plans/` per the [doc system](../references/doc-system.md), delegating the write to a subagent.
