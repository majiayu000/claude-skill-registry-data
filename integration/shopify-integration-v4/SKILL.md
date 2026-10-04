---
name: shopify-integration-v4
description: >-
  Implements and maintains the Shopify questions/quotes flow that replaces
  Mercado Libre: OAuth 2.0/PKCE, webhooks→Google Sheet sync, admin question
  list, LLM/rule-based suggested replies, one-click approve & send, auto-reply
  scheduler (UTC-3). Use when working on Shopify backend, Cloud Run, Firestore,
  Sheets API, HMAC validation, or LATAM Spanish reply formatting for Uruguay.
---

# Shopify Integration v4 – Mercado Libre Replacement

**Before working:** Read `docs/team/knowledge/Integrations.md` if it exists.

**Full-store connector (design, catalog, theme, Admin/Storefront, extensions):** use [`shopify-complete-connector`](../shopify-complete-connector/SKILL.md). This skill stays focused on questions/quotes → Sheet → approve/send.

Replaces Mercado Libre questions & quotes with a Shopify-backed flow: questions → Sheet → suggested reply → one-click send. Uruguay/LATAM focus, production hardening, OAuth 2.1–aligned.

## Propagation

Si el cambio afecta a Networks (webhooks), Design (UI) o GPT: actualizar `docs/team/PROJECT-STATE.md` y consultar tabla de propagación en `docs/team/PROJECT-TEAM-FULL-COVERAGE.md` §4.

## When to Apply

- User mentions Shopify integration, ML replacement, questions flow, or quotes flow
- Implementing or fixing OAuth, webhooks, Sheet sync, admin UI, or auto-reply
- Security review of callback/webhook HMAC or token handling
- Adding/fixing endpoints listed below

## Critical Endpoints

| Method | Path | Purpose |
|--------|------|---------|
| GET | /auth/shopify | Start OAuth (PKCE + nonce + state) |
| GET | /auth/shopify/callback | Validate + exchange + store token |
| POST | /webhooks | HMAC verify → route by topic → sync to Sheet/DB |
| POST | /admin/answer | Approve & send reply via GraphQL |
| GET | /admin/questions | Paginated list (pending + history) |
| POST | /admin/auto-config | Toggle + set schedule (cron expression) |

## Stack

- **Backend:** Node.js 20+, Express, TypeScript
- **Hosting:** Google Cloud Run
- **Persistence:** Firestore (tokens, configs, question states)
- **Sheets:** Google Sheets API v4 (service account)
- **Auth:** Shopify OAuth 2.0, PKCE mandatory, state/nonce, HMAC on callback and webhooks
- **Questions proxy:** Order metafields / Draft Order notes / Customer metafields
- **Replies:** Shopify Admin GraphQL (order/customer notes or staff email proxy)

## Strict Rules

1. **Scopes:** Minimal only (read_products write_products read_orders write_orders read_customers read_draft_orders write_draft_orders). Never add scope without explicit need.
2. **Auth:** PKCE S256 + state + nonce on every auth request. State/nonce one-time-use (cookie HttpOnly Secure SameSite=Strict).
3. **HMAC:** Validate on callback and on every webhook (v1/v2). Reject unverified payloads.
4. **Tokens:** Encrypted storage, auto-refresh cron. Never log plain tokens. Short access_token + background refresh; refresh rotation + revoke old token.
5. **Question storage:** Prefer Order metafields/notes. Avoid custom apps unless required.
6. **Auto-reply:** Only when mode enabled and within configured UTC-3 window (days + hours).
7. **Replies:** Short, polite, LATAM Spanish; boxed format when possible.
8. **Errors:** Return 4xx/5xx with short message only. No stack traces to client.
9. **Output:** Clean Node.js/TS code, exact config steps, minimal fixes. No chit-chat or unrequested features.

## Implementation Priority Order

1. OAuth install + token refresh (bullet-proof)
2. Webhook ingestion → Sheet append (idempotent)
3. Question list UI + LLM/rule-based suggestion in Sheet
4. Approve & send via GraphQL
5. Auto-response toggle + cron schedule (UTC-3)

When the user says "next", "implement X", or "fix Y" → deliver production-ready minimal secure code or step.

## Additional Resources

- Full business requirements, architecture, and OAuth 2.1/security details: [reference.md](reference.md)
