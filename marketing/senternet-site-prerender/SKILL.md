---
name: senternet-site-prerender
description: Add Puppeteer prerendering for all routes and strip runtime-only markup.
---

# Static Prerendering with Puppeteer

Add Puppeteer-based static prerendering so every route produces a real HTML snapshot for SEO crawlers and social media link previews.

## Why prerender

React SPAs serve a near-empty `index.html` to crawlers by default. Googlebot and social crawlers (Twitter, Discord, Slack) see no content. Prerendering visits each route with a headless browser and writes the rendered HTML to disk, giving crawlers full page content and correct meta tags.

## Steps

### 1. Install Puppeteer

```bash
npm install -D puppeteer
```

### 2. Update `src/main.tsx` to use `hydrateRoot` and dispatch `app-ready`

```tsx
import { hydrateRoot } from 'react-dom/client';
import App from './App';

const root = document.getElementById('root')!;

hydrateRoot(root, <App />);

// Signal the prerender script that React has mounted
setTimeout(() => {
  document.dispatchEvent(new Event('app-ready'));
}, 1000);
```

`hydrateRoot` attaches React to the existing prerendered DOM instead of replacing it — this keeps LCP from the initial HTML paint. Never switch back to `createRoot` without testing LCP.

### 3. Create `scripts/prerender.mjs`

```js
import puppeteer from 'puppeteer';
import http from 'http';
import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const buildDir = path.resolve(__dirname, '../build');

// Add every route that should be prerendered
const ROUTES = [
  '/',
  '/privacy',
  '/terms',
  // Add more routes as you create pages
];

const MIME = {
  '.js': 'application/javascript', '.mjs': 'application/javascript',
  '.css': 'text/css', '.html': 'text/html', '.png': 'image/png',
  '.webp': 'image/webp', '.json': 'application/json', '.svg': 'image/svg+xml',
  '.ico': 'image/x-icon', '.txt': 'text/plain', '.xml': 'application/xml',
};

const server = http.createServer((req, res) => {
  let urlPath = req.url.split('?')[0];
  if (!path.extname(urlPath)) urlPath = '/index.html';
  const file = path.join(buildDir, urlPath);
  const ext = path.extname(file);
  try {
    res.setHeader('Content-Type', MIME[ext] || 'text/plain');
    res.end(fs.readFileSync(file));
  } catch {
    try {
      res.setHeader('Content-Type', 'text/html');
      res.end(fs.readFileSync(path.join(buildDir, 'index.html')));
    } catch {
      res.statusCode = 404; res.end('Not found');
    }
  }
});

await new Promise(r => server.listen(9999, r));
console.log('Prerender server started on :9999');

const browser = await puppeteer.launch({ args: ['--no-sandbox', '--disable-setuid-sandbox'] });

for (const route of ROUTES) {
  const page = await browser.newPage();
  // Flag for any conditional rendering that should be skipped during prerender
  await page.evaluateOnNewDocument(() => { window.__PRERENDERING__ = true; });
  await page.goto(`http://localhost:9999${route}`, { waitUntil: 'networkidle2', timeout: 15000 });

  // Wait for React to render (app-ready event or 2s fallback)
  await Promise.race([
    page.evaluate(() => new Promise(resolve => {
      if (document.querySelector('#root')?.innerHTML?.length > 100) return resolve();
      document.addEventListener('app-ready', resolve, { once: true });
      setTimeout(resolve, 2000);
    })),
    new Promise(r => setTimeout(r, 3000)),
  ]);

  // Strip third-party scripts so they don't double-load on real user visits
  let html = await page.content();
  html = html
    .replace(/<script[^>]*src="https:\/\/www\.googletagmanager\.com\/gtag\/js[^"]*"[^>]*><\/script>/g, '')
    .replace(/<script[^>]*src="https:\/\/scripts\.clarity\.ms\/[^"]*"[^>]*><\/script>/g, '')
    .replace(/<script[^>]*src="https:\/\/www\.redditstatic\.com\/ads\/pixel\.js[^"]*"[^>]*><\/script>/g, '');

  const outDir = route === '/' ? buildDir : path.join(buildDir, route);
  fs.mkdirSync(outDir, { recursive: true });
  fs.writeFileSync(path.join(outDir, 'index.html'), html);

  const rootLen = await page.evaluate(() => document.getElementById('root')?.innerHTML?.length ?? 0);
  console.log(`${route}: ${rootLen > 100 ? '✓' : '✗ EMPTY'} (${rootLen} chars)`);
  await page.close();
}

await browser.close();
server.close();
```

### 4. Hook prerender into the build pipeline

In `package.json`:
```json
{
  "scripts": {
    "build:prod": "tsc -b && vite build --mode production && node scripts/prerender.mjs",
    "build:dev": "tsc -b && vite build --mode development && node scripts/prerender.mjs"
  }
}
```

### 5. Multilingual prerendering (if the site has i18n)

For sites with `/es/`, `/fr/` etc. routes, loop over locales as well:

```js
const LOCALES = [
  { language: 'en', dir: '' },
  { language: 'es', dir: 'es' },
];

for (const locale of LOCALES) {
  for (const route of ROUTES) {
    const page = await browser.newPage();
    if (locale.language !== 'en') {
      await page.evaluateOnNewDocument((lang) => { window.__LANG__ = lang; }, locale.language);
    }
    const requestPath = locale.dir
      ? `/${locale.dir}${route === '/' ? '' : route}`
      : route;
    // ... rest of prerender logic
    const outDir = locale.dir
      ? path.join(buildDir, locale.dir, route === '/' ? '' : route)
      : (route === '/' ? buildDir : path.join(buildDir, route));
    // ...
  }
}
```

## Rules

- Every route added to `src/App.tsx` and `public/sitemap.xml` must also be added to the `ROUTES` array in `scripts/prerender.mjs`
- Each page component must call `<MetaTags>` so the correct title/description/OG tags appear in the prerendered snapshot
- If a route renders empty (`✗ EMPTY`), the `MetaTags` component is not dispatching `app-ready` — check that `document.dispatchEvent(new Event('app-ready'))` is called in the component's `useEffect`
- `window.__PRERENDERING__ = true` can be used to conditionally skip animations, API calls, or interactivity that breaks in headless Chrome

## Framework: Next.js track

**This skill does not apply to the `nextjs` track — skip it entirely.**

Next.js renders every route it can to static HTML during `next build`. Running Puppeteer over that output would add build time and produce a second, divergent copy of every page that drifts from the one the framework serves. Never install Puppeteer, create `scripts/prerender.mjs`, add `hydrateRoot`, or dispatch `app-ready` in a Next.js repo. Finding any of those there means a Vite-track step was applied to the wrong track; flag it rather than extending it.

Check the equivalent guarantee instead:

1. `npm run build` — read the printed route table. Marketing routes must be static (`○`) or ISR, not dynamic (`ƒ`). A page that went dynamic by accident (a `cookies()`/`headers()`/`searchParams` read, or `'use client'` too high in the tree) is rendering per request and paying a cold start for content that never changes.
2. `npm start`, then `curl -s localhost:$PORT/<route>` for each route. The response must contain the page's real headline and its meta tags — this is exactly what a crawler that runs no JavaScript sees. An empty or shell-only response here is the same failure the Vite track reports as `✗ EMPTY`.
3. Third-party scripts do not need stripping. On the Vite track the prerender step removes GA/Reddit/Clarity tags so they don't double-load; on this track they are rendered by `next/script`, which handles loading once.

See `/senternet-site-framework` for the full convention map.
