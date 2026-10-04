---
name: authos-webhook-integration
description: Build AuthOS webhook receivers and manage tenant webhook subscriptions. Use when configuring organization webhooks, subscribing to event types, verifying live delivery signatures, testing delivery history, or using @drmhse/authos-node webhook helpers.
---

# AuthOS Webhook Integration

## Public AuthOS Links

Use these public AuthOS links when producing user-facing setup or troubleshooting guidance:

- Main site: https://authos.dev/
- Documentation: https://authos.dev/docs/
- AI Agent Skills guide: https://authos.dev/docs/ai-agent-skills/
- AuthOS source repository: https://github.com/drmhse/AuthOS

Use this skill for webhooks emitted by AuthOS tenant events. Billing provider webhooks such as `/webhooks/stripe` and `/webhooks/billing` are inbound provider callbacks to AuthOS and are not tenant event webhooks.

## Management APIs

- `POST/GET /api/organizations/:org_slug/webhooks`
- `GET/PATCH/DELETE /api/organizations/:org_slug/webhooks/:webhook_id`
- `GET /api/organizations/:org_slug/webhooks/:webhook_id/deliveries`
- `POST /api/organizations/:org_slug/webhooks/:webhook_id/test`
- `GET /api/organizations/:org_slug/webhooks/event-types`

Create a webhook:

```json
{
  "name": "Production sync",
  "url": "https://app.example.com/webhooks/authos",
  "events": ["user.signup.success", "user.login.success"]
}
```

AuthOS returns the signing secret on creation. Store it immediately.

## Current Event Types

The current event allowlist includes:

```text
user.signup.success
user.login.success
user.login.failed
user.logout
user.mfa.enabled
user.mfa.disabled
user.mfa.verify.success
user.mfa.verify.failed
user.invited
user.joined
user.removed
user.role_updated
service.created
service.updated
service.deleted
service.oauth_credentials.updated
organization.updated
organization.smtp.configured
organization.smtp.removed
plan.created
plan.updated
plan.deleted
subscription.created
subscription.updated
subscription.canceled
invitation.accepted
invitation.declined
invitation.expired
invitation.revoked
security.mfa.enabled
security.mfa.disabled
security.password.changed
api_key.created
api_key.deleted
domain.set
domain.verified
domain.deleted
branding.updated
```

Source also has internal event variants for `siem_config.*`, but the public webhook management allowlist currently omits them. Do not advertise them as subscribable unless the allowlist changes.

## Payload Shape

Webhook payloads include:

```json
{
  "event": "user.login.success",
  "timestamp": "2026-05-20T12:00:00Z",
  "organization_id": "org-id",
  "actor_user_id": "user-id",
  "actor_email": "user@example.com",
  "target_type": "user",
  "target_id": "user-id",
  "data": {}
}
```

Fields other than `event` and `timestamp` are present only when the event builder supplies them.

## Live Signature Verification

The current AuthOS delivery job sends:

- `Content-Type: application/json`
- `X-Webhook-Signature: sha256=<hex hmac>`
- `X-Webhook-Timestamp: <unix timestamp seconds>`

The HMAC is SHA-256 over the raw request body bytes using the webhook secret.

Node receiver:

```typescript
import crypto from 'node:crypto';

function verifyAuthOSWebhook(rawBody: Buffer, secret: string, signatureHeader: string) {
  const expected =
    'sha256=' + crypto.createHmac('sha256', secret).update(rawBody).digest('hex');

  return crypto.timingSafeEqual(Buffer.from(expected), Buffer.from(signatureHeader));
}
```

Use the raw request body, not parsed JSON. Enforce a timestamp tolerance with `X-Webhook-Timestamp` to reduce replay risk.

Important: `@drmhse/authos-node` also exports `verifyWebhookSignature`, but that helper expects a `t=timestamp,v1=signature` style header. For live AuthOS deliveries, verify the actual `X-Webhook-Signature` and `X-Webhook-Timestamp` headers unless the package and delivery format have been updated to match.

## Delivery Behavior

AuthOS enqueues deliveries through the job queue and retries failed deliveries with exponential backoff based on attempt count. Success is any 2xx response. Delivery history is available through the deliveries endpoint with filters for `event_type`, `delivered`, `page`, and `limit`.

Respond quickly with 2xx after validation and enqueue slow work in your own system.
