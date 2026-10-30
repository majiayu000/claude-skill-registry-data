---
name: vercel-deploy
description: >-
  Deploy applications and websites to Vercel. Use when the user requests deployment actions like "deploy my app", "deploy and give me the link", "push this live", or "create a preview deployment".
---
# Vercel Deploy

Deploy any project to Vercel instantly. **Always deploy as preview** (not production) unless the user explicitly asks for production.

## Prerequisites

- Check whether the Vercel CLI is installed **without** escalated permissions (for example, `command -v vercel`).
- Only escalate the actual deploy command if sandboxing blocks the deployment network calls (`sandbox_permissions=require_escalated`).
- The deployment might take a few minutes. Use appropriate timeout values.

## Quick Start

1. Check whether the Vercel CLI is installed (no escalation for this check):

```bash
command -v vercel
```

2. If `vercel` is installed, run this (with a 10 minute timeout):
```bash
vercel deploy [path] -y
```

**Important:** Use a 10 minute (600000ms) timeout for the deploy command since builds can take a while.

3. If `vercel` is not installed, or if the CLI fails with "No existing credentials found", use the fallback method below.

## Fallback (No Auth)

The fallback script is also an external deployment action, not a no-auth verification path. Use it only after explicit authorization; if CLI auth fails during audit, record `unverified` and do not deploy:

```bash
skill_dir="<path-to-skill>"

# Deploy current directory
bash "$skill_dir/scripts/deploy.sh"

# Deploy specific project
bash "$skill_dir/scripts/deploy.sh" /path/to/project

# Deploy existing tarball
bash "$skill_dir/scripts/deploy.sh" /path/to/project.tgz
```

The script handles framework detection, packaging, and deployment. It waits for the build to complete and returns JSON with `previewUrl` and `claimUrl`. These outputs are only available after an authorized external deployment.

**Do not claim deployment readiness from the script path or configuration alone.**

## Production Deploys

Only if user explicitly asks:
```bash
vercel deploy [path] --prod -y
```

## Output

Show the user the deployment URL. For fallback deployments, also show the claim URL.

**Do not** curl or fetch the deployed URL to verify it works. Just return the link.

## Troubleshooting

### Escalated Network Access

If deployment fails due to network issues (timeouts, DNS errors, connection resets), record the failure as `unverified` and stop before retrying. A retry or escalation requires separate explicit authorization; it does not prove deployment or service health.

Example guidance to the user:

```
The deploy needs escalated network access to deploy to Vercel. I can rerun the command with escalated permissions—want me to proceed?
```
