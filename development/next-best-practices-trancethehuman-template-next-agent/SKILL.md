---
name: next-best-practices
description: Check version-matched Next.js App Router documentation before changing routes, server components, data access, caching, or deployment behavior.
---

# Next.js guidance for this starter

This file is original project guidance. For the broader upstream skill, see [vercel-labs/next-skills](https://github.com/vercel-labs/next-skills). Its text is linked rather than redistributed here.

1. Inspect this project's `package.json` and `node_modules/next/dist/docs/` before editing Next.js code. Next.js 16 behavior can differ from older examples.
2. Keep server-only credentials and model calls in server modules. Make a component a client component only when it needs browser state or events.
3. Validate route input on the server, even if the browser already validated it. Preserve the access check on both run creation and run streaming.
4. Review the installed documentation for route handlers, runtime choice, async request APIs, caching, and metadata when touching those features.
5. Run `bun run typecheck` and `bun run build` after framework or routing changes, then exercise the affected route in a browser.

Official references: [Next.js App Router](https://nextjs.org/docs/app), [Next.js route handlers](https://nextjs.org/docs/app/getting-started/route-handlers).
