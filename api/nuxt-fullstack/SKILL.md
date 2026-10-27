---
name: nuxt-fullstack
description: "Nuxt 3 full-stack architecture, auto-imports, Nitro engine, server middleware, and universal state."
---

# Nuxt 3 Full-Stack Protocol

Build performant Nuxt applications with unified client and server capabilities.

---

## 1. Nitro Engine & Server Endpoints

1. Place backend endpoints in `server/api/` exporting `defineEventHandler`.
2. Access query parameters with `getQuery(event)` and body with `readBody(event)`.

---

## 2. Universal Data Fetching

- Use `useAsyncData` and `useFetch` with unique cache keys to prevent duplicate requests during SSR hydration.
