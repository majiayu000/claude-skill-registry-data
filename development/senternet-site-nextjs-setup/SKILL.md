---
name: senternet-site-nextjs-setup
description: Scaffold a production-ready Next.js (App Router) + TypeScript site targeting Firebase App Hosting.
---

# Next.js + TypeScript Site Setup

Initialize a production-ready Next.js App Router site for a marketing site, configured for SSR on **Firebase App Hosting**.

This is the `nextjs` track. Read `/senternet-site-framework` first for how this track differs from the `vite` track — especially the convention map, which every later skill translates through.

## When to use this instead of `/senternet-site-vite-setup`

Use this only when the site actually needs server rendering, route handlers, middleware, or on-demand regeneration. For a static marketing site, the Vite track is cheaper and faster. `/senternet-site-framework` has the full decision guidance.

## Steps

### 1. Choose the local dev port

Ask the user which local dev port to use. Default is `3000` (also Next's own default). Explain that they may want a different one if they run multiple sites locally (e.g. 3001, 3002, 3003). Use their answer as `$PORT` throughout.

### 2. Scaffold the project

```bash
npx create-next-app@latest $SITE_NAME \
  --typescript \
  --tailwind \
  --eslint \
  --app \
  --no-src-dir \
  --import-alias "@/*" \
  --use-npm
cd $SITE_NAME
```

Replace `$SITE_NAME` with the project directory name (e.g. `myapp-site`). Accept the default answer for any prompt the flags do not cover (Turbopack for dev is fine).

This gives Tailwind CSS v4 wired through `@import "tailwindcss"` in `app/globals.css`, matching the rest of the suite. Confirm that import is present; add it if the generator's version differs.

Install the build-script dependencies the other skills use:

```bash
npm install -D sharp
```

Puppeteer is **not** needed on this track — Next renders HTML itself.

### 3. Write `.site-framework.json`

In the site root, so every later skill and every upfit run knows which track this is:

```json
{
  "framework": "nextjs",
  "renderMode": "ssr-app-hosting",
  "host": "firebase-app-hosting"
}
```

### 4. Create the route manifest at `config/routes.mjs`

This is the single source of truth for sitemap, robots, and IndexNow. It is plain `.mjs` so both the TypeScript app and the Node build scripts can import it without a transpile step.

```js
/** @type {import('./routes.d.mts').SiteRoute[]} */
export const ROUTES = [
  { path: '/',        changefreq: 'weekly',  priority: 1.0, indexable: true },
  { path: '/privacy', changefreq: 'yearly',  priority: 0.3, indexable: false },
  { path: '/terms',   changefreq: 'yearly',  priority: 0.3, indexable: false },
  // Add every new page here. Legal pages stay indexable: false.
];

export const indexableRoutes = () => ROUTES.filter(r => r.indexable);
```

And `config/routes.d.mts` so the app gets types:

```ts
export interface SiteRoute {
  path: string;
  changefreq: 'always' | 'hourly' | 'daily' | 'weekly' | 'monthly' | 'yearly' | 'never';
  priority: number;
  indexable: boolean;
}
export declare const ROUTES: SiteRoute[];
export declare function indexableRoutes(): SiteRoute[];
```

### 5. Configure `next.config.ts`

```ts
import type { NextConfig } from 'next';

const securityHeaders = [
  { key: 'X-Content-Type-Options', value: 'nosniff' },
  { key: 'X-Frame-Options', value: 'SAMEORIGIN' },
  { key: 'Referrer-Policy', value: 'strict-origin-when-cross-origin' },
];

const nextConfig: NextConfig = {
  reactStrictMode: true,
  poweredByHeader: false,
  trailingSlash: false,
  images: {
    formats: ['image/avif', 'image/webp'],
  },
  async headers() {
    return [
      { source: '/:path*', headers: securityHeaders },
      {
        // Everything under /public that is content-hashed by the build already
        // gets an immutable cache from Next. These are the hand-placed assets.
        source: '/:all*(svg|png|jpg|jpeg|webp|avif|ico|woff2)',
        headers: [{ key: 'Cache-Control', value: 'public, max-age=31536000, immutable' }],
      },
    ];
  },
};

export default nextConfig;
```

Do **not** set `output: 'export'`. Static export disables route handlers, middleware, image optimization, and ISR — which are the only reasons to be on this track. Do not override `distDir` either; App Hosting expects the default `.next/`.

### 6. Create `apphosting.yaml`

At the repo root. This is how App Hosting sizes the backend and injects configuration at build and runtime.

```yaml
runConfig:
  minInstances: 0
  maxInstances: 2
  concurrency: 80
  cpu: 1
  memoryMiB: 512

env:
  - variable: NEXT_PUBLIC_BASE_URL
    value: https://www.DOMAIN.com
    availability:
      - BUILD
      - RUNTIME
```

Notes on the values:

- `minInstances: 0` means cold starts on a quiet marketing site. Raise it to `1` only if the user accepts paying for an always-warm instance to remove that latency.
- Every variable the browser reads must be prefixed `NEXT_PUBLIC_` **and** listed with `BUILD` availability, or it will be `undefined` in the client bundle.
- Secrets are never `value:` entries. They are Secret Manager references:
  ```yaml
  env:
    - variable: RESEND_API_KEY
      secret: resend-api-key
      availability:
        - RUNTIME
  ```
  Create and grant those with `firebase apphosting:secrets:set` and `firebase apphosting:secrets:grantaccess` when the skill that needs them runs.

For a separate dev backend, add `apphosting.dev.yaml` with the dev values — App Hosting merges the environment-specific file over `apphosting.yaml`.

In a monorepo, `apphosting.yaml` goes in the **app's** directory (the backend's root dir, e.g. `apps/site/apphosting.yaml`), not at the repo root. See the next step.

### 6b. Monorepos and workspaces

**If the repo uses npm/pnpm/yarn workspaces, App Hosting needs a supported monorepo tool on top of them — use Turborepo.** Workspaces alone are not enough: the builder resolves the app's dependencies through the monorepo tool, and a repo that declares `workspaces` without one fails to build. The supported tools are Nx and Turborepo (Turborepo support [shipped in January 2026](https://firebase.blog/posts/2026/01/apphosting-turborepo/)). Turborepo is the right default for a Next.js site.

Skip this step entirely for a single-package repo. Do not add Turborepo to a repo that has no workspaces — it buys nothing and adds a build tool to maintain.

Required layout:

```
├── packages/            # shared code, if any
├── apps/
│   └── site/            # the Next.js app — this is the backend's root dir
│       ├── apphosting.yaml
│       ├── next.config.ts
│       └── package.json
├── turbo.json           # at the repo root
├── package.json         # root, declaring "workspaces"
└── package-lock.json    # one lockfile, at the repo root
```

1. Root `package.json` declares the workspaces and takes `turbo` as a devDependency:
   ```json
   {
     "private": true,
     "workspaces": ["apps/*", "packages/*"],
     "devDependencies": { "turbo": "^2" },
     "scripts": { "build": "turbo run build", "dev": "turbo run dev" }
   }
   ```
2. `turbo.json` at the repo root declares the build task and its dependency order, so shared packages build before the app that imports them:
   ```json
   {
     "$schema": "https://turbo.build/schema.json",
     "tasks": {
       "build": { "dependsOn": ["^build"], "outputs": [".next/**", "!.next/cache/**"] },
       "dev": { "cache": false, "persistent": true }
     }
   }
   ```
3. Keep a single lockfile at the repo root. A second lockfile inside the app directory makes the builder resolve dependencies from the wrong tree.
4. Tell the backend which app to build. During the GitHub connection flow, give the app's path (e.g. `apps/site`) as the root directory. For CLI deploys, put it in `firebase.json`:
   ```json
   {
     "apphosting": {
       "backendId": "my-site",
       "rootDir": "/apps/site",
       "ignore": ["node_modules", ".git", "firebase-debug.log"]
     }
   }
   ```

Known limitation: App Hosting does not support Turborepo **remote** caching. Local task caching within a build still applies.

### 7. Set up `app/layout.tsx`

The layout carries the base metadata that `index.html` carries on the Vite track:

```tsx
import type { Metadata } from 'next';
import './globals.css';

const baseUrl = process.env.NEXT_PUBLIC_BASE_URL ?? 'http://localhost:3000';

export const metadata: Metadata = {
  metadataBase: new URL(baseUrl),
  title: {
    default: 'APPNAME - Tagline',
    template: '%s | APPNAME',
  },
  description: 'One sentence description for search results.',
  applicationName: 'APPNAME',
  robots: { index: true, follow: true },
  openGraph: {
    type: 'website',
    siteName: 'APPNAME',
    locale: 'en_US',
    url: '/',
    images: [{ url: '/share/home.png', width: 1200, height: 630, alt: 'APPNAME' }],
  },
  twitter: {
    card: 'summary_large_image',
    creator: '@HANDLE',
    site: '@HANDLE',
  },
  alternates: { canonical: '/' },
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}
```

`metadataBase` is what makes every relative `url` and `images` path in page metadata resolve to an absolute URL. Without it, OG images silently ship as relative paths that crawlers cannot fetch.

### 8. Create `app/sitemap.ts` and `app/robots.ts`

Both read the route manifest, so adding a page in one place keeps them in sync.

```ts
// app/sitemap.ts
import type { MetadataRoute } from 'next';
import { indexableRoutes } from '@/config/routes.mjs';

const baseUrl = process.env.NEXT_PUBLIC_BASE_URL ?? 'http://localhost:3000';

export default function sitemap(): MetadataRoute.Sitemap {
  const lastModified = new Date();
  return indexableRoutes().map(route => ({
    url: `${baseUrl}${route.path === '/' ? '' : route.path}`,
    lastModified,
    changeFrequency: route.changefreq,
    priority: route.priority,
  }));
}
```

```ts
// app/robots.ts
import type { MetadataRoute } from 'next';

const baseUrl = process.env.NEXT_PUBLIC_BASE_URL ?? 'http://localhost:3000';

export default function robots(): MetadataRoute.Robots {
  return {
    rules: [{ userAgent: '*', allow: '/' }],
    sitemap: `${baseUrl}/sitemap.xml`,
  };
}
```

Only `indexable: true` routes reach the sitemap. `noindex` pages still render and are still crawlable by direct link — they just must never be advertised.

### 9. Create the home page

`app/page.tsx`. Keep it a server component (no `'use client'`) so it renders to HTML with no JS cost:

```tsx
export default function HomePage() {
  return (
    <main>
      <h1>APPNAME</h1>
    </main>
  );
}
```

Every page below the root exports its own `metadata`:

```tsx
// app/about/page.tsx
import type { Metadata } from 'next';

export const metadata: Metadata = {
  title: 'About',
  description: 'Learn more about what we do.',
  alternates: { canonical: '/about' },
  openGraph: { url: '/about', images: [{ url: '/share/about.png', width: 1200, height: 630 }] },
};

export default function AboutPage() {
  return <main>{/* ... */}</main>;
}
```

### 10. Server vs client components

Default to server components. Add `'use client'` only to the leaf component that actually needs state, effects, or event handlers — a mobile nav toggle, a form, an analytics hook. Marking a whole page `'use client'` ships the entire subtree to the browser and gives back the main reason to be on this framework.

There is no `hydrateRoot`, no `app-ready` event, and no `window.__PRERENDERING__` on this track. Any skill that references them is describing the Vite track; skip that step.

### 11. Environment files

```bash
# .env.development
NEXT_PUBLIC_BASE_URL=http://localhost:$PORT
NEXT_PUBLIC_GA_ID=
```

```bash
# .env.production
NEXT_PUBLIC_BASE_URL=https://www.DOMAIN.com
NEXT_PUBLIC_GA_ID=G-XXXXXXXXXX
```

`.env.local` stays untracked for machine-specific overrides. In deployed environments the values in `apphosting.yaml` are what actually apply, so any variable added to `.env.production` must be mirrored there or it will be missing in the build. On upfit runs, preserve an existing non-empty `NEXT_PUBLIC_GA_ID` rather than overwriting it with the placeholder.

Confirm `.gitignore` covers `.env*.local` and `.next/`.

### 12. `package.json` scripts

```json
{
  "scripts": {
    "dev": "next dev --port $PORT",
    "build": "next build",
    "start": "next start --port $PORT",
    "lint": "next lint",
    "typecheck": "tsc --noEmit",
    "build:prod": "next build",
    "deploy:prod": "firebase apphosting:rollouts:create $BACKEND_ID --project $PREFIX-prod --git-branch main && node scripts/indexnow.mjs"
  }
}
```

There is no separate prerender step to chain onto `build:prod` — `next build` produces the static HTML itself. `build:prod` is kept as an alias so the shared workflow steps and CI in the rest of the suite keep working.

### 13. Set up the App Hosting backend

Run `/senternet-site-firebase` and follow its **Next.js track / App Hosting** section. It creates the Firebase projects, connects the GitHub repo, creates the backend, and handles the custom domain. App Hosting deploys from a connected git branch, so the repo needs a GitHub remote first — run `/senternet-site-github-setup` before that step if there isn't one.

### 14. Directory layout

Create the directories the later skills expect:

```
app/            # routes, layout, sitemap.ts, robots.ts
components/     # shared React components
config/         # routes.mjs, routes.d.mts
lib/            # analytics helpers, utilities
public/         # favicon, share images, static assets
scripts/        # indexnow.mjs, generate-share-images.mjs
```

## Verification

The scaffold is done when all of these pass:

1. `npm run dev` starts cleanly on `$PORT`
2. `npm run build` completes with no TypeScript errors, and the build output marks `/` as static (`○`) rather than dynamic (`ƒ`) — a marketing page rendering dynamically means something in the tree opted into request-time rendering by accident
3. `npm run typecheck` is clean
4. `npm run build && npm start`, then `curl -s localhost:$PORT | grep "<h1"` returns the heading — this is the crawler's view, and it must contain real content
5. `curl -s localhost:$PORT/sitemap.xml` lists only indexable routes
6. `curl -s localhost:$PORT/robots.txt` points at the sitemap on the canonical host
7. `.site-framework.json`, `apphosting.yaml`, and `config/routes.mjs` all exist
8. If the root `package.json` declares `workspaces`: `turbo.json` exists at the repo root, there is exactly one lockfile (also at the root), and the backend's root directory points at the app rather than `/`. Verify with `npm run build` **from the repo root** — building only from inside the app directory hides the dependency-resolution failure that App Hosting will hit.

## Notes

- App Hosting rollouts are triggered by pushes to the connected branch. `firebase apphosting:rollouts:create` forces one without a new commit. Verify the backend exists with `firebase apphosting:backends:list --project $PREFIX-prod` before wiring the deploy script, and check `firebase apphosting --help` if a subcommand name has moved — this CLI surface changes faster than the Hosting one.
- `firebase.json` is not used for **headers** on this track — anything the Vite track puts in `firebase.json` `headers` belongs in `next.config.ts` `headers()` instead. It is still used for App Hosting itself: the `apphosting` block (`backendId`, `rootDir`, `ignore`) is what CLI deploys read to find the app.
- In a monorepo, the paths in every other skill are relative to the **app** directory, not the repo root. `app/`, `config/routes.mjs`, `public/`, and `apphosting.yaml` all live under the backend's root dir; `turbo.json`, the root `package.json`, the lockfile, and `firebase.json` live at the repo root.
- Cold starts are the tradeoff for SSR. Prefer static rendering for every page that can be static, and reach for `revalidate` over request-time rendering when content needs to change without a deploy.
- Do not add `react-router-dom`. Routing is the framework's job here, and mixing the two breaks server rendering.
