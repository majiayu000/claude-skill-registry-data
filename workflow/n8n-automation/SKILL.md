---
name: n8n-automation
description: >
  Scaffold n8n workflow JSON for common patterns: lead capture → CRM, order → fulfillment,
  booking → confirmation email, payment → webhook → customer notification.
  Triggers when user asks to set up an n8n workflow, automation webhook,
  n8n setup, or workflow automation.
---

# n8n Automation Agent

## Workflow Patterns

### Pattern 1: Booking → Confirmation Email + Slack

```json
{
  "name": "Booking Confirmation",
  "nodes": [
    {
      "name": "Webhook",
      "type": "n8n-nodes-base.webhook",
      "parameters": {
        "httpMethod": "POST",
        "path": "booking-confirmed",
        "responseMode": "onReceived"
      }
    },
    {
      "name": "Send Confirmation Email",
      "type": "n8n-nodes-base.emailSend",
      "parameters": {
        "to": "={{ $json.body.guestEmail }}",
        "subject": "Booking Confirmed — {{ $json.body.bookingId }}",
        "html": "<h1>Your booking is confirmed!</h1><p>Date: {{ $json.body.bookingDate }}</p>"
      }
    },
    {
      "name": "Notify Slack",
      "type": "n8n-nodes-base.slack",
      "parameters": {
        "channel": "#bookings",
        "text": "New booking: {{ $json.body.guestName }} — {{ $json.body.totalAmount }}"
      }
    }
  ],
  "connections": {
    "Webhook": { "main": [[{ "node": "Send Confirmation Email" }]] },
    "Send Confirmation Email": { "main": [[{ "node": "Notify Slack" }]] }
  }
}
```

### Pattern 2: Lead Capture → Resend → Slack

```json
{
  "name": "Lead Capture Pipeline",
  "nodes": [
    { "name": "Webhook", "type": "n8n-nodes-base.webhook", "parameters": { "path": "lead-capture" }},
    {
      "name": "Add to Resend Audience",
      "type": "n8n-nodes-base.resend",
      "parameters": {
        "operation": "upsertSubscriber",
        "audienceId": "{{ $env.RESEND_AUDIENCE_ID }}",
        "email": "={{ $json.email }}",
        "firstName": "={{ $json.name }}",
        "tags": ["={{ $json.source }}"]
      }
    },
    {
      "name": "Slack Handoff",
      "type": "n8n-nodes-base.slack",
      "parameters": {
        "channel": "#sales-leads",
        "text": "*New lead:* {{ $json.name }}\n*Company:* {{ $json.company }}\n*Email:* {{ $json.email }}"
      }
    }
  ]
}
```

### Pattern 3: Payment Webhook → Refund Alert

```json
{
  "name": "Payment Webhook Processor",
  "nodes": [
    { "name": "Paymob Webhook", "type": "n8n-nodes-base.webhook", "parameters": { "path": "paymob-webhook" }},
    {
      "name": "Slack on Refund",
      "type": "n8n-nodes-base.slack",
      "parameters": {
        "channel": "#finance",
        "text": "Refund processed: EGP {{ $json.body.obj.amount_cents / 100 }}"
      },
      "conditions": {
        "conditions": [{ "id": "type", "value": "TRANSACTION_REFUND" }]
      }
    }
  ]
}
```

## Deployment

```bash
# Option 1: n8n Cloud
# Create workflow → copy JSON → paste into n8n Cloud UI
# Get webhook URL → configure in app

# Option 2: Self-hosted n8n
docker run -d --name n8n -p 5678:5678 n8nio/n8n
# Connect via https://n8n.example.com

# Environment variables
N8N_BASIC_AUTH_ACTIVE=true
N8N_BASIC_AUTH_USER=admin
N8N_BASIC_AUTH_PASSWORD=xxx
WEBHOOK_URL=https://n8n.example.com
```

## n8n ↔ App Integration Points

| Event | App calls n8n | n8n calls app |
|---|---|---|
| Booking confirmed | POST /webhook/booking | GET /api/booking/{id} |
| Lead qualified | POST /webhook/lead | — |
| Payment received | POST /webhook/paymob | — |
| Refund processed | — | POST /api/refund-confirm |
| Guest checked in | POST /webhook/checkin | — |
