---
name: cloudflare-pages
description: Use when hosting static sites or small full-stack apps on Cloudflare Pages — Direct Upload deployments with wrangler from a local script, Pages Functions and middleware, D1 (SQLite) databases with migrations, redirects and headers, custom domains, and keeping deployments out of CI. Also use when a deploy goes to the wrong branch, a Function cannot see its binding, or D1 data differs between local and remote.
---

# Cloudflare Pages (+ Functions, D1)

Default: build locally, deploy with **Direct Upload** (`wrangler pages deploy`) from one script on the production branch, Functions in `functions/`, D1 for relational data, project and DNS declared in Terraform, deployments not triggered by CI.

## Deploy script

```bash
#!/usr/bin/env bash
set -euo pipefail
[[ $(git rev-parse --abbrev-ref HEAD) == main ]] || { echo "deploy from main only" >&2; exit 1; }
git diff --quiet || { echo "uncommitted changes" >&2; exit 1; }
npm ci && npm run build && npm test
npx wrangler pages deploy dist --project-name "$PROJECT" --branch main
```

- `--branch` decides production vs preview: it must equal the project's production branch, or you publish a preview URL and the live site does not change.
- Keeping deployment in one local script (instead of CI) avoids spending CI minutes and makes "what is live" equal "what main was when someone ran the script".

## Pages Functions

- Files under `functions/` map to routes (`functions/api/items/[id].ts` → `/api/items/:id`). `_middleware.ts` runs before routes in its directory.
- Bindings (D1, KV, environment variables) arrive on the `env` property of the Function context; declare them in `wrangler.toml` (or the dashboard) for both production and preview.
- Functions run on the edge runtime: Web APIs (`fetch`, Web Crypto), not Node built-ins, and limited CPU time per request.
- Return explicit `Cache-Control` headers; HTML for authenticated pages must not be cached publicly.

## D1

```bash
npx wrangler d1 migrations create DB add_table
npx wrangler d1 migrations apply DB --local     # local dev database
npx wrangler d1 migrations apply DB --remote    # production
```

- Migrations are append-only; never edit one that has been applied remotely.
- Local and remote databases are separate; seed local data for tests and do not copy production data down casually.
- Use prepared statements with bound parameters (`env.DB.prepare(sql).bind(...)`); batch related writes with `env.DB.batch([...])`.

## Static routing

- `_redirects` for redirects and SPA fallback (`/* /index.html 200`), `_headers` for security headers.
- `robots.txt` must be reachable without authentication if you want crawlers to read it — including a site you want to keep out of search results.

## Verification loop

1. Build and tests pass locally.
2. Deploy with the script; confirm the output names the production deployment, not a preview.
3. `curl -sI https://<domain>/` for status and headers; open a Function route and a D1-backed page.
4. Check that unauthenticated requests to protected paths are refused.

## Pitfalls

- **Wrong production branch** in project settings (or a renamed branch) silently turns every deploy into a preview.
- **Binding names** are case-sensitive and must match between config and code.
- **Large files:** Pages has per-file and per-deployment limits; keep build output lean.
- **Terraform and deploy overlap:** let Terraform own the project, domains and DNS; let the script own deployments. Do not try to deploy content from Terraform.
- **Provider major upgrades** (for example the Cloudflare Terraform provider moving to a new major version) change resource schemas; run `plan` until it shows no changes after migrating state.
