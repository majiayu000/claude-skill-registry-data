---
name: beautyline-next-app-router
description: >-
  Next.js App Router conventions for Beautyline Server vs Client Components,
  route groups, and leaf boundaries for interactivity and context providers.
  Use when adding pages, layouts, hooks, forms, modals, or fixing bundle or
  hydration issues.
---

# Beautyline: Next.js App Router

## Server Components by default

- **Do not** add `'use client'` unless the module needs hooks, browser-only APIs, event handlers at top level, or React context consumed in client scope.
- **Push interactivity down**: Prefer a Server Component parent that renders a small **client** leaf (form, modal, carousel) rather than marking an entire layout or page client-only.

## Where `'use client'` already appears

- Auth and cart **`contexts`** are client modules.
- Interactive **`components`** (contact form, consent banner, navbar, admin forms, checkout-related views) appropriately use `'use client'`.
- **`app/(protected)/admin/layout.tsx`** and similar layouts that orchestrate providers are client boundaries when they must wrap hooks or client children.

When adding parallel features (e.g. another modal-heavy section), mirror this split: server page → client child only where needed.

## Route groups

- App uses **`(protected)`**, **`(auth)`**, etc. under `src/app/`. New routes should follow existing grouping for auth/session expectations and layouts.

## Data and env

- Server-only data fetching and secrets belong in Server Components, `route handlers`, or `src/lib/` helpers invoked from server code — not leaked into unnecessary client bundles.
