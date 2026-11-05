---
name: coolify-deployment
description: Deep knowledge about deploying applications to Coolify (self-hosted PaaS).
type: transform
tier: library
domain: deploy
trigger: "when deploying to Coolify"
---

## Context
Deploying {{project_name}} ({{project_type}}) to Coolify.
You will follow a strict 6-phase Deployment Lifecycle Contract. 

## Instructions

Execute the following phases in order:

### Phase 1: Authentication
1. Coolify is often triggered via a webhook or Git integration rather than a CLI tool.
2. If deploying manually, ensure you have the `COOLIFY_API_TOKEN` (or webhook secret) available in your environment variables.
3. If using an SSH-based CLI script for Coolify, ensure your SSH keys (`~/.ssh/id_rsa`) are configured and authorized on the Coolify server.

### Phase 2: Build
1. Prepare the artifacts for deployment. Coolify typically relies on Nixpacks, buildpacks, or a `Dockerfile` in the repository root.
2. If using a `Dockerfile`, ensure it successfully builds locally (`docker build .`) to verify correctness before pushing.
3. If generating static assets before pushing, run your framework's build command (e.g., `npm run build`).

### Phase 3: Install / Provisioning
1. Ensure the target Coolify application exists on the Coolify dashboard.
2. Ensure the webhook URL provided by Coolify is correctly configured in your Git repository (GitHub/GitLab/Bitbucket) or available for the agent to trigger.
3. Ensure any necessary databases (PostgreSQL, Redis, etc.) are provisioned and linked to your application in Coolify.

### Phase 4: Deploy
1. Ship the artifact to Coolify.
2. If integrated with Git, a `git push origin main` or a pull request merge will automatically trigger a deployment.
3. If deploying manually via a webhook, trigger it using `curl -X POST <COOLIFY_WEBHOOK_URL>`.
4. If Coolify provides an API endpoint for deployment, use it with the required authentication token.

### Phase 5: Checking
1. Verify the deployment was successful.
2. Check the Coolify dashboard for the deployment status. If available, retrieve the deployment logs via the Coolify API.
3. Retrieve the public URL assigned by Coolify and use `curl -sSf <URL>` to ensure the application returns a 200 OK status code.

### Phase 6: Update / Rollback
1. If Phase 5 fails, immediately initiate a rollback.
2. Coolify supports reverting to previous deployments via its dashboard or by pushing a revert commit to the connected Git branch.
3. Note the failure in the progress log.

## Validation
- [ ] Coolify webhook or API authentication is successful.
- [ ] Build (remote via Coolify) succeeds.
- [ ] Service is up and running on the assigned domain.
- [ ] Health check (curl) returns 200 OK.
