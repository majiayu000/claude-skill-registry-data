---
name: celery-redis-reliability
description: 'Implement reliable async processing with Celery/Redis in HIVMeet backend. Use for task design, retry policy, idempotency, failure handling, and monitoring of background jobs.'
argument-hint: 'Describe task purpose, side effects, retry expectations, and failure impact.'
user-invocable: true
---

# Celery and Redis Reliability

## Purpose
Ensure background processing remains correct, observable, and safe under retries, worker restarts, and partial failures.

## Use When
- Creating or updating Celery tasks
- Moving synchronous logic to async jobs
- Debugging flaky background processing
- Hardening retry and idempotency behavior

## Mandatory Workflow

### 1. Task Contract Definition
- Define task input schema, expected output, and side effects
- Define idempotency key/condition for side-effecting tasks
- Define acceptable retry semantics

### 2. Reliability-Oriented Implementation
- Keep task body small and deterministic
- Use explicit retry policy for transient failures
- Separate retriable versus non-retriable exceptions

### 3. Idempotency and Deduplication
- Guard external side effects (emails, payments, notifications)
- Ensure repeat execution does not duplicate critical business events
- Persist execution markers when needed

### 4. Timeout and Resource Controls
- Define task soft/hard time limits where relevant
- Avoid unbounded loops and large in-memory payloads
- Chunk high-volume processing workloads

### 5. Observability and Operability
- Log task lifecycle with safe context
- Expose failure reasons and retry counts in logs/monitoring
- Provide runbook steps for manual replay/recovery

### 6. Validation
- Test success path, transient failure path, and terminal failure path
- Test idempotency under repeated execution
- Verify no user-facing inconsistency when task fails late

### 7. Output Contract
1. Task reliability model
2. Retry/idempotency strategy
3. Failure handling and monitoring signals
4. Test evidence
5. Residual operational risks

## Quality Gates
- No side-effecting task without idempotency strategy
- No retry policy that can trigger uncontrolled duplicates
- No critical async flow without observability hooks
