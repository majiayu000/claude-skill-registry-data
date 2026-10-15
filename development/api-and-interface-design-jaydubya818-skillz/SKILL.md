---
name: api-and-interface-design
description: "Design API contracts, compatibility, and duplicate-safe mutations."
license: MIT
metadata:
  author: Addy Osmani and Skillz contributors
  source: addyosmani/agent-skills
  source-commit: 1401c8b8030e023baeebb31781a6653fe8e93026
  adaptation: curated-rewrite
  owner: software-factory
  risk: high
  capabilities: addyosmani,api-and-interface-design
---

# API and interface design

Define the contract before implementing or changing a public API. Start with
existing callers, schema conventions, authorization rules, and retry behavior.
A module-local refactor needs only the contract that crosses its boundary.

## Work from consumer behavior

1. Identify callers and independently deployed versions. Record required
   behavior, including ordering, nullability, defaults, errors, and observable
   quirks. A type-compatible change can still break a consumer.
2. Specify inputs, outputs, validation, resource ownership, and failure cases
   using the repository's schema or interface format. Separate caller input
   from server-owned fields. Do not accept roles, prices, ownership, or state
   transitions just because the request matches a type.
3. Validate untrusted data where it enters, including provider responses and
   persisted data whose invariants are not guaranteed. Typed internal calls
   do not need repeated shape validation; business invariants still apply.
4. Define stable machine-readable errors and appropriate transport semantics.
   Keep internal details out of public responses. Follow existing conventions
   for validation errors and access-denied versus not-found behavior.
5. Bound list queries. Specify a maximum page size, stable ordering with a
   tie-breaker, cursor or offset behavior, and what concurrent writes do to
   pagination. Do not promise a consistent snapshot unless it exists.
6. Specify partial-update behavior for omitted values, explicit nulls, empty
   collections, and concurrent edits. Use version checks or transactions where
   stale writes could overwrite another actor's work.
7. Prefer compatible extensions, but test real consumers. Optional fields and
   new enum values can break strict decoders. Existing public versioning and
   migration commitments take precedence over a preference for one version.

## State changes and retries

For operations with side effects, read
[retry and idempotency rules](references/idempotency.md). Apply these when
implementing payments, provisioning, webhook processing, or replayable jobs.
An accepted idempotency header alone does not make retrying safe.

Document which failures are retryable, who retries, the bounded retry policy,
and how callers discover an operation's status after a lost response. Payment
amounts need an explicit currency and representation, such as integer minor
units with currency-specific precision. Do not use floating-point arithmetic
for ledger values or trust client-supplied totals.

## Verify the contract

Exercise the real boundary with representative consumers. Cover malformed
inputs, unauthorized and cross-tenant access, missing resources, pagination
edges, concurrent updates, and duplicate delivery where applicable. Verify
response bodies as well as status codes. Keep contract documentation next to
the implementation and identify any consumers that could not be checked.

Return the contract changes, compatibility evidence, and unresolved decisions.
Designing an API does not authorize publishing it or migrating live consumers.
