---
name: email-delivery
description: Email delivery patterns including single, batch, scheduled emails and attachment handling. Use when building transactional email systems, batch communication workflows, scheduled delivery, or implementing file/URL attachments with reply-to and CC/BCC functionality.
allowed-tools: Read, Write, Bash, Grep
---

# Email Delivery Skill

Comprehensive patterns and templates for implementing robust email delivery with Resend, covering single emails, batch operations, scheduled delivery, and attachment handling.

## Use When

- Building transactional email systems (confirmations, notifications, alerts)
- Implementing batch email campaigns (up to 100 recipients per request)
- Setting up scheduled/delayed email delivery
- Handling file attachments, buffers, or URL-based attachments
- Adding reply-to, CC, and BCC functionality
- Creating email templates with variables and dynamic content
- Implementing retry logic and delivery error handling

## Core Patterns

### 1. Single Email Sending

**Transactional emails** for immediate delivery with minimal latency:

```typescript
import { Resend } from 'resend';

const resend = new Resend('your_resend_key_here');

async function sendTransactionalEmail() {
  const { data, error } = await resend.emails.send({
    from: 'notifications@example.com',
    to: 'user@example.com',
    subject: 'Welcome to Example',
    html: '<h1>Welcome!</h1><p>Thank you for signing up.</p>',
  });

  if (error) {
    console.error('Failed to send email:', error);
    return null;
  }

  return data;
}
```

### 2. Batch Email Sending

**Bulk operations** for sending up to 100 emails in a single request:

```typescript
async function sendBatchEmails(recipients: Array<{email: string; name: string}>) {
  const emails = recipients.map(recipient => ({
    from: 'newsletter@example.com',
    to: recipient.email,
    subject: `Hello ${recipient.name}!`,
    html: `<p>Welcome ${recipient.name}</p>`,
  }));

  const { data, error } = await resend.batch.send(emails);

  if (error) {
    console.error('Batch send failed:', error);
    return null;
  }

  return data;
}
```

### 3. Scheduled Email Delivery

**Time-based delivery** for emails sent at specific times:

```typescript
async function scheduleEmail(scheduledAt: Date) {
  const { data, error } = await resend.emails.send({
    from: 'marketing@example.com',
    to: 'user@example.com',
    subject: 'Scheduled Message',
    html: '<p>This was scheduled!</p>',
    scheduled_at: scheduledAt.toISOString(),
  });

  if (error) {
    console.error('Failed to schedule email:', error);
    return null;
  }

  return data;
}
```

### 4. Attachment Handling

**File attachments** from files, buffers, or URLs:

#### File-based Attachment

```typescript
import fs from 'fs';
import path from 'path';

async function sendWithFileAttachment(filePath: string) {
  const fileContent = fs.readFileSync(filePath);
  const fileName = path.basename(filePath);

  const { data, error } = await resend.emails.send({
    from: 'documents@example.com',
    to: 'recipient@example.com',
    subject: 'Your Document',
    html: '<p>Please find attached your document.</p>',
    attachments: [
      {
        filename: fileName,
        content: fileContent,
      },
    ],
  });

  return { data, error };
}
```

#### Buffer-based Attachment

```typescript
async function sendWithBufferAttachment(buffer: Buffer, filename: string) {
  const { data, error } = await resend.emails.send({
    from: 'reports@example.com',
    to: 'user@example.com',
    subject: 'Monthly Report',
    html: '<p>Your monthly report is attached.</p>',
    attachments: [
      {
        filename: filename,
        content: buffer,
      },
    ],
  });

  return { data, error };
}
```

#### URL-based Attachment

```typescript
async function sendWithUrlAttachment(fileUrl: string) {
  const response = await fetch(fileUrl);
  const buffer = await response.arrayBuffer();

  const { data, error } = await resend.emails.send({
    from: 'notifications@example.com',
    to: 'user@example.com',
    subject: 'Download Your File',
    html: '<p>Your file is ready.</p>',
    attachments: [
      {
        filename: 'document.pdf',
        content: Buffer.from(buffer),
      },
    ],
  });

  return { data, error };
}
```

### 5. Reply-To and CC/BCC

**Message routing** with multiple recipients and reply addresses:

```typescript
async function sendWithRouting(mainRecipient: string) {
  const { data, error } = await resend.emails.send({
    from: 'support@example.com',
    to: mainRecipient,
    reply_to: 'support-team@example.com',
    cc: ['manager@example.com'],
    bcc: ['archive@example.com'],
    subject: 'Support Ticket #12345',
    html: '<p>We received your support request.</p>',
  });

  return { data, error };
}
```

## Python Patterns

### Single Email (Python)

```python
import os
from resend import Resend

client = Resend(api_key=os.environ.get("RESEND_API_KEY"))

def send_email():
    email = {
        "from": "notifications@example.com",
        "to": "user@example.com",
        "subject": "Welcome",
        "html": "<h1>Welcome!</h1>",
    }

    response = client.emails.send(email)
    return response
```

### Batch Email (Python)

```python
def send_batch_emails(recipients):
    emails = [
        {
            "from": "newsletter@example.com",
            "to": recipient["email"],
            "subject": f"Hello {recipient['name']}",
            "html": f"<p>Welcome {recipient['name']}</p>",
        }
        for recipient in recipients
    ]

    response = client.batch.send(emails)
    return response
```

### File Attachment (Python)

```python
def send_with_attachment(file_path):
    with open(file_path, 'rb') as f:
        file_content = f.read()

    email = {
        "from": "documents@example.com",
        "to": "recipient@example.com",
        "subject": "Your Document",
        "html": "<p>Document attached.</p>",
        "attachments": [
            {
                "filename": "document.pdf",
                "content": file_content,
            }
        ],
    }

    response = client.emails.send(email)
    return response
```

## Template Variables

### Environment Variables Required

```bash
RESEND_API_KEY=your_resend_key_here
RESEND_FROM_EMAIL=your-verified-email@example.com
```

### Email Template Variables

```typescript
interface EmailPayload {
  from: string;              // Verified sender email
  to: string | string[];     // Recipient(s)
  cc?: string[];            // Carbon copy recipients
  bcc?: string[];           // Blind carbon copy
  reply_to?: string;        // Reply-to address
  subject: string;          // Email subject
  html?: string;            // HTML content
  text?: string;            // Plain text fallback
  attachments?: Array<{
    filename: string;
    content: Buffer | string;
  }>;
  scheduled_at?: string;    // ISO 8601 datetime for scheduling
  tags?: Array<{
    name: string;
    value: string;
  }>;
}
```

## Best Practices

### Error Handling

Always implement retry logic for transient failures:

```typescript
async function sendWithRetry(emailPayload, maxRetries = 3) {
  for (let attempt = 1; attempt <= maxRetries; attempt++) {
    const { data, error } = await resend.emails.send(emailPayload);

    if (!error) return { data, success: true };

    if (error.message?.includes('rate_limit') && attempt < maxRetries) {
      const delay = Math.pow(2, attempt) * 1000;
      await new Promise(resolve => setTimeout(resolve, delay));
      continue;
    }

    return { error, success: false };
  }
}
```

### Rate Limiting

Resend has rate limits. For batch operations over 100 emails:

```typescript
async function sendLargeBatch(emails: EmailPayload[]) {
  const batchSize = 100;
  const results = [];

  for (let i = 0; i < emails.length; i += batchSize) {
    const batch = emails.slice(i, i + batchSize);
    const { data, error } = await resend.batch.send(batch);

    if (error) {
      console.error(`Batch ${Math.floor(i / batchSize) + 1} failed:`, error);
      results.push({ success: false, error });
    } else {
      results.push({ success: true, data });
    }

    // Rate limit handling - wait between batches
    if (i + batchSize < emails.length) {
      await new Promise(resolve => setTimeout(resolve, 1000));
    }
  }

  return results;
}
```

### Template Best Practices

- Use responsive HTML templates
- Always provide text fallback
- Test across email clients
- Include unsubscribe links for marketing emails
- Avoid large attachments (keep under 25MB)

## Examples Directory Structure

- `single-email/` - Basic transactional email patterns
- `batch-emails/` - Bulk sending with 50-100 recipients
- `attachments/` - File, buffer, and URL attachment handling
- `scheduled/` - Time-based delivery scheduling

See individual example README files for complete code and usage patterns.

## Related Skills

- **email-templates** - HTML template management and rendering
- **email-validation** - Recipient address validation
- **email-webhooks** - Delivery event tracking and bounce handling

## Resources

- [Resend API Documentation](https://resend.com/docs)
- [Email Authentication (SPF, DKIM, DMARC)](https://resend.com/docs/knowledge-base/authentication)
- [Batch Email API](https://resend.com/docs/api-reference/emails/batch)
- [Scheduled Emails](https://resend.com/docs/api-reference/emails/send#scheduled_at)

## Security Notes

- API keys should be stored in environment variables (never hardcoded)
- Use `RESEND_API_KEY` from secure secret management
- Verify sender emails before using in production
- Implement authentication for email submission endpoints
- Log email events for compliance and debugging
