---
$schema: https://gist.githubusercontent.com/remorses/9f3737a6f516c01f4bdb612045c64072/raw/agent-skill.schema.json
name: cloudflare-deploy-button
description: >
  "Deploy to Cloudflare" button for self-hostable Workers apps. Covers
  wrangler.jsonc setup, D1 migrations in deploy script, secret descriptions,
  .dev.vars.example, monorepo handling, custom domains, and the cloudflare
  field in package.json. Load this skill when adding a deploy button to a
  Cloudflare Workers project or making an app easy to self-host on Cloudflare.
---

# Deploy to Cloudflare Button

Make any Cloudflare Workers app deployable with one click. Users click a
button in your README → Cloudflare forks the repo, provisions all
resources (D1, KV, R2, etc.), and deploys the worker. No CLI needed.

## The button

Add this to your README:

```markdown
[![Deploy to Cloudflare](https://deploy.workers.cloudflare.com/button)](https://deploy.workers.cloudflare.com/?url=https://github.com/OWNER/REPO)
```

For a subdirectory in a monorepo:

```markdown
[![Deploy to Cloudflare](https://deploy.workers.cloudflare.com/button)](https://deploy.workers.cloudflare.com/?url=https://github.com/OWNER/REPO/tree/main/packages/my-app)
```

## What the button does automatically

1. **Forks** the repo into the user's GitHub/GitLab
2. **Reads `wrangler.jsonc`** to discover required resources
3. **Auto-provisions** D1 databases, KV namespaces, R2 buckets, Durable Objects, Queues, Vectorize, Workers AI, Hyperdrive, Secrets Store
4. **Replaces** placeholder `database_id`, `namespace_id`, etc. with real IDs
5. **Runs `build` then `deploy`** scripts from `package.json`
6. **Sets up Workers Builds** CI/CD — future pushes auto-deploy

## What the button does NOT do

- **Custom domains** — the worker gets `*.workers.dev`. Users add custom domains from the Cloudflare dashboard after deploy.
- **Run arbitrary setup scripts** — only `build` and `deploy` from `package.json`
- **Clone git submodules** — submodules are NOT cloned. All dependencies must be resolvable via the package manager.

## Required setup in your repo

### 1. `package.json` scripts — migrations in `deploy`

The deploy button runs the `deploy` script. Chain D1 migrations before
`wrangler deploy` using `&&` so they run as a single atomic step.

**Always reference the binding name (`DB`), not the database name**, because users can customize the database name during setup.

```json
{
  "scripts": {
    "build": "vite build",
    "deploy": "wrangler d1 migrations apply DB --remote && wrangler deploy"
  }
}
```

If no `deploy` script exists, the button defaults to `npx wrangler deploy`.
If no `build` script exists, the build step is skipped.

### 2. Secret descriptions in `package.json`

Add a `cloudflare.bindings` section to describe secrets. These descriptions
are shown to users on the deploy setup page so they know what to enter.

Supports inline markdown: `` `code` ``, `**bold**`, `__italics__`, and `[links](url)`.

```json
{
  "cloudflare": {
    "bindings": {
      "MY_SECRET": {
        "description": "Random signing key. Generate with `openssl rand -base64 32`."
      },
      "API_KEY": {
        "description": "Your [Stripe API key](https://dashboard.stripe.com/apikeys) (starts with `sk_live_`)."
      }
    }
  }
}
```

### 3. `.dev.vars.example` for secrets

Create a `.dev.vars.example` (or `.env.example`) file with dotenv format.
The deploy button reads this and shows input fields for each secret:

```env
BETTER_AUTH_SECRET=change-me # Random string for signing sessions
ENCRYPTION_KEY= # Optional: openssl rand -base64 32
```

### 4. Template metadata (optional)

For apps listed in Cloudflare's template gallery, add metadata:

```json
{
  "cloudflare": {
    "label": "My App",
    "products": ["Workers", "D1"],
    "categories": ["storage"],
    "publish": true
  }
}
```

### 5. `wrangler.jsonc` — keep placeholder IDs

The button replaces `database_id`, `namespace_id`, etc. with real values
after provisioning. Keep your existing IDs in the config — they serve as
placeholders and are overwritten for new deployers.

```jsonc
{
  "name": "my-app",
  "d1_databases": [
    {
      "binding": "DB",
      "database_name": "my-app-db",
      "database_id": "placeholder-gets-replaced",
      "migrations_dir": "./migrations"
    }
  ]
}
```

**`routes` with `custom_domain: true`** are safe to keep. The button
ignores domains it can't configure. The worker deploys to `*.workers.dev`
and users add custom domains later from the dashboard.

**`secrets.required`** tells wrangler which secrets must exist. Keep this —
it validates that users set their secrets after deploy.

## Custom domains

The deploy button does NOT set up custom domains. After deploy:

1. Worker is accessible at `my-app.username.workers.dev`
2. User goes to Cloudflare dashboard → Workers → their worker → Settings → Domains & Routes
3. User adds their own domain (must be in their Cloudflare account)

Document this as a post-deploy step in your README. Example:

```markdown
### Custom domain (optional)

After deploying, your app runs at `https://your-worker.workers.dev`.
To use your own domain:

1. Add your domain to Cloudflare (it must use Cloudflare DNS)
2. Go to **Workers & Pages** → your worker → **Settings** → **Domains & Routes**
3. Click **Add** → **Custom Domain** and enter your domain
```

## Monorepo handling

### The problem

The deploy button supports a `?url=` subdirectory path, but from the
official docs:

> If your repository URL contains a subdirectory, your application must be
> **fully isolated within that subdirectory**, including any dependencies.
> Cloudflare treats this subdirectory as the root of the new repository.

This means pointing at a subdirectory like `/tree/main/app` **breaks**
if the app has `workspace:^` dependencies on sibling packages. The
subdirectory is extracted alone — workspace siblings are not included.

Git submodules are also **not cloned** by the deploy button.

### Always use the repo root

**Never point the deploy button at a subdirectory if you have workspace
dependencies.** Always point at the repo root and add `build` and
`deploy` scripts to the **root** `package.json` that delegate to the
app package:

```json
{
  "scripts": {
    "build": "pnpm --filter my-app build",
    "deploy": "wrangler d1 migrations apply DB --remote && wrangler deploy"
  }
}
```

The deploy button URL should be the repo root, not a subdirectory:

```markdown
<!-- ✅ Correct — repo root -->
[![Deploy to Cloudflare](https://deploy.workers.cloudflare.com/button)](https://deploy.workers.cloudflare.com/?url=https://github.com/owner/repo)

<!-- ❌ Wrong — subdirectory with workspace deps -->
[![Deploy to Cloudflare](https://deploy.workers.cloudflare.com/button)](https://deploy.workers.cloudflare.com/?url=https://github.com/owner/repo/tree/main/app)
```

The entire repo is cloned including all workspace packages, so
`workspace:^` dependencies resolve correctly. The `wrangler.jsonc`
inside the app subfolder is discovered by wrangler automatically (or
you can pass `--config app/wrangler.jsonc` in the deploy script).

**Submodules:** if a workspace dep is a git submodule, remove it and
depend on the published npm package instead. Submodules are never
cloned by the deploy button.

## What happens if the repo owner clicks their own button

- **Same Cloudflare account**: the worker name from `wrangler.jsonc` is
  used as default. If a worker with that name already exists, it will be
  **overwritten**. Change the name on the setup page to avoid this.
- **Different Cloudflare account**: works fine — creates a fresh worker
  with a new D1 database.

The setup page lets users customize: worker name, database names,
resource names, and secret values before deploying.

## Full example: self-hostable app with D1

### `wrangler.jsonc`

```jsonc
{
  "name": "my-app",
  "compatibility_date": "2026-05-01",
  "compatibility_flags": ["nodejs_compat"],
  "main": "src/index.ts",
  "d1_databases": [
    {
      "binding": "DB",
      "database_name": "my-app-db",
      "database_id": "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx",
      "migrations_dir": "./migrations"
    }
  ],
  "vars": {
    "PUBLIC_URL": "https://my-app.example.com"
  },
  "secrets": {
    "required": ["AUTH_SECRET"]
  },
  "routes": [
    { "pattern": "my-app.example.com", "custom_domain": true }
  ]
}
```

### `package.json`

```json
{
  "name": "my-app",
  "scripts": {
    "build": "vite build",
    "deploy": "wrangler d1 migrations apply DB --remote && wrangler deploy",
    "dev": "wrangler d1 migrations apply DB --local && wrangler dev"
  },
  "cloudflare": {
    "label": "My App",
    "products": ["Workers", "D1"],
    "bindings": {
      "AUTH_SECRET": {
        "description": "Random string for signing sessions. Generate with `openssl rand -base64 32`."
      }
    }
  }
}
```

### `.dev.vars.example`

```env
AUTH_SECRET=change-me # openssl rand -base64 32
```

### `README.md`

```markdown
## Self-hosting

[![Deploy to Cloudflare](https://deploy.workers.cloudflare.com/button)](https://deploy.workers.cloudflare.com/?url=https://github.com/owner/my-app)

After clicking the button:

1. Set `AUTH_SECRET` to a random string (the deploy page will prompt you)
2. Your app is live at `https://my-app.USERNAME.workers.dev`
3. (Optional) Add a custom domain from Workers settings in the Cloudflare dashboard
```

## Derive URLs from the request — never hardcode app URLs

Self-hosted apps must work on any domain the deployer chooses. Never
hardcode your own domain in env vars like `BETTER_AUTH_URL`, `APP_URL`,
or `PUBLIC_ORIGIN`. Instead, derive the URL from the incoming request:

```typescript
// ✅ Correct — works on any domain
const origin = new URL(request.url).origin
const auth = betterAuth({
  baseURL: origin,
  // ...
})

// ❌ Wrong — breaks for every self-hoster
const auth = betterAuth({
  baseURL: env.APP_URL, // hardcoded to your domain
})
```

This matters for BetterAuth specifically because `baseURL` is used to:
- **Generate OAuth callback URLs** — `{baseURL}/api/auth/callback/{provider}`
- **Set cookie scope** — cookie domain is derived from baseURL
- **Validate redirects** — checks origins against baseURL + trustedOrigins

If `baseURL` doesn't match the actual domain, OAuth flows break with
`redirect_uri_mismatch` and cookies don't get set correctly.

### Why this is safe on Cloudflare Workers

Using the request host as `baseURL` is normally dangerous — an attacker
could forge the `Host` header and trick the app into generating callbacks
to a malicious domain. But **Cloudflare Workers are safe** because:

1. **Cloudflare controls routing** — a Worker only receives requests for
   domains explicitly configured in the dashboard (Custom Domains or
   `*.workers.dev`). You cannot invoke a worker with a forged host.
2. **Host header is locked** — Cloudflare overwrites the Host header to
   match the actual routed domain. Forged Host headers are blocked.
3. **No upstream proxy** — unlike Node.js behind nginx where Host can
   be spoofed, Cloudflare IS the edge. There's no intermediary.

References:
- Custom Domains require exact hostname match: https://developers.cloudflare.com/workers/configuration/routing/custom-domains/
- Cloudflare blocks forged Host headers: https://news.ycombinator.com/item?id=25058579

### Pattern for localhost/tunnel support

For local development behind a tunnel (e.g. kimaki tunnel, cloudflared),
the request URL shows `localhost` but the real public URL is different.
Handle this by checking forwarded headers only on localhost:

```typescript
function getRequestOrigin(request: Request): string {
  const url = new URL(request.url)

  // On non-localhost, trust the request URL directly (Cloudflare guarantees it)
  if (url.hostname !== 'localhost' && url.hostname !== '127.0.0.1') {
    return url.origin
  }

  // On localhost, check forwarded headers for tunnel support
  const forwardedHost = request.headers.get('x-forwarded-host')
  if (forwardedHost) {
    const host = forwardedHost.split(',')[0]!.trim()
    const proto = request.headers.get('x-forwarded-proto')?.split(',')[0]?.trim() ?? 'https'
    return `${proto}://${host}`
  }

  return url.origin
}
```

### What about vars like `PUBLIC_URL` in wrangler.jsonc?

If your app has a `PUBLIC_URL` or `APP_URL` var in `wrangler.jsonc` for
things like email links or OpenGraph tags, **remove it** and derive from
the request instead. Any hardcoded URL becomes a config burden for
self-hosters. The only exception is when the URL must be known at build
time (e.g. baked into static HTML) — in that case document it clearly as
a required post-deploy configuration step.

## References

- **Official docs**: https://developers.cloudflare.com/workers/platform/deploy-buttons/
- **Official templates repo** (canonical reference for patterns): https://github.com/cloudflare/templates
  - `d1-template/package.json` — D1 + migrations pattern
  - `saas-admin-template/package.json` — Astro + D1 + workflows
  - `openauth-template/package.json` — OpenAuth + D1 + KV
- **Legacy deploy button source** (GitHub Actions-based, older): https://github.com/cloudflare/deploy.workers.cloudflare.com
- **Workers SDK** (Wrangler source): https://github.com/cloudflare/workers-sdk
- **D1 migrations docs**: https://developers.cloudflare.com/d1/reference/migrations/
- **Custom domains docs**: https://developers.cloudflare.com/workers/configuration/custom-domains/
- **Workers Builds (CI/CD)**: https://developers.cloudflare.com/workers/ci-cd/builds/
