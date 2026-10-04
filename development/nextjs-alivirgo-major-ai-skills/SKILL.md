---
name: nextjs
description: "Build Next.js applications with the App Router, server and client components, route handlers, caching, and deployment configuration."
category: development
risk: safe
source: self
source_type: self
date_added: "2026-08-26"
tags: ["nextjs", "react", "app-router", "server-components", "frontend", "claude"]
tools: ["claude", "cursor", "gemini", "codex"]
---

# Next.js App Router AI Skill Guide

## Overview & Engine Architecture

Next.js (App Router) uses the `app/` directory for file-based routes, React Server Components by default, and optional Client Components when interactivity is required. Data fetching can run on the server with caching semantics; Client Components hydrate in the browser. Agents choose the server/client boundary intentionally and keep secrets out of any module imported by client code.

```
app/
  layout.tsx          (server by default)
  page.tsx            (server by default)
  loading.tsx / error.tsx
  api/route.ts        (route handlers)
components/
  *.tsx  +  "use client" only when needed
```

## When to use this skill

- Building or refactoring App Router applications
- Fixing misuse of `"use client"` / server-only imports
- Designing caching and revalidation for server fetches
- Preparing `next build` for deployment

## Operational directives

1. Default to Server Components; add `"use client"` only for state, effects, or browser APIs.
2. Never put server secrets in `NEXT_PUBLIC_*` or files imported by client components.
3. Prefer colocated `loading.tsx` / `error.tsx` over ad-hoc spinners everywhere.
4. Treat `fetch` cache options and `revalidate` as part of the product contract.
5. Keep route segments small and composable via `layout.tsx` nesting.

## Minimal page + client island

```tsx
// app/page.tsx (Server Component)
import { Counter } from "@/components/counter";

export default async function Page() {
  const data = await fetch(process.env.API_URL + "/items", {
    next: { revalidate: 60 },
  }).then((r) => r.json());

  return (
    <main>
      <h1>Items ({data.length})</h1>
      <Counter />
    </main>
  );
}
```

```tsx
// components/counter.tsx
"use client";
import { useState } from "react";

export function Counter() {
  const [n, setN] = useState(0);
  return <button onClick={() => setN((x) => x + 1)}>{n}</button>;
}
```

## Commands

```bash
npx create-next-app@latest
npm run dev
npm run build
npm run start
```

## Common pitfalls

| Pitfall | Why it hurts | Fix |
| --- | --- | --- |
| Marking everything client | Larger bundles, weaker security boundary | Push logic up to server |
| Importing DB client in client component | Leaks credentials / fails build | Split modules |
| No `revalidate` strategy | Stale or over-fetched data | Explicit cache policy |
| Using pages router patterns in app/ | Broken routing | Follow app file conventions |

## Best practices

- Use the Metadata API for titles/descriptions per route.
- Optimize images with `next/image` and real width/height.
- Gate experimental features behind flags.
- Match Node version to deployment platform expectations.

## Limitations

- Caching semantics differ between hosting targets (Vercel vs Node server vs static export).
- Server Actions need CSRF/origin awareness and careful authz checks.
- Partial Prerendering and advanced caching modes evolve across major versions - verify against the project's Next version docs.

## Related skills

- `@react` - component and hooks fundamentals
- `@typescript` - typing props and server data
- `@vercel` - deployment specifics when targeting Vercel
