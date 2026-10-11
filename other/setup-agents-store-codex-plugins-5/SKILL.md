---
name: setup
description: Verify Next.js project environment and readiness. This skill should be used when the user asks to "verify Next.js setup", "check Next.js project", "is my Next.js app configured correctly", "test Next.js environment", or needs to confirm their project is ready for development.
---

# Verify Next.js Project Setup

Confirm that a Next.js project is properly configured for modern App Router development. Run these checks in order and report results.

## Prerequisites

- Node.js 22 or 24 LTS recommended. Next.js 16 formally requires `>=20.9.0`, but Node 20 reached end-of-life on 2026-04-30 and no longer gets fixes; Vitest 5 needs Node >= 22.12
- TypeScript 5.1+
- A Next.js project directory with `package.json`

## Step 1: Check Next.js Version

Read `package.json` and locate the `next` dependency. The recommended range is `^16.3.8`:

```json
{
  "dependencies": {
    "next": "^16.3.8"
  }
}
```

| Version | Status | Notes |
|---------|--------|-------|
| 16.3.x, at 16.3.8 or later | Current | Cache Components, Turbopack default, `proxy.ts`, built-in MCP at `/_next/mcp` |
| 16.x below 16.3.8 | Patch now | Missing security fixes: RCE on Windows-hosted servers and via AVIF in Image Optimization (16.3.3), RCE in `next/og` `ImageResponse` (16.3.6), and in 16.3.8 an SSRF in Image Optimization, Draft Mode and root-param leaks in `use cache`, and `/_next/mcp` without an origin check |
| 15.x | Maintenance | Backport releases only; stay on 15.5.27 or later. `middleware.ts` era, no built-in MCP |
| 14.x | Legacy | App Router GA, consider upgrading |
| 13.x or below | Outdated | Upgrade required for modern patterns |

Verify the installed (not just the declared) version and the registry latest:

```bash
npm ls next
npm view next@latest version   # compare: installed must be >= 16.3.8 on the 16.3 line
```

Next.js ships a formal monthly security-release program (since 2026-07-13), so re-run this check each month instead of leaving an old range in place.

## Step 2: Verify App Router Structure

Check that the project uses the `app/` directory (not just `pages/`):

```
app/
├── layout.tsx       # Root layout (required)
├── page.tsx         # Home page
├── loading.tsx      # Optional loading state
├── error.tsx        # Optional error boundary
└── not-found.tsx    # Optional 404 page
```

If only `pages/` exists, the project uses the legacy Pages Router. Recommend migrating to App Router for new features.

## Step 3: Verify TypeScript Configuration

Check for `tsconfig.json` with Next.js recommended settings:

```json
{
  "compilerOptions": {
    "target": "ES2017",
    "lib": ["dom", "dom.iterable", "esnext"],
    "jsx": "preserve",
    "module": "esnext",
    "moduleResolution": "bundler",
    "strict": true,
    "paths": {
      "@/*": ["./src/*"]
    },
    "plugins": [{ "name": "next" }]
  }
}
```

Key checks:
- `strict: true` is set
- Path aliases (`@/*`) are configured
- The `next` plugin is present for IDE support

## Step 4: Verify Next.js Config

Check for `next.config.ts` (TypeScript) or `next.config.mjs`:

```ts
import type { NextConfig } from 'next'

const nextConfig: NextConfig = {
  // Configuration options
}

export default nextConfig
```

The config file can be `next.config.ts` natively (TypeScript is fully supported). Common configuration to verify:
- `images.remotePatterns` — if using external image domains
- `cacheComponents` — must be `true` for `use cache` / Cache Components (16+). Record whether it is on: it decides which caching model applies (`export const revalidate` / `dynamic` work only when it is off, and are removed when it is on — see the `data-fetching` skill)
- `experimental` — any experimental features enabled
- `output` — `'standalone'` for Docker deployments

## Step 5: Check Dev Server

Run the development server to confirm it starts:

```bash
npm run dev
# or
pnpm dev
```

Verify the server starts on `http://localhost:3000` without errors.

## Step 6: Verify MCP Integration (Next.js 16+)

For Next.js 16+, the built-in MCP endpoint is available at `/_next/mcp` when the dev server is running. Use `next@>=16.3.8` for it: earlier dev servers did not verify the request origin, so a website the developer visits could read project data from the endpoint. Check for `.mcp.json` in the project root:

```json
{
  "mcpServers": {
    "next-devtools": {
      "command": "npx",
      "args": ["-y", "next-devtools-mcp@latest"]
    }
  }
}
```

Or install with one command: `npx add-mcp next-devtools-mcp@latest`.

If not present, recommend adding it for enhanced AI-assisted development.

## Optional: CI Type Checking

Recommend `next typegen && npx tsc --noEmit` in CI — `next typegen` generates route and `PageProps` types without a full build.

## What This Skill Does NOT Cover

- Installing Node.js or package managers — see Node.js official docs
- Creating a new project from scratch — use `npx create-next-app@latest`
- Configuring MCP servers — that belongs to project-level `.mcp.json` configuration
- Setting up CI/CD or deployment — see deployment guides