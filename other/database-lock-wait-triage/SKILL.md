---
name: database-lock-wait-triage
description: "Use when database sessions are blocked by locks and a wait chain is needed to identify the responsible transaction; not for generic slow-query or index analysis."
---

# Database Lock Wait Triage

## Purpose

Identify the blocking transaction and provide a low-risk response to lock contention.

## Required inputs

Database engine/version, lock and activity snapshots, transaction ages, affected queries, deployment timeline, and read-only diagnostic permissions.

## Workflow

1. Capture a timestamped snapshot of blocked sessions, lock modes, wait events, transaction age, and query fingerprints using engine-supported read-only diagnostics.
2. Build the blocking graph from waiting session to blocker, including chains and idle-in-transaction sessions.
3. Correlate the blocker with application request, deployment, batch job, or migration while preserving query privacy.
4. Recommend a response ordered by risk: let a short transaction finish, pause the responsible workload, request owner intervention, or terminate a confirmed harmful session with explicit approval.

## Verification checklist

- [ ] The report distinguishes blocker from downstream waiters.
- [ ] Transaction age, lock mode, and captured timestamp accompany the diagnosis.
- [ ] The suspected blocker is supported by evidence rather than query text alone.
- [ ] Any terminate/cancel recommendation states expected impact and requires authorized review.

## Required output

A lock-wait graph, evidence snapshot, likely cause, immediate mitigation options, and prevention recommendations.

## Boundaries and failure handling

Start with read-only queries. Never kill a database session automatically just because it is blocking others; account for transaction rollback cost.

When required evidence, permissions, or environment details are unavailable, stop at the supported analysis, record the missing prerequisite, and do not report an unexecuted validation as passing.

## Trigger examples

- **Positive:** A deployment stalls because many requests wait on one open transaction.
- **Negative:** High CPU caused by an inefficient query plan without lock waits.
