---
name: dev-api
description: Backend API patterns for Shopify app. Auto-apply when writing webhooks, Prisma models, background jobs, API routes, authentication, or server-side code in app/models/ or app/services/.
allowed-tools: Read, Grep, Glob, Bash, Edit, Write, WebSearch, WebFetch
argument-hint: [API endpoint hoặc backend feature]
---

# Shopify App Backend — Development Conventions

Áp dụng conventions này khi develop **backend code**: API routes, webhooks, database, background jobs, authentication.

## Tech Stack

| Layer | Technology | Notes |
|-------|-----------|-------|
| Runtime | Node.js | LTS version |
| Framework | Remix (server-side) | Loaders/actions = API endpoints |
| ORM | Prisma | Type-safe DB access |
| Database | SQLite → PostgreSQL | SQLite for start, PostgreSQL when scaling |
| Queue | DB-based queue | Lightweight, no Redis dependency |
| Cron | node-cron | In-process scheduled tasks |
| Validation | Zod | Runtime type validation |
| Auth | Shopify OAuth | Via `@shopify/shopify-app-remix` |

## Core Principles

1. **Validate at boundaries**: Zod validate mọi input (request body, query params, webhook payload)
2. **Idempotent operations**: Webhooks có thể gửi nhiều lần → handler phải idempotent
3. **Fail gracefully**: Return proper HTTP status codes, structured error responses
4. **Background heavy work**: Webhook handlers respond 200 ngay, xử lý async qua DB-based queue
5. **Type-safe DB**: Luôn dùng Prisma typed queries, KHÔNG raw SQL trừ performance-critical
6. **Secure by default**: HMAC validation, rate limiting, input sanitization

## Directory Structure

```
app/
├── models/              # Prisma helper functions (data access layer)
│   ├── product.server.ts
│   ├── order.server.ts
│   └── setting.server.ts
├── services/            # Business logic layer
│   ├── order-processing.server.ts
│   ├── sync.server.ts
│   └── notification.server.ts
├── jobs/                # Background job definitions
│   ├── queue.server.ts       # DB-based queue setup
│   ├── cron.server.ts        # Scheduled tasks (node-cron)
│   ├── processOrder.ts
│   └── syncInventory.ts
├── utils/
│   ├── validation.server.ts  # Zod schemas
│   └── errors.server.ts      # Custom error classes
└── webhooks/            # Webhook handlers
    ├── orders-create.ts
    ├── app-uninstalled.ts
    └── index.ts              # Webhook registry
```

### Naming Conventions
- `.server.ts` suffix cho server-only code (Remix tree-shakes client bundles)
- Model files = data access (thin, no business logic)
- Service files = business logic (orchestration)
- Job files = async processing

## Code Patterns

Xem chi tiết tại [patterns.md](patterns.md) bao gồm:
- Prisma model helper pattern
- Webhook handler pattern (HMAC + idempotency)
- DB-based queue pattern (lightweight, no Redis)
- Cron job pattern (node-cron)
- API response pattern (structured errors)
- Zod validation pattern
- Rate limiting pattern (in-memory, no Redis)
- App Proxy endpoint pattern
- Transaction pattern (Prisma)
- Structured logging pattern
- Health check pattern (monitoring endpoint)

## Prisma Schema Conventions

```prisma
// Naming: PascalCase models, camelCase fields
// Mọi model có timestamps
// Soft delete qua deletedAt
// Shop relation bắt buộc (multi-tenant)

model Resource {
  id          String    @id @default(cuid())
  shop        String    // Shopify shop domain (tenant key)
  name        String
  slug        String
  status      ResourceStatus @default(DRAFT)
  description String?

  // Relations
  items       Item[]

  // Timestamps
  createdAt   DateTime  @default(now())
  updatedAt   DateTime  @updatedAt
  deletedAt   DateTime? // Soft delete

  // Indexes
  @@unique([shop, slug])
  @@index([shop, status])
  @@index([deletedAt])
}

enum ResourceStatus {
  DRAFT
  ACTIVE
  PAUSED
  ARCHIVED
}
```

## Do's and Don'ts

### DO
- Dùng `.server.ts` suffix cho tất cả server-only code
- Validate input bằng Zod trước khi xử lý
- Return structured errors: `{ error: { code, message, details } }`
- Dùng Prisma transactions cho multi-step operations
- Log structured JSON (không `console.log` plain text)
- Verify webhook HMAC trước khi process
- Respond 200 to webhooks ngay, queue heavy processing
- Dùng `cuid()` hoặc `ulid()` cho IDs (không auto-increment)
- Index columns dùng trong WHERE clauses
- Soft delete cho business-critical data

### DON'T
- KHÔNG expose internal errors ra client (security risk)
- KHÔNG raw SQL trừ khi Prisma query quá chậm (document lý do)
- KHÔNG xử lý heavy logic trong webhook handler (queue nó)
- KHÔNG trust client-side data — validate lại server-side
- KHÔNG `console.log` trong production — dùng structured logger
- KHÔNG skip HMAC validation cho webhooks
- KHÔNG hard-delete data liên quan đến orders/payments
- KHÔNG store secrets trong code — dùng environment variables
- KHÔNG dùng `any` type cho API responses

$ARGUMENTS
