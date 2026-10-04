---
name: monday
description: |
  monday.com via Apideck's Proxy API + managed Vault auth — Apideck handles auth and proxies HTTP calls to monday.com's native API. Use when the user wants to call monday.com (no unified API resource mapping). Routes through Apideck with serviceId "monday".
license: Apache-2.0
alwaysApply: false
metadata:
  author: apideck
  version: "1.0.0"
  serviceId: monday
  proxyOnly: true
  unifiedApis: []
  authType: apiKey
  tier: "2"
  verified: true
  status: beta
  difficulty: moderate
  partnershipRequired: false
  sandboxAvailable: true
---

# monday.com (via Apideck Proxy)

Access monday.com through Apideck's **Proxy API** with managed Vault auth. Apideck stores credentials, refreshes tokens, and forwards your HTTP calls to monday.com's native API — you keep using monday.com's own request and response shapes, while Apideck eliminates per-tenant credential plumbing and gives you a single auth integration shared across every Apideck connector.

> **Auth-only / proxy-only connector.** Apideck does not map monday.com to a unified-API resource model — your code talks monday.com's own API directly through the Proxy. You still get Vault credential storage, token refresh, retries, and a consistent request envelope.

## Quick facts

- **Apideck serviceId:** `monday`
- **Mode:** Proxy-only (no unified API resources)
- **Auth type:** apiKey
- **Status:** beta
- **Apideck setup guide:** [OAuth credentials](https://unify.apideck.com/connector/connectors/monday/docs/application_owner+oauth_credentials)
- **Gotchas:** [page](https://developers.apideck.com/apis/proxy/monday/gotchas)
- **monday.com docs:** https://developer.monday.com/api-reference/docs
- **Homepage:** https://monday.com/

## At a glance

- **Implementation difficulty:** moderate — Personal API Token - Each Consumer Copies Their Own Token from monday.com
- **Vendor partnership required:** no
- **Apideck-managed credentials:** not available — Apideck holds no shared monday.com test account.
- **Account type required:** A monday.com account where the connecting user is an admin or member; viewers, guests, deactivated users and student accounts cannot use a personal API token.
- **Consumer access level:** The token mirrors the connecting user's permissions in monday.com, so the connection sees only the workspaces, boards and items that user can open.
- **Sandbox:** available ([signup](https://developer.monday.com/api-reference/docs/developer-sandbox-account)) — A free monday.com developer account, kept separate from production data, gives you a token to test with.
- **Costs:** API access is included in every monday.com plan.
- **Rate limits:** Daily call cap by plan: 1,000 (Free, Standard, Basic), 10,000 (Pro), 25,000 (Enterprise); per-minute query cap of 1,000 to 5,000 by plan.
- **Authentication:** The consumer's personal API token sent in the Authorization header; not OAuth.
- **Webhooks:** No webhooks - monday.com events are not surfaced; poll for changes through the Proxy API instead.

**Important to know:**

- monday.com is an auth-only connector: there are no unified Project Management or Issue Tracking endpoints. Every read and write goes through the Proxy API as a GraphQL request against monday.com's own API.

> Facts synced from Apideck's connector metadata API — `GET /connector/connectors/monday` (`overview` field) is the live, authoritative version.

## When to use this skill

Activate this skill when the user wants to call monday.com via Apideck — for example, "call the monday.com API" or "fetch data from monday.com". This skill teaches the agent:

1. That monday.com routes through Apideck's **Proxy API**, not a unified resource API
2. The correct `serviceId` to pass on every call (`monday`)
3. How to keep using monday.com's native request/response shapes while Apideck handles Vault auth

If you need a unified-API surface (one method shape across many vendors), see the connector skills in this catalog whose serviceId is mapped to a unified API.

## Auth

- **Type:** API Key
- **Managed by:** Apideck Vault — the user pastes their monday.com API key into the Vault modal; Apideck stores it encrypted and injects it on every request.
- **Rotation:** if the user rotates their key, they re-enter it in Vault. No code changes needed.

## Calling monday.com via the Proxy API

Send any HTTP request to `https://unify.apideck.com/proxy`. Apideck looks up the user's stored monday.com credentials by `x-apideck-consumer-id` + `x-apideck-service-id`, injects them on the way out, and returns monday.com's raw response.

```bash
curl 'https://unify.apideck.com/proxy' \
  -H "Authorization: Bearer ${APIDECK_API_KEY}" \
  -H "x-apideck-app-id: ${APIDECK_APP_ID}" \
  -H "x-apideck-consumer-id: ${CONSUMER_ID}" \
  -H "x-apideck-service-id: monday" \
  -H "x-apideck-downstream-url: <target endpoint on monday.com>" \
  -H "x-apideck-downstream-method: GET"
```

For `POST`/`PATCH`/`PUT`/`DELETE`, change `x-apideck-downstream-method` and pass the body as you would to monday.com directly. Apideck does not transform the body — it forwards bytes.

See [monday.com's API docs](https://developer.monday.com/api-reference/docs) for available endpoints.

## See also

- [Apideck OAuth setup guide for monday.com](https://unify.apideck.com/connector/connectors/monday/docs/application_owner+oauth_credentials)
- [monday.com gotchas](https://developers.apideck.com/apis/proxy/monday/gotchas)
- [Apideck Proxy API reference](https://developers.apideck.com/apis/proxy/reference)
- [`apideck-rest`](../../skills/apideck-rest/) — REST patterns including the Proxy
- [`apideck-best-practices`](../../skills/apideck-best-practices/) — Vault, error handling, retries
- [`apideck-unified-api`](../../skills/apideck-unified-api/) — when to use unified vs proxy
- [monday.com official docs](https://developer.monday.com/api-reference/docs)
