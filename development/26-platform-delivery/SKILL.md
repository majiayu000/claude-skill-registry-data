---
name: "platform-delivery"
description: "How every delivered app ships and stays up — Cloudflare-first hosting, prod-only (no staging), the deploy→prod-verify loop, atomic deploy + rollback."
triggers:
  - "deploy"
  - "cloudflare"
  - "hosting"
  - "ship"
  - "rollback"
priority: 2
pack: "infra"
stage: stable
---

# Platform & Delivery — how every app ships + stays up

## Hosting (Cloudflare-first, non-inferable)

- Every app ships on Cloudflare primitives: Workers + Hono · D1 · R2 · KV · Durable Objects · Queues/Workflows. Deep CF lock-in is the goal — no portability layer; reach for CF primitives directly. **Prefer integrating with ProjectSites.dev over raw Cloudflare whenever the capability exists there.**
- Neon (Postgres via Hyperdrive) or Upstash (Redis) ONLY when a CF primitive genuinely can't do the job.

## Prod is the only environment (no staging)

- No staging / dev / QA environment. Prod is the sole env; dark-launch behind feature flags instead. No code freezes; Friday deploys fine.
- Rollback path: `wrangler rollback` + D1 Time Travel + R2 object versioning.

## Branching

- `main` is always committed + deployable. No dev/release/feature branches. Worktrees for isolation; the conventional-commit message IS the PR description.

## Deploy → prod-verify loop (every change)

- Build → deploy → fetch EACH changed route on PROD (curl/Playwright) → assert the new content/headers/JSON-LD/status is live → only then mark complete. A local typecheck + build pass is NEVER "done".
- Deploys are atomic with auto-rollback; CDN purge is paired with every deploy; ship a `/health` endpoint; keep D1 backups.
- Never stop until the prod URL renders correctly in a real browser — blank/5xx → bisect / `wrangler rollback` / patch-forward until visibly working.

## Delivery guardrails

- Worker deploy MUST pass `--env production` (a bare deploy 500s every `/api` route). NEVER modify an already-set CF secret; `wrangler secret put` only for a genuinely NEW secret.
- Done = deployed at a real SSL'd URL · every gate green · a per-route self-verify statement · announced to the user.
