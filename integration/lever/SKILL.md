---
name: lever
description: |
  Lever integration via Apideck's ATS unified API — same methods work across every connector in ATS, switch by changing `serviceId`. Use when the user wants to read, write, or sync jobs, applicants, and applications in Lever. Routes through Apideck with serviceId "lever".
license: Apache-2.0
alwaysApply: false
metadata:
  author: apideck
  version: "1.0.0"
  serviceId: lever
  unifiedApis: ["ats"]
  authType: oauth2
  tier: "1b"
  verified: true
  difficulty: straightforward
  partnershipRequired: false
  sandboxAvailable: true
---

# Lever (via Apideck)

Access Lever through Apideck's **ATS** unified API — one of 11 ATS connectors that share the same method surface. Code you write here ports to Greenhouse, Workday, Workable and 7 other ATS connectors by changing a single `serviceId` string. Apideck handles auth, pagination, rate limiting, and retries so you don't write per-tenant Lever plumbing.

## Quick facts

- **Apideck serviceId:** `lever`
- **Unified API:** ATS
- **Auth type:** oauth2
- **Gotchas:** [page](https://developers.apideck.com/apis/ats/lever/gotchas)
- **Lever docs:** https://hire.lever.co/developer
- **Homepage:** https://www.lever.co/

## At a glance

- **Implementation difficulty:** straightforward — Apideck OAuth App Available; No Partnership Required
- **Vendor partnership required:** no ([developer portal](https://www.lever.co/partnershipinterest)) — Only for your own OAuth app: joining gives you a client ID and secret plus an Integrator Sandbox, with production credentials after a Lever QA run-through.
- **Apideck-managed credentials:** available — OAuth consent shows Apideck as the requesting application.
- **Account type required:** Any Lever account.
- **Consumer access level:** A Lever Super Admin, who authorises the connection for the whole organisation.
- **Sandbox:** available ([signup](https://www.lever.co/partnershipinterest)) — An Integrator Sandbox account, issued once Lever approves your partnership interest form. Email is switched off in it, so invited users get no invitation.
- **Rate limits:** 10 requests per second steady state, with bursts up to 20 when possible.
- **Authentication:** Authorization Code flow; Lever issues no API keys to integrations.
- **Webhooks:** Virtual webhooks - applicant and job created and updated events, detected by polling.

> Facts synced from Apideck's connector metadata API — `GET /connector/connectors/lever` (`overview` field) is the live, authoritative version.

## When to use this skill

Activate this skill when the user explicitly wants to work with **Lever** — for example, "list open jobs in Lever" or "move an applicant through stages in Lever". This skill teaches the agent:

1. Which Apideck unified API covers Lever (ATS)
2. The correct `serviceId` to pass on every call (`lever`)
3. Lever-specific auth and coverage caveats

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

// List applicants in Lever
const { data } = await apideck.ats.applicants.list({
  serviceId: "lever",
});
```

## Portable across 11 ATS connectors

The Apideck **ATS** unified API exposes the same methods for every connector in its catalog. Switching from Lever to another ATS connector is a one-string change — no rewrite, no new SDK.

```typescript
// Today — Lever
await apideck.ats.applicants.list({ serviceId: "lever" });

// Tomorrow — same code, different connector
await apideck.ats.applicants.list({ serviceId: "greenhouse" });
await apideck.ats.applicants.list({ serviceId: "workday" });
```

This is the compounding advantage of using Apideck over integrating Lever directly: code against the unified ATS API once, gain access to every connector in it. New connectors Apideck adds become available to your app without code changes.

## Lever via Apideck ATS

Lever is a recruiting platform with strong pipeline tooling. Apideck maps its opportunity-centric model.

### Entity mapping

| Lever entity | Apideck ATS resource |
|---|---|
| Posting | `jobs` |
| Opportunity | `applicants` |
| Application (Opportunity on a Posting) | `applications` |
| Stage | exposed via `applications.current_stage` |

### Coverage highlights

- ✅ List postings (jobs) by status
- ✅ List and create opportunities (applicants)
- ✅ Create/update applications
- ✅ Move through stages
- ⚠️ Feedback forms and scorecards — use Proxy
- ❌ Nurture campaigns — use Proxy

### Auth

- **Type:** OAuth 2.0, managed by Apideck Vault
- **Org binding:** each connection is bound to one Lever org.
- **Scopes:** read/write on postings and opportunities; Apideck Vault requests the minimum needed.

### Example: create a candidate with source attribution

```typescript
const { data } = await apideck.ats.applicants.create({
  serviceId: "lever",
  applicant: {
    first_name: "Morgan",
    last_name: "Lee",
    emails: [{ email: "morgan@example.com", type: "personal" }],
    source: { name: "LinkedIn" },
  },
});
```

## Escape hatch: Proxy API

When an endpoint isn't covered by the ATS unified API, use Apideck's Proxy to call Lever directly — Apideck injects auth headers and handles token refresh. Set `x-apideck-downstream-url` to the target endpoint on Lever's own API:

```bash
curl 'https://unify.apideck.com/proxy' \
  -H "Authorization: Bearer ${APIDECK_API_KEY}" \
  -H "x-apideck-app-id: ${APIDECK_APP_ID}" \
  -H "x-apideck-consumer-id: ${CONSUMER_ID}" \
  -H "x-apideck-service-id: lever" \
  -H "x-apideck-downstream-url: <target endpoint on Lever>" \
  -H "x-apideck-downstream-method: GET"
```

See [Lever's API docs](https://hire.lever.co/developer) for available endpoints.

## Sibling connectors

Other **ATS** connectors that share this unified API surface (same method signatures, just change `serviceId`):

[`greenhouse`](../greenhouse/), [`workday`](../workday/), [`workable`](../workable/) *(beta)*, [`bullhorn-ats`](../bullhorn-ats/) *(beta)*, [`teamtailor`](../teamtailor/) *(beta)*, [`freshteam`](../freshteam/), [`jobadder`](../jobadder/) *(beta)*, [`recruitee`](../recruitee/), and 2 more.

## See also

- [ATS OpenAPI spec](https://specs.apideck.com/ats.yml) · [API Explorer](https://developers.apideck.com/api-explorer?id=ats)
- [`apideck-connector-coverage`](../../skills/apideck-connector-coverage/) — programmatic coverage checks
- [`apideck-best-practices`](../../skills/apideck-best-practices/) — architecture, Vault, pagination, error handling
- [`apideck-node`](../../skills/apideck-node/) — TypeScript / Node SDK patterns
- [Lever official docs](https://hire.lever.co/developer)
