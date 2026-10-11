---
name: async-jobs
description: Async jobs — idempotency, retry strategy, DLQ, observability.
---

## Detection Signals

- `queue`, `worker`, `job`, or `consumer` directories or files in the project
- Dependencies: `laravel/horizon`, `sidekiq`, `celery`, `bullmq`, `bee-queue`, `faktory`, `resque`, `delayed_job`
- Cloud queue services: `aws-sdk` with SQS usage, `@google-cloud/pubsub`, Azure Service Bus, RabbitMQ, Kafka
- `QUEUE_*` / `REDIS_QUEUE_*` / `SQS_*` env vars
- Cron/scheduler configs: `app/Console/Kernel.php`, `celerybeat`, `node-cron`, `whenever` gem

---

## When to Use a Job vs. Synchronous Processing

Use a background job when:
- The operation takes longer than the acceptable HTTP response time (~200ms threshold for user-facing actions)
- The operation involves external services that can be slow or unavailable (email, SMS, payment processor, webhooks)
- The operation can be retried independently if it fails (idempotent by nature or can be made so)
- Fan-out: one event triggers multiple independent downstream actions

Keep it synchronous when:
- The user needs the result to proceed (e.g., payment status before showing confirmation)
- The operation is fast and its failure should block the response (e.g., saving the primary record)
- Ordering guarantee is critical and queues add non-determinism

---

## Idempotency — Most Critical Rule

**Every job must be safe to run more than once with the same payload.**

Queues guarantee at-least-once delivery — a job will be retried on failure and may execute multiple times. A non-idempotent job causes duplicate records, double charges, or double notifications.

```python
# ❌ Non-idempotent — creates a duplicate on retry
def send_welcome_email(user_id: str):
    user = User.find(user_id)
    Email.send(to=user.email, template="welcome")

# ✅ Idempotent — checks state before acting
def send_welcome_email(user_id: str):
    user = User.find(user_id)
    if user.welcome_email_sent_at is not None:
        return  # already sent — safe to skip
    Email.send(to=user.email, template="welcome")
    user.update(welcome_email_sent_at=now())
```

**Idempotency patterns:**
- **State check**: read current state before acting; bail out if the action was already completed
- **Unique constraint**: use a database unique key on `(job_type, entity_id)` to prevent duplicate execution
- **Idempotency key**: pass a UUID with the job payload; store it as processed after first execution

---

## Payload Validation

Treat job payloads with the same rigor as HTTP input — validate before processing:

```ts
// ✅ Validate payload shape before using it
async handle(payload: unknown) {
  const { orderId, userId } = validateOrderPayload(payload); // throws on invalid
  const order = await Order.findOrFail(orderId);
  // ...
}
```

**Rules:**
- Never assume payload fields are present and correctly typed — they may come from an old version of the job or be corrupted
- Validate required fields and types at the start of the handler, before any side effects
- If validation fails: fail permanently (do not retry) — retrying a malformed payload wastes queue capacity

---

## Retry Strategy

| Failure type | Action |
|---|---|
| Transient (network timeout, 503) | Retry with exponential backoff |
| Business rule failure (record not found yet) | Retry with delay |
| Validation failure (malformed payload) | Fail permanently — do not retry |
| Unexpected exception | Retry up to max attempts, then DLQ |

**Exponential backoff formula**: `base_delay * 2^attempt` with jitter — prevents thundering herd when many jobs fail simultaneously.

**Minimum retry baseline** — unless the project defines otherwise: **3 attempts with exponential backoff starting at 2 s** (`2s → 4s → 8s`), then DLQ.

Configure per-job retry limits (not global defaults) — a payment job and an analytics job have different tolerance for retries. A payment job warrants fewer attempts and faster DLQ escalation than an analytics event.

---

## Dead Letter Queue (DLQ)

Every queue must have a DLQ configured. Jobs that exhaust retries move there instead of being silently dropped.

**After moving to DLQ:**
1. Alert the on-call team (do not let DLQ fill silently)
2. Inspect failed jobs to identify root cause
3. Fix the root cause, then replay or discard

**Never delete DLQ messages without inspecting them** — they contain the data of failed operations that may need manual resolution.

---

## Job Structure

```ts
// TypeScript / BullMQ example — same principles apply in any framework
class ProcessOrderJob {
  static queue = 'orders';
  static attempts = 3;
  static backoff = { type: 'exponential', delay: 2000 };

  async handle(payload: ProcessOrderPayload): Promise<void> {
    // 1. Validate payload
    const { orderId } = validateProcessOrderPayload(payload);

    // 2. Idempotency check
    const order = await Order.findOrFail(orderId);
    if (order.status !== OrderStatus.PENDING) return;

    // 3. Execute in a transaction if multiple writes are involved
    await db.transaction(async (trx) => {
      await order.process({ trx });
      await Inventory.reserve(order.items, { trx });
    });

    // 4. Trigger downstream jobs (don't chain synchronously)
    await SendOrderConfirmationJob.dispatch({ orderId });
  }
}
```

---

## Observability

- **Log on start and completion** — include job ID, entity ID, and duration; useful for tracing stuck jobs
- **Never log sensitive payload fields** — mask emails, card numbers, passwords in logs
- **Emit metrics** — queue depth, job duration p95, failure rate; connect to the monitoring dashboard
- **Unique job ID in logs** — every log line inside a job handler must carry the job ID for correlation

```python
# ✅ Structured log with context
logger.info("order.processed", extra={
    "job_id": self.request.id,
    "order_id": order_id,
    "duration_ms": elapsed,
})
```

---

## Framework-Specific Notes

| Framework | Key consideration |
|---|---|
| **Laravel Queue** | Use `ShouldBeUnique` for deduplication; `ShouldBeIdempotent` pattern via `uniqueId()`; Horizon for monitoring |
| **Sidekiq / ActiveJob** | Use `sidekiq-unique-jobs` for deduplication; set `retry` and `dead` thresholds per worker class |
| **Celery** | Set `acks_late=True` for at-least-once; use `task_id` for idempotency; Flower for monitoring |
| **BullMQ** | Use `jobId` option for deduplication; configure `removeOnComplete` to avoid memory bloat |
| **AWS SQS** | Visibility timeout must exceed max job duration; use `MessageDeduplicationId` on FIFO queues |
| **RabbitMQ** | Set `acks_late` / manual ack — never auto-ack before processing completes; configure a dead-letter exchange (`x-dead-letter-exchange`) per queue; use `x-message-ttl` to cap retry window; prefer quorum queues over classic for durability |
| **Apache Kafka** | Idempotency is consumer-side — commit offset only after successful processing (`enable.auto.commit=false`); use a unique `group.id` per consumer app; store processed offsets or business keys to detect replays; DLQ = a dedicated topic (e.g. `topic.DLT`); monitor consumer lag as the primary health signal |
