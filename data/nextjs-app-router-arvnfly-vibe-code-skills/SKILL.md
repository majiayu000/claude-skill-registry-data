---
name: nextjs-app-router
description: "Next.js 15 App Router architecture, Server Actions, Route Handlers, parallel routes, and ISR caching."
---

# Next.js App Router Architecture Protocol

Leverage Next.js App Router idioms safely and efficiently.

---

## 1. Server Actions & Mutations

1. Mark mutation files or functions with `'use server'`.
2. Always validate input arguments inside Server Actions using Zod before mutating databases.
3. Trigger cache revalidation using `revalidatePath()` or `revalidateTag()` after successful mutations.

---

## 2. Layouts, Loading & Error Boundaries

- Co-locate `loading.tsx` for Suspense streaming.
- Co-locate `error.tsx` as client error boundaries with retry triggers.
- Use Route Handlers (`app/api/.../route.ts`) for webhook receivers and non-browser consumers.
