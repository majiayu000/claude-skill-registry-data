---
name: database-engine-development
description: "Use when implementing a database engine, storage layer, query executor, or transaction feature to define the data model and durability guarantees first, then build a small persistent slice with explicit recovery and resource limits. Trigger for page storage, indexing, query planning, transactions, logging, or database compatibility work."
---

# Database Engine Development

## Overview

This skill applies when implementing a database engine, storage layer, query executor, or transaction feature. Its intended outcome is to define the data model and durability guarantees first, then build a small persistent slice with explicit recovery and resource limits.

## When to Use

### Preserved source section: When to Use

Use for a database implementation or a substantial low-level storage/query subsystem. State whether the goal is an educational engine, embedded store, or compatible production component; the required guarantees differ.

## Scope

**Does:** Follow the task boundary stated under When to Use and Instructions.

**Does not:** See the preserved source boundaries below and under Stop Conditions.

### Source boundary statements from: Safety and Acceptance

Never experiment against production data. Use disposable test directories and preserve backups before migration testing. Accept a feature only when stated durability and transaction properties are demonstrated by repeatable tests, and when corrupted or unsupported formats fail safely rather than being silently reinterpreted.

## Inputs

**Required:** See the preserved source input guidance below.

**Optional:** Not specified in source skill.

**Prerequisites:** Not specified in source skill.

### Preserved source section: Inputs

- Record and query model, expected workload, data sizes, and consistency requirements.
- Durability, isolation, crash-recovery, concurrency, and compatibility expectations.
- Storage format, supported platforms, test harness, and benchmark baseline.

## Instructions

### Preserved source section: Procedure

1. **Specify invariants.** Define key/value or relational semantics, ordering, null behavior, transaction boundaries, and what a successful write promises after a crash.
2. **Build a minimal storage path.** Implement encode, write, reopen, and read for a tiny dataset. Validate checksums, lengths, version tags, and corruption handling before adding complex indexes.
3. **Add query and index layers separately.** Compare index results with a simple reference scan. Make plans observable and preserve a correctness path when an optimization is unavailable.
4. **Implement transactions deliberately.** Choose a documented logging or copy-on-write approach, define atomicity and isolation scope, and test partial writes, process termination, and recovery.
5. **Control concurrency and resources.** Specify locking, snapshot behavior, page-cache limits, query limits, and behavior under disk-full or memory pressure.
6. **Test failure, not just throughput.** Use deterministic fixtures, property tests for serialization, restart tests, fault injection where safe, and benchmarks with recorded data and environment.
7. **Version the format.** Plan upgrades, compatibility checks, and backup/restore before changing durable structures.

## Decision Rules

The following source conditional guidance is preserved verbatim; no unstated action is inferred.

### Source conditional guidance from: Procedure

3. **Add query and index layers separately.** Compare index results with a simple reference scan. Make plans observable and preserve a correctness path when an optimization is unavailable.

### Source conditional guidance from: Safety and Acceptance

Never experiment against production data. Use disposable test directories and preserve backups before migration testing. Accept a feature only when stated durability and transaction properties are demonstrated by repeatable tests, and when corrupted or unsupported formats fail safely rather than being silently reinterpreted.

## Output Format

Not specified in source skill.

## Validation Checklist

- [ ] Verify the source-defined success criteria above.

## Edge Cases and Recovery

### Source edge/failure guidance from: Inputs

- Durability, isolation, crash-recovery, concurrency, and compatibility expectations.

### Source edge/failure guidance from: Procedure

4. **Implement transactions deliberately.** Choose a documented logging or copy-on-write approach, define atomicity and isolation scope, and test partial writes, process termination, and recovery.
6. **Test failure, not just throughput.** Use deterministic fixtures, property tests for serialization, restart tests, fault injection where safe, and benchmarks with recorded data and environment.

### Source edge/failure guidance from: Safety and Acceptance

Never experiment against production data. Use disposable test directories and preserve backups before migration testing. Accept a feature only when stated durability and transaction properties are demonstrated by repeatable tests, and when corrupted or unsupported formats fail safely rather than being silently reinterpreted.

## Examples

Not specified in source skill. The original provided no input/output example, and none has been invented.

## Success Criteria

### Preserved source section: Safety and Acceptance

Never experiment against production data. Use disposable test directories and preserve backups before migration testing. Accept a feature only when stated durability and transaction properties are demonstrated by repeatable tests, and when corrupted or unsupported formats fail safely rather than being silently reinterpreted.
