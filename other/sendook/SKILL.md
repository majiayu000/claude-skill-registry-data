---
name: sendook-openclaw
description: Read and send emails from an existing Sendook inbox. Use when an AI agent needs to check for new emails, read messages, reply to conversations, or send new emails from a pre-configured inbox. Limited to message operations only — no inbox creation, domain management, or webhook configuration.
homepage: https://github.com/obaid/sendook-skills
metadata: { "openclaw": { "requires": { "env": ["SENDOOK_API_KEY", "SENDOOK_INBOX_ID"] }, "primaryEnv": "SENDOOK_API_KEY", "homepage": "https://github.com/obaid/sendook-skills" } }
---

# Sendook Email

Read and send emails from an existing Sendook inbox.

> **Scope Limitations**: This skill can ONLY read and send emails from a pre-configured inbox. You CANNOT create or delete inboxes, manage domains, manage webhooks, or manage API keys. Do not attempt these operations — they are not available.

## Installation

Install the skill into your OpenClaw workspace:

```bash
clawhub install sendook-openclaw
```

This adds the skill to your workspace's `skills/` directory. OpenClaw will automatically pick it up on the next session start.

### Environment Variables

Set these in your OpenClaw workspace or shell environment:

- `SENDOOK_API_KEY` — Your Sendook API key
- `SENDOOK_INBOX_ID` — The inbox ID this agent is allowed to use

## Setup

Install the SDK ([npm](https://www.npmjs.com/package/@sendook/node) | [source](https://github.com/getrupt/sendook)):

```bash
npm install @sendook/node
```

```typescript
import Sendook from "@sendook/node";

const client = new Sendook(process.env.SENDOOK_API_KEY);
const INBOX_ID = process.env.SENDOOK_INBOX_ID;
```

Both environment variables are required. Use a least-privileged API key scoped to the target inbox only.

## Reading Emails

### List Messages

```typescript
// List all messages in the inbox
const messages = await client.inbox.message.list(INBOX_ID);

// Search messages (regex-based search across to/from/cc, subject, and body)
const results = await client.inbox.message.list(INBOX_ID, "invoice");
```

```bash
# List all messages
curl https://api.sendook.com/v1/inboxes/$SENDOOK_INBOX_ID/messages \
  -H "Authorization: Bearer $SENDOOK_API_KEY"

# Search messages
curl "https://api.sendook.com/v1/inboxes/$SENDOOK_INBOX_ID/messages?query=invoice" \
  -H "Authorization: Bearer $SENDOOK_API_KEY"
```

### Get Message

```typescript
const message = await client.inbox.message.get(INBOX_ID, "msg_def456");
```

```bash
curl https://api.sendook.com/v1/inboxes/$SENDOOK_INBOX_ID/messages/msg_def456 \
  -H "Authorization: Bearer $SENDOOK_API_KEY"
```

**Response**:
```json
{
  "id": "msg_def456",
  "from": "sender@example.com",
  "to": ["support@yourdomain.com"],
  "subject": "Question about my order",
  "text": "Hi, I have a question about order #12345...",
  "html": "<p>Hi, I have a question about order #12345...</p>",
  "labels": [],
  "threadId": "thread_ghi789",
  "createdAt": "2025-01-15T10:35:00Z"
}
```

### List Threads

```typescript
const threads = await client.inbox.thread.list(INBOX_ID);
```

```bash
curl https://api.sendook.com/v1/inboxes/$SENDOOK_INBOX_ID/threads \
  -H "Authorization: Bearer $SENDOOK_API_KEY"
```

### Get Thread

Retrieve a full conversation with all messages.

```typescript
const thread = await client.inbox.thread.get(INBOX_ID, "thread_ghi789");
// thread.messages contains all messages in the conversation
```

```bash
curl https://api.sendook.com/v1/inboxes/$SENDOOK_INBOX_ID/threads/thread_ghi789 \
  -H "Authorization: Bearer $SENDOOK_API_KEY"
```

## Sending Emails

### Send Message

```typescript
await client.inbox.message.send({
  inboxId: INBOX_ID,
  to: ["recipient@example.com"],
  subject: "Hello from Sendook",
  text: "Plain text body",
  html: "<h1>Hello</h1><p>HTML body</p>",
});
```

```bash
curl -X POST https://api.sendook.com/v1/inboxes/$SENDOOK_INBOX_ID/messages/send \
  -H "Authorization: Bearer $SENDOOK_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "to": ["recipient@example.com"],
    "subject": "Hello from Sendook",
    "text": "Plain text body"
  }'
```

### Send with Attachments

> **Important**: Always confirm with the user before reading any local file to attach. Only attach files the user has explicitly requested. Never read files outside the current working directory or project scope (e.g., no `~/.ssh`, `~/.env`, `/etc`, or credential files).

```typescript
import { readFileSync } from "fs";
import { resolve } from "path";

// Only attach files explicitly provided by the user
const filePath = resolve("./reports/report.pdf");

await client.inbox.message.send({
  inboxId: INBOX_ID,
  to: ["recipient@example.com"],
  subject: "Report attached",
  text: "Please find the report attached.",
  attachments: [
    {
      content: readFileSync(filePath).toString("base64"),
      name: "report.pdf",
      contentType: "application/pdf",
    },
  ],
});
```

### Reply to Message

```typescript
await client.inbox.message.reply({
  inboxId: INBOX_ID,
  messageId: "msg_def456",
  text: "Thanks for your email! We'll look into this.",
  html: "<p>Thanks for your email! We'll look into this.</p>",
});
```

```bash
curl -X POST https://api.sendook.com/v1/inboxes/$SENDOOK_INBOX_ID/messages/msg_def456/reply \
  -H "Authorization: Bearer $SENDOOK_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"text": "Thanks for your email! We'\''ll look into this."}'
```

## Complete Example

List recent emails, read the latest, and reply:

```typescript
import Sendook from "@sendook/node";

const client = new Sendook(process.env.SENDOOK_API_KEY);
const INBOX_ID = process.env.SENDOOK_INBOX_ID;

// 1. List recent messages
const messages = await client.inbox.message.list(INBOX_ID);

if (messages.length > 0) {
  // 2. Read the latest message
  const latest = await client.inbox.message.get(INBOX_ID, messages[0].id);
  console.log(`From: ${latest.from}`);
  console.log(`Subject: ${latest.subject}`);
  console.log(`Body: ${latest.text}`);

  // 3. Reply to it
  await client.inbox.message.reply({
    inboxId: INBOX_ID,
    messageId: latest.id,
    text: `Thanks for reaching out! We received your message about "${latest.subject}".`,
  });
}

// 4. Send a new email
await client.inbox.message.send({
  inboxId: INBOX_ID,
  to: ["team@example.com"],
  subject: "Daily inbox summary",
  text: `Processed ${messages.length} messages today.`,
});
```

## Error Handling

```typescript
try {
  await client.inbox.message.send({
    inboxId: INBOX_ID,
    to: ["recipient@example.com"],
    subject: "Hello",
    text: "Body",
  });
} catch (error) {
  if (error.response) {
    console.error(error.response.status, error.response.data);
  } else if (error.request) {
    console.error("No response:", error.request);
  } else {
    console.error("Error:", error.message);
  }
}
```

### Common Errors

| Status | Meaning |
|---|---|
| `400` | Bad request — check parameters (missing `to`, `subject`, etc.) |
| `401` | Unauthorized — invalid or missing API key |
| `404` | Message or thread not found |
| `429` | Rate limit exceeded — retry with backoff |
| `500` | Internal server error |

## API Reference

| Method | Description |
|---|---|
| `client.inbox.message.list(inboxId, query?)` | List or search messages |
| `client.inbox.message.get(inboxId, messageId)` | Get a specific message |
| `client.inbox.message.send(options)` | Send a new email |
| `client.inbox.message.reply(options)` | Reply to a message |
| `client.inbox.thread.list(inboxId)` | List conversation threads |
| `client.inbox.thread.get(inboxId, threadId)` | Get thread with all messages |

No other methods are available in this skill. Do not attempt to create/delete inboxes, manage domains, configure webhooks, or manage API keys.
