---
name: notion
description: |
  Notion via Apideck's Proxy API + managed Vault auth — Apideck handles auth and proxies HTTP calls to Notion's native API. Use when the user wants to call Notion (no unified API resource mapping). Routes through Apideck with serviceId "notion".
license: Apache-2.0
alwaysApply: false
metadata:
  author: apideck
  version: "1.0.0"
  serviceId: notion
  proxyOnly: true
  unifiedApis: []
  authType: oauth2
  tier: "2"
  verified: true
  status: beta
---

# Notion (via Apideck Proxy)

Access Notion through Apideck's **Proxy API** with managed Vault auth. Apideck stores credentials, refreshes tokens, and forwards your HTTP calls to Notion's native API — you keep using Notion's own request and response shapes, while Apideck eliminates per-tenant credential plumbing and gives you a single auth integration shared across every Apideck connector.

> **Auth-only / proxy-only connector.** Apideck does not map Notion to a unified-API resource model — your code talks Notion's own API directly through the Proxy. You still get Vault credential storage, token refresh, retries, and a consistent request envelope.

## Quick facts

- **Apideck serviceId:** `notion`
- **Mode:** Proxy-only (no unified API resources)
- **Auth type:** oauth2
- **Status:** beta
- **Apideck setup guide:** [OAuth credentials](https://unify.apideck.com/connector/connectors/notion/docs/application_owner+oauth_credentials)
- **Gotchas:** [page](https://developers.apideck.com/apis/proxy/notion/gotchas)
- **Notion docs:** https://developers.notion.com/
- **Homepage:** https://notion.so

## When to use this skill

Activate this skill when the user wants to call Notion via Apideck — for example, "call the Notion API" or "fetch data from Notion". This skill teaches the agent:

1. That Notion routes through Apideck's **Proxy API**, not a unified resource API
2. The correct `serviceId` to pass on every call (`notion`)
3. How to keep using Notion's native request/response shapes while Apideck handles Vault auth

If you need a unified-API surface (one method shape across many vendors), see the connector skills in this catalog whose serviceId is mapped to a unified API.

## Auth

- **Type:** OAuth 2.0
- **Managed by:** Apideck Vault — Apideck handles the full OAuth dance (authorization code flow, token exchange, refresh). Never ask the user for API keys or tokens directly.
- **User setup:** Users authorize via the Vault modal. Connection state progresses `available → added → authorized → callable`.
- **Token refresh:** automatic. Expired tokens are refreshed transparently on the next API call.

## Calling Notion via the Proxy API

Send any HTTP request to `https://unify.apideck.com/proxy`. Apideck looks up the user's stored Notion credentials by `x-apideck-consumer-id` + `x-apideck-service-id`, injects them on the way out, and returns Notion's raw response.

```bash
curl 'https://unify.apideck.com/proxy' \
  -H "Authorization: Bearer ${APIDECK_API_KEY}" \
  -H "x-apideck-app-id: ${APIDECK_APP_ID}" \
  -H "x-apideck-consumer-id: ${CONSUMER_ID}" \
  -H "x-apideck-service-id: notion" \
  -H "x-apideck-downstream-url: <target endpoint on Notion>" \
  -H "x-apideck-downstream-method: GET"
```

For `POST`/`PATCH`/`PUT`/`DELETE`, change `x-apideck-downstream-method` and pass the body as you would to Notion directly. Apideck does not transform the body — it forwards bytes.

See [Notion's API docs](https://developers.notion.com/) for available endpoints.

## See also

- [Apideck OAuth setup guide for Notion](https://unify.apideck.com/connector/connectors/notion/docs/application_owner+oauth_credentials)
- [Notion gotchas](https://developers.apideck.com/apis/proxy/notion/gotchas)
- [Apideck Proxy API reference](https://developers.apideck.com/apis/proxy/reference)
- [`apideck-rest`](../../skills/apideck-rest/) — REST patterns including the Proxy
- [`apideck-best-practices`](../../skills/apideck-best-practices/) — Vault, error handling, retries
- [`apideck-unified-api`](../../skills/apideck-unified-api/) — when to use unified vs proxy
- [Notion official docs](https://developers.notion.com/)
