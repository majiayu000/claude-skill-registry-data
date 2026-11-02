---
name: distributed-outbox-inbox
description: Evaluate transactional outbox/inbox patterns for reliable event publication and duplicate-safe consumption across service boundaries.
---

# Distributed Outbox Inbox

## Goal

Avoid lost events when database commits and message-broker publication cannot share one atomic transaction.

## Inputs to inspect

Database mutation path, broker/topic, consumer behavior, event IDs, transaction model, and delivery guarantees.

## Workflow

1. Trace the business transaction and identify the exact gap between database commit and event publication or between delivery and consumer commit.
2. Define an outbox record written in the same transaction as business data, then specify polling/CDC publication and retry semantics.
3. Design the consumer inbox or deduplication ledger so repeated deliveries do not repeat irreversible work.
4. Specify ordering keys, poison-message handling, retention/cleanup, and behavior when publication succeeds but acknowledgment is lost.
5. Inject crashes before commit, after commit, after publish, during consume, and before acknowledgment; verify recovery and business invariants.

## Validation checklist

- [ ] Business state and outbox creation are atomic under the chosen database transaction.
- [ ] Consumers are duplicate-safe for the required side effects.
- [ ] Ordering is guaranteed only where specified and has explicit partition/key semantics.
- [ ] Retries, poison events, and dead-letter handling are observable and recoverable.
- [ ] The design avoids claims of global exactly-once delivery unsupported by the components.

## Required output

Produce a transaction-boundary diagram, outbox/inbox schema, retry/replay rules, crash matrix, and operational monitoring plan.

## Boundaries and failure handling

Do not publish directly before the transaction commits and assume a later rollback retracts the event; do not delete unprocessed outbox rows during cleanup.

When repository evidence is incomplete, label the gap explicitly and request only the missing information that changes the decision. Do not claim commands, benchmarks, tests, or runtime checks passed unless their outputs were observed.
