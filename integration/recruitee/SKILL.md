---
name: recruitee
description: |
  Recruitee integration via Apideck's ATS unified API — same methods work across every connector in ATS, switch by changing `serviceId`. Use when the user wants to read, write, or sync jobs, applicants, and applications in Recruitee. Routes through Apideck with serviceId "recruitee".
license: Apache-2.0
alwaysApply: false
metadata:
  author: apideck
  version: "1.0.0"
  serviceId: recruitee
  unifiedApis: ["ats"]
  authType: apiKey
  tier: "2"
  verified: true
  difficulty: moderate
  partnershipRequired: false
  sandboxAvailable: true
---

# Recruitee (via Apideck)

Access Recruitee through Apideck's **ATS** unified API — one of 11 ATS connectors that share the same method surface. Code you write here ports to Greenhouse, Workday, Lever and 7 other ATS connectors by changing a single `serviceId` string. Apideck handles auth, pagination, rate limiting, and retries so you don't write per-tenant Recruitee plumbing.

## Quick facts

- **Apideck serviceId:** `recruitee`
- **Unified API:** ATS
- **Auth type:** apiKey
- **Apideck setup guide:** [Connection guide](https://developers.apideck.com/connectors/recruitee/docs/consumer+connection)
- **Gotchas:** [page](https://developers.apideck.com/apis/ats/recruitee/gotchas)
- **Homepage:** https://recruitee.com/

## At a glance

- **Implementation difficulty:** moderate — Personal API Token + Company ID Each Consumer Supplies
- **Vendor partnership required:** no ([Recruitee Marketplace Technology Partner programme](https://tellent.com/technology-partner-application)) — Joining the Marketplace Technology Partner programme gives you a Recruitee test environment to build in, and a Marketplace listing after a demo and approval.
- **Apideck-managed credentials:** not available — Each consumer creates their own personal API token in Recruitee.
- **Account type required:** Recruitee account on a plan with API access. The token belongs to one company; an owner with several companies needs one token per company.
- **Consumer access level:** A user whose Hiring role includes the Manage API tokens permission; the connection reaches only what that user can see.
- **Sandbox:** available ([signup](https://auth.tellent.com/sign-up)) — 18-day free trial of the Advance plan, as account administrator; no automatic subscription.
- **Costs:** No separate API fee is published. The pricing page lists API access from the Start plan; direct API support from Recruitee is limited to the Optimize plan.
- **Rate limits:** 1,000 requests a minute per API token.
- **Authentication:** Personal API token sent as a bearer token, plus the Company ID; not OAuth.
- **Webhooks:** Virtual webhooks - applicant created and updated, job created and updated

**Important to know:**

- The token is personal: it stops working if its creator revokes it or leaves the company, and only that user can see it, so a lost token means creating a new one and reconnecting.

> Facts synced from Apideck's connector metadata API — `GET /connector/connectors/recruitee` (`overview` field) is the live, authoritative version.

## When to use this skill

Activate this skill when the user explicitly wants to work with **Recruitee** — for example, "list open jobs in Recruitee" or "move an applicant through stages in Recruitee". This skill teaches the agent:

1. Which Apideck unified API covers Recruitee (ATS)
2. The correct `serviceId` to pass on every call (`recruitee`)
3. Recruitee-specific auth and coverage caveats

For the full method surface (parameters, pagination, filtering), use your language SDK skill:

- [`apideck-node`](../../skills/apideck-node/), [`apideck-python`](../../skills/apideck-python/), [`apideck-dotnet`](../../skills/apideck-dotnet/), [`apideck-java`](../../skills/apideck-java/), [`apideck-go`](../../skills/apideck-go/), [`apideck-php`](../../skills/apideck-php/), or [`apideck-rest`](../../skills/apideck-rest/)

For the raw OpenAPI spec:

- **ATS:** [https://specs.apideck.com/ats.yml](https://specs.apideck.com/ats.yml) · [API Explorer](https://developers.apideck.com/api-explorer?id=ats)

## Minimal example (TypeScript)

```typescript
import { Apideck } from "@apideck/unify";

const apideck = new Apideck({
  apiKey: process.env.APIDECK_API_KEY,
  appId: process.env.APIDECK_APP_ID,
  consumerId: "your-consumer-id",
});

// List applicants in Recruitee
const { data } = await apideck.ats.applicants.list({
  serviceId: "recruitee",
});
```

## Portable across 11 ATS connectors

The Apideck **ATS** unified API exposes the same methods for every connector in its catalog. Switching from Recruitee to another ATS connector is a one-string change — no rewrite, no new SDK.

```typescript
// Today — Recruitee
await apideck.ats.applicants.list({ serviceId: "recruitee" });

// Tomorrow — same code, different connector
await apideck.ats.applicants.list({ serviceId: "greenhouse" });
await apideck.ats.applicants.list({ serviceId: "workday" });
```

This is the compounding advantage of using Apideck over integrating Recruitee directly: code against the unified ATS API once, gain access to every connector in it. New connectors Apideck adds become available to your app without code changes.

## Authentication

- **Type:** API Key
- **Managed by:** Apideck Vault — the user pastes their Recruitee API key into the Vault modal; Apideck stores it encrypted and injects it on every request.
- **Rotation:** if the user rotates their key, they re-enter it in Vault. No code changes needed.

**Setup guide:** Apideck publishes a step-by-step guide for registering an OAuth app / configuring credentials for Recruitee — see [https://developers.apideck.com/connectors/recruitee/docs/consumer+connection](https://developers.apideck.com/connectors/recruitee/docs/consumer+connection). Use that as the authoritative source when walking users through connection setup.

See [`apideck-best-practices`](../../skills/apideck-best-practices/) for Vault setup, connection lifecycle, and handling re-auth flows.

## Verifying coverage

Not every ATS operation is supported by every connector. Always verify before assuming a method works:

```bash
curl 'https://unify.apideck.com/connector/connectors/recruitee' \
  -H "Authorization: Bearer ${APIDECK_API_KEY}" \
  -H "x-apideck-app-id: ${APIDECK_APP_ID}"
```

See [`apideck-connector-coverage`](../../skills/apideck-connector-coverage/) for patterns around `UnsupportedOperationError` and connector-specific fallbacks.

## Escape hatch: Proxy API

When an endpoint isn't covered by the ATS unified API, use Apideck's Proxy to call Recruitee directly — Apideck injects auth headers and handles token refresh. Set `x-apideck-downstream-url` to the target endpoint on Recruitee's own API:

```bash
curl 'https://unify.apideck.com/proxy' \
  -H "Authorization: Bearer ${APIDECK_API_KEY}" \
  -H "x-apideck-app-id: ${APIDECK_APP_ID}" \
  -H "x-apideck-consumer-id: ${CONSUMER_ID}" \
  -H "x-apideck-service-id: recruitee" \
  -H "x-apideck-downstream-url: <target endpoint on Recruitee>" \
  -H "x-apideck-downstream-method: GET"
```

See [Recruitee's API docs](#) for available endpoints.

## Sibling connectors

Other **ATS** connectors that share this unified API surface (same method signatures, just change `serviceId`):

[`greenhouse`](../greenhouse/), [`workday`](../workday/), [`lever`](../lever/), [`workable`](../workable/) *(beta)*, [`bullhorn-ats`](../bullhorn-ats/) *(beta)*, [`teamtailor`](../teamtailor/) *(beta)*, [`freshteam`](../freshteam/), [`jobadder`](../jobadder/) *(beta)*, and 2 more.

## See also

- [Apideck connection guide for Recruitee](https://developers.apideck.com/connectors/recruitee/docs/consumer+connection)
- [ATS OpenAPI spec](https://specs.apideck.com/ats.yml) · [API Explorer](https://developers.apideck.com/api-explorer?id=ats)
- [`apideck-connector-coverage`](../../skills/apideck-connector-coverage/) — programmatic coverage checks
- [`apideck-best-practices`](../../skills/apideck-best-practices/) — architecture, Vault, pagination, error handling
- [`apideck-node`](../../skills/apideck-node/) — TypeScript / Node SDK patterns
