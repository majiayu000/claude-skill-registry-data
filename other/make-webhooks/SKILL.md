---
name: make-webhooks
description: Use when designing, modifying, or debugging Make.com webhook integrations ג€” payload shapes, signature verification, scenario interfaces, retry policy. Covers the Make MCP server and `src/routes/` webhook handlers.
---

# Make.com Webhooks skill

## When to invoke

- Touching `src/routes/` (any webhook endpoint)
- Defining the contract for a Make scenario that calls our system
- Modifying payload shape passed back to Make
- Debugging dropped/duplicate webhook events

## Available MCP tools

`validate_scenario_interface` ג€” validates that a scenario's expected I/O matches our route handler's expected payload. Run before deploying any new scenario.

## Architecture

```
Make scenario (trigger: WhatsApp / Gmail / CRM / Calendar event)
   ג†“ HTTP POST with JSON payload
src/routes/<channel>.ts (Express handler)
   ג†“ verify + normalize
src/orchestrator/master.ts
```

## Hard rules

1. **Verify signature** on every inbound webhook ג€” never trust payload without HMAC check (`X-Make-Signature` header)
2. **Idempotency**: every webhook carries `event_id`. Store last N event_ids and reject duplicates ג€” Make retries aggressively
3. **Respond fast** (under 3s) ג€” acknowledge with 200, process async. Long handlers cause Make to time out and retry
4. **Schema validation** with Zod at the route boundary ג€” reject malformed payloads with 400, log to monitoring
5. **Never** echo PII back to Make in error responses ג€” only event_id and error code

## Standard payload envelope

```json
{
  "event_id": "uuid",
  "source": "whatsapp|gmail|crm|calendar|manual",
  "timestamp": "ISO-8601",
  "customer_ref": "phone_or_email_or_crm_id",
  "payload": { }
}
```

## Retry policy (our side)

If we need to call back into Make: max 3 retries with exponential backoff (1s, 4s, 16s). After that, escalate to human via internal alert channel.

## Testing

Webhook routes have integration tests in `tests/routes/` using supertest. Always add a test for new event types ג€” Make scenarios are hard to debug after the fact.