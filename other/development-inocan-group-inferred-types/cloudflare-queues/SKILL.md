---
name: cloudflare-queues
description: |
  Build async message queues with Cloudflare Queues for background processing. Use when: handling async tasks, batch processing, implementing retries, configuring dead letter queues, managing consumer concurrency, or troubleshooting queue timeout, batch retry, message loss, or throughput exceeded.
---

# Cloudflare Queues

**Status**: Production Ready ✅
**Last Updated**: 2025-11-24
**Dependencies**: cloudflare-worker-base (for Worker setup)
**Latest Versions**: wrangler@4.50.0, @cloudflare/workers-types@4.20251121.0

**Recent Updates (2025)**:
- **April 2025**: Pull consumers increased limits (5,000 msg/s per queue, up from 1,200 requests/5min)
- **March 2025**: Pause & Purge APIs (wrangler queues pause-delivery, queues purge)
- **2025**: Customizable retention (60s to 14 days, previously fixed at 4 days)
- **2025**: Increased queue limits (10,000 queues per account, up from 10)

---

## Quick Start (5 Minutes)

```bash
# 1. Create queue
npx wrangler queues create my-queue

# 2. Add producer binding to wrangler.jsonc
# { "queues": { "producers": [{ "binding": "MY_QUEUE", "queue": "my-queue" }] } }

# 3. Send message from Worker
await env.MY_QUEUE.send({ userId: '123', action: 'process-order' });

# 4. Add consumer binding to wrangler.jsonc
# { "queues": { "consumers": [{ "queue": "my-queue", "max_batch_size": 10 }] } }

# 5. Process messages
export default {
  async queue(batch: MessageBatch, env: Env): Promise<void> {
    for (const message of batch.messages) {
      await processMessage(message.body);
      message.ack(); // Explicit acknowledgement
    }
  }
};

# 6. Deploy and test
npx wrangler deploy
npx wrangler tail my-consumer
```

---

## Producer API

```typescript
// Send single message
await env.MY_QUEUE.send({ userId: '123', action: 'send-email' });

// Send with delay (max 12 hours)
await env.MY_QUEUE.send({ action: 'reminder' }, { delaySeconds: 600 });

// Send batch (max 100 messages or 256 KB)
await env.MY_QUEUE.sendBatch([
  { body: { userId: '1' } },
  { body: { userId: '2' } },
]);
```

**Critical Limits:**
- Message size: **128 KB max** (including ~100 bytes metadata)
- Messages >128 KB will fail - store in R2 and send reference instead
- Batch size: 100 messages or 256 KB total
- Delay: 0-43200 seconds (12 hours max)

---

## Consumer API

```typescript
export default {
  async queue(batch: MessageBatch, env: Env, ctx: ExecutionContext): Promise<void> {
    for (const message of batch.messages) {
      // message.id - unique UUID
      // message.timestamp - Date when sent
      // message.body - your content
      // message.attempts - retry count (starts at 1)

      await processMessage(message.body);
      message.ack(); // Explicit ack (critical for non-idempotent ops)
    }
  }
};

// Retry with exponential backoff
message.retry({ delaySeconds: Math.min(60 * Math.pow(2, message.attempts - 1), 3600) });

// Batch methods
batch.ackAll();   // Ack all messages
batch.retryAll(); // Retry all messages
```

**Critical:**
- **`message.ack()`** - Mark success, prevents retry even if handler fails later
- **Use explicit ack for non-idempotent operations** (DB writes, API calls, payments)
- **Implicit ack** - If handler returns successfully without calling ack(), all messages auto-acknowledged
- **Ordering not guaranteed** - Don't assume FIFO message order

---

## Critical Consumer Patterns

### Explicit Acknowledgement (Non-Idempotent Operations)

**ALWAYS use explicit ack() for:** Database writes, API calls, financial transactions

```typescript
export default {
  async queue(batch: MessageBatch, env: Env): Promise<void> {
    for (const message of batch.messages) {
      try {
        await env.DB.prepare('INSERT INTO orders (id, amount) VALUES (?, ?)')
          .bind(message.body.orderId, message.body.amount).run();
        message.ack(); // Only ack on success
      } catch (error) {
        console.error(`Failed ${message.id}:`, error);
        // Don't ack - will retry
      }
    }
  }
};
```

**Why?** Prevents duplicate writes if one message in batch fails. Failed messages retry independently.

---

### Exponential Backoff for Rate-Limited APIs

```typescript
export default {
  async queue(batch: MessageBatch, env: Env): Promise<void> {
    for (const message of batch.messages) {
      try {
        await fetch('https://api.example.com/process', {
          method: 'POST',
          body: JSON.stringify(message.body),
        });
        message.ack();
      } catch (error) {
        if (error.status === 429) {
          const delaySeconds = Math.min(60 * Math.pow(2, message.attempts - 1), 3600);
          message.retry({ delaySeconds });
        } else {
          message.retry();
        }
      }
    }
  }
};
```

---

### Dead Letter Queue (DLQ) - CRITICAL for Production

**⚠️ Without DLQ, failed messages are DELETED PERMANENTLY after max_retries**

```bash
npx wrangler queues create my-dlq
```

**wrangler.jsonc:**
```jsonc
{
  "queues": {
    "consumers": [{
      "queue": "my-queue",
      "max_retries": 3,
      "dead_letter_queue": "my-dlq"  // Messages go here after 3 failed retries
    }]
  }
}
```

**DLQ Consumer:**
```typescript
export default {
  async queue(batch: MessageBatch, env: Env): Promise<void> {
    for (const message of batch.messages) {
      console.error('PERMANENTLY FAILED:', message.id, message.body);
      await env.DB.prepare('INSERT INTO failed_messages (id, body) VALUES (?, ?)')
        .bind(message.id, JSON.stringify(message.body)).run();
      message.ack(); // Remove from DLQ
    }
  }
};
```

---

## Consumer Configuration

```jsonc
{
  "queues": {
    "consumers": [{
      "queue": "my-queue",
      "max_batch_size": 100,           // 1-100 (default: 10)
      "max_batch_timeout": 30,         // 0-60s (default: 5s)
      "max_retries": 5,                // 0-100 (default: 3)
      "retry_delay": 300,              // Seconds (default: 0)
      "max_concurrency": 10,           // 1-250 (default: auto-scale)
      "dead_letter_queue": "my-dlq"    // REQUIRED for production
    }]
  }
}
```

**Critical Settings:**

- **Batching** - Consumer called when EITHER condition met (max_batch_size OR max_batch_timeout)
- **max_retries** - After exhausted: with DLQ → sent to DLQ, without DLQ → **DELETED PERMANENTLY**
- **max_concurrency** - Only set if upstream has rate limits or connection limits. Otherwise leave unset for auto-scaling (up to 250 concurrent invocations)
- **DLQ** - Create separately: `npx wrangler queues create my-dlq`

---

## Wrangler Commands

```bash
# Create queue
npx wrangler queues create my-queue
npx wrangler queues create my-queue --message-retention-period-secs 1209600  # 14 days

# Manage queues
npx wrangler queues list
npx wrangler queues info my-queue
npx wrangler queues delete my-queue  # ⚠️ Deletes ALL messages!

# Pause/Purge (March 2025 - NEW)
npx wrangler queues pause-delivery my-queue   # Pause processing, keep receiving
npx wrangler queues resume-delivery my-queue
npx wrangler queues purge my-queue            # ⚠️ Permanently deletes all messages!

# Consumer management
npx wrangler queues consumer add my-queue my-consumer-worker \
  --batch-size 50 --batch-timeout 10 --message-retries 5
npx wrangler queues consumer remove my-queue my-consumer-worker
```

---

## Limits & Quotas

| Feature | Limit |
|---------|-------|
| **Queues per account** | 10,000 |
| **Message size** | 128 KB (includes ~100 bytes metadata) |
| **Message retries** | 100 max |
| **Batch size** | 1-100 messages |
| **Batch timeout** | 0-60 seconds |
| **Messages per sendBatch** | 100 (or 256 KB total) |
| **Queue throughput** | 5,000 messages/second per queue |
| **Message retention** | 4 days (default), 14 days (max) |
| **Queue backlog size** | 25 GB per queue |
| **Concurrent consumers** | 250 (push-based, auto-scale) |
| **Consumer duration** | 15 minutes (wall clock) |
| **Consumer CPU time** | 30 seconds (default), 5 minutes (max) |
| **Visibility timeout** | 12 hours (pull consumers) |
| **Message delay** | 12 hours (max) |
| **API rate limit** | 1200 requests / 5 minutes |

---

## Pricing

**Requires Workers Paid plan** ($5/month)

**Operations Pricing:**
- First 1,000,000 operations/month: **FREE**
- After that: **$0.40 per million operations**

**What counts as an operation:**
- Each 64 KB chunk written, read, or deleted
- Messages >64 KB count as multiple operations:
  - 65 KB message = 2 operations
  - 127 KB message = 2 operations
  - 128 KB message = 2 operations

**Typical message lifecycle:**
- 1 write + 1 read + 1 delete = **3 operations**

**Retries:**
- Each retry = additional **read operation**
- Message retried 3 times = 1 write + 4 reads + 1 delete = **6 operations**

**Dead Letter Queue:**
- Writing to DLQ = additional **write operation**

**Cost examples:**
- 1M messages/month (no retries): ((1M × 3) - 1M) / 1M × $0.40 = **$0.80**
- 10M messages/month: ((10M × 3) - 1M) / 1M × $0.40 = **$11.60**
- 100M messages/month: ((100M × 3) - 1M) / 1M × $0.40 = **$119.60**

---


## Error Handling

### Common Errors

#### 1. Message Too Large

```typescript
// ❌ Bad: Message >128 KB
await env.MY_QUEUE.send({
  data: largeArray, // >128 KB
});

// ✅ Good: Check size before sending
const message = { data: largeArray };
const size = new TextEncoder().encode(JSON.stringify(message)).length;

if (size > 128000) {
  // Store in R2, send reference
  const key = `messages/${crypto.randomUUID()}.json`;
  await env.MY_BUCKET.put(key, JSON.stringify(message));
  await env.MY_QUEUE.send({ type: 'large-message', r2Key: key });
} else {
  await env.MY_QUEUE.send(message);
}
```

---

#### 2. Throughput Exceeded

```typescript
// ❌ Bad: Exceeding 5000 msg/s per queue
for (let i = 0; i < 10000; i++) {
  await env.MY_QUEUE.send({ id: i }); // Too fast!
}

// ✅ Good: Use sendBatch
const messages = Array.from({ length: 10000 }, (_, i) => ({
  body: { id: i },
}));

// Send in batches of 100
for (let i = 0; i < messages.length; i += 100) {
  await env.MY_QUEUE.sendBatch(messages.slice(i, i + 100));
}

// ✅ Even better: Rate limit with delay
for (let i = 0; i < messages.length; i += 100) {
  await env.MY_QUEUE.sendBatch(messages.slice(i, i + 100));
  if (i + 100 < messages.length) {
    await new Promise(resolve => setTimeout(resolve, 100)); // 100ms delay
  }
}
```

---

#### 3. Consumer Timeout

```typescript
// ❌ Bad: Long processing without CPU limit increase
export default {
  async queue(batch: MessageBatch): Promise<void> {
    for (const message of batch.messages) {
      await processForMinutes(message.body); // CPU timeout!
    }
  },
};

// ✅ Good: Increase CPU limit in wrangler.jsonc
```

**wrangler.jsonc:**

```jsonc
{
  "limits": {
    "cpu_ms": 300000  // 5 minutes (max allowed)
  }
}
```

---

#### 4. Backlog Growing

```typescript
// Issue: Consumer too slow, backlog growing

// ✅ Solution 1: Increase batch size
{
  "queues": {
    "consumers": [{
      "queue": "my-queue",
      "max_batch_size": 100  // Process more per invocation
    }]
  }
}

// ✅ Solution 2: Let concurrency auto-scale (don't set max_concurrency)

// ✅ Solution 3: Optimize consumer code
export default {
  async queue(batch: MessageBatch, env: Env): Promise<void> {
    // Process in parallel
    await Promise.all(
      batch.messages.map(async (message) => {
        await process(message.body);
        message.ack();
      })
    );
  },
};
```

---

## Critical Rules

**Always:**
- ✅ Configure DLQ for production (`dead_letter_queue` in consumer config)
- ✅ Use explicit `message.ack()` for non-idempotent ops (DB writes, API calls)
- ✅ Validate message size <128 KB before sending
- ✅ Use `sendBatch()` for multiple messages (more efficient)
- ✅ Implement exponential backoff: `60 * Math.pow(2, message.attempts - 1)`
- ✅ Let concurrency auto-scale (don't set `max_concurrency` unless upstream has rate limits)

**Never:**
- ❌ Never assume FIFO ordering - not guaranteed
- ❌ Never rely on implicit ack for non-idempotent ops - use explicit `ack()`
- ❌ Never send messages >128 KB - will fail (store in R2 instead)
- ❌ Never skip DLQ in production - failed messages DELETED PERMANENTLY without DLQ
- ❌ Never exceed 5,000 msg/s per queue (push consumers) or rate limits apply
- ❌ Never process messages synchronously - use `Promise.all()` for parallelism

---

## Troubleshooting

### Issue: Messages not being delivered to consumer

**Possible causes:**
1. Consumer not deployed
2. Wrong queue name in wrangler.jsonc
3. Delivery paused
4. Consumer throwing errors

**Solution:**

```bash
# Check queue info
npx wrangler queues info my-queue

# Check if delivery paused
npx wrangler queues resume-delivery my-queue

# Check consumer logs
npx wrangler tail my-consumer
```

---

### Issue: Entire batch retried when one message fails

**Cause:** Using implicit acknowledgement with non-idempotent operations

**Solution:** Use explicit ack()

```typescript
// ✅ Explicit ack
for (const message of batch.messages) {
  try {
    await dbWrite(message.body);
    message.ack(); // Only ack on success
  } catch (error) {
    console.error(`Failed: ${message.id}`);
    // Don't ack - will retry
  }
}
```

---

### Issue: Messages deleted without processing

**Cause:** No Dead Letter Queue configured

**Solution:**

```bash
# Create DLQ
npx wrangler queues create my-dlq

# Add to consumer config
```

```jsonc
{
  "queues": {
    "consumers": [{
      "queue": "my-queue",
      "dead_letter_queue": "my-dlq"
    }]
  }
}
```

---

### Issue: Consumer not auto-scaling

**Possible causes:**
1. `max_concurrency` set to 1
2. Consumer returning errors (not processing)
3. Batch processing too fast (no backlog)

**Solution:**

```jsonc
{
  "queues": {
    "consumers": [{
      "queue": "my-queue",
      // Don't set max_concurrency - let it auto-scale
      "max_batch_size": 50  // Increase batch size instead
    }]
  }
}
```

---

## Related Documentation

- [Cloudflare Queues Docs](https://developers.cloudflare.com/queues/)
- [How Queues Works](https://developers.cloudflare.com/queues/reference/how-queues-works/)
- [JavaScript APIs](https://developers.cloudflare.com/queues/configuration/javascript-apis/)
- [Batching & Retries](https://developers.cloudflare.com/queues/configuration/batching-retries/)
- [Consumer Concurrency](https://developers.cloudflare.com/queues/configuration/consumer-concurrency/)
- [Dead Letter Queues](https://developers.cloudflare.com/queues/configuration/dead-letter-queues/)
- [Wrangler Commands](https://developers.cloudflare.com/queues/reference/wrangler-commands/)
- [Limits](https://developers.cloudflare.com/queues/platform/limits/)
- [Pricing](https://developers.cloudflare.com/queues/platform/pricing/)

---

**Last Updated**: 2025-10-21
**Version**: 1.0.0
**Maintainer**: Jeremy Dawes | jeremy@jezweb.net
