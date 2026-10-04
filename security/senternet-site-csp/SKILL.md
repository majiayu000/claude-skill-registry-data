---
name: senternet-site-csp
description: Add a Content Security Policy for Senternet marketing sites.
---

# Content Security Policy (CSP) Setup

Add a `Content-Security-Policy` header to Firebase Hosting that locks down which scripts, styles, and connections the site is allowed to make. Covers all services in the Senternet skill suite (GA4, Ahrefs Web Analytics, Reddit Pixel, Firebase).

## Steps

### 1. Audit which third-party services the project uses

Check `index.html` and `src/` to determine which services are active:

```bash
grep -r "googletagmanager\|analytics.ahrefs.com\|redditstatic\|firebase\|googleapis" index.html src/ --include="*.tsx" --include="*.ts" --include="*.html" -l
```

Note which are present — the CSP policy is additive based on what's actually in the project.

### 2. Move inline scripts to external files

Inline `<script>` blocks require either `'unsafe-inline'` (insecure) or SHA-256 hashes in the policy. The cleaner solution is to move each inline script to a file in `public/` and reference it with a `src=` attribute — external scripts are allowed by `script-src 'self'` with no hashing needed.

**General pattern:**

Find all inline `<script>` blocks in `index.html`:
```bash
grep -n "<script>" index.html
```

For each one:
1. Extract the content to `public/<descriptive-name>.js`
2. Replace the `<script>...</script>` block with `<script src="/<descriptive-name>.js"></script>`

The file lands in `public/` so it's served as a static asset from the site root. Vite copies `public/` contents to `build/` verbatim — no import or bundling needed.

**Example — GA bootstrap stub:**
```html
<!-- before -->
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());
</script>

<!-- after -->
<script src="/ga-init.js"></script>
```

**Example — Reddit pixel stub:**
```html
<!-- before -->
<script>
  window.rdt = window.rdt || function() {
    (window.rdt.callQueue = window.rdt.callQueue || []).push(arguments);
  };
  window.rdt.callQueue = window.rdt.callQueue || [];
</script>

<!-- after -->
<script src="/reddit-init.js"></script>
```

If an inline script cannot be moved (e.g. it references a build-time variable substituted by the Vite plugin), leave it in place and compute its hash in step 3 instead.

### 3. Compute SHA-256 hashes for any remaining inline scripts

For each inline `<script>` block that cannot be moved to an external file, compute its hash. The content must be the exact string between the `<script>` and `</script>` tags (no leading/trailing whitespace changes).

```bash
# Copy the exact inline script content to a temp file, then:
openssl dgst -sha256 -binary /tmp/inline.js | base64
```

Or use Node:
```bash
node -e "
const crypto = require('crypto');
const fs = require('fs');
const content = fs.readFileSync('/tmp/inline.js', 'utf8');
console.log(\"'sha256-\" + crypto.createHash('sha256').update(content).digest('base64') + \"'\");
"
```

Collect all hashes — they go into `script-src` in the next step.

### 4. Add the CSP header to `firebase.json`

Add a new header object to the `"headers"` array in `firebase.json`. Keep it after the asset-specific rules and before (or merged with) the existing `**` catch-all:

```json
{
  "source": "**",
  "headers": [
    {
      "key": "Content-Security-Policy",
      "value": "default-src 'self'; script-src 'self' INLINE_HASHES; style-src 'self' 'unsafe-inline'; img-src 'self' data:; connect-src 'self'; font-src 'self'; frame-src 'none'; object-src 'none'; base-uri 'self'; form-action 'self';"
    }
  ]
}
```

Replace `INLINE_HASHES` with any hashes from step 3 (e.g. `'sha256-abc123=='`). Then extend each directive based on which services are active:

**If Google Analytics (GA4) is present**, extend:
```
script-src  → add: https://www.googletagmanager.com
img-src     → add: https://www.google-analytics.com https://www.googletagmanager.com
connect-src → add: https://www.google-analytics.com https://analytics.google.com https://stats.g.doubleclick.net https://region1.google-analytics.com
```

**If Reddit Pixel is present**, extend:
```
script-src  → add: https://www.redditstatic.com
connect-src → add: https://alb.reddit.com https://www.redditstatic.com
img-src     → add: https://www.redditstatic.com
```

**If Ahrefs Web Analytics is present** (from `/senternet-site-ahrefs-web-analytics`), extend:
```
script-src  → add: https://analytics.ahrefs.com
connect-src → add: https://analytics.ahrefs.com
```

**If Firebase Auth or Firestore is used** (check `src/` for `initializeApp`), extend:
```
connect-src → add: https://*.firebase.com https://*.firebaseapp.com https://*.googleapis.com wss://*.firebaseio.com
frame-src   → add: https://*.firebaseapp.com
```

**If Google Fonts is used**, extend:
```
style-src → add: https://fonts.googleapis.com
font-src  → add: https://fonts.gstatic.com
```

A complete example for a site with GA4 + Reddit Pixel:
```json
{
  "key": "Content-Security-Policy",
  "value": "default-src 'self'; script-src 'self' 'sha256-HASH1==' 'sha256-HASH2==' https://www.googletagmanager.com https://www.redditstatic.com; style-src 'self' 'unsafe-inline'; img-src 'self' data: https://www.google-analytics.com https://www.googletagmanager.com https://www.redditstatic.com; connect-src 'self' https://www.google-analytics.com https://analytics.google.com https://stats.g.doubleclick.net https://region1.google-analytics.com https://alb.reddit.com; font-src 'self'; frame-src 'none'; object-src 'none'; base-uri 'self'; form-action 'self';"
}
```

Make sure `firebase.json`'s `**` catch-all does not duplicate header keys — merge the CSP entry into the existing `**` block if one exists.

### 5. Start in report-only mode first

Before enforcing, deploy with `Content-Security-Policy-Report-Only` so violations are logged to the console without breaking the site:

```json
{ "key": "Content-Security-Policy-Report-Only", "value": "..." }
```

Deploy to the dev environment and browse the full site while watching DevTools → Console for CSP violation messages. Each violation tells you which directive blocked what origin — add missing origins to the policy.

```bash
npm run deploy:dev
```

### 6. Switch to enforcing mode

Once no violations appear in the console:

1. Rename the header key from `Content-Security-Policy-Report-Only` to `Content-Security-Policy`
2. Deploy to dev once more to confirm nothing breaks
3. Deploy to prod

```bash
npm run deploy:prod
```

### 7. Verify the header is live

```bash
curl -sI https://www.DOMAIN.com/ | grep -i content-security-policy
```

Should print the full policy string. Also check Chrome DevTools → Network → response headers for the HTML document.

## Notes

- `'unsafe-inline'` in `style-src` is needed for most React apps that use any inline style props — removing it breaks many UI libraries. It does not weaken `script-src`.
- `object-src 'none'` and `base-uri 'self'` are the most impactful directives for preventing XSS escalation — never omit them.
- `frame-src 'none'` prevents clickjacking; if you later embed an iframe (e.g. YouTube), add the specific origin there rather than opening it up.
- Files placed in `public/` are served as static assets and included in the 1-year immutable cache by the Firebase asset rule — correct behavior since they don't change between deploys.
- For Vite's dev server, CSP headers are not enforced locally (the dev server doesn't use `firebase.json`) — all testing of the enforced policy must be done against a deployed Firebase environment.
- If a new third-party service is added later (e.g. Intercom, Stripe, Segment), always extend the CSP in report-only mode on dev before deploying to prod.
- Google's CSP Evaluator (`csp-evaluator.withgoogle.com`) can grade your policy and flag common weaknesses.

### Why not nonces?

Nonces are the recommended best practice for CSP because they avoid maintaining a hash list and work well with dynamically injected scripts. However, **nonces require the server to generate a fresh random value per request** and inject it into both the `Content-Security-Policy` header and the `nonce="..."` attribute on each inline `<script>` simultaneously.

Firebase Hosting is a CDN serving pre-built static files. Headers in `firebase.json` are static strings — the same value goes out on every response. A static nonce is cryptographically identical to `'unsafe-inline'`: any attacker who reads the nonce from the HTML source can reuse it indefinitely.

For a static host, **SHA-256 hashes are the correct nonce equivalent.** The script content is deterministic (the same on every deploy), so the hash is stable, and the browser verifies the content hasn't been tampered with — which is exactly the security property nonces provide in a dynamic context.

If the project later adopts SSR (e.g. via Firebase Functions or Cloud Run serving the HTML), nonces become viable: generate `crypto.randomBytes(16).toString('base64')` per request, stamp it onto each `<script nonce="...">` in the rendered HTML, and set the header dynamically. At that point, the hash approach can be dropped entirely.

## Framework: Next.js track

The "Why not nonces?" section above ends by noting that nonces become viable once the site is server-rendered. On the `nextjs` track, that has already happened — **use nonces, not hashes.**

Firebase App Hosting serves Next.js from Cloud Run, so every HTML response is generated per request and can carry a fresh nonce. That removes the hash list entirely: no `openssl dgst` step, no re-hashing when an inline script changes, and no risk of a stale hash silently blocking a script.

### 1. Generate the nonce in `middleware.ts`

```ts
import { NextResponse, type NextRequest } from 'next/server';

export function middleware(request: NextRequest) {
  const nonce = Buffer.from(crypto.randomUUID()).toString('base64');
  const csp = [
    `default-src 'self'`,
    `script-src 'self' 'nonce-${nonce}' 'strict-dynamic' https:`,
    `style-src 'self' 'unsafe-inline'`,
    `img-src 'self' data:`,
    `connect-src 'self'`,
    `font-src 'self'`,
    `frame-src 'none'`,
    `object-src 'none'`,
    `base-uri 'self'`,
    `form-action 'self'`,
  ].join('; ');

  const headers = new Headers(request.headers);
  headers.set('x-nonce', nonce);
  headers.set('Content-Security-Policy', csp);

  const response = NextResponse.next({ request: { headers } });
  response.headers.set('Content-Security-Policy', csp);
  return response;
}

export const config = {
  matcher: [{ source: '/((?!_next/static|_next/image|favicon.ico).*)', missing: [{ type: 'header', key: 'next-router-prefetch' }] }],
};
```

The nonce goes out on both the request headers (so the page can read it) and the response header (so the browser enforces it).

### 2. Read it in the layout and pass it to every `<Script>`

```tsx
import { headers } from 'next/headers';

const nonce = (await headers()).get('x-nonce') ?? undefined;
// <Script nonce={nonce} ... />
```

Next also stamps the nonce onto its own inline bootstrap scripts automatically once it sees the CSP header, which is the part a static host cannot do.

### 3. Per-service directives are unchanged

The GA4, Reddit Pixel, Ahrefs, Firebase, and Google Fonts extension lists above apply verbatim. `'strict-dynamic'` lets a nonced loader script pull in its own dependencies, which is what makes the third-party tag managers work without listing every CDN host.

### Caveats specific to this track

- **Reading headers opts routes into dynamic rendering.** Only the layout should read the nonce, and check the build's route table afterward — if pages flipped from `○` to `ƒ`, the nonce read leaked into a page that should be static. If keeping pages static matters more than nonces on those routes, fall back to the hash approach for them.
- **Do not put the CSP in `firebase.json`.** It is not read on this track. Static headers, if you want them alongside middleware, go in `next.config.ts` `headers()`.
- **Report-only first still applies.** Ship `Content-Security-Policy-Report-Only` from the middleware, browse the deployed dev backend watching the console, then rename the header key.
- Verify against the deployed backend, not `next dev`: `curl -sI https://www.DOMAIN.com/ | grep -i content-security-policy`. Two requests should return two different nonces — an identical nonce on every response means the value is being cached and is no better than `'unsafe-inline'`.

See `/senternet-site-framework` for the full convention map.
