---
name: workable
description: |
  Workable integration via Apideck's ATS unified API — same methods work across every connector in ATS, switch by changing `serviceId`. Use when the user wants to read, write, or sync jobs, applicants, and applications in Workable. Routes through Apideck with serviceId "workable".
license: Apache-2.0
alwaysApply: false
metadata:
  author: apideck
  version: "1.0.0"
  serviceId: workable
  unifiedApis: ["ats"]
  authType: oauth2
  tier: "1b"
  verified: true
  status: beta
  difficulty: straightforward
  partnershipRequired: false
  sandboxAvailable: true
---

# Workable (via Apideck)

Access Workable through Apideck's **ATS** unified API — one of 11 ATS connectors that share the same method surface. Code you write here ports to Greenhouse, Workday, Lever and 7 other ATS connectors by changing a single `serviceId` string. Apideck handles auth, pagination, rate limiting, and retries so you don't write per-tenant Workable plumbing.

> **Beta connector.** Workable is currently in beta on Apideck. Expect partial resource coverage and occasional mapping gaps. Always verify coverage (see below) and fall back to the Proxy API for unsupported operations.

## Quick facts

- **Apideck serviceId:** `workable`
- **Unified API:** ATS
- **Auth type:** oauth2
- **Status:** beta
- **Gotchas:** [page](https://developers.apideck.com/apis/ats/workable/gotchas)
- **Workable docs:** https://workable.readme.io
- **Homepage:** https://workable.com

## At a glance

- **Implementation difficulty:** straightforward — Self-Service OAuth via Apideck's Approved Workable App, No Partnership of Your Own
- **Vendor partnership required:** no
- **Apideck-managed credentials:** available — OAuth shows "Apideck" as the requesting application.
- **Account type required:** Workable account, identified by its account subdomain.
- **Consumer access level:** Workable does not state a minimum role for the authorisation. The connection then reaches only the jobs and candidates the authorising user can access.
- **Sandbox:** available ([signup](https://www.workable.com/free-trial)) — 15-day free Workable trial, no card required; Workable does not say whether trial accounts can use the API.
- **Costs:** Workable publishes no API fee and does not say which plans include API access.
- **Rate limits:** 50 requests per 10 seconds.
- **Authentication:** Authorization Code flow.
- **Webhooks:** Virtual webhooks - applicant and job created and updated events.

> Facts synced from Apideck's connector metadata API — `GET /connector/connectors/workable` (`overview` field) is the live, authoritative version.

## When to use this skill

Activate this skill when the user explicitly wants to work with **Workable** — for example, "list open jobs in Workable" or "move an applicant through stages in Workable". This skill teaches the agent:

1. Which Apideck unified API covers Workable (ATS)
2. The correct `serviceId` to pass on every call (`workable`)
3. Workable-specific auth and coverage caveats

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

// List applicants in Workable
const { data } = await apideck.ats.applicants.list({
  serviceId: "workable",
});
```

## Portable across 11 ATS connectors

The Apideck **ATS** unified API exposes the same methods for every connector in its catalog. Switching from Workable to another ATS connector is a one-string change — no rewrite, no new SDK.

```typescript
// Today — Workable
await apideck.ats.applicants.list({ serviceId: "workable" });

// Tomorrow — same code, different connector
await apideck.ats.applicants.list({ serviceId: "greenhouse" });
await apideck.ats.applicants.list({ serviceId: "workday" });
```

This is the compounding advantage of using Apideck over integrating Workable directly: code against the unified ATS API once, gain access to every connector in it. New connectors Apideck adds become available to your app without code changes.

## Workable via Apideck ATS

Workable is a mid-market recruiting platform. Apideck maps its candidate-centric model.

### Entity mapping

| Workable entity | Apideck ATS resource |
|---|---|
| Job | `jobs` |
| Candidate | `applicants` |
| Application (candidate on a job) | `applications` |
| Stage | exposed via `applications.current_stage` |

### Coverage highlights

- ✅ List jobs (with status filter: published, draft, archived)
- ✅ List and create candidates
- ✅ Create applications (link candidate to job)
- ✅ Move candidates through stages via `application.current_stage`
- ⚠️ Requisitions and offers — not in unified; use Proxy

### Auth

- **Type:** OAuth 2.0, managed by Apideck Vault
- **Subdomain binding:** each connection is bound to one Workable subdomain.

### Example: list published jobs

```typescript
const { data } = await apideck.ats.jobs.list({
  serviceId: "workable",
  filter: { status: "published" },
});
```

## Escape hatch: Proxy API

When an endpoint isn't covered by the ATS unified API, use Apideck's Proxy to call Workable directly — Apideck injects auth headers and handles token refresh. Set `x-apideck-downstream-url` to the target endpoint on Workable's own API:

```bash
curl 'https://unify.apideck.com/proxy' \
  -H "Authorization: Bearer ${APIDECK_API_KEY}" \
  -H "x-apideck-app-id: ${APIDECK_APP_ID}" \
  -H "x-apideck-consumer-id: ${CONSUMER_ID}" \
  -H "x-apideck-service-id: workable" \
  -H "x-apideck-downstream-url: <target endpoint on Workable>" \
  -H "x-apideck-downstream-method: GET"
```

See [Workable's API docs](https://workable.readme.io) for available endpoints.

## Sibling connectors

Other **ATS** connectors that share this unified API surface (same method signatures, just change `serviceId`):

[`greenhouse`](../greenhouse/), [`workday`](../workday/), [`lever`](../lever/), [`bullhorn-ats`](../bullhorn-ats/) *(beta)*, [`teamtailor`](../teamtailor/) *(beta)*, [`freshteam`](../freshteam/), [`jobadder`](../jobadder/) *(beta)*, [`recruitee`](../recruitee/), and 2 more.

## See also

- [ATS OpenAPI spec](https://specs.apideck.com/ats.yml) · [API Explorer](https://developers.apideck.com/api-explorer?id=ats)
- [`apideck-connector-coverage`](../../skills/apideck-connector-coverage/) — programmatic coverage checks
- [`apideck-best-practices`](../../skills/apideck-best-practices/) — architecture, Vault, pagination, error handling
- [`apideck-node`](../../skills/apideck-node/) — TypeScript / Node SDK patterns
- [Workable official docs](https://workable.readme.io)
