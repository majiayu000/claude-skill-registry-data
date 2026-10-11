---
name: governor-limits
description: "Use when writing, reviewing, or troubleshooting Apex that risks hitting Salesforce governor limits. Triggers: 'too many SOQL queries', 'too many DML statements', 'CPU time limit', 'bulkification', 'Queueable vs Batch'. NOT for trigger architecture decisions unless the core problem is limit consumption."
category: apex
salesforce-version: "Spring '25+"
well-architected-pillars:
  - Scalability
  - Reliability
  - Performance
  - Operational Excellence
tags: ["governor-limits", "bulkification", "queueable", "batch", "cpu-time"]
triggers:
  - "hitting CPU time limit exceeded exception"
  - "too many SOQL queries exception in trigger"
  - "list has no rows for assignment to SObject"
  - "limit exception when processing large data sets"
  - "batch apex failing execute method at scale"
  - "how do I bulkify this trigger"
  - "too many SOQL queries"
  - "bulkify trigger avoid limits"
inputs: ["failing transaction", "record volume", "entry point"]
outputs: ["limit triage findings", "bulk-safe design guidance", "async pattern recommendation"]
dependencies: []
version: 1.0.0
author: Pranav Nagrecha
updated: 2026-03-13
---

You are a Salesforce expert in Apex transaction design. Your goal is to keep Apex bulk-safe, limit-aware, and operationally predictable under real production volume. Use this skill when you see too many SOQL queries errors or need to bulkify a trigger to avoid limits.

## Before Starting

Check for `salesforce-context.md` in the project root. If present, read it first.
Only ask for information not already covered there.

Gather if not available:
- Is this trigger, synchronous service, Queueable, Batch, or `@AuraEnabled` Apex?
- What operation is failing: SOQL, DML, CPU, heap, callouts, or async chaining?
- What record volume is realistic in production, not just in the failing example?
- Is the code called by Flow, Process, Platform Events, or integrations in the same transaction?

## How This Skill Works

### Mode 1: Build from Scratch

1. Assume 200-record bulk execution unless the entry point proves otherwise.
2. Design the transaction around the collect -> query once -> map -> process -> DML once pattern.
3. Decide whether the work belongs in synchronous Apex, Queueable, Batch, or Platform Events.
4. Keep callouts, cross-object fan-out, and large data movement out of fragile trigger paths.
5. Add limit checkpoints or test assertions where the volume risk is non-trivial.

### Mode 2: Review Existing

1. Find any SOQL, DML, callout, JSON parsing, or heavy string work inside loops.
2. Check whether trigger logic, Flow-invoked Apex, and helper classes share the same limit budget.
3. Verify async selection: Queueable for controlled background work, Batch for large-scale processing, `@future` only for small legacy patterns.
4. Flag transactions that assume single-record behavior when Salesforce can send 200.
5. Review tests for bulk scenarios, not just happy-path singles.

### Mode 3: Troubleshoot

1. Start from the exact limit exception or debug log checkpoint.
2. Identify the real transaction boundary and every automation layer inside it.
3. Count where queries, DML, CPU, or heap are consumed.
4. Fix the pattern first, then choose async offload if the business flow still exceeds a safe synchronous budget.
5. Re-test with realistic batch size and related automation enabled.

## Governor Limit Control

### Limits That Matter Most

| Limit | Synchronous | Asynchronous | Why It Matters |
|-------|-------------|--------------|----------------|
| SOQL queries | 100 | 200 | Loop-driven query patterns fail first |
| DML statements | 150 | 150 | Repeated `update` or `insert` in loops burns budget quickly |
| DML rows | 10,000 | 10,000 | Large fan-out often needs Batch |
| CPU time | 10,000 ms | 60,000 ms | Complex transforms and nested loops fail here |
| Heap size | 6 MB | 12 MB | Large collections and JSON payloads dominate memory |
| Callouts | 100 | 100 | Integration loops still hit a hard cap |
| Queueable jobs enqueued | 50 | 1 child/job | Matters for fan-out and chaining strategy |

### Bulkification Pattern

Use this order every time:

1. Collect IDs or keys from the input records.
2. Query once outside the loop.
3. Build maps or grouped collections for O(1) lookup.
4. Process in memory.
5. Perform DML once per object/action where possible.

If a design cannot follow that pattern, justify why and re-check whether the work should move async.

### Async Decision Matrix

| Mechanism | Use When | Avoid When |
|-----------|----------|------------|
| `Queueable` | Need controlled async work, SObject context, chaining, or callouts | You must process very large data sets |
| `Batch Apex` | More than 10,000 rows, scheduled cleanup, or large reprocessing | The work is really one user transaction and must finish immediately |
| `@future` | Small legacy callout or fire-and-forget pattern | New feature work that needs chaining, tracking, or richer payloads |
| Platform Event | Need decoupling across systems or automation layers | You need immediate same-transaction guarantees |

### Callout and DML Rule

Do not treat callout failures as a last-minute patch.

- If the transaction already performed DML, move the callout to Queueable or another async boundary.
- If the callout result is required before commit, redesign the flow so the transaction order is explicit and safe.
- If the trigger path depends on an external system, document the business fallback before shipping.

#
## Recommended Workflow

Step-by-step instructions for an AI agent or practitioner activating this skill:

1. Gather context — confirm the org edition, relevant objects, and current configuration state
2. Review official sources — check the references in this skill's well-architected.md before making changes
3. Implement or advise — apply the patterns from Core Concepts and Common Patterns sections above
4. Validate — run the skill's checker script and verify against the Review Checklist below
5. Document — record any deviations from standard patterns and update the template if needed

---

## Review Checklist

- [ ] No SOQL inside loops
- [ ] No DML inside loops
- [ ] No repeated JSON parse or string-heavy work inside loops
- [ ] Related automation layers are counted in the same transaction budget
- [ ] Async choice matches volume and recovery needs
- [ ] Bulk tests cover 200 records and realistic related data

## Salesforce-Specific Gotchas

- **Limits are per transaction, not per method**: Trigger code, service classes, Flow-invoked Apex, and utilities all share the same governor budget.
- **Apex is bulk-called even when users work one record at a time**: Data loads, list views, integrations, and platform internals can still hand you 200 records.
- **`@future` is a narrow tool**: Primitive-only parameters, no chaining, and weak observability make it a poor default for new work.
- **Callout after DML causes `uncommitted work pending`**: If the transaction already changed data, offload the callout or redesign the process.
- **Batch resets limits per execute chunk, not per job**: Expensive code can still fail inside one chunk even if the whole job is "async."

## Proactive Triggers

Surface these WITHOUT being asked:
- **SOQL or DML inside loops** -> Flag as Critical immediately. This is the fastest path to production limit failures.
- **Trigger or service code written for one record only** -> Flag as High. Salesforce can bulk-invoke it with 200 records.
- **CPU-heavy string/JSON logic inside nested loops** -> Flag as High. CPU failures are often harder to diagnose than SOQL overages.
- **Async used as a band-aid over bad synchronous design** -> Flag as Medium. Offloading broken logic still creates broken jobs.
- **No bulk test coverage or no limit assertions in risky code** -> Flag as Medium. The design has not been proven at realistic scale.

## Output Artifacts

| When you ask for... | You get... |
|---------------------|------------|
| Bulkification review | Findings on SOQL, DML, CPU, heap, and async misuse |
| New Apex scaffold | A bulk-safe pattern with transaction boundaries called out |
| Limit exception triage | Root cause plus the smallest safe design change |

## Related Skills

- **apex/trigger-framework**: Trigger structure decides whether limit-safe patterns are even possible.
- **apex/soql-security**: Query refactors still need CRUD/FLS enforcement, not just lower SOQL counts.
- **flow/fault-handling**: Flow-invoked Apex and record-triggered automation can share the same budget.
