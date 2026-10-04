---
name: senternet-site-ahrefs-web-analytics
description: Add Ahrefs Web Analytics with build-time env gating and lazy loading, as an alternative or addition to Google Analytics.
---

# Ahrefs Web Analytics Setup

Add Ahrefs Web Analytics to a Vite + React site with lazy loading, environment gating, and no render-blocking. Ahrefs Web Analytics is a free, privacy-friendly, cookieless visitor-tracking snippet, so there is no cookie banner and no consent gate to wire up. Use it as an alternative to Google Analytics, or alongside it — the two don't conflict.

This is Ahrefs **Web Analytics** (a first-party visitor-tracking snippet you embed on the site). It is not the Ahrefs Site Audit / API work covered by `/senternet-site-ahrefs-audit`, and it does not need the Ahrefs MCP server.

## Prerequisites

None beyond an Ahrefs account. Unlike GA4, there is no Firebase Console linking and no gcloud or Analytics Admin API step — Ahrefs Web Analytics is independent of Firebase and Google.

## Design principles

- The snippet loads after `window.load` so it never blocks FCP or LCP
- The tracking key is injected at build time via a Vite plugin so dev builds are analytics-free
- The block is stripped entirely in dev/staging — it never loads on non-prod environments
- All pageviews (including bounces) are tracked because the script loads on every visit, not on interaction

## Steps

### 1. Get the Ahrefs Web Analytics tracking key

The only value this skill needs is the `data-key`. Its shape is a **UUID**: 36 characters, lowercase hex in the `8-4-4-4-12` groupings, e.g. `a1b2c3d4-5678-90ab-cdef-1234567890ab` (regex `[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}`). Treat that pattern as a sanity check, not a hard gate — if a supplied value looks close but doesn't match exactly, confirm it with the user rather than rejecting it.

**If the user supplied the key when invoking this command, use it directly and skip the dashboard steps.** Accept either form and extract the key without asking again:

- a bare key: `a1b2c3d4-5678-90ab-cdef-1234567890ab`
- the whole install snippet pasted in — pull the value out of `data-key="..."`.

Only when no key was supplied, retrieve it from Ahrefs:

1. Sign in to the Ahrefs dashboard and open **Web Analytics**.
2. Add the website/project for this site's domain.
3. Ahrefs generates an install snippet of the form:
   ```html
   <script src="https://analytics.ahrefs.com/analytics.js" data-key="YOUR_KEY" async></script>
   ```
4. Copy the `data-key` value.

### 2. Add the Ahrefs block to `index.html`

Insert between comment markers so the Vite plugin can substitute or strip it:

```html
<!-- AHREFS_START -->
<script>
  window.addEventListener('load', function() {
    if (document.querySelector('script[src*="analytics.ahrefs.com/analytics.js"]')) return;
    var s = document.createElement('script');
    s.src = 'https://analytics.ahrefs.com/analytics.js';
    s.setAttribute('data-key', 'AHREFS_ANALYTICS_KEY');
    s.async = true;
    document.head.appendChild(s);
  });
</script>
<!-- AHREFS_END -->
```

The literal string `AHREFS_ANALYTICS_KEY` is replaced at build time by the Vite plugin below.

### 3. Extend the `htmlPlugin` in `vite.config.ts`

Mirror the existing GA branch: when the key is set, substitute the placeholder and unwrap the markers; when it is empty, strip the whole block. If the site already has the GA `htmlPlugin`, add the Ahrefs handling alongside it rather than creating a second plugin.

```typescript
const htmlPlugin = (gaId: string, ahrefsKey: string): Plugin => ({
  name: 'html-transform',
  transformIndexHtml(html) {
    // ... existing GA handling ...

    if (ahrefsKey) {
      html = html
        .replace(/AHREFS_ANALYTICS_KEY/g, ahrefsKey)
        .replace(/\s*<!-- AHREFS_START -->\n/, '\n      <!-- Ahrefs Web Analytics -->\n')
        .replace(/\n\s*<!-- AHREFS_END -->/, '');
    } else {
      html = html.replace(/[ \t]*<!-- AHREFS_START -->[\s\S]*?<!-- AHREFS_END -->\n?/g, '');
    }

    return html;
  },
});
```

Pass `env.VITE_AHREFS_ANALYTICS_KEY` into the plugin the same way the Measurement ID is passed.

### 4. Set `VITE_AHREFS_ANALYTICS_KEY` in env files

```bash
# .env.development — Ahrefs Web Analytics disabled in dev
VITE_AHREFS_ANALYTICS_KEY=

# .env.production — use the data-key retrieved above
VITE_AHREFS_ANALYTICS_KEY=your-ahrefs-key
```

### 5. Wire the production key into CI if the site deploys via GitHub Actions

`.env.production` is not committed, so a CI build has no key unless one is supplied through GitHub Actions. Check whether the repo has a deploy workflow that runs the production build:

```bash
ls .github/workflows/            # look for deploy.yml (the canonical Senternet site-deploy workflow)
grep -rl 'deploy:prod\|vite build' .github/workflows/ 2>/dev/null
```

If **no** deploy workflow exists, skip this step — the local `.env.production` value is enough. If one **does** exist, two edits are required (both, or the CI build silently strips the block and ships analytics-free HTML):

1. **Reference the secret in the workflow.** Add `VITE_AHREFS_ANALYTICS_KEY` to the build step's `env:` block, alongside the other `VITE_*` values, in `.github/workflows/deploy.yml`:

   ```yaml
       env:
         VITE_BASE_URL: ${{ secrets.VITE_BASE_URL }}
         VITE_GA_ID: ${{ secrets.VITE_GA_ID }}
         VITE_AHREFS_ANALYTICS_KEY: ${{ secrets.VITE_AHREFS_ANALYTICS_KEY }}
   ```

2. **Create the repo secret** with the same value as `.env.production` (skip if `gh secret list` already shows it):

   ```bash
   REPO=$(gh repo view --json nameWithOwner -q .nameWithOwner)
   gh secret set VITE_AHREFS_ANALYTICS_KEY --repo "$REPO" --body "your-ahrefs-key"
   gh secret list --repo "$REPO"    # confirm VITE_AHREFS_ANALYTICS_KEY is present
   ```

The secret name must match the env var name exactly. The value is the same Ahrefs `data-key` you put in `.env.production` — it is a public site identifier, not a credential, but it lives in secrets so the workflow's `env:` mapping stays uniform with the other `VITE_*` keys.

### 6. Strip the Ahrefs script from prerendered HTML

In `scripts/prerender.mjs`, strip the Ahrefs `<script>` tag so it isn't double-loaded when the hydrated app adds it (mirror the GA prerender-strip):

```js
html = html.replace(
  /<script[^>]*src="https:\/\/analytics\.ahrefs\.com\/analytics\.js[^"]*"[^>]*><\/script>/g,
  ''
);
```

### 7. Allowlist `analytics.ahrefs.com` in the CSP

If the site has a Content Security Policy (from `/senternet-site-csp`), the default `script-src 'self'` blocks the Ahrefs script from loading and `connect-src 'self'` blocks it from beaconing data back. Extend the policy in `firebase.json`:

```
script-src   → add: https://analytics.ahrefs.com
connect-src  → add: https://analytics.ahrefs.com
```

If the site has no CSP yet, skip this — `/senternet-site-csp` already knows to include Ahrefs Web Analytics when it generates the policy. After editing the CSP, confirm in DevTools that there are no CSP violation errors for `analytics.ahrefs.com` in the console.

## Verification

After deploying to production:
- Open Chrome DevTools → Network tab
- Filter by `analytics.ahrefs.com`
- Confirm the script loads after the page `load` event fires, not during initial HTML parse
- Check the Ahrefs Web Analytics dashboard to confirm visits are arriving

## Framework: Next.js track

No `index.html` and no `htmlPlugin` on this track. Load the analytics script with `next/script` from `app/layout.tsx`, gated on the env var:

```tsx
import Script from 'next/script';

const ahrefsKey = process.env.NEXT_PUBLIC_AHREFS_KEY;

{ahrefsKey && (
  <Script src="https://analytics.ahrefs.com/analytics.js" data-key={ahrefsKey} strategy="lazyOnload" />
)}
```

- `NEXT_PUBLIC_AHREFS_KEY` replaces the `VITE_*` name, and must also be listed in `apphosting.yaml` with `BUILD` availability.
- `strategy="lazyOnload"` gives the same off-the-critical-path loading the Vite track gets from its `load`-event deferral.
- Leave the key empty in `.env.development` so local traffic never reports.
- No prerender strip step is needed.

See `/senternet-site-framework` for the full convention map.
