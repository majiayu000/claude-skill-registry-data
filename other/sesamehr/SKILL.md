---
name: sesamehr
description: |
  Sesame HR via Apideck's Proxy API + managed Vault auth — Apideck handles auth and proxies HTTP calls to Sesame HR's native API. Use when the user wants to call Sesame HR (no unified API resource mapping). Routes through Apideck with serviceId "sesamehr".
license: Apache-2.0
alwaysApply: false
metadata:
  author: apideck
  version: "1.0.0"
  serviceId: sesamehr
  proxyOnly: true
  unifiedApis: []
  authType: apiKey
  tier: "2"
  verified: true
  status: early-access
---

# Sesame HR (via Apideck Proxy)

Access Sesame HR through Apideck's **Proxy API** with managed Vault auth. Apideck stores credentials, refreshes tokens, and forwards your HTTP calls to Sesame HR's native API — you keep using Sesame HR's own request and response shapes, while Apideck eliminates per-tenant credential plumbing and gives you a single auth integration shared across every Apideck connector.

> **Auth-only / proxy-only connector.** Apideck does not map Sesame HR to a unified-API resource model — your code talks Sesame HR's own API directly through the Proxy. You still get Vault credential storage, token refresh, retries, and a consistent request envelope.

## Quick facts

- **Apideck serviceId:** `sesamehr`
- **Mode:** Proxy-only (no unified API resources)
- **Auth type:** apiKey
- **Status:** early-access
- **Gotchas:** [page](https://developers.apideck.com/apis/proxy/sesamehr/gotchas)
- **Sesame HR docs:** https://developer.sesametime.com/
- **Homepage:** https://www.sesamehr.com/

## When to use this skill

Activate this skill when the user wants to call Sesame HR via Apideck — for example, "call the Sesame HR API" or "fetch data from Sesame HR". This skill teaches the agent:

1. That Sesame HR routes through Apideck's **Proxy API**, not a unified resource API
2. The correct `serviceId` to pass on every call (`sesamehr`)
3. How to keep using Sesame HR's native request/response shapes while Apideck handles Vault auth

If you need a unified-API surface (one method shape across many vendors), see the connector skills in this catalog whose serviceId is mapped to a unified API.

## Auth

- **Type:** API Key
- **Managed by:** Apideck Vault — the user pastes their Sesame HR API key into the Vault modal; Apideck stores it encrypted and injects it on every request.
- **Rotation:** if the user rotates their key, they re-enter it in Vault. No code changes needed.

## Calling Sesame HR via the Proxy API

Send any HTTP request to `https://unify.apideck.com/proxy`. Apideck looks up the user's stored Sesame HR credentials by `x-apideck-consumer-id` + `x-apideck-service-id`, injects them on the way out, and returns Sesame HR's raw response.

```bash
curl 'https://unify.apideck.com/proxy' \
  -H "Authorization: Bearer ${APIDECK_API_KEY}" \
  -H "x-apideck-app-id: ${APIDECK_APP_ID}" \
  -H "x-apideck-consumer-id: ${CONSUMER_ID}" \
  -H "x-apideck-service-id: sesamehr" \
  -H "x-apideck-downstream-url: <target endpoint on Sesame HR>" \
  -H "x-apideck-downstream-method: GET"
```

For `POST`/`PATCH`/`PUT`/`DELETE`, change `x-apideck-downstream-method` and pass the body as you would to Sesame HR directly. Apideck does not transform the body — it forwards bytes.

See [Sesame HR's API docs](https://developer.sesametime.com/) for available endpoints.

## See also

- [Sesame HR gotchas](https://developers.apideck.com/apis/proxy/sesamehr/gotchas)
- [Apideck Proxy API reference](https://developers.apideck.com/apis/proxy/reference)
- [`apideck-rest`](../../skills/apideck-rest/) — REST patterns including the Proxy
- [`apideck-best-practices`](../../skills/apideck-best-practices/) — Vault, error handling, retries
- [`apideck-unified-api`](../../skills/apideck-unified-api/) — when to use unified vs proxy
- [Sesame HR official docs](https://developer.sesametime.com/)
