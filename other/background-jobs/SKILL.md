---
name: background-jobs
description: Use when designing asynchronous job processing. Covers queue selection, idempotency, retry and backoff policy, scheduling, poison messages, and observability for work that happens outside the request.
metadata:
  category: backend
  version: 1.0.0
  tags: [jobs, queues, workers, retries, scheduling]
---

# Background Jobs

## Purpose

Move work out of the request path without losing it. A job system is a distributed system with a friendly interface; the failure modes are the same, and they are hidden until they are not.

## When to Use

- Work that is slow, retriable, or must survive a request timeout: emails, exports, webhooks, media processing.
- Scheduled and recurring work.
- Diagnosing duplicate side effects, stuck queues, or jobs that silently disappear.

## Capabilities

- Queue and worker design, including priority and isolation.
- Idempotency and exactly-once effects.
- Retry policy: backoff, jitter, attempt limits, dead-letter handling.
- Scheduling: cron jobs, delayed jobs, and deduplicating them across instances.
- Observability: queue depth, age, failure rate.

## Inputs

- The work to be done and whether it can safely run twice.
- Latency expectations: seconds, minutes, or overnight.
- Volume, and how bursty it is.

## Outputs

- Job handlers that are idempotent by construction.
- Explicit retry and DLQ policies per job type.
- Alerts on queue depth and oldest-message age.

## Workflow

1. **Make it idempotent first** — Before anything else. A job will run twice; design so that this is harmless. Key the side effect, not the invocation.
2. **Pass identifiers, not objects** — Enqueue `{"order_id": "..."}`, not a serialized order. By the time the job runs, the object may be stale.
3. **Set the retry policy per job** — A transient network failure deserves exponential backoff and ten attempts. A validation failure deserves zero retries and a DLQ.
4. **Isolate the queues** — A flood of low-priority image resizes must not delay password-reset emails. Separate queues, separate workers.
5. **Deduplicate scheduled work** — With multiple instances, every instance's scheduler fires. Use a lock keyed on the job name and window.
6. **Alert on age, not just depth** — A queue with 10 messages that are 3 hours old is a worse signal than a queue with 10,000 that are 5 seconds old.

## Best Practices

- Every job handler must tolerate being called twice with the same arguments. This is the single rule that prevents most job-system incidents.
- Never enqueue inside a database transaction that has not committed. The worker will pick the job up and find no row. Use the outbox pattern or an after-commit hook.
- A job with no timeout will eventually hang and hold a worker forever. Set one.
- Retry only what is retriable. Retrying a 400 from an upstream API twenty times is a way to get rate-limited for a permanent failure.
- Log the job ID, the attempt number, and the argument identifiers on every execution. Without this, debugging is guesswork.
- Keep handlers small. A job that does five things fails partway through the third.

## Examples

**Idempotent handler with a natural key:**

```python
@job(queue="billing", max_attempts=5, backoff="exponential", timeout=30)
def send_invoice(invoice_id: str) -> None:
    invoice = Invoice.get(invoice_id)

    # The natural idempotency key: an invoice is sent at most once.
    if invoice.sent_at is not None:
        logger.info("invoice_already_sent", extra={"invoice_id": invoice_id})
        return

    message_id = mailer.send(
        to=invoice.customer_email,
        template="invoice",
        context=invoice.render_context(),
        idempotency_key=f"invoice:{invoice_id}",   # the provider dedupes too
    )

    invoice.update(sent_at=utcnow(), provider_message_id=message_id)
```

Two protections, deliberately: the local check handles the common case, and the provider's idempotency key handles the crash between `send` and `update`.

**Enqueue after commit, not inside the transaction:**

```python
with db.transaction():
    order = Order.create(...)
    db.after_commit(lambda: send_invoice.enqueue(order.invoice_id))
```

## Notes

- The most common job-system bug is enqueueing from inside an uncommitted transaction. The worker is fast enough to look for a row that does not exist yet, and the job fails with "not found" only under load.
- Exponential backoff without jitter causes retry storms to synchronize. Always add jitter.
- Long-running jobs should checkpoint. A 40-minute export that fails at minute 39 and restarts from zero will never complete under any retry policy.
