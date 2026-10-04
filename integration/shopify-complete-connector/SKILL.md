---
name: shopify-complete-connector
description: >-
  Complete Shopify store connector for Calculadora BMC: OAuth/PKCE, Admin GraphQL,
  Storefront API, webhooks, catalog sync, products/variants/inventory/prices, orders,
  customers, discounts, metafields, theme/Liquid/design, Checkout Extensibility,
  Shopify Functions, app embeds, and Partner Dashboard options. Use when the user
  wants to develop Shopify design, functionality, catalog, storefront, theme, app
  extensions, or any Shopify option from this repo; also for shopify connector,
  conectar Shopify, tienda Shopify, theme Liquid, Online Store 2.0, or full-store
  Shopify integration (broader than shopify-integration-v4 questions/quotes).
---

# Shopify Complete Connector (BMC)

**Scope:** Full-store development surface from this repo — **design**, **functionality**, and **Shopify platform options** — not only the questions/quotes flow.

**Narrow sibling:** For Mercado Libre–style questions → Sheet → approve/send only, use [`shopify-integration-v4`](../shopify-integration-v4/SKILL.md). This skill **owns** catalog, theme/design, Admin/Storefront APIs, PIM publish, visor sync, and expanding the connector.

**Before coding:** Read [`docs/team/PROJECT-STATE.md`](../../../docs/team/PROJECT-STATE.md) and audit existing Shopify code (table below). Never hardcode secrets, shop domains, or sheet IDs.

## When to apply

- User asks for a **complete Shopify connector**, store development, or “all Shopify options”
- Design / theme / Liquid / Online Store 2.0 / Checkout UI / app embed work
- Catalog, products, variants, inventory, prices, collections, metafields
- Orders, customers, discounts, draft orders, fulfillment
- Webhooks, OAuth, Partner app, Shopify CLI, Functions, Hydrogen/Oxygen
- Visor/CDN sync (`visor:shopify-*`), PIM publish (`publish-panelin-to-shopify`)
- Extending `server/routes/shopify.js` beyond questions/quotes

## Repo map (canonical)

| Area | Path |
|------|------|
| Routes (OAuth, webhooks, catalog, admin Q&A) | `server/routes/shopify.js` |
| Encrypted per-shop tokens | `server/shopifyStore.js` |
| Env / scopes | `server/config.js` (`SHOPIFY_*`) |
| OAuth state (Postgres single-use) | `server/lib/oauthStateStore.js` |
| Mount + raw body for HMAC | `server/index.js` (`/webhooks/shopify`) |
| Visor CDN map / families | `scripts/build-quote-visor-shopify-*.mjs`, `src/data/quoteVisorShopify*.json` |
| PIM → Shopify publish | `scripts/publish-panelin-to-shopify.mjs` |
| Embedded chat app scaffold | `shop-chat-agent/` (`shopify.app.toml`) |
| Commercial tone (IVA / lists) | `docs/team/policies/COMERCIAL-CHAT-ML-SHOPIFY.md` |
| Env template | `.env.example` (`SHOPIFY_CLIENT_ID`, `SECRET`, `WEBHOOK_SECRET`, `SCOPES`, `QUESTIONS_SHEET_TAB`) |

## Decision tree

1. **Questions / auto-reply only?** → Prefer `shopify-integration-v4`; still verify HMAC/OAuth here if touching shared routes.
2. **Catalog / prices / inventory / PIM?** → Admin GraphQL via installed shop token; reuse `/api/shopify/products` and `/api/shopify/catalog/full`; publish via `publish-panelin-to-shopify.mjs` (dry-run default).
3. **Design / theme / storefront UX?** → Theme app extension or Online Store theme (Liquid + JSON templates); Storefront API or public `products.json` for read-only media; never put Admin tokens in the browser.
4. **New Shopify capability (discounts, checkout, Functions)?** → Check Partner app scopes → add minimal scope → implement Admin GraphQL or Shopify Function → webhook if event-driven → document in `.env.example` + PROJECT-STATE.
5. **Embedded admin app UI?** → Extend `shop-chat-agent/` (Shopify app + App Bridge) or add Hub route under `/hub/*` that calls BMC API with `API_AUTH_TOKEN` / JWT.

## Standard workflow

Copy and track:

```
Shopify connector task:
- [ ] 1. Audit existing routes/store/env
- [ ] 2. Name capability + required scopes (minimal)
- [ ] 3. Implement behind existing auth patterns
- [ ] 4. Webhooks: HMAC + idempotency + fast 200
- [ ] 5. Smoke: OAuth status / catalog / webhook topic
- [ ] 6. Update PROJECT-STATE + .env.example if new env
```

### 1. Audit

- Confirm `SHOPIFY_CLIENT_ID` / `SECRET` / `WEBHOOK_SECRET` / `TOKEN_ENCRYPTION_KEY` / `PUBLIC_BASE_URL`.
- Confirm install: `GET /auth/shopify?shop=STORE.myshopify.com` → callback stores encrypted token in `.shopify-shops/`.
- List what already exists before adding parallel clients.

### 2. Auth & security (non-negotiable)

- OAuth: PKCE S256 + state/nonce; consume state via `oauthStateStore.consume()` (single-use).
- Validate HMAC on callback query and every webhook body (`X-Shopify-Hmac-Sha256`).
- Tokens: encrypted at rest (`shopifyStore.js`); never log access tokens.
- Browser: only Storefront / public catalog URLs; Admin GraphQL stays server-side.
- API catalog routes: `requireApiAuth` (`Authorization: Bearer` or `X-Api-Key` = `API_AUTH_TOKEN`).
- GDPR: handle `customers/data_request`, `customers/redact`, `shop/redact` when enabling customer webhooks.
- Scopes: start from current `SHOPIFY_SCOPES`; add only what the feature needs; document why.

### 3. Capability matrix (develop from here)

| Track | What to build | Primary APIs / surfaces |
|-------|---------------|-------------------------|
| **A. Auth & app** | Install, token refresh, Partner app, CLI | OAuth, `shopify.app.toml`, Shopify CLI |
| **B. Catalog & PIM** | Products, variants, images, collections, sync | Admin GraphQL; `/api/shopify/*`; visor scripts; publish script |
| **C. Commerce ops** | Orders, draft orders, customers, fulfillments | Admin GraphQL + webhooks (`orders/*`, `customers/*`) |
| **D. Merchandising** | Discounts, price lists, metafields, metaobjects | Admin GraphQL; metaobject definitions |
| **E. Design / theme** | Theme, sections, CSS, brand assets, OS 2.0 | Theme editor, Liquid, theme app extensions |
| **F. Storefront UX** | Product pages, cart, customer account | Storefront API, Hydrogen (optional), Checkout Extensibility |
| **G. App extensions** | Admin blocks, checkout UI, POS, Flow | Shopify app extensions + Functions |
| **H. Comms** | Questions/quotes, chat agent | `shopify-integration-v4` + `shop-chat-agent/` |
| **I. Analytics / markets** | Markets, duties, reports (read) | Admin GraphQL; respect Uruguay/LATAM + USD list prices |

Prices in BMC remain **USD ex-IVA**; 22% IVA at totals. Channel `web` aligns with Shopify list — see commercial policy doc. Do not invent prices; source from MATRIZ / `constants.js` / Panelin PIM.

### 4. Existing HTTP surface

| Method | Path | Auth | Purpose |
|--------|------|------|---------|
| GET | `/auth/shopify` | public | Start OAuth (PKCE) |
| GET | `/auth/shopify/callback` | public | Exchange + store token |
| POST | `/webhooks/shopify` | HMAC | Ingest topics → Sheet/DB |
| GET | `/api/shopify/products` | API key | Paginated Admin catalog |
| GET | `/api/shopify/catalog/full` | API key | Multi-page catalog sweep |
| GET | `/admin/questions` | (module) | Pending questions list |
| POST | `/admin/answer` | (module) | Approve & send reply |
| GET/POST | `/admin/auto-config` | (module) | Auto-reply schedule (UTC-3) |

GraphQL Admin version in routes today: `2024-01` — when bumping, update one constant and regression-test catalog + answer mutations.

### 5. Design track (theme & brand)

When the user asks for **design** on Shopify:

1. Prefer **theme app extension** (app-owned) over editing the live theme blindly.
2. Match BMC brand tokens where the storefront should feel continuous with the calculator/hub; do not invent a purple/cream generic AI look.
3. Use Online Store 2.0 JSON templates + sections; keep assets on Shopify CDN.
4. For calculator visor media: sync from storefront/CDN via `npm run visor:shopify-sync` (abort if remote returns 0 products).
5. Never expose Admin API credentials in theme Liquid or storefront JS.

### 6. Functionality track (ops & sync)

1. **Read path:** Admin GraphQL through `shopifyGraphql` helper in `server/routes/shopify.js`.
2. **Write path:** mutations only with explicit operator/service auth; prefer dry-run scripts first (`publish-panelin-to-shopify.mjs --dry-run`).
3. **Events:** register webhooks for the topics you handle; verify HMAC; ack quickly; process idempotently.
4. **Idempotency:** key by Shopify GID / topic + id; safe retries.
5. **Errors:** 4xx/5xx short messages; no stack traces to clients; use `pino` in server paths.

### 7. Local / prod commands

| Goal | Command |
|------|---------|
| Ensure `.env` | `npm run env:ensure` |
| API | `npm run start:api` (or `dev:full` if stack not already up) |
| Visor sync from store | `npm run visor:shopify-sync` |
| PIM publish dry-run | `node scripts/publish-panelin-to-shopify.mjs --dry-run` |
| Health | `curl -sS http://localhost:3001/health` |

Redirect URI: `{PUBLIC_BASE_URL}/auth/shopify/callback`. Webhook URL: `{PUBLIC_BASE_URL}/webhooks/shopify`.

## Guardrails

- Do **not** replace `shopify-integration-v4` behavior without an explicit request.
- Do **not** use `npm audit fix --force`.
- Do **not** commit `.env`, tokens, or `.shopify-shops/*.enc`.
- Do **not** hardcode `*.myshopify.com` or Partner client secrets.
- Prefer extending `server/routes/shopify.js` + `shopifyStore.js` over a second OAuth stack.
- Sheets failures stay **503** (never 500 for Sheets-down).
- After behavior changes: append **Cambios recientes** in `docs/team/PROJECT-STATE.md`.

## Propagation

If webhooks/URLs/scopes change → notify Networks (`networks-development-agent`).  
If hub/calculator UI changes → Design / calculadora specialist.  
If commercial copy/IVA → `COMERCIAL-CHAT-ML-SHOPIFY.md`.  
Update propagation table in `docs/team/PROJECT-TEAM-FULL-COVERAGE.md` §4 when cross-area.

## Additional resources

- API & webhook detail: [reference.md](reference.md)
- Design / theme / extensions playbook: [design-and-storefront.md](design-and-storefront.md)
- Capability checklist & examples: [examples.md](examples.md)
- Questions/quotes only: [../shopify-integration-v4/SKILL.md](../shopify-integration-v4/SKILL.md)
