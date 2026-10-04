---
name: backend-systems-guidance
description: Canonical overlay for non-trivial server-side networked implementation and review involving multi-layer architecture, data access, reliability, trust boundaries, or deeper testing; use `backend-guidance` for thin routine handlers. Compose with matching implementation guidance for APIs, queues, repositories, transactions, or auth-sensitive flows.
---

# Backend Systems Guidance

This is a composable overlay, not a standalone workflow.
Use alongside the repo's implementation skill when the change touches backend
code.

Choose activity independently from backend depth. A review request is read-only
unless the user also asks for remediation; use the architecture and reliability
rules as inspection criteria and report findings instead of changing code.

This is the canonical backend overlay in this repo.
It extends the thin baseline `backend-guidance` overlay with stronger guidance
for non-trivial service boundaries, repositories, reliability, and trust
boundaries.

Prefer it over `backend-guidance` when the task includes new endpoints or
consumers, multi-layer refactors, repository or transaction work, auth or
trust-boundary logic, or backend review that needs explicit testing and
reliability checks.

Use the bundled references only when needed:

- [references/trigger-evals.md](references/trigger-evals.md) for lightweight
  prompt checks when revising the trigger or scope

## When to use

- the repo has server-side networked code such as HTTP handlers, gRPC methods,
  webhooks, queue consumers, or message producers
- the task adds or reshapes routes, controllers, services, repositories,
  middleware, or request-processing boundaries
- the task changes auth, authorization, validation, idempotency, retries,
  external requests, caching, or observability
- the task needs backend review beyond basic handler thinness, especially for
  security, data access, or missing tests

## Not for

- HTTP client code, CLI tooling, offline batch scripts, or data pipelines with
  no request or consumer boundary
- frontend-only work
- threat modeling or security audit work where `security` should be the primary
  workflow skill

Do not fold infrastructure deployment workflows, outbound-client-only guidance,
or full security-audit checklists into this skill. Keep this overlay centered
on backend request and consumer systems plus their immediate reliability and
trust boundaries.

## Core workflow

1. Read the touched backend files and map the request or consumer path end to
   end: boundary, service logic, data access, external calls, and state
   changes.
2. Pick the activity and depth before changing code:
   - implementation when the user asks to add, change, refactor, harden, or
     remediate backend behavior
   - review when the user asks for findings or assessment; inspect the remaining
     steps without editing or requiring findings to be fixed
   - baseline backend change when the work is mostly a thin handler or small
     service fix
   - service-boundary change when responsibilities, data access, or dependency
     direction may need to move
   - reliability-hardening or review mode when the main risk is missing tests,
     auth gaps, retries, observability, or unsafe failure handling
3. Keep the boundary thin: decode input, authenticate, validate transport shape,
   call the shared policy/service path, map transport errors, and serialize
   output. Authorization must cover every entrypoint; business decisions belong
   in service code that can run without the transport layer.
4. Place persistence and external integrations deliberately:
   - repositories or data adapters own query shape, batching, and transaction
     details when that improves clarity or testing
   - services coordinate business rules, idempotency, retries, and side-effect
     ordering
   - handlers and controllers do not reach directly into ORM or network clients
     unless the change is truly trivial and stays trivial
5. Place trust and validation concerns in their owning layers:
   - decode, authenticate, and validate the external transport shape at ingress
   - enforce authorization in the earliest shared policy layer traversed by
     every relevant entrypoint, before business actions
   - enforce business invariants in service or domain code and persistence
     constraints in the data layer
   - set timeouts, retry rules, and destination allowlists for outbound calls
   - use structured logging, correlation identifiers, and explicit error
     mapping for observable failure paths
6. Choose the smallest test set that proves the change:
   - unit tests for service logic and decision branches
   - integration tests for handlers, consumers, repositories, and transaction
     behavior
   - auth and permission tests for protected flows
   - contract or schema tests when the change alters external API or event
     shapes
   - load or concurrency tests only for changed hotspots, queue throughput, or
     latency-sensitive paths
7. Review the result for boundary leaks, unsafe defaults, data-access
   inefficiency, and missing verification before finishing.

## Decision rules

- Start with `backend-guidance` for ordinary backend edits. Use this overlay
  when the task needs stronger design pressure, harder review, or explicit
  backend quality gates.
- Keep handlers thin in responsibility, not by literal line count. If a
  handler or consumer owns business decisions, retries, transaction branching,
  or query orchestration, extract inward.
- Keep business logic transport-free. If testing a rule requires booting HTTP,
  gRPC, or queue infrastructure, the logic is in the wrong place.
- Add a repository or data-access interface when it reduces duplication,
  isolates non-trivial queries, helps transaction composition, or makes tests
  materially simpler. Do not add one for single-call trivial CRUD.
- Validate transport shape once at ingress, then pass typed data inward. Keep
  authorization, domain invariants, and persistence constraints in their
  owning layers; avoid duplicate checks only when they protect the same
  contract and boundary.
- Treat retries as a design choice, not a default. Only retry idempotent or
  explicitly deduplicated work, and pair retries with deadlines or backoff.
- Use idempotency keys or duplicate-detection for retried creates, webhook
  handlers, and queue consumers that can be re-delivered.
- Every outbound request needs a timeout and failure policy. For user-controlled
  destinations, apply allowlists or equivalent SSRF protections.
- Keep error handling explicit: domain code returns or throws domain-level
  failures; boundary code maps them to HTTP, gRPC, queue, or job semantics.
- Measure before adding caching. Cache only stable read paths with clear
  invalidation or bounded staleness.

## Validation

For implementation, a backend change is done when, in addition to the base
implementation skill's validation:

- handlers or consumers stay as boundary glue and delegate business decisions to
  testable service code
- data access and external I/O live behind clear seams when the change is
  non-trivial
- external transport shape, authentication, and transport-specific error
  mapping stay at the edge; shared authorization and domain invariants cannot
  be bypassed through another entrypoint
- retries, idempotency, timeouts, and failure handling are explicit where the
  change can duplicate work or call remote systems
- tests cover the changed behavior at the correct level, including integration
  coverage for boundary behavior and permission or failure cases when relevant
- new high-risk paths emit enough evidence to debug production behavior

For review, completion means prioritized findings map the affected request or
consumer path, cite evidence, explain likely impact, and identify unverified
behavior. Unfixed findings do not make the review incomplete.
