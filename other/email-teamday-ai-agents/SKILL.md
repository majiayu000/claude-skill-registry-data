---
name: email
description: Send emails via Resend, Mailgun, or SendGrid using your own API credentials. Auto-detects available provider. Use for reports, alerts, client communications, and business emails.
version: 1.0.0
allowed-tools: Bash
metadata:
  credentials:
    - RESEND_API_KEY (Resend)
    - EMAIL_FROM (Resend/SendGrid sender)
    - MAILGUN_API_KEY (Mailgun)
    - MAILGUN_DOMAIN (Mailgun)
    - SENDGRID_API_KEY (SendGrid)
---

# Email Skill

Send emails to any recipient using your own email provider credentials.

## Quick Start

```bash
# Resend (simplest — 1 curl call)
curl -X POST https://api.resend.com/emails \
  -H "Authorization: Bearer $RESEND_API_KEY" \
  -H "Content-Type: application/json" \
  -d "{\"from\":\"$EMAIL_FROM\",\"to\":\"recipient@example.com\",\"subject\":\"Hello\",\"text\":\"Your message\"}"
```

## Provider Detection

Check which credentials are available and use that provider:

```bash
if [ -n "$RESEND_API_KEY" ]; then
  echo "Provider: Resend"
elif [ -n "$MAILGUN_API_KEY" ]; then
  echo "Provider: Mailgun"
elif [ -n "$SENDGRID_API_KEY" ]; then
  echo "Provider: SendGrid"
else
  echo "ERROR: No email credentials configured."
  echo "Set one of: RESEND_API_KEY, MAILGUN_API_KEY, or SENDGRID_API_KEY"
  exit 1
fi
```

## Prerequisites

At least one provider's credentials must be configured as Space environment variables.

| Provider | Required Variables | Free Tier |
|----------|-------------------|-----------|
| **Resend** (recommended) | `RESEND_API_KEY`, `EMAIL_FROM` | 3,000 emails/month |
| **Mailgun** | `MAILGUN_API_KEY`, `MAILGUN_DOMAIN` | 1,000 emails/month (trial) |
| **SendGrid** | `SENDGRID_API_KEY`, `EMAIL_FROM` | 100 emails/day |

### Verify Setup

```bash
echo "Resend: ${RESEND_API_KEY:+configured}"
echo "Mailgun: ${MAILGUN_API_KEY:+configured}"
echo "SendGrid: ${SENDGRID_API_KEY:+configured}"
echo "From: ${EMAIL_FROM:-not set}"
```

## Resend Recipes

Resend has the simplest API — recommended for new users.

### Send Plain Text Email

```bash
curl -s -X POST https://api.resend.com/emails \
  -H "Authorization: Bearer $RESEND_API_KEY" \
  -H "Content-Type: application/json" \
  -d "{
    \"from\": \"$EMAIL_FROM\",
    \"to\": \"recipient@example.com\",
    \"subject\": \"Your Subject\",
    \"text\": \"Plain text message body\"
  }"
```

### Send HTML Email

```bash
curl -s -X POST https://api.resend.com/emails \
  -H "Authorization: Bearer $RESEND_API_KEY" \
  -H "Content-Type: application/json" \
  -d "{
    \"from\": \"$EMAIL_FROM\",
    \"to\": \"recipient@example.com\",
    \"subject\": \"Weekly Report\",
    \"html\": \"<h1>Report</h1><p>Your HTML content here</p>\"
  }"
```

### Send to Multiple Recipients

```bash
curl -s -X POST https://api.resend.com/emails \
  -H "Authorization: Bearer $RESEND_API_KEY" \
  -H "Content-Type: application/json" \
  -d "{
    \"from\": \"$EMAIL_FROM\",
    \"to\": [\"user1@example.com\", \"user2@example.com\"],
    \"cc\": [\"manager@example.com\"],
    \"subject\": \"Team Update\",
    \"text\": \"Message to the team\"
  }"
```

## Mailgun Recipes

Battle-tested provider, more complex API but very reliable.

### Send Email via Mailgun

```bash
# Determine API endpoint (US or EU region)
if [ "$MAILGUN_REGION" = "EU" ]; then
  MAILGUN_API="https://api.eu.mailgun.net"
else
  MAILGUN_API="https://api.mailgun.net"
fi

curl -s --user "api:${MAILGUN_API_KEY}" \
  "${MAILGUN_API}/v3/${MAILGUN_DOMAIN}/messages" \
  -F from="${MAILGUN_FROM_EMAIL:-noreply@${MAILGUN_DOMAIN}}" \
  -F to="recipient@example.com" \
  -F subject="Your Subject" \
  -F text="Plain text message"
```

### Send HTML via Mailgun

```bash
if [ "$MAILGUN_REGION" = "EU" ]; then
  MAILGUN_API="https://api.eu.mailgun.net"
else
  MAILGUN_API="https://api.mailgun.net"
fi

curl -s --user "api:${MAILGUN_API_KEY}" \
  "${MAILGUN_API}/v3/${MAILGUN_DOMAIN}/messages" \
  -F from="${MAILGUN_FROM_EMAIL:-noreply@${MAILGUN_DOMAIN}}" \
  -F to="recipient@example.com" \
  -F subject="Report" \
  --form-string html="<h1>Report</h1><p>Your HTML content</p>"
```

## SendGrid Recipes

Enterprise-standard email provider.

### Send Email via SendGrid

```bash
curl -s -X POST https://api.sendgrid.com/v3/mail/send \
  -H "Authorization: Bearer $SENDGRID_API_KEY" \
  -H "Content-Type: application/json" \
  -d "{
    \"personalizations\": [{\"to\": [{\"email\": \"recipient@example.com\"}]}],
    \"from\": {\"email\": \"$EMAIL_FROM\"},
    \"subject\": \"Your Subject\",
    \"content\": [{\"type\": \"text/plain\", \"value\": \"Message body\"}]
  }"
```

### Send HTML via SendGrid

```bash
curl -s -X POST https://api.sendgrid.com/v3/mail/send \
  -H "Authorization: Bearer $SENDGRID_API_KEY" \
  -H "Content-Type: application/json" \
  -d "{
    \"personalizations\": [{\"to\": [{\"email\": \"recipient@example.com\"}]}],
    \"from\": {\"email\": \"$EMAIL_FROM\"},
    \"subject\": \"Report\",
    \"content\": [{\"type\": \"text/html\", \"value\": \"<h1>Report</h1><p>Your content</p>\"}]
  }"
```

## Email Templates

### Report Delivery

```bash
SUBJECT="[Report] ${REPORT_NAME} — $(date +%Y-%m-%d)"
BODY="Hi,

Your report '${REPORT_NAME}' is ready.

Summary:
${REPORT_SUMMARY}

The full report is attached to this Space at: ${REPORT_PATH}

— Your TeamDay Agent"
```

### Error Alert

```bash
SUBJECT="[Alert] ${SERVICE_NAME} — Action Required"
BODY="An issue was detected that requires your attention.

Service: ${SERVICE_NAME}
Error: ${ERROR_MESSAGE}
Time: $(date -u +"%Y-%m-%d %H:%M:%S UTC")

Recommended action:
${RECOMMENDED_ACTION}

— Your TeamDay Agent"
```

### Weekly Summary

```bash
SUBJECT="[Weekly Summary] $(date +%Y-%m-%d)"
BODY="Here's your weekly summary:

${SUMMARY_CONTENT}

Key metrics:
${KEY_METRICS}

— Your TeamDay Agent"
```

## Error Handling

Always check the HTTP response:

```bash
RESPONSE=$(curl -s -w "\n%{http_code}" -X POST https://api.resend.com/emails \
  -H "Authorization: Bearer $RESEND_API_KEY" \
  -H "Content-Type: application/json" \
  -d "{\"from\":\"$EMAIL_FROM\",\"to\":\"user@example.com\",\"subject\":\"Test\",\"text\":\"Test\"}")

HTTP_CODE=$(echo "$RESPONSE" | tail -n1)
BODY=$(echo "$RESPONSE" | sed '$d')

if [ "$HTTP_CODE" -ge 200 ] && [ "$HTTP_CODE" -lt 300 ]; then
  echo "Email sent successfully"
else
  echo "Failed to send email (HTTP $HTTP_CODE): $BODY"
fi
```

## Common Errors

| Error | Provider | Cause | Solution |
|-------|----------|-------|----------|
| 401/403 | All | Invalid API key | Check credentials in Space env vars |
| 422 | Resend | Invalid `from` address | Verify domain in Resend dashboard |
| 400 | Mailgun | Domain not verified | Complete DNS verification |
| 403 | SendGrid | Sender not verified | Verify sender identity in SendGrid |

## Provider Setup Guides

### Resend (Recommended)
1. Sign up at resend.com
2. Add and verify your domain (or use `onboarding@resend.dev` for testing)
3. Create an API key — set as `RESEND_API_KEY`
4. Set `EMAIL_FROM` to your verified sender (e.g., `reports@yourdomain.com`)

### Mailgun
1. Sign up at mailgun.com
2. Add and verify your sending domain
3. Get API key from Settings — API Keys — set as `MAILGUN_API_KEY`
4. Set `MAILGUN_DOMAIN` to your verified domain

### SendGrid
1. Sign up at sendgrid.com
2. Verify a sender identity
3. Create an API key with "Mail Send" permissions — set as `SENDGRID_API_KEY`
4. Set `EMAIL_FROM` to your verified sender

## Security Note

This skill sends emails using YOUR provider credentials to ANY recipient. You are responsible for:
- Email content and reputation
- Compliance with anti-spam laws (CAN-SPAM, GDPR)
- Managing your sending domain's reputation

For notifications sent only to yourself, use the `notify-user` skill instead (uses TeamDay-managed credentials).

## Tips

- **Start with Resend** — simplest API, generous free tier
- **Use templates** — consistent formatting improves deliverability
- **Check response codes** — don't assume success
- **Plain text fallback** — always include a text version alongside HTML
- **Rate limiting** — space out bulk sends to avoid provider limits
