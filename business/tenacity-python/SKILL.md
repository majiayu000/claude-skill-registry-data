---
name: tenacity-python
description: Use for writing, reviewing, debugging, or testing bounded retry policies in Python with Tenacity, including retry predicates, stop and wait strategies, jitter, exception propagation, callbacks, Retrying, and AsyncRetrying. Do not use for generic loops, scheduled jobs, domain polling without a retryable operation, or operations whose side effects are not safe to repeat.
argument-hint: "[Tenacity retry task, policy, code, failure, or test]"
---

# Tenacity Python

Treat a retry as a policy around repeated attempts, not as an error-handling
decorator added after a failure. Preserve the operation's idempotency, deadline,
failure taxonomy, and observability.

## Boundary

Use this skill when a project uses Tenacity or explicitly requests it for a
transient operation. Do not retry permanent validation/authentication errors,
unknown broad exceptions, local programmer defects, or irreversible operations
without an idempotency mechanism. Do not add Tenacity around a client that
already owns an adequate retry policy until duplicate retry multiplication is
resolved.

## Know the policy objects

| Object | Meaning | Required decision |
|---|---|---|
| `retry(...)` | Decorator creating a retry controller per call | Predicate, stop, wait, propagation, hooks. |
| `Retrying` | Synchronous controller/call/block iterator | Use when policy is dynamic or a block, not a whole function, is retried. |
| `AsyncRetrying` | Await-aware controller | Awaited operation and sleep remain nonblocking. |
| Retry predicate | Decides whether the last exception/result is retryable | Must be narrow and domain-grounded. |
| Stop strategy | Bounds attempts or elapsed retry time | Always finite in application code. |
| Wait strategy | Delay before another attempt | Respect service pressure and add jitter for contention. |
| `RetryCallState` | Attempt number, outcome, timing, next action | Source for callbacks and tests, not mutable business state. |

Read [the retry state model](references/retry-model.md) before composing
predicates, retrying results, or using block iteration.

## Ordered workflow

1. Name the exact attempted operation and its side effect. Establish whether
   repetition is safe, conditionally safe through an idempotency key, or unsafe.
2. Classify failures from the real client/library: retry only enumerated
   transient exceptions or results. Exclude cancellation, invalid input,
   permission/auth failures, and deterministic defects.
3. Establish the outer deadline/budget. Choose a finite stop condition that
   cannot outlive it; attempts include the first call.
4. Choose wait behavior from the dependency contract. For shared remote
   services, use capped exponential random wait or honor a supported server
   retry delay. Do not busy-loop.
5. Decide terminal failure: normally `reraise=True` so callers see the final
   domain exception. Use `RetryError` only when callers intentionally consume
   retry-controller state.
6. Attach structured `before_sleep` telemetry without secrets. Log only an
   attempt that will actually retry, not every call as an error.
7. Test with zero wait/fake sleep and deterministic outcomes. Assert attempt
   count, retry classification, final exception/result, and side effects.

## Policy decision table

| Condition | Action |
|---|---|
| Operation is not repeat-safe | Do not retry; add idempotency/transaction semantics first. |
| Failure is permanent or unknown | Propagate immediately. |
| Client already retries | Configure one owner; prevent multiplicative nested attempts. |
| Attempts are cheap and local | Small attempt bound; `wait_none`/fixed wait only if pressure is irrelevant. |
| Remote service is contended | Bounded exponential random wait with cap. |
| Caller has a hard deadline | Stop by elapsed time/attempts beneath that deadline; retain transport timeout per attempt. |
| Async operation | Use async-decorated function or `AsyncRetrying`; never block the loop with `time.sleep`. |
| Return value signals transient incompleteness | Use `retry_if_result` only when the result has an unambiguous retry state. |

## Canonical bounded policy

```python
from tenacity import (
    retry,
    retry_if_exception_type,
    stop_after_attempt,
    wait_random_exponential,
)


class TemporaryStoreError(Exception):
    pass


@retry(
    retry=retry_if_exception_type(TemporaryStoreError),
    stop=stop_after_attempt(4),
    wait=wait_random_exponential(multiplier=0.25, max=4),
    reraise=True,
)
def load_record(store, record_id: str):
    return store.load(record_id)
```

The operation still needs a per-attempt timeout. Tenacity bounds retrying, not
an individual call stuck forever. Do not decorate an entire workflow when only
one read is retryable; repeat the narrowest safe unit.

## Side effects and nested budgets

- Reads are not automatically safe if they consume messages or advance cursors.
- Writes require a stable idempotency key, transactional upsert, or explicit
  proof that a repeated request cannot duplicate effects.
- A timeout does not prove the server did nothing. Treat an ambiguous write
  outcome separately from a known pre-commit failure.
- Multiply configured layers to find the real worst-case attempts. Prefer one
  retry owner and one outer deadline.
- Do not retry `BaseException`, cancellation, keyboard interrupts, or a blanket
  `Exception` just because examples do.

Read [policy and testing](references/policy-testing.md) for budgets, deterministic
tests, and non-idempotent operations.

## Async and observability

Tenacity supports coroutines and `AsyncRetrying`. Ensure the awaited client
call, sleep function, cancellation behavior, and caller deadline all remain
async. In `before_sleep`, record operation name, attempt, elapsed time, next
delay, and exception class; exclude credentials, payloads, and full response
bodies. A counter should distinguish attempts from completed calls and terminal
failures. Read [async and observability](references/async-observability.md).

## Version grounding and completion

Inspect the installed version of Tenacity and its signatures before
using a copied helper or callback field. This foundry did not have Tenacity
installed during authoring, so examples are source-grounded but not locally
executed. Do not turn that into a runtime-version claim.

Completion requires: repetition safety is proven; retry and non-retry failures
are enumerated; per-attempt timeout and overall stop are finite; wait avoids a
hot loop; terminal exceptions match the caller contract; async code does not
block; telemetry reveals attempts without leaking data; and deterministic tests
prove attempt counts, terminal behavior, and exactly-once visible effects.

## References

- [Retry state model](references/retry-model.md)
- [Policy and deterministic testing](references/policy-testing.md)
- [Async and observability](references/async-observability.md)
