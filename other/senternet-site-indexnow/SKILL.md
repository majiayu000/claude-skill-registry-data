---
name: senternet-site-indexnow
description: Generate an IndexNow key and submission script for production deploys.
---

# IndexNow Setup (Bing / Search Engine Indexing)

Submit all site URLs to Bing and other search engines via IndexNow immediately after each production deploy.

## What IndexNow does

IndexNow is a protocol supported by Bing, Yandex, and others that lets you push URLs directly to search engines. This eliminates the crawl delay — pages get indexed within hours of publish instead of waiting days for Googlebot's next crawl.

## Steps

### 1. Generate an IndexNow key

Any random hex string works as the key. Generate one:
```bash
openssl rand -hex 16
```

Save the key — you'll use it in two places.

### 2. Create the key verification file

Create `public/YOUR_KEY_HERE.txt` containing only the key:
```
YOUR_KEY_HERE
```

Replace `YOUR_KEY_HERE` with the actual key string. This file must be publicly accessible at `https://www.DOMAIN.com/YOUR_KEY_HERE.txt`.

### 3. Create `scripts/indexnow.mjs`

```js
#!/usr/bin/env node
import { readFileSync } from 'fs';
import { fileURLToPath } from 'url';
import { dirname, join } from 'path';

const __dirname = dirname(fileURLToPath(import.meta.url));

const KEY = 'YOUR_KEY_HERE'; // same key as in public/YOUR_KEY_HERE.txt
const HOST = 'www.DOMAIN.com';

// Read URLs from the generated sitemap
const sitemapXml = readFileSync(join(__dirname, '../public/sitemap.xml'), 'utf8');
const urlList = [...new Set(
  [...sitemapXml.matchAll(/<loc>(https?:\/\/[^<]+)<\/loc>/g)].map(m => m[1])
)];

console.log(`Submitting ${urlList.length} URLs to IndexNow...`);

const res = await fetch('https://api.indexnow.org/indexnow', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json; charset=utf-8' },
  body: JSON.stringify({
    host: HOST,
    key: KEY,
    keyLocation: `https://${HOST}/${KEY}.txt`,
    urlList,
  }),
});

if (res.ok) {
  console.log(`IndexNow: ${res.status} — submitted ${urlList.length} URLs`);
} else {
  const body = await res.text();
  console.error(`IndexNow error: ${res.status} ${body}`);
  process.exit(1);
}
```

### 4. Wire into the deploy script

In `package.json`, the `deploy:prod` script should run IndexNow after Firebase deploy:
```json
{
  "scripts": {
    "deploy:prod": "npm run build:prod && firebase deploy --only hosting --project \"APPNAME-prod\" && node scripts/indexnow.mjs",
    "indexnow": "node scripts/indexnow.mjs"
  }
}
```

The `indexnow` script can also be run standalone after manually adding pages.

### 5. Verify the key is accessible

After first deploy, visit:
```
https://www.DOMAIN.com/YOUR_KEY_HERE.txt
```
It should return the key string. If it returns 404, check that Firebase Hosting serves files from `public/` and that `firebase.json` doesn't have a rewrite catching `.txt` files before static file serving.

## Notes

- IndexNow only submits to Bing; Google has its own indexing via Google Search Console and doesn't use IndexNow
- Submit on every deploy, not just when content changes — the overhead is minimal and ensures freshness
- The key file must match exactly — no trailing newline issues
- For large sites (1000+ URLs), the API accepts up to 10,000 URLs per request

## Framework: Next.js track

Two changes on the `nextjs` track; everything else about the key file and the submission payload is identical.

**1. The URL list comes from the route manifest, not from a built sitemap file.** There is no `public/sitemap.xml` on disk to parse — the sitemap is generated per request. Read `config/routes.mjs` directly:

```js
import { indexableRoutes } from '../config/routes.mjs';

const baseUrl = process.env.NEXT_PUBLIC_BASE_URL;
const urlList = indexableRoutes().map(r => `${baseUrl}${r.path === '/' ? '' : r.path}`);
```

The key file itself still lives at `public/<key>.txt` and is served from the site root unchanged.

**2. It runs after the rollout, not after `firebase deploy`.** App Hosting deploys asynchronously, so submitting URLs the moment the command returns tells Bing to crawl the *previous* build. Wait for the rollout to report `READY` first:

```json
"deploy:prod": "firebase apphosting:rollouts:create $BACKEND_ID --project \"$PREFIX-prod\" --git-branch main && node scripts/indexnow.mjs"
```

If the deploy happens by pushing to the connected branch rather than through this script, run `node scripts/indexnow.mjs` manually once the rollout is live, or move the submission into the CI job that watches the rollout.

See `/senternet-site-framework` for the full convention map.
