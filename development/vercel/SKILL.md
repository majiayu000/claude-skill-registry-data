---
name: vercel
description: "Configure Vercel projects, environment variables, build settings, and preview deployments before a production rollout."
category: development
risk: safe
source: self
source_type: self
date_added: "2026-08-26"
tags: ["vercel", "nextjs", "deploy", "edge", "preview", "claude"]
tools: ["claude", "cursor", "gemini", "codex"]
---

# Vercel Deployment AI Skill Guide

## Overview & Engine Architecture

Vercel builds frontend/Next.js apps on Git push into immutable deployments. Preview URLs cover PRs; production tracks the production branch. Runtime can be Node serverless functions, Edge Middleware, or static assets depending on framework output. Agents keep secrets in Vercel env scopes, fail closed on missing prod env, and treat build logs as the source of truth for deploy failures.

```
Git push / vercel deploy
        |
  Build (install + build command)
        |
  Output (static / serverless / edge)
        |
  Preview URL  or  Production domain
```

## When to use this skill

- Deploying Next.js or static frontends to Vercel
- Configuring environment variables per environment
- Debugging failed builds or runtime 500s after deploy
- Setting up preview deployments for PR review

## Operational directives

1. Put secrets in Vercel Project Env (Preview/Production/Development) - never in git.
2. `NEXT_PUBLIC_*` is exposed to the browser - no private keys there.
3. Pin Node version (`engines` or Project settings) to match local CI.
4. Prefer framework presets; override build/output only when needed.
5. Promote/protect production with branch protection and required checks.

## `vercel.json` sketch (optional overrides)

```json
{
  "framework": "nextjs",
  "regions": ["iad1"],
  "headers": [
    {
      "source": "/(.*)",
      "headers": [
        { "key": "X-Content-Type-Options", "value": "nosniff" }
      ]
    }
  ]
}
```

## Commands

```bash
npm i -g vercel
vercel login
vercel link
vercel env pull .env.local
vercel --prod
vercel logs <deployment-url>
```

## Common pitfalls

| Pitfall | Why it hurts | Fix |
| --- | --- | --- |
| Missing prod env vars | Runtime crashes | Mirror env scopes |
| Relying on localhost URLs | Broken previews | Relative URLs / env-based base |
| Edge-incompatible Node APIs | Build/runtime errors | Check runtime per route |
| Ignoring build cache issues | Mysterious stale output | Redeploy without cache |

## Best practices

- Use Preview deployments for QA; never hot-edit production-only.
- Set up `VERCEL_URL` aware absolute URL helpers when needed.
- Monitor Core Web Vitals and function duration after launch.
- Document monorepo root/`cd` settings when the app is not repo root.

## Limitations

- Long-running background jobs need external workers - not request functions.
- Region and limits differ on hobby vs pro plans.
- Custom servers (arbitrary Express listening forever) are not the Vercel model.

## Related skills

- `@nextjs` - App Router app that Vercel deploys well
- `@nodejs` - runtime constraints inside serverless functions
- `@playwright-ci` - smoke-testing preview deployments
