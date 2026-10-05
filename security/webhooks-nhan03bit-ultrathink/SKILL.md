---
name: webhooks
description: Webhook design patterns — delivery, retry with exponential backoff, HMAC signature verification, payload validation, idempotency keys
layer: utility
category: backend
triggers:
  - "webhook"
  - "webhooks"
  - "webhook signature"
  - "hmac verification"
  - "idempotency key"
  - "webhook retry"
linksTo:
  - api-designer
  - message-queues
  - authentication
linkedFrom:
  - microservices
  - stripe
---

# Webhooks Skill

## Purpose

Design patterns for sending and receiving webhooks reliably: HMAC signature verification, exponential backoff retries, idempotency, and payload validation.

## Receiving: Signature Verification

```typescript
import { createHmac, timingSafeEqual } from 'crypto';

function verifyWebhookSignature(payload: string, signature: string, secret: string): boolean {
  const expected = `sha256=${createHmac('sha256', secret).update(payload).digest('hex')}`;
  const a = Buffer.from(expected, 'utf8');
  const b = Buffer.from(signature, 'utf8');
  return a.length === b.length && timingSafeEqual(a, b);
}
```

## Receiving: Handler with Idempotency

```typescript
// app/api/webhooks/route.ts
export async function POST(req: NextRequest) {
  const rawBody = await req.text();
  const signature = req.headers.get('x-webhook-signature') ?? '';

  if (!verifyWebhookSignature(rawBody, signature, process.env.WEBHOOK_SECRET!)) {
    return NextResponse.json({ error: 'Invalid signature' }, { status: 401 });
  }

  const event = webhookEventSchema.parse(JSON.parse(rawBody));
  const idempotencyKey = event.id;

  // Skip if already processed
  const existing = await db.webhookEvent.findUnique({ where: { idempotencyKey } });
  if (existing) return NextResponse.json({ status: 'already_processed' });

  try {
    await processWebhookEvent(event);
    await db.webhookEvent.create({
      data: { idempotencyKey, eventType: event.type, processedAt: new Date() },
    });
    return NextResponse.json({ status: 'processed' });
  } catch {
    return NextResponse.json({ error: 'Processing failed' }, { status: 500 });
  }
}
```

## Receiving: Payload Validation

```typescript
import { z } from 'zod';

const webhookEventSchema = z.discriminatedUnion('type', [
  z.object({
    type: z.literal('order.created'),
    id: z.string().uuid(),
    data: z.object({ orderId: z.string(), amount: z.number().positive() }),
  }),
  z.object({
    type: z.literal('order.cancelled'),
    id: z.string().uuid(),
    data: z.object({ orderId: z.string(), reason: z.string().optional() }),
  }),
]);
```

## Sending: Delivery with Exponential Backoff

```typescript
async function deliverWebhook(url: string, secret: string, event: WebhookEvent) {
  const payload = JSON.stringify(event);
  const signature = `sha256=${createHmac('sha256', secret).update(payload).digest('hex')}`;

  for (let attempt = 0; attempt <= 5; attempt++) {
    try {
      const res = await fetch(url, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'X-Webhook-Signature': signature,
          'X-Webhook-Id': event.id,
        },
        body: payload,
        signal: AbortSignal.timeout(10_000),
      });
      if (res.ok) return { success: true, attempts: attempt + 1 };
      if (res.status >= 400 && res.status < 500 && res.status !== 429) {
        return { success: false, attempts: attempt + 1 }; // Don't retry 4xx
      }
    } catch { /* network error, will retry */ }

    if (attempt < 5) {
      const delay = Math.min(1000 * Math.pow(2, attempt) + Math.random() * 1000, 30_000);
      await new Promise((r) => setTimeout(r, delay));
    }
  }
  return { success: false, attempts: 6 };
}
```

## Best Practices

1. **Always verify signatures** with timing-safe comparison before processing
2. **Always use idempotency keys** — webhooks may be delivered more than once
3. **Respond 200 quickly**, then process asynchronously for heavy work
4. **Don't retry on 4xx** (except 429) — the payload itself is the problem
5. **Include timestamps** in signed payloads to prevent replay attacks
6. **Use a job queue** (BullMQ, SQS) for production delivery instead of in-process retries
7. **Log all events** with idempotency keys for debugging delivery issues
