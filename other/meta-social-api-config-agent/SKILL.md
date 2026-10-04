---
name: meta-social-api-config-agent
description: Configure and integrate Meta platform APIs (WhatsApp Business Platform, Instagram Graph API, and Facebook Graph API) end-to-end for an application, including app setup, auth tokens, webhooks, permissions, backend endpoints, testing, and production hardening. Use when asked to build or debug social messaging/posting integrations, webhook flows, or Meta developer console configuration.
---

# Meta Social API Config Agent

## Overview

Use this skill to implement full-stack Meta integrations safely and predictably: developer console setup, backend implementation, verification, and go-live hardening.

## Workflow Decision Tree

1. Identify requested channels:
   - WhatsApp only
   - Instagram + Facebook only
   - Full omnichannel (all three)
2. Identify requested capability:
   - Inbound webhook handling
   - Outbound messaging/posting
   - Auth and token lifecycle
   - End-to-end production readiness
3. Load only the needed reference file sections from `references/meta-api-playbook.md`.

## Standard Implementation Workflow

1. Audit existing project state.
   - Locate env handling, API routes, auth middleware, and secret management.
   - Confirm deployment target and public HTTPS webhook URL.
2. Define integration contract.
   - Document required user stories (send message, receive message, publish media, etc.).
   - Define event schema normalization for WhatsApp/Instagram/Facebook payloads.
3. Configure Meta app and products.
   - Add products (WhatsApp, Instagram Graph, Facebook Login/Pages).
   - Request minimal permissions first; expand later.
4. Implement backend.
   - Add webhook verification and signature validation (always use the app secret as the HMAC key).
   - Add outbound clients with retry, timeout, and error mapping.
   - Add token management (short-lived vs long-lived/system user).
5. Validate in sandbox/test mode.
   - Use test phone numbers/pages/users.
   - Execute smoke tests in the playbook checklist.
6. Harden for production.
   - Ensure secrets rotation path exists.
   - Add idempotency and replay protection for webhook events.
   - Add structured logs and alerting for API failures and permission errors.

## Output Requirements

When implementing changes, always provide:

- `.env.example` additions for required credentials.
- A concise setup checklist for Meta Developer Console and Business Manager.
- A mapping table of webhook event type -> internal action.
- A test matrix covering verification challenge, inbound events, and outbound API calls.

## Guardrails

- Never hardcode tokens, app secrets, or verify tokens.
- Never disable signature verification in production paths.
- Request least-privilege scopes and document why each permission is needed.
- Prefer versioned Graph API endpoints and centralize the version constant.
- Implement graceful handling for expired token, missing permission, and rate limit errors.

## References

- `references/meta-api-playbook.md`: Practical end-to-end checklist, endpoint map, webhook handling patterns, and troubleshooting guidance.
