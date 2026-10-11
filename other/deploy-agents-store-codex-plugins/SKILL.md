---
name: deploy
description: Deploy the current project to Vercel. Pass "prod" or "production" as argument to deploy to production. Default is to ask the user which target (production or preview).
---

# Deploy to Vercel

Deploy the current project to Vercel using the CLI, with preflight safety checks, explicit production confirmation, and post-deploy verification.

## Preflight

Run these checks before any deployment. Stop on failure and print actionable guidance.

1. **CLI available?** — Confirm `vercel` is on PATH.
   - If missing: `npm i -g vercel` (or `pnpm add -g vercel` / `bun add -g vercel`).
2. **Project linked?** — Check for `.vercel/project.json` in the current directory or nearest parent.
   - If not found: run `vercel link` interactively, then re-run `/deploy`.
3. **Monorepo detection** — Look for `turbo.json` or `pnpm-workspace.yaml` at the repo root.
   - If detected: confirm which package is targeted. If ambiguous, ask the user before proceeding.
4. **Uncommitted changes** — Run `git status --porcelain`.
   - If output is non-empty: warn the user that uncommitted changes will **not** be included in the deploy. Ask whether to continue or commit first.
   - If not a git repo, skip this check.
5. **VERCEL_TOKEN conflict?** — Check if `VERCEL_TOKEN` is set in the environment (`echo $VERCEL_TOKEN`).
   - If set: it overrides CLI interactive login and may cause auth failures (e.g., token from Infisical/CI that doesn't match the CLI-authenticated account). Run `unset VERCEL_TOKEN` before all `vercel` CLI commands in this session, or prefix each command with `unset VERCEL_TOKEN &&`.
6. **Framework detection (Next.js)?** — If the project has a `next.config.ts` or `next.config.js` but **no `vercel.json`** with a `"framework"` field:
   - Create `vercel.json` with `{"$schema": "https://openapi.vercel.sh/vercel.json", "framework": "nextjs"}`.
   - **Why:** Without this, CLI-only deploys (no Git integration) may use a generic builder. The build appears to succeed, but all routes return 404 because Vercel doesn't generate the correct routing configuration. This is the #1 cause of "build succeeds but site shows 404".
7. **`output: 'standalone'` in Next.js config?** — Check `next.config.ts` / `next.config.js` for `output: 'standalone'`.
   - If found: note that `standalone` output is meant for Docker/self-hosting and is a **possible** cause of a Ready-but-404 deploy on Vercel (not reproduced; a wrong Framework Preset, see step 6, is the documented cause). If the deploy 404s, suggest conditionally disabling it:
     ```typescript
     ...(process.env.VERCEL ? {} : { output: 'standalone' as const }),
     ```
   - Ask the user before modifying the config.
8. **Git author email vs Vercel team (Hobby plan)?** — If `.vercel/project.json` exists and contains an `orgId` starting with `team_`:
   - Run `vercel teams ls` and `git log -1 --format='%ae'` to check if the git author email matches the team owner.
   - On Hobby plans, only the team owner can deploy. If emails don't match, warn the user and suggest: `git config user.email "<team-owner-email>"` followed by an empty commit (`git commit --allow-empty -m "chore: update deploy author"`).
9. **Env vars for preview?** — If deploying a preview and the project has no Git integration (`vercel.json` has no `github` config or project was linked without Git):
   - Preview env vars may not be configured. Check `vercel env ls` for Preview entries.
   - If missing: add them to Preview non-interactively. The Git branch is optional (`--git-branch` only narrows it):
     ```bash
     vercel env add KEY preview --value "value" --yes
     ```
     `--value` is visible in the process list and shell history; for secrets pipe the value on stdin instead.
   - Or pass env vars for this deploy only via `-b` (build-time) and `-e` (runtime) flags — still valid, nothing is stored:
     ```bash
     vercel deploy -b KEY="value" -e KEY="value"
     ```
   - Read required vars from `.env.local` or `.env.example`.
10. **Observability preflight** (production deploys only) —

Before promoting to production, verify observability readiness:

- **Drains check**: Query configured drains via MCP `list_drains` or REST API. If no drains are configured on a Pro/Enterprise plan, warn:
  > ⚠️ No drains configured. Production errors won't be forwarded to external monitoring.
  > Configure drains via Dashboard or REST API before promoting.
- **Errored drains**: If any drain is in error state, warn and suggest remediation before deploying:
  > ⚠️ Drain "<url>" is errored. Fix or recreate before production deploy to avoid monitoring gaps.
- **Error monitoring**: Check that at least one of these is in place: configured drains, an error tracking integration (e.g., Sentry, Datadog via `vercel integration ls`), or `@vercel/analytics` in the project.
- These are warnings, not blockers — the user may proceed after acknowledgment.

## Plan

State the intended action before executing:

- **Preview deploy**: `vercel` — creates a preview deployment on a unique URL.
- **Production deploy**: `vercel --prod` — deploys to production domains.

If "$ARGUMENTS" contains "prod" or "production":

> ⚠️ **Production deployment requested.**
> This will deploy to your live production URL and affect real users.
> **Ask the user for explicit confirmation before proceeding.** Do not deploy to production without a clear "yes."

If "$ARGUMENTS" is empty (no target specified):

> **Ask the user before proceeding:** "Deploy to **production** or **preview**?"
> Do not assume a default — the user must explicitly choose the deployment target. Deploying to the wrong target wastes build minutes and causes confusion (e.g., preview deployments may lack required env vars).

If "$ARGUMENTS" contains "preview":

> Deploying a **preview** build. This creates an isolated URL and does not affect production.

## Commands

### Preview Deployment

<!-- Sourced from deployments-cicd skill: Deployment Commands > Preview Deployment -->
```bash
# Deploy from project root (creates preview URL)
vercel

# Equivalent explicit form
vercel deploy
```

Preview deployments are created automatically for every push to a non-production branch when using Git integration. They provide a unique URL for testing.

### Production Deployment (requires confirmation)

<!-- Sourced from deployments-cicd skill: Deployment Commands > Production Deployment -->
```bash
# Deploy directly to production
vercel --prod
vercel deploy --prod

# Force a new deployment (skip cache)
vercel --prod --force
```

Capture the full command output. Extract the **deployment URL** from the output (the line containing the `.vercel.app` URL or custom domain URL).

Record the current git commit SHA for the summary:

```bash
git rev-parse --short HEAD
```

## Verification

After deployment completes, verify the result:

### Live Status (MCP)

If the Vercel MCP server exposes `open_deployments`, call it with `view: "preview"`, `teamId` (`orgId`) and `projectId` from `.vercel/project.json`, plus `branch` (`git rev-parse --abbrev-ref HEAD`) and `sha` (`git rev-parse HEAD`). Hosts that support MCP Apps show a live view that updates until the build finishes; use its text summary for the steps below. If the build fails, the view's **Send Logs to Chat** button asks the agent to investigate with `get_deployment_build_logs`.

### 1. Inspect the Deployment

<!-- Sourced from deployments-cicd skill: Deployment Commands > Inspect Deployments -->
```bash
# View deployment details (build info, functions, metadata)
vercel inspect <deployment-url>

# List recent deployments
vercel ls

# View logs for a deployment
vercel logs <deployment-url>
vercel logs <deployment-url> --follow
```

Extract: deployment state (READY / ERROR / QUEUED / BUILDING), build duration, framework, Node.js version, function count.

### 2. On Failure — Fetch Build Logs

If the deployment state is **ERROR** or the deploy command exited non-zero:

```bash
vercel logs <deployment-url>
```

Present the last 50 lines of build logs to help diagnose the failure. Highlight any lines containing `error`, `Error`, `ERR!`, or `FATAL`.

### 3. On Success — Quick Smoke Check

If the deployment state is **READY**, note the URL is live and accessible.

### 4. Post-Deploy Error Scan (production deploys)

For production deployments, wait 60 seconds after READY state, then scan for early runtime errors:

```bash
vercel logs <deployment-url> --level error --since 1h
```

Or via MCP if available: use `get_runtime_logs` with level filter `error`.

**Interpret results:**

| Finding | Action |
|---------|--------|
| No errors | ✓ Clean deploy — no runtime errors in first hour |
| Errors detected | List error count and first 5 unique error messages. Suggest: check drain payloads for correlated traces, review function logs in Dashboard |
| 500 status codes in logs | Correlate timestamps with drain data (if configured) or `vercel logs <url> --json` for structured output. Flag for immediate investigation |
| Timeout errors | Check function duration limits in `vercel.json` or project settings. Consider increasing `maxDuration` |

**Fallback (no drains):**

If no drains are configured, the error scan relies on CLI and Dashboard:

```bash
# Stream live errors
vercel logs <deployment-url> --level error --follow

# JSON output for parsing
vercel logs <deployment-url> --level error --since 1h --json
```

> For richer post-deploy monitoring, configure drains to forward logs/traces to an external platform via Dashboard or REST API.

## Summary

<!-- Sourced from deployments-cicd skill: Deploy Summary Format -->
Present a structured deploy result block:

```
## Deploy Result
- **URL**: <deployment-url>
- **Target**: production | preview
- **Status**: READY | ERROR | BUILDING | QUEUED
- **Commit**: <short-sha>
- **Framework**: <detected-framework>
- **Build Duration**: <duration>
```

If the deployment failed, append:

```
- **Error**: <summary of failure from logs>
```

For production deploys, also include:

```
### Post-Deploy Observability
- **Error scan**: <N errors found / clean> (scanned via vercel logs --level error --since 1h)
- **Drains**: <N configured / none>
- **Monitoring**: <active / gaps identified>
```

## Next Steps

<!-- Sourced from deployments-cicd skill: Deploy Next Steps -->
Based on the deployment outcome:

- **Success (preview)** → "Visit the preview URL to verify. When ready, run `/deploy prod` to promote to production."
- **Success (production)** → "Your production site is live. Run `/status` to see the full project overview."
- **Build error** → "Check the build logs above. Common fixes: verify `build` script in package.json, check for missing env vars with `/env list`, ensure dependencies are installed."
- **Missing env vars** → "Run `/env pull` to sync environment variables locally, or `/env list` to review what's configured on Vercel."
- **Monorepo issues** → "Set the Root Directory in Project Settings to the app's folder; `vercel.json` has no `rootDirectory` key."
- **Post-deploy errors detected** → "Review errors above. Check `vercel logs <url> --level error` for details. If drains are configured, correlate with external monitoring."
- **No monitoring configured** → "Set up drains or install an error tracking integration before the next production deploy. Run `/status` for a full observability diagnostic."