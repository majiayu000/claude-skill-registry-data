---
name: exception-handling
description: "Use when writing, reviewing, or debugging Apex exception handling, DmlException behavior, custom exception hierarchies, or user-safe error messages. Triggers: 'DmlException', 'swallowed exception', 'AuraHandledException', 'trigger rollback', 'try catch'. NOT for choosing async execution models or general governor-limit tuning."
category: apex
salesforce-version: "Spring '25+"
well-architected-pillars:
  - Reliability
  - Operational Excellence
tags:
  - exception-handling
  - dml-exception
  - aurahandledexception
  - logging
  - error-mapping
triggers:
  - "DmlException happening in bulk update"
  - "swallowed exception in Apex service class"
  - "AuraHandledException message for LWC"
  - "trigger rollback caused by unhandled exception"
  - "how should I structure custom exceptions in Apex"
inputs:
  - "execution context such as trigger, Aura/LWC controller, REST, Queueable, or Batch"
  - "whether partial success is acceptable for the operation"
  - "available logging or monitoring mechanism in the org"
outputs:
  - "exception handling pattern recommendation"
  - "code review findings for error handling risks"
  - "remediation plan for bulk-safe and user-safe failures"
dependencies: []
version: 1.0.0
author: Pranav Nagrecha
updated: 2026-03-13
---

Use this skill when Apex error handling is becoming part of the design, not just a syntax exercise. The goal is to prevent swallowed failures, preserve operational visibility, and return the right kind of error for the calling context without corrupting bulk processing.

## Before Starting

- What is the entry point: trigger, controller, REST resource, Queueable, Batch, invocable, or scheduled job?
- Should one bad record fail the whole transaction, or is partial success acceptable?
- Where do production failures go today: custom log object, platform event, observability tool, or nowhere?

## Core Concepts

### Catch Expected Failures, Not Everything

Apex supports standard exception types such as `DmlException`, `QueryException`, and `CalloutException`, plus custom exceptions. Catch the most specific exception you can actually handle. Salesforce guidance is to catch expected exceptions, add context, and let unexpected exceptions propagate instead of masking the root cause. A blanket `catch (Exception e)` that returns `null` or `false` usually turns a debuggable failure into silent data loss.

### Bulk DML Failure Semantics Matter

`insert records;` and `update records;` throw a `DmlException` on failure and stop the transaction. `Database.insert(records, false)` and `Database.update(records, false)` behave differently: they allow partial success and return `Database.SaveResult[]`. In bulk code, this choice is architectural. If the business process can tolerate some failures, inspect `SaveResult` per record and log or surface the rejected records. Do not wrap a whole bulk update in one `try/catch` and assume that makes it bulk-safe.

### Boundary-Specific Error Translation

Different Apex boundaries need different failure behavior. In a trigger, business-rule failures generally belong on the record through `addError`, while unexpected exceptions should surface and roll back the transaction. In an Aura/LWC controller, raw system messages are poor UX, so map known failures to `AuraHandledException` with a human-safe message. In background jobs, user messaging is irrelevant; logging and retry classification matter more.

### Log Once, At The Right Layer

Centralize logging at a service boundary or integration boundary. If every layer catches and logs the same exception, production monitoring fills with duplicates and the real signal disappears. Prefer a single structured log entry containing the operation, record IDs or correlation ID, failure type, and whether the exception was rethrown or transformed.

## Common Patterns

### Specific Catch With Domain Mapping

**When to use:** A service class knows how to turn a low-level Salesforce failure into a business-facing failure.

**How it works:** Catch `DmlException` or `CalloutException`, log structured context once, then throw a domain-specific exception or boundary-safe exception such as `AuraHandledException`.

**Why not the alternative:** Catching generic `Exception` in every layer hides the original failure and produces inconsistent messages.

### Partial Success For Bulk Operations

**When to use:** A batch-like service should process as many records as possible even if some fail validation.

**How it works:** Use `Database.insert/update/delete(records, false)`, inspect every `SaveResult`, and store or return the failed record IDs and messages.

**Why not the alternative:** A single `update records;` statement plus one catch block loses per-record visibility and fails the entire transaction.

### Trigger Business Validation With `addError`

**When to use:** The user should be told exactly which record violates a business rule during DML.

**How it works:** Add errors to offending records in trigger context for expected business validation failures. Reserve thrown exceptions for truly unexpected or system-level faults.

## Decision Guidance

| Situation | Recommended Approach | Reason |
|---|---|---|
| User-facing controller needs a safe error message | Catch the specific exception and map it to `AuraHandledException` | Preserves UX while avoiding raw internal messages |
| Trigger validation should block a save for a known business rule | Use `record.addError()` | Keeps the error attached to the record and fits trigger semantics |
| Bulk service can accept partial success | Use `Database.*(list, false)` and inspect `SaveResult[]` | Avoids one bad record failing the whole batch |
| Unexpected null pointer or design bug | Let it bubble after optional boundary logging | Hidden defects are harder to fix than loud failures |


## Recommended Workflow

Step-by-step instructions for an AI agent or practitioner activating this skill:

1. Gather context — confirm the org edition, relevant objects, and current configuration state
2. Review official sources — check the references in this skill's well-architected.md before making changes
3. Implement or advise — apply the patterns from Core Concepts and Common Patterns sections above
4. Validate — run the skill's checker script and verify against the Review Checklist below
5. Document — record any deviations from standard patterns and update the template if needed

---

## Review Checklist

- [ ] Catch blocks are specific; generic `catch (Exception e)` is justified or removed.
- [ ] No catch block silently returns success, `null`, or `false` without logging or rethrowing.
- [ ] Bulk DML paths use `SaveResult[]` when partial success is required.
- [ ] Trigger code uses `addError` for expected business validation, not generic swallowed exceptions.
- [ ] User-facing controllers return safe, human-readable messages instead of raw internal stack traces.
- [ ] Logging happens once with operation context, record scope, and failure type.

## Salesforce-Specific Gotchas

1. **Unhandled trigger exceptions roll back the transaction** — if a trigger throws unexpectedly, the entire DML operation fails, including unrelated records in the same transaction.
2. **`Database.update(list, false)` does not throw for every row failure** — record-level failures move into `SaveResult[]`; if you never inspect those results, you silently lose failures.
3. **`AuraHandledException` is a boundary tool, not a service-layer base class** — using it deep in service code couples business logic to UI transport concerns.
4. **A debug-only catch block is effectively a swallowed exception** — `System.debug` is not monitoring, and production users never see it.

## Output Artifacts

| Artifact | Description |
|---|---|
| Exception handling review | Findings on swallow risks, bulk failure behavior, and boundary-appropriate error translation |
| Remediation pattern | Recommended catch, log, rethrow, or `addError` structure for the current context |
| Failure classification matrix | Expected vs unexpected failures with the correct handling strategy per entry point |

## Related Skills

- `apex/async-apex` — use when the real fix is moving work to Queueable, Batch, or Scheduled Apex instead of trapping errors in a synchronous transaction.
- `apex/test-class-standards` — use alongside this skill to verify negative-path assertions, exception expectations, and mock-based error scenarios.
- `apex/trigger-framework` — use when trigger structure is making exception handling chaotic or duplicated across multiple handlers.
