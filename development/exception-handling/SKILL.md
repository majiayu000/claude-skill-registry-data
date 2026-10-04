---
name: exception-handling
description: "Use when writing, reviewing, or debugging Apex exception handling, DmlException behavior, custom exception hierarchies, or user-safe error messages. Triggers: 'DmlException', 'swallowed exception', 'AuraHandledException', 'trigger rollback', 'try catch'. NOT for a specific runtime error — use apex/common-apex-runtime-errors. Also: 'LimitException', 'getDmlIndex', 'SaveResult', 'Savepoint rollback callout', 'Assert.fail', 'finalizer getException', 'Apex exception email'. NOT for a cross-cutting error framework — use apex/error-handling-framework."
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
  - "catch a LimitException in Apex"
  - "why did my finally block not run"
  - "map Database.SaveResult errors back to the input rows"
  - "figure out which row failed in a bulk insert"
  - "wrap an exception without losing the original stack trace"
  - "stop the raw DML error showing to the user in LWC"
  - "write a test that asserts an exception is thrown"
  - "use addError or throw an exception in a trigger"
  - "release a savepoint before making a callout"
  - "log the exception that killed my Queueable job"
  - "custom exception class will not compile in Apex"
  - "why am I not getting Apex exception emails"
  - "apex exception handling best practices for try catch and custom exceptions"
inputs:
  - "execution context such as trigger, Aura/LWC controller, REST, Queueable, or Batch"
  - "whether partial success is acceptable for the operation"
  - "available logging or monitoring mechanism in the org"
outputs:
  - "exception handling pattern recommendation"
  - "code review findings for error handling risks"
  - "remediation plan for bulk-safe and user-safe failures"
  - "deployable custom exception class, service, @AuraEnabled controller and bulk test class"
  - "package.xml, deploy order, and post-deploy verification queries"
dependencies: []
version: 1.1.0
author: Pranav Nagrecha
updated: 2026-09-05
---

Use this skill when Apex error handling is becoming part of the design, not just a syntax exercise. The goal is to prevent swallowed failures, preserve operational visibility, and return the right kind of error for the calling context without corrupting bulk processing.

## Before Starting

- What is the entry point: trigger, controller, REST resource, Queueable, Batch, invocable, or scheduled job?
- Should one bad record fail the whole transaction, or is partial success acceptable?
- Where do production failures go today: custom log object, platform event, observability tool, or nowhere?

## Questions to Ask Before Configuring

Ask these before writing a single `catch`. The answers decide the DML mode, the exception type, and the
sink — and an LLM that skips them produces a `try/catch (Exception e)` that hides a governor limit it
could never have caught anyway.

| Ask | Why it matters | What a good answer adds |
|---|---|---|
| "If one row of two hundred is bad, what should happen to the other 199?" | `insert records;` and `Database.insert(records, true)` roll all 200 back; with `allOrNone` false "the remainder of the DML operation can still succeed. You must iterate through the returned results" (`apexdev` L9060–9063) | The DML mode, and whether the caller needs a per-row result object at all |
| "Who reads the failure — the user, the operator, or a support queue?" | A `DmlException` message carries the failing field API names and the validation-rule text (`apexrefguide` L215130–215147); an `@AuraEnabled` failure sends **no** exception email at all (`apexdev` L39609–39610) | The boundary conversion, and the durable sink that has to exist because the email will not |
| "Which failure here is a business rule and which is a defect?" | Business rules belong on the record: `addError` on an Apex-spawned DML still compiles a comprehensive error list before rolling back (`apexdev` L15832–15833); an unhandled `throw` marks every record and stops (`apexdev` L15844) | The `addError` / `throw` split per failure mode, written down before the trigger is written |
| "Does anything in this path call out to an external system?" | A callout with an active savepoint raises `System.CalloutException`: "All active Savepoints must be released before making callouts." (`apexdev` L8742–8750) | The rollback-then-`releaseSavepoint`-then-call-out order, and whether the notification belongs in a finalizer instead |
| "Is this synchronous, or is it a Queueable or Batch?" | The failures that actually kill async jobs are uncatchable — `catch` and `finally` are both skipped (`apexdev` L39722–39728) — and are only readable from `FinalizerContext.getException()` (`apexdev` L16330–16336) | A finalizer or `Database.RaisesPlatformEvents` on the class, instead of a `catch` that will never fire |
| "Could the exception message ever contain customer data?" | "The Apex exception handler and testing framework can’t determine if sensitive data is contained in user-defined messages" (`apexdev` L40308–40311) | A typed field on the exception subclass for the identifying data, and a message that carries only ids and a correlation reference |
| "How will the test prove the exception is still thrown next quarter?" | A negative test without `Assert.fail()` passes when the method stops throwing; the assertion failure itself "can’t be caught in the try/catch block" (`apexrefguide` L200594–200595) | `Assert.fail(...)` before the `catch`, plus assertions on type, message and `getDmlIndex` |

What a designed exception path adds over a `try/catch`: the caller can tell "rejected by a rule" from
"the platform broke", the operator gets one log row per operation instead of one per row, the user never
reads a field API name, and the row that failed is identified by its original position rather than by
the loop counter that happened to be in scope.

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

1. **Classify every failure in the path first.** Fill the Failure Classification table in
   `templates/exception-handling-template.md` — expected business rule, row-level DML failure, external
   timeout, or defect. That table, not the code, decides `addError` vs `throw` vs `SaveResult`.
2. **Pick the DML mode from the Questions table answer, before writing the catch.** All-or-none means a
   `DmlException` and `getDmlIndex`; partial success means `Database.SaveResult[]` and **no exception at
   all**. The two error-mapping loops are different shapes — both are in
   `references/code-examples.md` (`CaseIntakeService`).
3. **Write one custom exception, not a hierarchy.** Extend `Exception`, end the name in `Exception`, put
   granularity in an enum field and the chained cause. Use the static-factory shape from
   `references/code-examples.md` (`CaseIntakeException`) rather than declaring a constructor, and check
   whether `templates/apex/BaseService.cls` already gives you what you need — it ships a
   `ServiceException` and `logAndRethrow`.
4. **Convert at the boundary and nowhere else.** `AuraHandledException` is constructed only in the
   `@AuraEnabled` method (`CaseIntakeController.toAura`), which logs the real exception through
   `templates/apex/ApplicationLogger.cls` first. Do not add a logger of your own — sink design belongs to
   `apex/debug-and-logging`.
5. **If the path calls out or takes a savepoint, order the catch block explicitly:**
   `Database.rollback(sp)` → `Database.releaseSavepoint(sp)` → callout → log → throw. Any other order
   raises `CalloutException` instead of notifying anyone (`references/gotchas.md`).
6. **Write the negative test with `Assert.fail()` and 200 rows.** Assert the exception type, the message
   the caller will actually see, the cause chain, and `getDmlIndex` — `CaseIntakeServiceTest` in
   `references/code-examples.md` is the template. Build the data with
   `templates/apex/tests/TestDataFactory.cls`.
7. **Run the checker over the source tree before deploying:**
   `python3 skills/apex/exception-handling/scripts/check_exception_handling.py --manifest-dir force-app/main/default`
   It flags empty catches, debug-only catches, mis-named exception classes, raw `getMessage()` reaching
   `AuraHandledException`, savepoint-then-callout, uninspected partial-success results, and negative
   tests missing `Assert.fail`.

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
5. **A `LimitException` skips your `finally` block, not just your `catch`** — so cleanup that "always runs" does not.
6. **A custom exception whose name does not end in `Exception` will not save** — and `throw` needs an object, so the `new` is mandatory.
7. **Wrapping with the single-`String` constructor deletes the cause** — `getCause()` returns `null` and the original line number is gone.
8. **`getDmlIndex(i)` is a row position; `i` is a failure ordinal** — indexing the input list with `i` names the wrong record.
9. **`addError` and `throw` have opposite blast radii in a trigger** — one compiles a full error list, the other stops everything.
10. **`Database.setSavepoint()` spends a DML statement and blocks the next callout** — release it before calling out.
11. **`@AuraEnabled` failures never generate an exception email** — the log write in the catch block is the only record.
12. **A Queueable's fatal exception is readable only from `FinalizerContext.getException()`** — the `catch` inside `execute` never saw it.
13. **The exception message is a data-privacy surface** — put identifying data in a typed field on the subclass, not in the message.

Full detail with guide citations in `references/gotchas.md`.

## Output Artifacts

| Artifact | Description |
|---|---|
| Exception handling review | Findings on swallow risks, bulk failure behavior, and boundary-appropriate error translation |
| Remediation pattern | Recommended catch, log, rethrow, or `addError` structure for the current context |
| Failure classification matrix | Expected vs unexpected failures with the correct handling strategy per entry point |

## Reference Files

| File | Read it when |
|---|---|
| `references/code-examples.md` | You are building the thing: the base custom exception, the partial-success handler, the savepoint/callout order, the `@AuraEnabled` wrapper, the 200-row test class, package.xml, deploy order, verification |
| `references/gotchas.md` | A failure behaved differently from how the code reads — 15 platform behaviours with guide citations |
| `references/llm-anti-patterns.md` | Reviewing generated exception code; nine failure shapes with detection hints |
| `references/examples.md` | You want the worked partial-success, boundary-mapping, or rollback-then-notify example rather than the full deployable slice |
| `references/well-architected.md` | Choosing between fail-fast and partial success, or citing the sources behind a decision |
| `templates/exception-handling-template.md` | Running an exception-handling review over someone else's code |
| `scripts/check_exception_handling.py` | Before deploying — seven rules over the `.cls` and `.trigger` files this skill produces |

## Related Skills

- `apex/debug-and-logging` — owns the sink. This skill decides what to catch and what to throw; that one decides where the record lands, why a rollback discards it, and how `ApplicationLogger` is wired.
- `apex/apex-savepoint-and-rollback` — owns savepoint design in depth: nesting, release semantics, and the API 60.0 test behaviour. This skill states only the rules a catch block must obey.
- `apex/callout-and-dml-transaction-boundaries` — owns the uncommitted-work rule and the ordering of DML and callouts across a transaction.
- `apex/apex-transaction-finalizers` — owns `System.Finalizer`, re-enqueue budgets, and `BatchApexErrorEvent`. Go there when the failure is async.
- `apex/apex-dml-patterns` — owns bulk DML shape and `Database.*` method selection beyond the error-handling slice.
- `apex/error-handling-framework` — owns the cross-cutting framework (retry policy, error catalogue, org-wide conventions) once more than one team consumes it.
- `apex/common-apex-runtime-errors` — owns diagnosing one specific runtime error you are looking at right now.
- `apex/test-class-standards` — owns negative-path assertions, exception expectations, and mock-based error scenarios.
- `apex/trigger-framework` — owns trigger structure when handler sprawl is what is making exception handling chaotic.
- `apex/async-apex` — use when the real fix is moving work off the synchronous transaction rather than trapping errors in it.
- `lwc/lwc-error-boundaries` — owns what the component does with the error once `AuraHandledException` reaches JavaScript.
