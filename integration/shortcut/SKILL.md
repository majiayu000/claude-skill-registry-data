---
name: shortcut
description: |
  Shortcut via Apideck's Proxy API + managed Vault auth — Apideck handles auth and proxies HTTP calls to Shortcut's native API. Use when the user wants to call Shortcut (no unified API resource mapping). Routes through Apideck with serviceId "shortcut".
license: Apache-2.0
alwaysApply: false
metadata:
  author: apideck
  version: "1.0.0"
  serviceId: shortcut
  proxyOnly: true
  unifiedApis: []
  authType: apiKey
  tier: "2"
  verified: true
  status: beta
---

# Shortcut (via Apideck Proxy)

Access Shortcut through Apideck's **Proxy API** with managed Vault auth. Apideck stores credentials, refreshes tokens, and forwards your HTTP calls to Shortcut's native API — you keep using Shortcut's own request and response shapes, while Apideck eliminates per-tenant credential plumbing and gives you a single auth integration shared across every Apideck connector.

> **Auth-only / proxy-only connector.** Apideck does not map Shortcut to a unified-API resource model — your code talks Shortcut's own API directly through the Proxy. You still get Vault credential storage, token refresh, retries, and a consistent request envelope.

## Quick facts

- **Apideck serviceId:** `shortcut`
- **Mode:** Proxy-only (no unified API resources)
- **Auth type:** apiKey
- **Status:** beta
- **Apideck setup guide:** [OAuth credentials](https://unify.apideck.com/connector/connectors/shortcut/docs/application_owner+oauth_credentials)
- **Gotchas:** [page](https://developers.apideck.com/apis/proxy/shortcut/gotchas)
- **Shortcut docs:** https://developer.shortcut.com/api/rest/v3
- **Homepage:** https://shortcut.com/

## When to use this skill

Activate this skill when the user wants to call Shortcut via Apideck — for example, "call the Shortcut API" or "fetch data from Shortcut". This skill teaches the agent:

1. That Shortcut routes through Apideck's **Proxy API**, not a unified resource API
2. The correct `serviceId` to pass on every call (`shortcut`)
3. How to keep using Shortcut's native request/response shapes while Apideck handles Vault auth

If you need a unified-API surface (one method shape across many vendors), see the connector skills in this catalog whose serviceId is mapped to a unified API.

## Auth

- **Type:** API Key
- **Managed by:** Apideck Vault — the user pastes their Shortcut API key into the Vault modal; Apideck stores it encrypted and injects it on every request.
- **Rotation:** if the user rotates their key, they re-enter it in Vault. No code changes needed.

## Calling Shortcut via the Proxy API

Send any HTTP request to `https://unify.apideck.com/proxy`. Apideck looks up the user's stored Shortcut credentials by `x-apideck-consumer-id` + `x-apideck-service-id`, injects them on the way out, and returns Shortcut's raw response.

```bash
curl 'https://unify.apideck.com/proxy' \
  -H "Authorization: Bearer ${APIDECK_API_KEY}" \
  -H "x-apideck-app-id: ${APIDECK_APP_ID}" \
  -H "x-apideck-consumer-id: ${CONSUMER_ID}" \
  -H "x-apideck-service-id: shortcut" \
  -H "x-apideck-downstream-url: <target endpoint on Shortcut>" \
  -H "x-apideck-downstream-method: GET"
```

For `POST`/`PATCH`/`PUT`/`DELETE`, change `x-apideck-downstream-method` and pass the body as you would to Shortcut directly. Apideck does not transform the body — it forwards bytes.

See [Shortcut's API docs](https://developer.shortcut.com/api/rest/v3) for available endpoints.

## See also

- [Apideck OAuth setup guide for Shortcut](https://unify.apideck.com/connector/connectors/shortcut/docs/application_owner+oauth_credentials)
- [Shortcut gotchas](https://developers.apideck.com/apis/proxy/shortcut/gotchas)
- [Apideck Proxy API reference](https://developers.apideck.com/apis/proxy/reference)
- [`apideck-rest`](../../skills/apideck-rest/) — REST patterns including the Proxy
- [`apideck-best-practices`](../../skills/apideck-best-practices/) — Vault, error handling, retries
- [`apideck-unified-api`](../../skills/apideck-unified-api/) — when to use unified vs proxy
- [Shortcut official docs](https://developer.shortcut.com/api/rest/v3)
