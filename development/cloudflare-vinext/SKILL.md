---
name: cloudflare--vinext
description: "Vinext — Next.js API trên Vite, deploy tới Cloudflare Workers. 94% Next.js 16 API coverage, App Router + RSC, Cloudflare Bindings (D1/R2/KV/AI). Builds nhanh hơn."
allowed-tools: Bash, Read, Write
user-invocable: true
---

Vinext: reimplements Next.js API trên Vite — same code, faster builds, deploy trực tiếp lên Cloudflare Workers. "Pragmatic compatibility, not bug-for-bug parity."

## Migrate từ Next.js

```bash
npx skills add cloudflare/vinext
# Rồi nói với AI: "migrate this project to vinext"

# Hoặc manual:
npm install -D vinext vite @vitejs/plugin-react
npx vinext init    # one-command migration
```

## CLI

```bash
npx vinext dev     # dev server
npx vinext build   # production build
npx vinext deploy  # deploy to Cloudflare Workers
```

## Cloudflare Bindings

```typescript
import { env } from "cloudflare:workers"

// D1 Database
const result = await env.DB.prepare("SELECT * FROM users").all()

// R2 Storage
await env.BUCKET.put("key", data)

// KV
const value = await env.KV.get("key")

// Cloudflare AI
const response = await env.AI.run("@cf/meta/llama-3.1-8b-instruct", { prompt })
```

## API Coverage (94% của Next.js 16)

```
✅ Pages Router + App Router
✅ React Server Components (via @vitejs/plugin-rsc)
✅ Server Actions + streaming SSR
✅ Dynamic routes, catch-all, parallel routes
✅ Metadata API, sitemap, robots, OG images
✅ ISR, static export, caching
✅ All next/* module shims
✅ Multi-platform via Nitro (Vercel, Netlify, AWS, Deno)

❌ Build-time image optimization (dùng @unpic/react)
❌ Self-hosted Google Fonts
```

## Lý do dùng

```
Faster builds  — Vite + Rolldown
Lighter bundles — aggressive tree-shaking
Edge deployment — Cloudflare Workers native
```

## Source

https://github.com/cloudflare/vinext · MIT · experimental
