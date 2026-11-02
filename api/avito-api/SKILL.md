---
name: avito-api
description: >-
  Integrate and troubleshoot Avito Business API: listings, Messenger, orders,
  delivery, jobs, Autoload, Autoteka, Promo and Ads. Look up bundled endpoint
  schemas, choose authentication and official Ads SDKs, and check migrations.
  Use for Avito API requests and integrations, not ordinary browsing of avito.ru.
---

# Avito Business API

Use the bundled OpenAPI snapshot to find Avito operations, then verify the relevant live section when freshness matters. It contains **248 paths / 256 operations / 27 sections**, fetched from the official catalog on **2026-10-03**.

Refresh attempted on **2026-10-18**: the catalog returned HTTP 429, and browser
access was blocked by the browser security policy. The bundled schema retains
its original date; current endpoint changes remain unverified. Official Ads SDK
revisions were rechecked on 2026-10-18 and are unchanged. See
[source verification](references/sources.md).

The developer portal moved to `www.avito.ru/developers`; each section guide in `references/sections/` ends with the official changelog (`## История изменений`) — check it for migrations. See [sources and refresh procedure](references/sources.md) for provenance and how to rebuild the snapshot with `scripts/build_spec.py`.

Run the commands below from this skill's directory, or use absolute script paths. The ~2 MB spec is intended for targeted lookup, not a full context load.

## Choose the product and client

- **Business API** (listings, Messenger, Autoload, etc.): use the endpoint lookup and an existing HTTP client in the project.
- **Авито Реклама / Ads**: first consider the official Python, Go, TypeScript or PHP SDK. Read [Ads SDK integration](references/ads-sdk.md) for selection, account credentials, environments and retry behavior.
- **Авито Promo** is the agency API (`avito-promo`); the Ads SDKs do not cover it. Autoteka also has its own product credentials and host conventions.

## Authentication — OAuth2 Client Credentials

Almost every endpoint requires a Bearer token. Cache it according to the token response's `expires_in` (commonly 86400 seconds for Business API; product-specific tokens can differ). For Business API, obtain `client_id` and `client_secret` through the account's API settings / [developer portal](https://www.avito.ru/developers); availability depends on the product and account permissions. For Ads, an administrator creates separate keys in the advertising cabinet's API tab, tied to a specific advertising account. See the matching section guide before requesting credentials.

**Get a token:**

```bash
AVITO_CLIENT_ID=... AVITO_CLIENT_SECRET=... \
  python3 scripts/get_token.py
# prints just the access_token; add --json for the full response
```

Or directly:

```bash
curl -s -X POST https://api.avito.ru/token \
  -H "Content-Type: application/x-www-form-urlencoded" \
  --data-urlencode "grant_type=client_credentials" \
  --data-urlencode "client_id=$AVITO_CLIENT_ID" \
  --data-urlencode "client_secret=$AVITO_CLIENT_SECRET"
# {"access_token":"...","token_type":"Bearer","expires_in":86400}
```

**Use the token** in every API call as `Authorization: Bearer <token>`. On `401` — refresh and retry once. Don't re-fetch the token before every call; cache it for the session and refresh on expiry/401.

Use **Client Credentials** for your own account and **Authorization Code** with the declared scopes for another user's delegated access. `show` returns the operation's `security` and matching `securitySchemes`. Separate objects in the `security` array are alternatives: `[ {"AuthorizationCode": ["messenger:read"]}, {"ClientCredentials": []} ]` permits either scheme. The presence of `AuthorizationCode` alone does not mean Client Credentials is unavailable. For Authorization Code setup and refresh tokens, read [references/sections/auth.md](references/sections/auth.md).

## How to find the right endpoint — DO THIS FIRST

The OpenAPI spec is too big to read whole. The skill ships a CLI to navigate it:

```bash
# 1) See all categories with endpoint counts
python3 scripts/lookup_endpoint.py tags

# 2) Find endpoints by keyword (matches path, summary, tag — case-insensitive,
#    auto-falls-back to a shorter stem so Russian inflections work)
python3 scripts/lookup_endpoint.py search чат
python3 scripts/lookup_endpoint.py search остатки      # finds "Управление остатками" too
python3 scripts/lookup_endpoint.py search --tag Продвижение
python3 scripts/lookup_endpoint.py search /autoload/v2

# 3) Get the full operation details (parameters, request/response schemas, rate limit)
python3 scripts/lookup_endpoint.py show '/messenger/v2/accounts/{user_id}/chats'
python3 scripts/lookup_endpoint.py show /stock-management/1/info --method post
```

`show` resolves top-level `$ref` for readability but leaves nested refs alone — for a deeper schema, read `references/avito-api-openapi.json` directly with `jq`:

```bash
jq '.components.schemas.stocksInfoResult' references/avito-api-openapi.json
```

For a category overview, browse [references/index.md](references/index.md) — a flat per-section list of all paths and summaries.

**Per-section integration docs.** Every section also has a markdown doc in `references/sections/<slug>.md` — these are the official Avito integration guides (sandbox setup, examples, edge cases, scope details) and they're often more useful than the OpenAPI spec for non-trivial flows. Available slugs (load on demand):

`accounts-hierarchy`, `ads`, `auction`, `auth`, `autoload`, `autostrategy`, `autoteka`, `avito-promo`, `calltracking`, `cpa`, `cpxpromo`, `delivery-sandbox`, `digital-goods`, `item`, `job`, `messenger`, `order-management`, `promotion`, `ratings`, `sbc-gateway`, `stock-management`, `str`, `tariff`, `tariff-composition`, `trxpromo`, `user`.

(`realty-reports` is in the catalog/OpenAPI but the catalog publishes no guide for it, so there is no `sections/realty-reports.md`.)

**Why this matters:** the spec has many similar-looking paths (`/messenger/v1/...` vs `/messenger/v2/...`, ru/en duplicate tags, deprecated endpoints with newer replacements). Guessing leads to 404s, wrong schemas, or calling deprecated paths. Always look up before composing a request.

## Calling pattern

Once you have the endpoint details and a token:

```bash
ACCESS_TOKEN=$(AVITO_CLIENT_ID=... AVITO_CLIENT_SECRET=... python3 scripts/get_token.py)

# example: list user's items
curl -s "https://api.avito.ru/core/v1/items" \
  -H "Authorization: Bearer $ACCESS_TOKEN" \
  | jq .

# example: send a chat message (Messenger v1)
curl -s -X POST "https://api.avito.ru/messenger/v1/accounts/$USER_ID/chats/$CHAT_ID/messages" \
  -H "Authorization: Bearer $ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"type":"text","message":{"text":"Здравствуйте! Чем могу помочь?"}}'
```

For direct Python calls, use the project's HTTP client (`requests` or `httpx`) with a timeout and the same Bearer header. For Ads integrations, compare this with the [official SDKs](references/ads-sdk.md) before implementing token caching and pagination yourself.

## Conventions and gotchas

- **Base URL** for Business API is `https://api.avito.ru`. Check `servers`, operation prose and the section guide for product-specific hosts and sandbox prefixes. Operations of sections on another host carry an operation-level `servers` (Автотека: `https://pro.autoteka.ru`). The merged `/token` is canonical to Авторизация (`api.avito.ru`); Автотека also publishes it (`x-avito-also-in`) and its guide uses `https://pro.autoteka.ru/token/`. `scripts/get_token.py` targets `api.avito.ru/token` for Business/Ads credentials and does not support the Autoteka host. Shared path names do not make credentials or token lifetimes interchangeable.
- **User ID** (`user_id` in messenger and similar endpoints) is the numeric Avito account ID, not the login. Get it from `GET /core/v1/accounts/self`.
- **Rate limits** are per-endpoint. The spec exposes them in `x-rate-limiter.default` (requests per minute). Some endpoints cap at 5 rpm (CallTracking), others at 1000 rpm. Respect them — `429` responses are common otherwise.
- **Pagination** is mostly `limit`/`offset` query params. Some newer endpoints use cursor-based pagination; check the response schema with `show`.
- **Date formats** are RFC3339 unless the field description says otherwise. Some Autoload endpoints use Unix timestamps.
- **Timezones**: many endpoints accept and return UTC. Don't pass local time without a `Z` or `+03:00` suffix.
- **Versioning**: prefer the documented replacement for an operation with `deprecated: true` or a deprecation notice. A higher version number alone does not prove equivalent behavior; compare its schema and migration guide.
- **Autoload deprecation / migration:** several Autoload report/list methods have a retirement schedule in the bundled guide: partial degradation from **08.09.2026** (methods start returning less data); removal with **HTTP 410 Gone** on **08.03.2027**. Prefer the current v4 upload-status paths (`/autoload/v4/uploads/...`) and read `sections/autoload.md` + the catalog migration plan before writing new Autoload integrations.
- **Shared path+method across sections:** a few operations appear in more than one catalog section (e.g. Promo agency stats vs item stats, `/token` in auth vs autoteka). The merged OpenAPI keeps one **canonical** body (`x-avito-section`) and lists other publishers in `x-avito-also-in`. Same-named components with different content are kept apart as `<name>__<slug>` (e.g. `Campaign__autostrategy`), so `$ref`s always point to the publishing section's schema. Non-default hosts have separate auth schemes: `ClientCredentials__autoteka` retains Autoteka's token URL, while `ClientCredentials` uses `api.avito.ru`. The source typo `Client Credentials` in autostrategy is normalized to its declared `ClientCredentials`; `x-avito-original-security` retains the original. Do not invent extra OAuth scopes for Авито Promo — official Promo agency ops use the section’s published `security` (typically Client Credentials as declared on the operation); check `show` rather than assuming scopes.
- **Russian/English duplicate tags** (`Messenger` and `Мессенджер`, `Доставка`, etc.) refer to the same endpoints. The lookup tool handles both — search either language.
- **Spec text vs JSON schema can disagree on limits.** For example, `POST /stock-management/1/info` describes a maximum of 10 items while the schema sets `maxItems: 500`. Use the stricter documented cap and verify conflicting limits with the official section or support. Treat `x-rate-limiter.default` as the published limit; apply a stricter observed limit if the API returns `429`.
- **Field naming is mostly camelCase but stock-management uses snake_case** (`item_ids`, `external_id`, `is_unlimited`). Don't assume one convention across the API — read the request body schema with `show` before composing.

## Errors

Standard HTTP codes. **The error body shape is not consistent across endpoints** — Avito uses several. The two most common ones in the wild:

```json
// shape A — short list of human-readable strings
{"errors": ["Тариф должен принадлежать к категории \"Транспорт\"."]}

// shape B — single structured error
{"error": {"code": 400, "message": "human-readable reason"}}
```

Other endpoints return `{"result": {"status": "error", "messages": [...]}}` or a bare `{"message": "...", "code": N}`. Don't write code that depends on one specific shape — retain the diagnostic fields needed to explain the failure, redact secrets and personal data, and extract the error message for display. Check HTTP status and Content-Type before JSON decoding; the portal or a proxy can return HTML.

Common codes:

- `400` — validation: re-read the request schema with `show`.
- `401` — token expired or revoked: refresh once and retry.
- `403` — access denied: check the chosen auth scheme, delegated scopes, account ownership and product/tariff permissions. Switching to Authorization Code is appropriate for delegated access, not a general fix for `403`.
- `404` — wrong path, wrong ID, item belongs to a different user, OR a soft "not applicable" (e.g. `/tariff/info/1` returns 404 with `errors: [...]` for non-Транспорт accounts — that's not a path bug).
- `429` — rate limit: honor `Retry-After` when present, reduce request rate, and use bounded backoff with jitter. Apply the write-retry rule below when completion is uncertain.
- `5xx` / timeout — retry reads with bounded backoff. For writes (messages, orders, funds, promotion), first verify whether the operation already succeeded; retry only when the documented idempotency mechanism or a confirmed failure makes it safe.

When reporting an error, include the HTTP code and relevant redacted response fields. Exclude tokens, credentials and unrelated personal data.

## Sections at a glance

27 sections, sorted by endpoint count (canonical `x-avito-section` attribution). Full list with paths is in [references/index.md](references/index.md).

| Section | # | Notes |
|---|---:|---|
| Доставка | 31 | Avito Доставка integration: parcel processing, tariffs, sandbox. Includes B2C Дверь–Терминал and reverse-direction flows. Detailed sandbox docs in `sections/delivery-sandbox.md`. |
| Автотека | 26 | Paid car history reports. Host `https://pro.autoteka.ru`, own credentials. |
| Авито.Работа | 25 | Vacancies, applications, resumes, webhooks. Mix of v1 and v2; check each operation's schema and migration notes. |
| Авито Реклама | 24 | Ads cabinet API (`/ads/v1/...`): accounts, advertisers, contracts, campaigns/groups/creatives stats, budgets. Schema 1.3.0: lists return `statusReasons`/`topStatusReason` (tolerate unknown codes); `BudgetFrequency` is only `entirePeriod`. Own `client_id`/`client_secret` from the Авито Реклама cabinet (per ad account). Sandbox at `/ads-sandbox/`. Sandbox account creation can return `207 Multi-Status` when account creation succeeds but test-data preparation is incomplete; inspect `warnings`. See `sections/ads.md` and [official SDKs](references/ads-sdk.md). |
| Автозагрузка | 22 | Bulk listing upload via XML/JSON feeds. Prefer `/autoload/v4/uploads/...` for upload status. Legacy report/list methods: partial degradation from **08.09.2026**, removal / **410 Gone** on **08.03.2027** — see `sections/autoload.md` and the official migration plan. |
| Мессенджер | 13 | Bundled snapshot: v2 for chat reads, v3 for message reads and webhook subscription. Sending text messages uses `POST /messenger/v1/.../messages`. Check each operation's version independently. |
| Управление заказами | 12 | Order lifecycle for marketplace sellers, including label generation. |
| CPA Авито | 11 | Performance-billing actions, complaints, chats by time. |
| Авито Promo | 11 | Agency API (`avito-promo`): client list/invite/INN checks, agency balance & transfers, client stats. Official catalog also publishes 2 stats paths shared with Объявления (`x-avito-also-in`); use `show` for the canonical security/schema. Do not invent Promo-specific OAuth scopes beyond what the operation declares. |
| Объявления | 11 | Item CRUD-ish: list, view, status, edit price, deactivate. Owns canonical stats ops also listed under Promo. |
| Цифровые товары | 9 | `digital-goods`: orders of digital goods (codes, keys, subscriptions) — list, send to buyer, cancel, arbitration, payout link, order webhooks. New in 2026-09. |
| Продвижение | 8 | Paid promotion services and BBIP (bbip = повышенный показ). Use `POST /promotion/v2/items/services/get` (returns `degraded`); v1 is deprecated. Employee calls use `X-Ah-Employee-Id`. |
| Автостратегия | 7 | Auto-bidding strategies. |
| Иерархия Аккаунтов | 7 | Multi-account / agency setups. Employee calls on behalf of a company need the `X-Employee-Of` header (`X-Is-Employee` is deprecated). Prefer `checkAhUserV2` + `getAhInfoV1`. |
| Настройка цены целевого действия | 5 | CPA price tuning (`cpxpromo`). |
| Краткосрочная аренда | 5 | STR (short-term rent). |
| Рассылка скидок и спецпредложений в мессенджере (beta-version) | 5 | `sbc-gateway`. |
| Рейтинги и отзывы | 4 | |
| Авторизация | 3 | Token issue/refresh (`/token`, canonical here; also published by Автотека). |
| CallTracking[КТ] | 3 | Strict 5 rpm limit. Audio recordings ~30 min after call ends. |
| TrxPromo | 3 | Promo transactions. |
| Информация о пользователе | 3 | `GET /core/v1/accounts/self`, etc. |
| CPA-аукцион | 2 | |
| Аналитика по недвижимости | 2 | Realty market price reports (`realty-reports`). |
| Управление остатками | 2 | Read + bulk update stock quantities. |
| Тарифы | 1 | Current + scheduled tariff info. **Транспорт only, non-CPA.** |
| Тариф | 1 | `tariff-composition`: `GET /api/1/partner/tariff/info` — Недвижимость tariff status, level, listing package limits. Schema says paid Профи/Лидер; the section guide still says Расширенный/Максимальный. Verify eligibility for the account when these names disagree. |

For non-trivial flows (delivery sandbox, Promo agency, scope/auth setup, vacancies v2), open the matching `references/sections/<slug>.md` first — those docs cover prerequisites and gotchas the OpenAPI spec doesn't.

## Working with the user

- If the user's request maps to one obvious endpoint, look it up and execute within their authorized scope. Read-only calls need no extra confirmation.
- If the request is ambiguous (e.g. "посмотри статистику по объявлениям" — Stats? Autoload reports? CPA?), `search` first and ask which they mean before making calls.
- When credentials are missing, explain where to get them for the selected product and have the user configure credentials locally (`AVITO_CLIENT_ID` / `AVITO_CLIENT_SECRET` for the helper; `AVITO_ADS_*` for the Ads SDK example). Keep credentials and tokens out of chat, logs and committed files; without them, prepare the call and mark live acceptance unverified.
- Watch out for endpoints that mutate state (POST/PUT/DELETE on items, orders, messages). Obtain authorization for the concrete action when it is absent; an existing explicit instruction to perform it is sufficient. Some POST endpoints only read data, so classify the operation by its documented effects.
