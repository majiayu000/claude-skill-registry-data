---
name: vercel
description: Vercel — env vars, edge functions, caching, preview, monorepo.
---

## Project Configuration (`vercel.json`)

Keep `vercel.json` minimal — only override defaults when necessary.

```json
{
  "buildCommand": "npm run build",
  "outputDirectory": ".next",
  "installCommand": "npm ci",
  "framework": "nextjs"
}
```

| Field | When to set | Notes |
|-------|-------------|-------|
| `framework` | Always | Enables Vercel-specific optimizations |
| `buildCommand` | Override only | Defaults to framework's standard build |
| `outputDirectory` | Override only | Framework default is usually correct |
| `installCommand` | When using `npm ci` or `pnpm` | Speeds up builds with frozen lockfiles |
| `regions` | Latency-sensitive | Defaults to closest region; see Regions section |

---

## Environment Variables

**Rules:**
- Never commit secrets to `vercel.json` or the repository
- Use Vercel dashboard or CLI to set env vars: `vercel env add`
- Scope variables correctly: `Production`, `Preview`, `Development`
- Prefix public client-side vars with `NEXT_PUBLIC_` (Next.js) or framework equivalent

```bash
# Add a secret via CLI
vercel env add DATABASE_URL production

# Pull env vars to local .env.local (never commit this file)
vercel env pull .env.local
```

| Scope | When to use |
|-------|------------|
| `Production` | Live traffic only |
| `Preview` | All branch/PR deployments |
| `Development` | Local `vercel dev` only |

---

## Deployment Regions

Default: `iad1` (Washington DC). Set per-project in `vercel.json`:

```json
{ "regions": ["gru1"] }
```

| Code | Location | Best for |
|------|----------|---------|
| `iad1` | US East (N. Virginia) | Default, global baseline |
| `gru1` | South America (São Paulo) | Brazilian user base |
| `cdg1` | Europe (Paris) | EU user base |
| `sin1` | Asia (Singapore) | SEA / Asia-Pacific |

For globally distributed workloads, use Edge Functions (see below) instead of specifying multiple regions.

---

## Edge Functions vs Serverless Functions

| | Edge Functions | Serverless Functions |
|--|---------------|---------------------|
| Runtime | V8 isolates (no Node.js) | Node.js / Python / Go / Ruby |
| Cold start | ~0ms | 100–500ms |
| Max duration | 30s | 10s (Hobby) / 60s (Pro) |
| Use case | Auth, redirects, A/B, geo-routing | DB queries, heavy compute |
| File location | `middleware.ts` (Next.js) or `/api` with `export const runtime = 'edge'` | `/api/*.ts` (default) |

**Prefer Edge for:** response rewrites, authentication checks, geolocation headers, A/B testing flags.  
**Prefer Serverless for:** anything requiring Node.js APIs, database connections, or long-running tasks.

---

## Build & Cache Optimization

```json
{
  "headers": [
    {
      "source": "/_next/static/(.*)",
      "headers": [{ "key": "Cache-Control", "value": "public, max-age=31536000, immutable" }]
    },
    {
      "source": "/api/(.*)",
      "headers": [{ "key": "Cache-Control", "value": "no-store" }]
    }
  ]
}
```

- Static assets (JS/CSS with content hashes) → `immutable`, 1 year TTL
- API routes → `no-store` by default; add `s-maxage` only for stable, non-user-specific responses
- Images → use Vercel's built-in Image Optimization (`next/image`); avoid manual `<img>` tags

**Build cache**: Vercel caches `node_modules` and framework build caches automatically between deployments. Use `npm ci` (not `npm install`) to ensure reproducible installs.

---

## Preview Deployments

Every push to a non-production branch gets a unique preview URL.

Best practices:
- Add `VERCEL_URL` env var checks in code for environment-aware configuration
- Set `Preview` scope env vars to point to staging databases, not production
- Use Vercel's "Protection Bypass" secret for automated testing against preview URLs:
  ```bash
  # Header to bypass preview password protection in CI
  x-vercel-protection-bypass: <secret>
  ```
- Never merge a PR without checking the preview deployment first

---

## Monorepo Support

For monorepos, set `Root Directory` in the Vercel project settings (or via CLI `--cwd`) to the app subdirectory:

```bash
vercel --cwd apps/web
```

Or configure in `vercel.json` at the repo root:

```json
{ "rootDirectory": "apps/web" }
```

Each app in the monorepo should be a separate Vercel project. Use Turborepo's remote cache with Vercel for faster CI builds:
```bash
npx turbo login
npx turbo link
```

---

## Team Workflow

- **One project per environment is an anti-pattern** — use Vercel's built-in Production / Preview / Development scoping instead
- Protect Production branch: enable "Required reviewers" in Vercel project settings
- Use `vercel --prod` only for intentional production deploys; CI should auto-deploy via Git integration
- Audit deployment logs after every production release: `vercel logs --prod`
- Rotate `VERCEL_TOKEN` secrets at least quarterly; scope tokens to the minimum required project

---

## Common Pitfalls

| Problem | Cause | Fix |
|---------|-------|-----|
| Function timeout in production | Default 10s limit on Hobby | Upgrade plan or move to Edge |
| Env var not available at build time | Set as `Development` not `Preview`/`Production` | Re-scope in dashboard → redeploy |
| Large bundle size warnings | Dependencies imported at top level | Use dynamic `import()` for heavy libs |
| Cold starts on API routes | Serverless function not warmed | Move to Edge, or use Vercel's Fluid Compute (Pro) |
| Preview URL auth blocks CI | Protection enabled | Add `x-vercel-protection-bypass` header in CI |
