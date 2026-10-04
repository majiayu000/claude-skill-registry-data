---
name: dev-admin
description: Coding patterns for Shopify embedded admin app. Auto-apply when writing Remix routes, Polaris components, App Bridge interactions, or admin UI code in app/ directory.
allowed-tools: Read, Grep, Glob, Bash, Edit, Write, WebSearch, WebFetch
argument-hint: [component hoặc feature cần implement]
---

# Shopify Embedded Admin App — Development Conventions

Áp dụng conventions này khi develop code trong **admin app** (Remix + Polaris + App Bridge 4.x).

## Tech Stack

| Layer | Technology | Notes |
|-------|-----------|-------|
| Framework | Remix (Shopify App Template) | SSR, loader/action pattern |
| UI | Polaris React | Shopify design system, KHÔNG custom CSS trừ khi bắt buộc |
| Navigation | App Bridge 4.x | Embedded app navigation, modals, toasts |
| Language | TypeScript (strict mode) | No `any`, prefer `unknown` + type guards |
| State | Remix loaders/actions | Server-first, minimize client state |
| Auth | Shopify session tokens | Via `authenticate.admin()` |

## Core Principles

1. **Server-first**: Data fetching trong `loader`, mutations trong `action` — KHÔNG fetch từ client trừ khi realtime
2. **Polaris-only UI**: Dùng Polaris components, không custom HTML/CSS cho admin UI
3. **App Bridge 4.x**: Navigation, toasts, modals đều qua App Bridge — không dùng browser APIs
4. **Type-safe**: Strict TypeScript, Zod validation cho form data, API responses
5. **Error boundaries**: Mọi route đều có `ErrorBoundary` component
6. **Loading states**: Dùng Polaris `SkeletonPage` / `SkeletonBodyText` cho loading

## Route Structure

```
app/
├── routes/
│   ├── app._index.tsx          # Dashboard / landing
│   ├── app.settings.tsx        # Settings page
│   ├── app.[resource].tsx      # Resource list (e.g., app.products.tsx)
│   ├── app.[resource].$id.tsx  # Resource detail (e.g., app.orders.$id.tsx)
│   └── app.[resource].new.tsx  # Resource create
├── components/                  # Shared Polaris components
├── utils/                       # Helpers, validators
├── models/                      # Prisma model helpers
└── graphql/                     # Shopify GraphQL queries/mutations
```

### Route Naming
- Prefix `app.` cho tất cả authenticated routes
- kebab-case cho route segments
- `$id` cho dynamic params
- `.new` suffix cho create pages

## Code Patterns

Xem chi tiết tại [patterns.md](patterns.md) bao gồm:
- Loader pattern (data fetching + authentication)
- Action pattern (form handling + validation)
- Polaris page layout pattern
- Error boundary pattern
- GraphQL query pattern (Shopify Admin API)
- Resource picker pattern (App Bridge)
- Toast/Banner notification pattern
- Pagination pattern (cursor-based)
- Bulk action pattern

## Shopify Authentication

```typescript
// LUÔN authenticate trước khi access admin API
const { admin, session } = await authenticate.admin(request);

// GraphQL query
const response = await admin.graphql(`
  #graphql
  query GetProducts($first: Int!) {
    products(first: $first) {
      edges {
        node {
          id
          title
        }
      }
    }
  }
`, { variables: { first: 10 } });
```

## Do's and Don'ts

### DO
- Dùng `authenticate.admin(request)` ở đầu mọi loader/action
- Dùng Polaris `Page`, `Layout`, `Card` cho page structure
- Dùng `useNavigation()` để show loading states
- Dùng Zod schema validate form data trong action
- Handle `Response` errors từ Shopify API gracefully
- Dùng `useAppBridge()` cho App Bridge interactions

### DON'T
- Không dùng `useState` cho data có thể fetch từ server
- Không custom CSS override Polaris styles
- Không `fetch()` từ client-side cho admin API calls
- Không hardcode shop domain, lấy từ session
- Không skip error boundaries
- Không dùng `window.location` — dùng App Bridge navigation

$ARGUMENTS
