---
name: clarila-backend
description: "Investigate and implement a scoped backend/API/data-path issue in its verified worktree. Does not authorize production migrations, deploys or unrelated infrastructure changes."
---

# Repair or implement backend behavior

Read the [shared workflow contract](../clarila/references/contract.md) before substantive work. This skill is part of the locally installed Clarila suite. Its source is in `~/Developer/skills`; resolve sibling skills relative to this directory.

## Procedure

1. Read the issue, repository instructions, existing ownership and relevant API/schema contracts. Resolve the correct worktree.
2. Reproduce the request or data-path failure with safe fixtures. Inspect callers, validation, authorization, persistence and error handling.
3. Plan and implement the smallest supported change. Make migrations reversible and separate their preparation from authorized execution.
4. Run relevant unit/integration/API checks including negative and unaffected cases. Use clarila-test for focused strategy, regression writing or test maintenance; prove relevant request/response, authorization, persistence and side-effect contracts with controlled fixtures. For a regression, demonstrate failure on the defective baseline when feasible and report baseline setup failures separately. Never use customer payloads as shared evidence.
5. Hand off exact source, request/response behavior, retained redacted evidence and independent verification/review needs.

## Check the whole request contract

Trace the failing public request through authorization, validation, persistence and its response. For changes that can be retried or run concurrently, define the operation identity and transaction boundary. Exercise the relevant replay, failed-write and existing-record cases with controlled data. Check the caller's observable response and resulting durable state.

Use database-specific guidance only for the database and operation actually involved. Retain the request fixture, expected status/body and state assertion beside the observed result. A schema or data change needs a compatibility and recovery decision for records created before the change.

For duplicate writes, concurrent requests, legacy records or provider effects, read [persistence decisions](references/persistence.md). Resolve `database-postgres` in the [expert catalog](../clarila/references/expertise.md) only when the actual datastore is PostgreSQL; other datastores need their own installed-version evidence.

## Synchronization and handoff

Resolve the same issue/workspace/session association before substantive work, including direct invocation. Read and update the private handoff described in the shared contract using available native file tools. Record the actual stage, source, findings, evidence, outcome and next action. If no native session identity is available, retain an unbound record.

## Deliverable

Return cause, change, API/data acceptance evidence and deployment or migration limits.

Load only the relevant specialist from the [catalog](../clarila/references/catalog.md). Missing tools change the available evidence, never its meaning.
