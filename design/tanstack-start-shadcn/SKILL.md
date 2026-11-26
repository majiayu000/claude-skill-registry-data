---
name: tanstack-start-shadcn
description: "TanStack Start + shadcn/ui setup. Use for React web apps."
version: 1.0.0
author: Charles Ponti, Hermes Agent
license: MIT
platforms: [macos, linux]
metadata:
  hermes:
    tags: [tanstack-start, react, tailwind, shadcn, vite, ui, dashboard, web-app]
---

# TanStack Start + Tailwind CSS v4 + shadcn/ui

## When to Use

- Building a React web app with TanStack Start (file-based routing, SSR)
- Adding Tailwind CSS v4 to a Vite project
- Setting up shadcn/ui components (Button, Card, Badge, etc.)
- Connecting a frontend to a REST API backend

## Setup: TanStack Start + Tailwind v4

1. Create app: `npx @tanstack/cli create my-app --framework React --no-install --no-git --blank`
2. Install Tailwind: `npm install tailwindcss @tailwindcss/vite --save-dev`
3. Add Tailwind plugin to `vite.config.ts`:
   ```typescript
   import tailwindcss from "@tailwindcss/vite";
   const config = defineConfig({
     plugins: [tanstackStart(), viteReact(), tailwindcss()],
   });
   ```
4. Replace `src/styles.css` content with `@import "tailwindcss";` + `@theme inline` with CSS variables

## shadcn/ui Setup

1. Install: `npm install class-variance-authority clsx tailwind-merge lucide-react @radix-ui/react-slot`
2. Create `src/lib/utils.ts` with `cn()` function (clsx + twMerge)
3. Create components in `src/components/ui/` using `../../lib/utils` imports

### Dark Theme (Seme Dashboard)

- CSS variables use HSL format with dark values (--background: 0 0% 4%, --foreground: 0 0% 98%)
- Gradient text utility: `.gradient-text` with white→zinc gradient
- Stat cards use gradient backgrounds with hover glow effects
- Header is sticky with backdrop-blur
- Nav uses pill-style active states with bg-accent

### shadcn Button Pattern

Uses `cva` for variants, `React.forwardRef`, `@radix-ui/react-slot` for `asChild`. See the `button.tsx` template.

## TanStack Start Patterns

- File-based routing in `src/routes/` (index.tsx, memories.tsx, etc.)
- `createFileRoute('/path')` defines a route
- `Outlet` renders child routes, `Link` for navigation
- API calls via `fetch` to external API (localhost:3000)
- Dev: `npm run dev -- --port 5173` (default port 3000 conflicts with API)

## Route generation and the build order

File-based routes come from a generated `src/routeTree.gen.ts`. **Commit it.** Builds that type-check before the plugin regenerates (`tsc -b && vite build`, the usual script order) fail on a fresh clone with `Cannot find module './routeTree.gen'`, and the local tree hides it because a dev run already wrote the file. Prove it by moving the file aside and running the type-check; generation is deterministic, so tracking it costs nothing.

## Hosting the SSR build inside an existing node server

TanStack Start emits two artefacts: `dist/client` (browser bundle) and `dist/server/server.js` (a fetch-style `{ default: { fetch(request) } }` handler). Serving both from your own node server adds four requirements:

- **Route `/api/*` before the SSR fallback**, and let the static handler answer only files that exist, so unknown paths reach the router: `if (!staticFile(path, res)) await serveStart(req, res, url)`. Point the static root at `dist/client`, not `dist`.
- **Load the server entry through a versioned specifier and reload it when the file's mtime changes.** A dynamic import is cached for the life of the process, so a rebuild otherwise serves new client assets against an old server render (React hydration mismatch that only appears after a deploy):
  ```ts
  if (shouldReload(cached, modifiedAt)) {
    const mod = await import(`${pathToFileURL(file).href}?v=${Math.trunc(modifiedAt)}`);
    cached = { loadedAt: modifiedAt, handler: mod.default };
  }
  ```
  Verify it by changing a visible string, rebuilding, and reading the new string back from the same PID (no restart).
- **Forward the request body** for non-GET/HEAD, or a route that reads one silently sees an empty request:
  ```ts
  init.body = Readable.toWeb(req) as ReadableStream<Uint8Array>;
  init.duplex = "half";
  ```
- **Set a root `notFoundComponent`.** Without one TanStack renders a bare "Not Found" _and logs a warning on every unknown request_, which floods the service log.

Error responses from your own control endpoints should be JSON with a reason (`{ error }`), not plain text: a browser client that expects JSON reports "Request failed (403)" and the human learns nothing.

## CORS for API integration

Manual middleware (built-in `hono/cors` may not load). Restrict to known hosts. See typescript-sqlite skill for full pattern.

## Pitfalls

- **Tailwind v4 uses `@import "tailwindcss"`** — not v3 directives (`@tailwind base/components/utilities`)
- **shadcn `cn()` utility** — must use `twMerge(clsx(inputs))` to resolve conflicting classes
- **Component imports** — use relative paths (`../../lib/utils`), not path aliases
- **Port conflicts** — TanStack Start defaults to 3000; change with `--port 5173`
- **CSS variables** — use HSL format (`0 0% 100%`) with `hsl(var(--background))` in `@theme inline`

## References

- Tailwind CSS v4: https://tailwindcss.com/docs/v4-upgrade
- shadcn/ui: https://ui.shadcn.com/docs
- TanStack Start: https://tanstack.com/start/latest/docs
