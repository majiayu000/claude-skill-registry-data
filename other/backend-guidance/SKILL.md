---
name: backend-guidance
description: Baseline overlay for routine thin HTTP, gRPC, or message-consumer implementation and review; use `backend-systems-guidance` for multi-layer, data-access, transaction, reliability, or trust-boundary work. Compose with matching implementation guidance. Not for outbound-client-only or security-audit tasks.
---

# Backend Guidance

This is a composable overlay, not a standalone workflow.
Use alongside the matching principle skill (for example,
`coding-guidance-cpp`) when the change touches backend code. Add
`project-core-dev` only when repository-specific completion checks still need
to be discovered or reported.

Choose the activity before applying the rules below:

- for implementation, make only the requested backend changes and validate them
- for review, inspect and report prioritized findings with evidence; do not
  edit files or require findings to be fixed unless the user also asks for
  remediation

Use this as the thin default backend overlay for ordinary backend work.
If the task includes service-boundary refactors, repository or transaction work,
queue or webhook reliability, stronger testing expectations, or explicit
trust-boundary hardening, prefer `backend-systems-guidance`.

Routing examples:

- thin route handler that delegates to existing service logic -> use this skill
- small message consumer bug fix with no retry or persistence redesign -> use
  this skill
- new endpoint with authz, repository, transaction, retry, or observability
  changes -> use `backend-systems-guidance`
- security audit of an endpoint or tenant membership/authorization boundary ->
  use `security` first; add `security-identity-access` when identity, session,
  or tenant authorization is central, and add the backend overlay only for
  implementation structure

## When to use

The repo has server-side networked code: HTTP route handlers, gRPC service
methods, message/event consumers, or similar request-processing pipelines.

## Not for

HTTP client code, CLI tools that make outbound requests, batch processors, or
offline data pipelines. These do not have the handler/service/boundary shape
this skill addresses.

## Rules

- Keep handlers thin in responsibility, not by literal line count — parse
  input, call a service function, map transport concerns, serialize output. If
  a handler starts owning business decisions, extract that logic into a service
  or core module.
- Keep business logic testable without transport — no HTTP context, no gRPC
  metadata leaking into domain functions.
- Isolate data access behind an interface when it simplifies testing. Do not
  add an abstraction layer when the data access is trivial or test-only.
- Decode, normalize, and validate the external transport shape at the untrusted
  boundary before it reaches business logic. Do not confuse that check with
  domain invariants that the service or domain owner must enforce.
- Keep transport-only concerns at the edge: request decoding, authentication,
  and transport-specific error mapping. Enforce authorization in the earliest
  shared policy layer that every relevant entrypoint traverses; an edge-only
  authorization check is sufficient only when no other entrypoint can bypass
  it.
- Keep business invariants in service or domain code and persistence invariants
  in the data layer. Avoid duplicate checks that enforce the same contract, but
  do not remove a check merely because another layer validates a different
  concern.
- Use dependency injection where it makes tests simpler — not as a default
  architectural pattern.

## Decision Heuristics

- **Handler responsibility:** extract business decisions from transport glue
  when they obscure ownership; line count alone is not an architectural defect.
- **Test seam:** if testing a business rule requires transport infrastructure,
  move that rule inward. Tests of routing, serialization, or middleware may
  correctly need a real transport boundary.
- **Validation placement:** validate each concern at its owning boundary:
  transport shape at ingress, shared authorization before the action, domain
  invariants in the domain owner, and storage constraints in persistence. If
  checks are scattered, identify whether they duplicate one contract or protect
  different boundaries before consolidating them.

## Validation

For implementation, a backend change is done when, in addition to the base
implementation skill's validation:

- handlers delegate to testable service functions
- business logic tests run without transport dependencies
- external transport shape is validated at ingress, shared authorization cannot
  be bypassed through another entrypoint, and domain invariants remain in their
  owning layer
- transport-specific error handling stays at the boundary instead of leaking
  into domain logic

For review, completion means prioritized findings name the affected request or
consumer path, supporting evidence, likely consequence, and validation gap.
Open findings do not make the review incomplete.
