---
name: agent-memory-write-policy
description: Define which findings an agent may persist to memory, with provenance, sensitivity filtering, staleness, and deletion rules.
---

# Agent Memory Write Policy

## Goal

Make persistent memory useful and trustworthy without storing secrets, unverified claims, or temporary noise.

## Inputs to inspect

Memory store schema, agent workflow, user preferences, repository facts, sensitivity rules, and retrieval behavior.

## Workflow

1. Classify candidate memory as stable preference, verified project fact, temporary task state, sensitive data, or unverified hypothesis.
2. Persist only items with clear future utility and supporting source/evidence; include scope, timestamp/version, confidence, and owner where appropriate.
3. Reject credentials, account identifiers, private personal details, and information outside the approved retention policy.
4. Define freshness checks and invalidation when branches, versions, project decisions, or user instructions change.
5. Test retrieval for stale facts, conflicting updates, accidental secret inclusion, and deletion of superseded/withdrawn memories.

## Validation checklist

- [ ] Each durable fact has provenance and a way to assess staleness.
- [ ] Sensitive data is filtered before any write, not only at retrieval time.
- [ ] Temporary task details expire or remain in task artifacts instead of becoming permanent memory.
- [ ] Conflicting memories are reconciled using an explicit policy.
- [ ] Users/operators can inspect and delete records according to the supported controls.

## Required output

Produce a memory eligibility policy, schema/provenance rules, redaction filters, expiration strategy, and adversarial test cases.

## Boundaries and failure handling

Do not persist secrets or speculative inferences; do not silently treat a remembered claim as current truth without checking its version.

When repository evidence is incomplete, label the gap explicitly and request only the missing information that changes the decision. Do not claim commands, benchmarks, tests, or runtime checks passed unless their outputs were observed.
