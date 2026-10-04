---
name: dev-shopify
description: Shopify platform conventions and requirements. Auto-apply when working with metafields, metaobjects, GraphQL API calls, rate limiting, app store submission, or Built for Shopify compliance.
allowed-tools: Read, Grep, Glob, Bash, Edit, Write, WebSearch, WebFetch
---

# Shopify Platform Conventions

Cross-cutting concerns áp dụng cho **toàn bộ codebase** — admin, storefront, và backend.

## Scope

Skill này cover 3 areas chính:

| Area | Reference | Khi nào apply |
|------|-----------|---------------|
| **Metafields & Metaobjects** | [metafields.md](metafields.md) | Khi define/read/write metafields, tạo metaobject definitions |
| **Built for Shopify (BfS)** | [built-for-shopify.md](built-for-shopify.md) | Khi review code quality, trước khi submit app, performance audit |
| **API Throttle Handling** | [throttle.md](throttle.md) | Khi gọi Shopify GraphQL/REST API, bulk operations, webhooks |

## Core Platform Rules

### 1. API Calls — Luôn handle throttle
```typescript
// KHÔNG BAO GIỜ gọi Shopify API mà không có retry logic
// Xem chi tiết: throttle.md
```
- Mọi GraphQL query phải track `extensions.cost` trong response
- Implement exponential backoff khi bị throttle (status 429)
- Dùng Bulk Operations cho > 250 items
- Cache responses khi appropriate (Redis, 5-15 min TTL)

### 2. Metafields — Namespace & typing đúng chuẩn
```typescript
// Namespace format: $app:<key> (app-owned) hoặc custom.<key> (merchant-editable)
// Xem chi tiết: metafields.md
```
- App-owned metafields: dùng reserved namespace `$app:`
- Merchant-editable: dùng `custom.` namespace
- Luôn define metafield definitions (type + validation) trước khi write
- Metaobjects cho complex/relational data, metafields cho simple key-value

### 3. Built for Shopify — Compliance checklist
```
// Mọi feature mới đều phải pass BfS criteria trước khi merge
// Xem chi tiết: built-for-shopify.md
```
- Performance: App load < 3s, Core Web Vitals pass
- Polaris UI: 100% admin UI dùng Polaris components
- Security: OAuth 2.0, HMAC validation, no secrets in client code
- Scopes: Request minimum scopes cần thiết, justify mỗi scope
- Error handling: Mọi route có ErrorBoundary, user-friendly messages

## Quick Decision Guide

### Metafield vs Metaobject?
```
Cần store simple value trên product/order/customer?
  → Metafield

Cần store structured data với multiple fields?
  → Metaobject (nếu < 5 fields, consider JSON metafield trước)

Cần relationships giữa custom data?
  → Metaobject + mixed references

Cần merchant edit trong admin?
  → Metafield definition với pin = true (hiện trong admin UI)
```

### REST vs GraphQL?
```
Default: GraphQL (lower cost, flexible queries)
Exceptions:
  - Webhook registration: REST simpler
  - File uploads: REST required
  - Simple CRUD on single resource: REST acceptable
```

### Cache hay không?
```
Cache (Redis, 5-15 min):
  - Shop info, theme info
  - Product lists (non-realtime)
  - Metafield definitions
  - App settings

KHÔNG cache:
  - Order data (realtime accuracy)
  - Inventory levels
  - Customer PII
  - Pricing/billing info
```

$ARGUMENTS
