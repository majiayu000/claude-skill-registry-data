---
name: write-spec
description: Draft testable requirements and boundaries for a proposed change. Use to create a specification; not to review one or verify code against it.
---

# Write a Specification

Draft a compact, implementable contract before a significant change. Adapted from Addy Osmani's `spec-driven-development` workflow; see the bundled license and repository third-party notice.

## Route precisely

- Use when the user requests a specification, PRD, or explicit requirements for a proposed feature or substantial change.
- Use `review-spec` to judge an existing draft, `api-and-interface-design` when the primary deliverable is one interface contract, `planning-and-task-breakdown` to order implementation work, and `verify-impl` to compare finished code with authoritative requirements.
- Do not require a specification for a mechanical edit. Do not start implementation merely because the spec is written.

## Establish authority and scope

Read the user's requested outcome, repository instructions, related contracts, existing behavior, and any binding decision records. Separate confirmed facts from proposed behavior and assumptions. Ask only for information that determines a material product or safety choice; otherwise make a clearly labeled draft assumption.

## Draft the contract

1. State the problem, intended users or consumers, objective, and scope. Identify what behavior is explicitly excluded when that prevents ambiguity.
2. Break a broad requirement into independently testable capabilities. For each, describe inputs, outputs, state changes, defaults, failure behavior, and the owner of the data or side effect where relevant.
3. Specify public interfaces, compatibility, authorization, trust boundaries, migration, concurrency, and recovery only to the level needed for this change. Do not invent a mandatory technology stack or file layout.
4. Give each material obligation an observable acceptance criterion. Include examples and edge cases that resolve otherwise plausible divergent implementations.
5. Record unresolved decisions with their consequence and the evidence or owner needed to settle them. Do not disguise an open decision as an accepted requirement.

## Deliver and check

Return the draft in the requested format or in chat. Check it for contradictions, unstated dependencies, untestable terms, and unsupported claims about current code. State what is confirmed, proposed, and unknown. A completed spec is ready for `review-spec` or planning; it does not establish implementation correctness.
