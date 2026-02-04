---
name: webhook-handlers
description: Webhook event handling patterns for email tracking (sent, delivered, bounced, opened, clicked). Use when implementing email event webhooks, signature verification, processing delivery events, logging email analytics, or building real-time email status tracking.
allowed-tools: Read, Write, Bash, Grep
---

# Webhook Handlers Skill

Comprehensive patterns and templates for implementing secure webhook handlers with Resend, covering event types, signature verification, and event processing strategies.

## Use When

- Implementing webhook endpoints for email events (sent, delivered, bounced, opened, clicked)
- Setting up signature verification for webhook authenticity
- Building email tracking and analytics systems
- Processing bounce and complaint events for list management
- Creating real-time email status dashboards
- Logging delivery events to database
- Implementing retry logic for webhook processing
- Handling multiple webhook events in parallel

## Webhook Event Types

### Resend Webhook Events

Resend sends webhooks for the following email events:

#### 1. Email Sent

Triggered when email is accepted by Resend.

```json
{
  "type": "email.sent",
  "created_at": "2024-01-15T10:30:00Z",
  "data": {
    "email_id": "123e4567-e89b-12d3-a456-426614174000",
    "from": "notifications@example.com",
    "to": "recipient@example.com",
    "subject": "Welcome to Example",
    "created_at": "2024-01-15T10:30:00Z"
  }
}
```

#### 2. Email Delivered

Triggered when email reaches recipient's mail server.

```json
{
  "type": "email.delivered",
  "created_at": "2024-01-15T10:35:00Z",
  "data": {
    "email_id": "123e4567-e89b-12d3-a456-426614174000",
    "from": "notifications@example.com",
    "to": "recipient@example.com",
    "created_at": "2024-01-15T10:35:00Z"
  }
}
```

#### 3. Email Bounced

Triggered when email cannot be delivered (hard bounce).

```json
{
  "type": "email.bounced",
  "created_at": "2024-01-15T10:40:00Z",
  "data": {
    "email_id": "123e4567-e89b-12d3-a456-426614174000",
    "from": "notifications@example.com",
    "to": "invalid@example.com",
    "reason": "Mailbox does not exist",
    "created_at": "2024-01-15T10:40:00Z"
  }
}
```

#### 4. Email Opened

Triggered when recipient opens the email (requires pixel tracking).

```json
{
  "type": "email.opened",
  "created_at": "2024-01-15T11:00:00Z",
  "data": {
    "email_id": "123e4567-e89b-12d3-a456-426614174000",
    "from": "notifications@example.com",
    "to": "recipient@example.com",
    "user_agent": "Mozilla/5.0...",
    "ip_address": "192.168.1.1",
    "created_at": "2024-01-15T11:00:00Z"
  }
}
```

#### 5. Email Clicked

Triggered when recipient clicks a link in the email.

```json
{
  "type": "email.clicked",
  "created_at": "2024-01-15T11:05:00Z",
  "data": {
    "email_id": "123e4567-e89b-12d3-a456-426614174000",
    "from": "notifications@example.com",
    "to": "recipient@example.com",
    "link": "https://example.com/promo",
    "user_agent": "Mozilla/5.0...",
    "ip_address": "192.168.1.1",
    "created_at": "2024-01-15T11:05:00Z"
  }
}
```

#### 6. Email Complained

Triggered when recipient marks email as spam.

```json
{
  "type": "email.complained",
  "created_at": "2024-01-15T11:10:00Z",
  "data": {
    "email_id": "123e4567-e89b-12d3-a456-426614174000",
    "from": "notifications@example.com",
    "to": "recipient@example.com",
    "created_at": "2024-01-15T11:10:00Z"
  }
}
```

## Signature Verification Patterns

### TypeScript Signature Verification

Verify webhook authenticity using HMAC-SHA256:

```typescript
import crypto from 'crypto';

interface WebhookEvent {
  type: string;
  created_at: string;
  data: Record<string, any>;
}

function verifyWebhookSignature(
  payload: string,
  signature: string,
  signingSecret: string
): boolean {
  const expectedSignature = crypto
    .createHmac('sha256', signingSecret)
    .update(payload)
    .digest('hex');

  return crypto.timingSafeEqual(
    Buffer.from(signature),
    Buffer.from(expectedSignature)
  );
}

// Usage in Express middleware
import express from 'express';

const webhookRouter = express.Router();

webhookRouter.post('/webhooks/resend', express.raw({ type: 'application/json' }), (req, res) => {
  const signature = req.headers['x-resend-signature'] as string;
  const payload = req.body.toString();

  if (!verifyWebhookSignature(payload, signature, process.env.RESEND_WEBHOOK_SECRET!)) {
    return res.status(401).json({ error: 'Invalid signature' });
  }

  const event: WebhookEvent = JSON.parse(payload);
  handleWebhookEvent(event);

  res.json({ success: true });
});

export default webhookRouter;
```

### Python Signature Verification

```python
import hmac
import hashlib
import json
from typing import Tuple

def verify_webhook_signature(
    payload: str,
    signature: str,
    signing_secret: str
) -> bool:
    """Verify Resend webhook signature using HMAC-SHA256."""
    expected_signature = hmac.new(
        signing_secret.encode(),
        payload.encode(),
        hashlib.sha256
    ).hexdigest()

    return hmac.compare_digest(signature, expected_signature)


def get_signature_from_headers(headers: dict) -> str:
    """Extract signature from request headers."""
    return headers.get('x-resend-signature', '')
```

## Event Processing Strategies

### TypeScript Event Handler

```typescript
interface EmailEvent {
  type: 'sent' | 'delivered' | 'bounced' | 'opened' | 'clicked' | 'complained';
  created_at: string;
  data: {
    email_id: string;
    from: string;
    to: string;
    [key: string]: any;
  };
}

async function handleWebhookEvent(event: EmailEvent): Promise<void> {
  try {
    // Log the event
    console.log(`Processing webhook: ${event.type}`, {
      email_id: event.data.email_id,
      timestamp: event.created_at,
    });

    // Route to specific handler
    switch (event.type) {
      case 'email.sent':
        await handleEmailSent(event.data);
        break;

      case 'email.delivered':
        await handleEmailDelivered(event.data);
        break;

      case 'email.bounced':
        await handleEmailBounced(event.data);
        break;

      case 'email.opened':
        await handleEmailOpened(event.data);
        break;

      case 'email.clicked':
        await handleEmailClicked(event.data);
        break;

      case 'email.complained':
        await handleEmailComplained(event.data);
        break;

      default:
        console.warn(`Unknown event type: ${event.type}`);
    }
  } catch (error) {
    console.error('Error handling webhook event:', error);
    throw error;
  }
}

// Individual event handlers
async function handleEmailSent(data: any): Promise<void> {
  // Update email status in database
  await db.emails.update(
    { id: data.email_id },
    {
      status: 'sent',
      sent_at: new Date(data.created_at),
      updated_at: new Date(),
    }
  );
}

async function handleEmailDelivered(data: any): Promise<void> {
  await db.emails.update(
    { id: data.email_id },
    {
      status: 'delivered',
      delivered_at: new Date(data.created_at),
      updated_at: new Date(),
    }
  );
}

async function handleEmailBounced(data: any): Promise<void> {
  // Update status and mark recipient as invalid
  await db.emails.update(
    { id: data.email_id },
    {
      status: 'bounced',
      bounce_reason: data.reason,
      bounced_at: new Date(data.created_at),
      updated_at: new Date(),
    }
  );

  // Add to bounce list
  await db.bounced_emails.create({
    email: data.to,
    reason: data.reason,
    bounced_at: new Date(data.created_at),
  });
}

async function handleEmailOpened(data: any): Promise<void> {
  await db.email_events.create({
    email_id: data.email_id,
    event_type: 'opened',
    user_agent: data.user_agent,
    ip_address: data.ip_address,
    created_at: new Date(data.created_at),
  });
}

async function handleEmailClicked(data: any): Promise<void> {
  await db.email_events.create({
    email_id: data.email_id,
    event_type: 'clicked',
    link: data.link,
    user_agent: data.user_agent,
    ip_address: data.ip_address,
    created_at: new Date(data.created_at),
  });
}

async function handleEmailComplained(data: any): Promise<void> {
  await db.emails.update(
    { id: data.email_id },
    {
      status: 'complained',
      complained_at: new Date(data.created_at),
      updated_at: new Date(),
    }
  );

  // Add to suppression list
  await db.suppressed_emails.create({
    email: data.to,
    reason: 'complaint',
    created_at: new Date(data.created_at),
  });
}
```

### Python Event Handler

```python
from enum import Enum
from datetime import datetime
from typing import Any, Dict

class EventType(Enum):
    SENT = "email.sent"
    DELIVERED = "email.delivered"
    BOUNCED = "email.bounced"
    OPENED = "email.opened"
    CLICKED = "email.clicked"
    COMPLAINED = "email.complained"


async def handle_webhook_event(event: Dict[str, Any]) -> None:
    """Route webhook events to appropriate handlers."""
    event_type = event.get('type')
    event_data = event.get('data', {})

    handlers = {
        EventType.SENT.value: handle_email_sent,
        EventType.DELIVERED.value: handle_email_delivered,
        EventType.BOUNCED.value: handle_email_bounced,
        EventType.OPENED.value: handle_email_opened,
        EventType.CLICKED.value: handle_email_clicked,
        EventType.COMPLAINED.value: handle_email_complained,
    }

    handler = handlers.get(event_type)
    if handler:
        await handler(event_data)
    else:
        print(f"Unknown event type: {event_type}")


async def handle_email_sent(data: Dict[str, Any]) -> None:
    """Update email status to sent."""
    await db.emails.update(
        {"id": data["email_id"]},
        {
            "status": "sent",
            "sent_at": datetime.fromisoformat(data["created_at"]),
        }
    )


async def handle_email_delivered(data: Dict[str, Any]) -> None:
    """Update email status to delivered."""
    await db.emails.update(
        {"id": data["email_id"]},
        {
            "status": "delivered",
            "delivered_at": datetime.fromisoformat(data["created_at"]),
        }
    )


async def handle_email_bounced(data: Dict[str, Any]) -> None:
    """Handle bounce event and add to suppression list."""
    await db.emails.update(
        {"id": data["email_id"]},
        {
            "status": "bounced",
            "bounce_reason": data.get("reason"),
        }
    )

    await db.bounced_emails.create({
        "email": data["to"],
        "reason": data.get("reason"),
        "bounced_at": datetime.fromisoformat(data["created_at"]),
    })


async def handle_email_opened(data: Dict[str, Any]) -> None:
    """Log email open event."""
    await db.email_events.create({
        "email_id": data["email_id"],
        "event_type": "opened",
        "user_agent": data.get("user_agent"),
        "ip_address": data.get("ip_address"),
        "created_at": datetime.fromisoformat(data["created_at"]),
    })


async def handle_email_clicked(data: Dict[str, Any]) -> None:
    """Log email click event."""
    await db.email_events.create({
        "email_id": data["email_id"],
        "event_type": "clicked",
        "link": data.get("link"),
        "user_agent": data.get("user_agent"),
        "ip_address": data.get("ip_address"),
        "created_at": datetime.fromisoformat(data["created_at"]),
    })


async def handle_email_complained(data: Dict[str, Any]) -> None:
    """Handle complaint event and add to suppression list."""
    await db.emails.update(
        {"id": data["email_id"]},
        {
            "status": "complained",
        }
    )

    await db.suppressed_emails.create({
        "email": data["to"],
        "reason": "complaint",
        "created_at": datetime.fromisoformat(data["created_at"]),
    })
```

## Database Logging Patterns

### TypeScript Database Schema

```typescript
// Prisma schema example

model Email {
  id                String    @id @default(uuid())
  resend_id         String    @unique
  from              String
  to                String
  subject           String
  status            String    @default("sent") // sent, delivered, bounced, opened, complained
  sent_at           DateTime?
  delivered_at      DateTime?
  bounced_at        DateTime?
  complained_at     DateTime?
  bounce_reason     String?
  created_at        DateTime  @default(now())
  updated_at        DateTime  @updatedAt
  events            EmailEvent[]

  @@index([status])
  @@index([to])
  @@index([created_at])
}

model EmailEvent {
  id          String    @id @default(uuid())
  email_id    String
  email       Email     @relation(fields: [email_id], references: [id], onDelete: Cascade)
  event_type  String    // opened, clicked
  link        String?
  user_agent  String?
  ip_address  String?
  created_at  DateTime  @default(now())

  @@index([email_id])
  @@index([event_type])
  @@index([created_at])
}

model BouncedEmail {
  id          String    @id @default(uuid())
  email       String    @unique
  reason      String
  bounced_at  DateTime
  created_at  DateTime  @default(now())

  @@index([email])
}

model SuppressedEmail {
  id          String    @id @default(uuid())
  email       String    @unique
  reason      String    // complaint, bounce, unsubscribe
  created_at  DateTime  @default(now())

  @@index([email])
}
```

### PostgreSQL Schema

```sql
CREATE TABLE emails (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  resend_id VARCHAR UNIQUE NOT NULL,
  from_address VARCHAR NOT NULL,
  to_address VARCHAR NOT NULL,
  subject TEXT NOT NULL,
  status VARCHAR DEFAULT 'sent',
  sent_at TIMESTAMP,
  delivered_at TIMESTAMP,
  bounced_at TIMESTAMP,
  complained_at TIMESTAMP,
  bounce_reason TEXT,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE email_events (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  email_id UUID NOT NULL REFERENCES emails(id) ON DELETE CASCADE,
  event_type VARCHAR NOT NULL,
  link TEXT,
  user_agent TEXT,
  ip_address INET,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE bounced_emails (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  email VARCHAR UNIQUE NOT NULL,
  reason TEXT,
  bounced_at TIMESTAMP NOT NULL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE suppressed_emails (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  email VARCHAR UNIQUE NOT NULL,
  reason VARCHAR NOT NULL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_emails_status ON emails(status);
CREATE INDEX idx_emails_to ON emails(to_address);
CREATE INDEX idx_emails_created ON emails(created_at);
CREATE INDEX idx_email_events_email_id ON email_events(email_id);
CREATE INDEX idx_email_events_type ON email_events(event_type);
CREATE INDEX idx_bounced_emails_email ON bounced_emails(email);
CREATE INDEX idx_suppressed_emails_email ON suppressed_emails(email);
```

## Webhook Setup

### Setting Webhook URL in Resend

```typescript
import { Resend } from 'resend';

const resend = new Resend(process.env.RESEND_API_KEY);

async function setupWebhook() {
  const response = await resend.webhooks.create({
    events: [
      'email.sent',
      'email.delivered',
      'email.bounced',
      'email.opened',
      'email.clicked',
      'email.complained',
    ],
    url: 'https://your-domain.com/api/webhooks/resend',
  });

  console.log('Webhook created:', response.data);
  // Save the webhook ID and signing secret securely
}
```

### Retrieving Webhook Details

```typescript
async function getWebhookDetails(webhookId: string) {
  const response = await resend.webhooks.get(webhookId);
  return response.data;
}

async function listWebhooks() {
  const response = await resend.webhooks.list();
  return response.data;
}
```

## Environment Variables Required

```bash
RESEND_API_KEY=your_resend_key_here
RESEND_WEBHOOK_SECRET=your_webhook_signing_secret_here
DATABASE_URL=your_database_connection_string
```

## Error Handling and Retries

### Webhook Retry Pattern

```typescript
interface WebhookTask {
  id: string;
  event: WebhookEvent;
  retries: number;
  max_retries: number;
  next_retry_at: Date;
}

async function processWebhookWithRetry(
  event: WebhookEvent,
  maxRetries: number = 3
): Promise<void> {
  let lastError: Error | null = null;

  for (let attempt = 1; attempt <= maxRetries; attempt++) {
    try {
      await handleWebhookEvent(event);
      console.log(`Webhook processed successfully: ${event.data.email_id}`);
      return;
    } catch (error) {
      lastError = error as Error;
      console.error(`Attempt ${attempt} failed:`, error);

      if (attempt < maxRetries) {
        // Exponential backoff: 5s, 25s, 125s
        const delay = Math.pow(5, attempt) * 1000;
        await new Promise(resolve => setTimeout(resolve, delay));
      }
    }
  }

  // Store failed event for manual review
  await db.failed_webhooks.create({
    event_id: event.data.email_id,
    event_type: event.type,
    payload: JSON.stringify(event),
    error: lastError?.message,
    created_at: new Date(),
  });

  throw lastError;
}
```

## Best Practices

- Implement idempotency: Track processed webhook IDs to prevent duplicate processing
- Use database transactions for atomic updates
- Log all webhook events for auditing and debugging
- Implement proper error handling and retry logic
- Verify webhook signatures on every request
- Use environment variables for sensitive data (never hardcode)
- Monitor webhook processing latency
- Set up alerts for failed webhooks
- Archive old webhook events for compliance

## Examples Directory Structure

- `nextjs-webhook/` - Next.js API route webhook handler
- `fastapi-webhook/` - FastAPI webhook handler with FastAPI patterns
- `event-processing/` - Database logging and event analytics

See individual example README files for complete code and usage patterns.

## Related Skills

- **email-delivery** - Email sending patterns and batch operations
- **email-templates** - HTML template management and rendering
- **email-validation** - Recipient address validation

## Resources

- [Resend Webhooks Documentation](https://resend.com/docs/webhooks)
- [Webhook Event Reference](https://resend.com/docs/webhooks/events)
- [Webhook Signature Verification](https://resend.com/docs/webhooks/signature-verification)
- [Resend API Reference](https://resend.com/docs/api-reference)

## Security Notes

- Webhook signing secrets must be stored in environment variables only
- Always verify webhook signatures before processing
- Use HTTPS for webhook endpoints (never HTTP)
- Implement rate limiting on webhook endpoints
- Store webhook payloads securely (may contain PII)
- Use database transactions for atomic operations
- Never hardcode API keys or secrets
- Implement request timeouts to prevent hanging
- Log security-relevant events for compliance
