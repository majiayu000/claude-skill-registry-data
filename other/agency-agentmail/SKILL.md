---
name: agency-agentmail
description: Integrate AgentMail (agentmail.to) for AI-powered email in the Social Media Agency. Use when sending client reports, approval notifications, outreach emails, managing per-org inboxes, handling email replies via webhooks/websockets, or attaching reports. Based on the official AgentMail skill (skills.sh/agentmail-to/agentmail-skills/agentmail).
---

# AgentMail Integration for Social Media Agency

AgentMail is an API-first email platform for AI agents. This skill covers the full SDK surface tailored to Agency use cases: multi-tenant org inboxes, client report delivery, approval notifications, prospecting outreach, reply handling, and real-time events.

**Docs**: https://docs.agentmail.to
**Console**: https://console.agentmail.to
**Official Skill**: https://skills.sh/agentmail-to/agentmail-skills/agentmail
**Base URL**: `https://api.agentmail.to/v0/`

## Use Cases

1. **Client Reports** — Send automated performance reports with PDF attachments
2. **Approval Notifications** — Notify managers when content is ready for review
3. **Client Onboarding** — Welcome emails when new clients are added
4. **Outreach** — Cold outreach to prospective agency clients
5. **Reply Handling** — Process client replies to reports or outreach emails
6. **Bounce Tracking** — Detect invalid emails for outreach lists

## Environment Variables

```
AGENTMAIL_API_KEY=am_...                    # Required
AGENTMAIL_DEFAULT_DOMAIN=yourdomain.com     # Custom domain
```

## SDK Setup

```python
# Python
from agentmail import AgentMail
client = AgentMail(api_key="YOUR_API_KEY")
```

```typescript
// TypeScript
import { AgentMailClient } from "agentmail";
const client = new AgentMailClient({ apiKey: "YOUR_API_KEY" });
```

## Inboxes

Each agency organization gets a dedicated inbox. Uses `client_id` for idempotent retries.

```python
# Create inbox with custom domain.
# The Python SDK (>=0.4) takes a request model, NOT keyword arguments —
# client.inboxes.create(username=...) raises TypeError.
from agentmail.inboxes import CreateInboxRequest

inbox = client.inboxes.create(
    request=CreateInboxRequest(
        username="agency-org123",
        domain="yourdomain.com",       # must be a VERIFIED domain
        display_name="Demo Agency",
        client_id="org-<uuid>",
    )
)

# List, get, delete (inbox_id is the full address, and is positional)
inboxes = client.inboxes.list()
inbox = client.inboxes.get("agency-org123@yourdomain.com")
client.inboxes.delete("agency-org123@yourdomain.com")
```

```typescript
const inbox = await client.inboxes.create({
  username: "agency-org123",
  domain: "yourdomain.com",
  displayName: "Demo Agency",
  clientId: "org-<uuid>",
});
```

## Messages — Client Report Delivery

Always send both `text` and `html` for best deliverability. Use labels to categorize emails.

```python
# Send performance report to client
import base64

with open("report.pdf", "rb") as f:
    content = base64.b64encode(f.read()).decode()

client.inboxes.messages.send(
    inbox_id="agency-org123@yourdomain.com",
    to="client@sunrisecoffee.com",
    subject="Monthly Social Media Report — March 2026",
    text="Hi Sarah, please find your monthly social media performance report attached.",
    html="<p>Hi Sarah,</p><p>Please find your monthly social media performance report attached.</p>",
    attachments=[{
        "content": content,
        "filename": "sunrise_coffee_march_2026.pdf",
        "content_type": "application/pdf",
    }],
    labels=["report", "client-report", "sunrise-coffee"],
)
```

```typescript
const content = Buffer.from(reportBytes).toString("base64");
await client.inboxes.messages.send({
  inboxId: "agency-org123@yourdomain.com",
  to: "client@sunrisecoffee.com",
  subject: "Monthly Social Media Report — March 2026",
  text: "Hi Sarah, please find your monthly social media performance report attached.",
  attachments: [
    { content, filename: "sunrise_coffee_march_2026.pdf", contentType: "application/pdf" },
  ],
  labels: ["report", "client-report"],
});
```

## Messages — Outreach

```python
# Cold outreach to prospective client
client.inboxes.messages.send(
    inbox_id="agency-org123@yourdomain.com",
    to="owner@targetbusiness.com",
    subject="Grow Your Social Media Presence — Free Audit",
    text="Hi Alex, I noticed your brand has great potential on social media...",
    html="<p>Hi Alex,</p><p>I noticed your brand has great potential on social media...</p>",
    labels=["outreach", "cold-email", "pending"],
)
```

## Messages — List & Update

```python
# List client replies
messages = client.inboxes.messages.list(
    inbox_id="agency-org123@yourdomain.com",
    labels=["received"],
)
for msg in messages.messages:
    print(msg.subject, msg.extracted_text or msg.text)

# Reply to client
client.inboxes.messages.reply(
    inbox_id="agency-org123@yourdomain.com",
    message_id="msg_123",
    text="Thanks for your feedback! We'll adjust the content strategy accordingly.",
)

# Update labels after processing
client.inboxes.messages.update(
    inbox_id="agency-org123@yourdomain.com",
    message_id="msg_123",
    add_labels=["replied", "processed"],
    remove_labels=["pending"],
)
```

## Threads

Threads group related messages in a conversation. Useful for tracking multi-step client communication (report → feedback → revision).

```python
threads = client.inboxes.threads.list(
    inbox_id="agency-org123@yourdomain.com",
    labels=["unreplied"],
)

thread = client.inboxes.threads.get(
    inbox_id="agency-org123@yourdomain.com",
    thread_id="thd_123",
)
```

## Drafts

Create drafts for human-in-the-loop approval before sending outreach or client emails.

```python
draft = client.inboxes.drafts.create(
    inbox_id="agency-org123@yourdomain.com",
    to="prospect@business.com",
    subject="Social Media Growth Opportunity",
    text="Hi, I'd love to discuss how we can help grow your social presence...",
)

# Manager reviews and approves → send
client.inboxes.drafts.send(
    inbox_id="agency-org123@yourdomain.com",
    draft_id=draft.draft_id,
)
```

## Pods (Multi-Tenant Isolation)

Each agency organization can be isolated in a pod for complete data separation.

```python
pod = client.pods.create(client_id=f"org-{org_id}")
inbox = client.inboxes.create(pod_id=pod.pod_id)
inboxes = client.inboxes.list(pod_id=pod.pod_id)
```

## Webhooks (Real-Time Events)

Register a webhook to receive events when clients reply to reports or outreach emails bounce.

```python
webhook = client.webhooks.create(
    url="https://your-api.fly.dev/api/v1/agentmail/webhook",
    event_types=["message.received", "message.bounced"],
)
```

### Webhook Payload Structure

```json
{
  "type": "event",
  "event_type": "message.received",
  "event_id": "evt_123abc",
  "message": {
    "inbox_id": "agency-org123@yourdomain.com",
    "thread_id": "thd_789",
    "message_id": "msg_123",
    "from": [{"name": "Sarah", "email": "sarah@sunrisecoffee.com"}],
    "to": [{"email": "agency-org123@yourdomain.com"}],
    "subject": "Re: Monthly Social Media Report",
    "text": "Thanks for the report! Can we increase posting frequency?",
    "labels": ["received"],
    "created_at": "2026-03-22T10:00:00Z"
  }
}
```

### Webhook Event Types

| Event | Use Case |
|-------|----------|
| `message.received` | Client replied to report or outreach response |
| `message.sent` | Confirmation that email was sent |
| `message.delivered` | Email delivered to recipient's server |
| `message.bounced` | Invalid email, remove from outreach list |
| `message.complained` | Recipient marked as spam |
| `message.rejected` | Email rejected before sending |

### FastAPI Webhook Handler

```python
# backend/src/agency/routers/agentmail_webhook.py
from fastapi import APIRouter, Depends, Request
from agency.dependencies import get_db

router = APIRouter(prefix="/agentmail", tags=["AgentMail Webhook"])

@router.post("/webhook")
async def handle_agentmail_webhook(
    request: Request,
    db=Depends(get_db),
):
    payload = await request.json()
    event_type = payload.get("event_type")

    if event_type == "message.received":
        message = payload.get("message", {})
        from_email = message.get("from", [{}])[0].get("email")
        labels = message.get("labels", [])

        if from_email:
            logger.info("email_received", from_email=from_email, labels=labels)
            # Route to appropriate handler based on thread labels

    elif event_type == "message.bounced":
        message = payload.get("message", {})
        logger.warning("email_bounced", message_id=message.get("message_id"))
        # Remove from outreach list or mark client email as invalid

    return {"status": "ok"}
```

## WebSockets (Real-Time Events)

For local development or when no public URL is available.

```python
from agentmail import AgentMail, Subscribe, MessageReceivedEvent

client = AgentMail(api_key="YOUR_API_KEY")

with client.websockets.connect() as socket:
    socket.send_subscribe(Subscribe(
        inbox_ids=["agency-org123@yourdomain.com"],
        event_types=["message.received"],
    ))

    for event in socket:
        if isinstance(event, MessageReceivedEvent):
            print(f"Reply from: {event.message.from_}")
            print(f"Subject: {event.message.subject}")
```

### Async WebSocket

```python
import asyncio
from agentmail import AsyncAgentMail, Subscribe, MessageReceivedEvent

client = AsyncAgentMail(api_key="YOUR_API_KEY")

async def listen_for_replies(inbox_ids: list[str]):
    async with client.websockets.connect() as socket:
        await socket.send_subscribe(Subscribe(inbox_ids=inbox_ids))
        async for event in socket:
            if isinstance(event, MessageReceivedEvent):
                await process_client_reply(event.message)
```

## Email Labels Convention

| Label | Applied When |
|-------|-------------|
| `client-report` | Performance report sent to client |
| `approval-notification` | Content approval request sent |
| `onboarding` | Client welcome email sent |
| `outreach` | Cold outreach email sent |
| `reminder` | Follow-up reminder sent |
| `pending` | Awaiting response |
| `replied` | Recipient has replied |
| `processed` | Reply has been handled |
| `bounced` | Email delivery failed |

## Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│  Agency Backend (FastAPI)                                       │
│                                                                 │
│  ┌──────────────────┐    ┌────────────────────────────────────┐ │
│  │  report_worker.py │───>│  agentmail_client.py               │ │
│  │  (client reports) │    │  - create_org_inbox() [pods]       │ │
│  └──────────────────┘    │  - send_report() [attachments]     │ │
│                           │  - send_outreach() [labels]        │ │
│  ┌──────────────────┐    │  - list_inbox_messages() [threads]  │ │
│  │  email_worker.py  │───>│                                    │ │
│  │  (outreach,       │    └─────────┬──────────────────────────┘ │
│  │   notifications)  │             │                             │
│  └──────────────────┘             │                             │
│                                    │                             │
│  ┌──────────────────┐             │                             │
│  │  organizations.py │             │                             │
│  │  POST /email/setup│             │                             │
│  │  GET /email/status│             │                             │
│  └──────────────────┘             │                             │
│                                    │                             │
│  ┌──────────────────┐             │                             │
│  │ agentmail_webhook │<────── webhooks (message.received,       │
│  │  POST /webhook    │        message.bounced)                  │
│  └──────────────────┘             │                             │
└────────────────────────────────────┼─────────────────────────────┘
                                     │
                                     ▼
                           ┌──────────────────┐
                           │  AgentMail API    │
                           │  api.agentmail.to │
                           └──────────────────┘
```

## Idempotency

Use `client_id` for safe retries on all create operations.

```python
inbox = client.inboxes.create(client_id=f"org-{org_id}")
# Retrying with same client_id returns the original inbox, not a duplicate
```

## Error Handling

- Always wrap AgentMail calls in try/except and log failures via structlog
- Use `client_id` for idempotent inbox creation (safe to retry)
- Handle 429 rate limit responses with exponential backoff
- Use `asyncio.to_thread()` for sync SDK calls in async FastAPI handlers

## Full SDK Reference

| Method | Purpose |
|--------|---------|
| `client.inboxes.create(username?, domain?, display_name?, client_id?, pod_id?)` | Create inbox |
| `client.inboxes.list(pod_id?)` | List inboxes |
| `client.inboxes.get(inbox_id)` | Get inbox details |
| `client.inboxes.delete(inbox_id)` | Delete inbox |
| `client.inboxes.messages.send(inbox_id, to, subject, text, html?, labels?, attachments?)` | Send email |
| `client.inboxes.messages.reply(inbox_id, message_id, text, html?)` | Reply to message |
| `client.inboxes.messages.list(inbox_id, limit?, page_token?, labels?)` | List messages |
| `client.inboxes.messages.get(inbox_id, message_id)` | Get message |
| `client.inboxes.messages.update(inbox_id, message_id, add_labels?, remove_labels?)` | Update labels |
| `client.inboxes.messages.get_attachment(inbox_id, message_id, attachment_id)` | Get attachment |
| `client.inboxes.threads.list(inbox_id, labels?)` | List threads |
| `client.inboxes.threads.get(inbox_id, thread_id)` | Get thread |
| `client.threads.list()` | List all threads (org-wide) |
| `client.inboxes.drafts.create(inbox_id, to, subject, text, html?)` | Create draft |
| `client.inboxes.drafts.send(inbox_id, draft_id)` | Send draft |
| `client.pods.create(client_id?)` | Create pod |
| `client.pods.list()` | List pods |
| `client.webhooks.create(url, event_types?)` | Register webhook |
| `client.webhooks.list()` | List webhooks |
| `client.webhooks.delete(webhook_id)` | Delete webhook |
| `client.websockets.connect()` | Open WebSocket connection |

Messages include `extracted_text` / `extracted_html` for reply content without quoted history.
