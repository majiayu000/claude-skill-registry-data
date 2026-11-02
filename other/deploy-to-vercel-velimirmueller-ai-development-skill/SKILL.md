---
name: deploy-to-vercel
description: Use when deploying to Vercel - linking the project, env vars per environment and vercel env pull, protected previews, the config file, regions near the database, crons, rolling releases and rollback, the firewall, and gated prebuilt deploys from CI.
---

# Deploy to Vercel

Vercel builds and serves the app; there is no image and no server to patch. One project, one config file, functions next to the database, previews protected behind the Git integration. Commercial use needs Pro; Hobby is non-commercial only.

## 1. Audit current state (change nothing)

```bash
cat .claude/stack-profile.md 2>/dev/null || cat ~/.claude/stack-profile.md 2>/dev/null
ls vercel.json vercel.ts vercel.toml .vercel/ .github/workflows 2>/dev/null
vercel --version 2>/dev/null
grep -n "\.vercel" .gitignore 2>/dev/null
```

Read from the profile: `hosting` must include `vercel`; `backend.track` (`nextjs`, `hono`, `fastapi` run on Vercel functions), `frontend.meta` (`next`, `nuxt`, `vite`), `database.host` (`supabase`) and its region, `package_manager`. Only one config file may exist (`vercel.json`, `vercel.ts`, or `vercel.toml`); two means delete one. Check token presence by NAME only (`VERCEL_TOKEN`, `VERCEL_ORG_ID`, `VERCEL_PROJECT_ID`); never print values.

## 2. Decide

- Profile `hosting` is not `vercel` → stop; see [hosting-decision.md](../_shared/hosting-decision.md).
- No config file and no `.vercel/` → full (steps 3 to 7).
- Config file exists → delta: check each step's checklist, fix only what fails.
- Everything in place and `vercel build` passes → "already in place" and stop.

## 3. Detect the track

| Evidence | Track |
|---|---|
| `next.config.*`, `app/` or `pages/` | Next.js |
| `nuxt.config.*` | Nuxt |
| `vite.config.*`, no server framework | Vite SPA (rewrite `/(.*)` to `index.html`) |
| `package.json` with `hono` / `express` / `fastapi` | Vercel functions |

Config-file choice: `vercel.json` (with `$schema`) for static config; `vercel.ts` only when the config needs build-time logic, using `@vercel/config` (pre-1.0); `vercel.toml` exists too. One file only.

## 4. Install only what is missing

```bash
pnpm add -D vercel@63.1.0     # dev dependency; or: pnpm dlx vercel@63.1.0
```

Never a global install in CI without a pinned version.

## 5. Generate the seams

1. **Link the project**: `vercel link` (writes `.vercel/`; add `.vercel/` to `.gitignore`).
2. **Config file** with `regions` next to the database (`fra1` for EU; the default `iad1` is a US region), per-function `maxDuration`, and `crons`:

```ts
import { routes, type VercelConfig } from '@vercel/config/v1';

export const config: VercelConfig = {
  framework: 'nextjs',
  regions: ['fra1'],
  functions: {
    'app/api/**/*': { maxDuration: 30 },
  },
  crons: [{ path: '/api/cron/reconcile', schedule: '*/15 * * * *' }],
  headers: [
    routes.header('/(.*)', [
      { key: 'X-Content-Type-Options', value: 'nosniff' },
      { key: 'Referrer-Policy', value: 'strict-origin-when-cross-origin' },
    ]),
  ],
};
```

Mode 2 below adds `git: { deploymentEnabled: false }` to this file; mode 1 must not. Cron schedules faster than once per day need Pro (Hobby: daily, hour-level precision).

3. **Cron route.** Vercel GETs the production deployment with `Authorization: Bearer <CRON_SECRET>`; reject when the secret is missing or the header differs:

```ts
// app/api/cron/reconcile/route.ts
export async function GET(request: Request) {
  const secret = process.env.CRON_SECRET;
  const auth = request.headers.get('authorization');
  if (!secret || auth !== `Bearer ${secret}`) {
    return new Response('Unauthorized', { status: 401 });
  }
  // idempotent work
  return new Response('ok');
}
```

4. **Env vars per environment.** Production, Preview and custom environments default to secret; Development defaults to config:

```bash
vercel env add DATABASE_URL production --sensitive --yes   # secret
vercel env add NEXT_PUBLIC_API_URL production --yes        # config (visible in the dashboard)
vercel env add CRON_SECRET production --sensitive --yes    # avoid --value: it lands in shell history
vercel env pull .env.local                                 # merge remote env into a local file
vercel env run -- pnpm test                                 # run with the env, no file written
```

Validate the result at startup with [validate-env](../../frontend/validate-env/SKILL.md) for TypeScript.

## 6. Wire

- **Previews:** the Git integration builds every pull request. Protect them with Deployment Protection → Standard Protection (all but production domains) plus Vercel Authentication.
- **Production gate, mode 1 (recommended):** Git integration + turn **Auto-assign Custom Production Domains** off, then promote after approval with `vercel promote`. This is the pipeline's `dev` = PR preview, `stg` = staged production build, `prd` = promote under the `prd` GitHub environment; see [set-up-delivery-pipeline](../set-up-delivery-pipeline/SKILL.md), do not restate its workflows.
- **Mode 2 (full CI control):** `git.deploymentEnabled: false`, then `vercel pull --yes --environment=...`, `vercel build`, `vercel deploy --prebuilt --archive=tgz` with `VERCEL_TOKEN`, `VERCEL_ORG_ID`, `VERCEL_PROJECT_ID` as GitHub environment secrets/variables. Skeleton for the production job (only these two actions; verified with `actionlint`, not run on GitHub):

```yaml
name: deploy-vercel

on:
  workflow_dispatch:

permissions: {}

jobs:
  production:
    runs-on: ubuntu-latest
    timeout-minutes: 20
    environment: prd
    steps:
      - uses: actions/checkout@3d3c42e5aac5ba805825da76410c181273ba90b1 # v7.0.1
        with:
          persist-credentials: false
      - uses: actions/setup-node@949feb2413d6458794dcd2491c4babbbce0c15c1 # v7.1.0
        with:
          node-version: 24
      - run: npx --yes vercel@63.1.0 pull --yes --environment=production --token "$VERCEL_TOKEN"
        env:
          VERCEL_TOKEN: ${{ secrets.VERCEL_TOKEN }}
          VERCEL_ORG_ID: ${{ vars.VERCEL_ORG_ID }}
          VERCEL_PROJECT_ID: ${{ vars.VERCEL_PROJECT_ID }}
      - run: npx --yes vercel@63.1.0 build --prod --token "$VERCEL_TOKEN"
        env:
          VERCEL_TOKEN: ${{ secrets.VERCEL_TOKEN }}
          VERCEL_ORG_ID: ${{ vars.VERCEL_ORG_ID }}
          VERCEL_PROJECT_ID: ${{ vars.VERCEL_PROJECT_ID }}
      - run: npx --yes vercel@63.1.0 deploy --prebuilt --prod --archive=tgz --token "$VERCEL_TOKEN"
        env:
          VERCEL_TOKEN: ${{ secrets.VERCEL_TOKEN }}
          VERCEL_ORG_ID: ${{ vars.VERCEL_ORG_ID }}
          VERCEL_PROJECT_ID: ${{ vars.VERCEL_PROJECT_ID }}
```

- **Firewall:** DDoS mitigation and WAF are on all plans; add custom rules for IP blocking and rate limiting (rate-limit plan details unverified).
- **BotID:** client `initBotId({ protect: [{ path, method }] })`, server `checkBotId()` from `botid/server` (returns `isBot`), Next.js `withBotId` wrapper. Snippets in [vercel-patterns.md](./vercel-patterns.md).
- On Vercel the preview deployment replaces the Netlify preview step in [configure-ci](../../frontend/configure-ci/SKILL.md); keep its lint, types, test and e2e gates.

## 7. Verify

```bash
vercel env ls production                      # every production variable listed
vercel build                                  # completes, prints a build summary
vercel deploy --prebuilt                      # prints a deployment URL
curl -fsS https://<preview-url>/api/health -H "x-vercel-protection-bypass: $VERCEL_AUTOMATION_BYPASS_SECRET"
```

Expect: the env list shows all names; the build completes; the deploy prints a URL; the health call returns 200 with the protection-bypass header; the deployment summary shows the function region (`fra1`). Rollback drill: use the dashboard Instant Rollback, then `vercel promote <url>` to undo. `vercel rollback` is not in the facts — treat it as unverified.

Unverified: none of this was run against a Vercel account (docs read and `vercel.ts` typechecked only). The workflow skeleton passed `actionlint` but was not run on GitHub.

## References

- [vercel-patterns.md](./vercel-patterns.md): the rules and why (config format, Fluid compute, regions, env, OIDC, crons, protection, rolling releases, rollback, firewall/BotID, prebuilt caveats).
- [../set-up-delivery-pipeline/SKILL.md](../set-up-delivery-pipeline/SKILL.md): the approval gate and promote workflow this skill links, not restates.
- [../_shared/environments.md](../_shared/environments.md), [../_shared/hosting-decision.md](../_shared/hosting-decision.md), [../_shared/stack-versions.md](../_shared/stack-versions.md).
- [../../frontend/validate-env/SKILL.md](../../frontend/validate-env/SKILL.md), [../../frontend/configure-ci/SKILL.md](../../frontend/configure-ci/SKILL.md).
