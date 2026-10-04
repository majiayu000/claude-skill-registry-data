---
name: utila-webhooks
description: >
  Receive and verify Utila webhooks. Use when setting up Utila webhook handlers,
  debugging x-utila-signature RSA/PSS verification, or handling Utila digital-asset
  events like TRANSACTION_CREATED, TRANSACTION_STATE_UPDATED, WALLET_CREATED,
  WALLET_ADDRESS_CREATED, and TRANSACTION_AML_SCREENING_RESULT_READY.
license: MIT
metadata:
  author: hookdeck
  version: "0.1.0"
  repository: https://github.com/hookdeck/webhook-skills
---

# Utila Webhooks

Utila is a digital-asset operations platform. Webhooks notify your endpoint when
transactions and wallets change state so you can reconcile them against the Utila
API. Verification is **asymmetric RSA**, not HMAC — there is no shared secret.

## When to Use This Skill

- How do I receive Utila webhooks?
- How do I verify the `x-utila-signature` header?
- Why is my Utila signature verification failing?
- How do I handle `TRANSACTION_CREATED` or `TRANSACTION_STATE_UPDATED` events?
- How do I configure a webhook in the Utila Console?

## How Verification Works

Utila signs each delivery with an **RSA-4096 private key** using **SHA-512** and
**PSS padding**, base64-encodes the result, and sends it in the `x-utila-signature`
header. You verify with Utila's **PEM-encoded RSA-4096 public key**, copied from the
Console (Vault Settings → Webhooks). Key facts:

- **No shared secret / no HMAC.** You hold only the *public* key.
- **Not Standard Webhooks.** There is no `webhook-id` / `webhook-timestamp` header.
- **No timestamp header**, so Utila provides no built-in replay protection — dedupe
  on the event `id` and treat deliveries as idempotent.
- Always verify over the **raw request body** (exact bytes), before JSON parsing.

## Verification (core)

```javascript
const crypto = require('crypto');

// signatureB64: the raw x-utila-signature header value.
// rawBody:      the exact request bytes (Buffer), NOT parsed JSON.
// publicKeyPem: Utila's PEM RSA-4096 PUBLIC key from the Console.
function verifyUtilaSignature(rawBody, signatureB64, publicKeyPem) {
  if (!signatureB64) return false;
  try {
    return crypto.verify(
      'sha512',
      rawBody,
      {
        key: publicKeyPem,
        padding: crypto.constants.RSA_PKCS1_PSS_PADDING,
        saltLength: crypto.constants.RSA_PSS_SALTLEN_AUTO, // auto-detect PSS salt
      },
      Buffer.from(signatureB64, 'base64')
    );
  } catch {
    return false; // malformed key/signature = not authentic
  }
}
```

> **For complete handlers with tests**, see [examples/express/](examples/express/), [examples/nextjs/](examples/nextjs/), [examples/fastapi/](examples/fastapi/).

## Common Event Types

Utila emits exactly five event types (SCREAMING_SNAKE_CASE), delivered in the
payload's `type` field:

| Event | Triggered When |
|-------|----------------|
| `TRANSACTION_CREATED` | A new transaction is created |
| `TRANSACTION_STATE_UPDATED` | A transaction changes state (e.g. signing, completed, failed) |
| `WALLET_CREATED` | A new wallet is created |
| `WALLET_ADDRESS_CREATED` | A new address is generated for a wallet |
| `TRANSACTION_AML_SCREENING_RESULT_READY` | An AML screening result becomes available |

Payloads are **thin** — they carry identifiers (`id`, `vault`, `type`,
`resourceType`, `resource`, optional `details`), not the full resource. Fetch the
complete object from the Utila API / Stream using the `resource` path.

See [references/overview.md](references/overview.md) for the full payload shape.

## Environment Variables

| Variable | Description |
|----------|-------------|
| `UTILA_WEBHOOK_PUBLIC_KEY` | Utila's PEM-encoded RSA-4096 **public** key (from the Console). |

The PEM is multi-line. Store it either as a real multi-line value or with escaped
`\n` newlines — the examples normalize `\n` back to real newlines.

> **SDK note:** Utila documents an npm package `@utila/api`, but it does not
> currently resolve on the public registry, and there is no Python SDK. The
> examples therefore verify manually with the platform crypto libraries
> (Node `crypto`, Python `cryptography`).

## Local Development

For local webhook testing, run the Hookdeck CLI via `npx` — no install required:

```bash
npx hookdeck-cli listen 3000 utila --path /webhooks/utila
```

No account required — the CLI creates a guest account on first run and provides a
local tunnel + web UI for inspecting requests.

## Reference Materials

- [references/overview.md](references/overview.md) — What Utila webhooks are, event types, payload structure
- [references/setup.md](references/setup.md) — Configure webhooks in the Utila Console, get the public key
- [references/verification.md](references/verification.md) — RSA/PSS signature verification details and gotchas
- [examples/express/](examples/express/) — Express (Node.js) handler + tests
- [examples/nextjs/](examples/nextjs/) — Next.js App Router handler + tests
- [examples/fastapi/](examples/fastapi/) — FastAPI (Python) handler + tests

## Recommended: webhook-handler-patterns

Install [webhook-handler-patterns](https://github.com/hookdeck/webhook-skills/tree/main/skills/webhook-handler-patterns)
alongside this skill for cross-cutting concerns. Utila sends no timestamp, so
idempotency matters especially:

- [Handler sequence](https://github.com/hookdeck/webhook-skills/blob/main/skills/webhook-handler-patterns/references/handler-sequence.md)
- [Idempotency](https://github.com/hookdeck/webhook-skills/blob/main/skills/webhook-handler-patterns/references/idempotency.md)
- [Error handling](https://github.com/hookdeck/webhook-skills/blob/main/skills/webhook-handler-patterns/references/error-handling.md)
- [Retry logic](https://github.com/hookdeck/webhook-skills/blob/main/skills/webhook-handler-patterns/references/retry-logic.md)

## Related Skills

- [circle-webhooks](https://github.com/hookdeck/webhook-skills/tree/main/skills/circle-webhooks) - Asymmetric (ECDSA) digital-asset webhooks
- [fireblocks-webhooks](https://github.com/hookdeck/webhook-skills/tree/main/skills/fireblocks-webhooks) - RSA-signed digital-asset custody webhooks
- [bridge-xyz-webhooks](https://github.com/hookdeck/webhook-skills/tree/main/skills/bridge-xyz-webhooks) - Stablecoin platform webhooks
- [zerohash-webhooks](https://github.com/hookdeck/webhook-skills/tree/main/skills/zerohash-webhooks) - Crypto-as-a-service webhooks
- [webhook-handler-patterns](https://github.com/hookdeck/webhook-skills/tree/main/skills/webhook-handler-patterns) - Idempotency, error handling, retry logic
- [hookdeck-event-gateway](https://github.com/hookdeck/webhook-skills/tree/main/skills/hookdeck-event-gateway) - Production webhook infrastructure
