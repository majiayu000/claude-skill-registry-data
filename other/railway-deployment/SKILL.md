---
name: railway-deployment
description: Deep knowledge about deploying applications to Railway (PaaS, Docker, Nixpacks).
type: transform
tier: library
domain: deploy
trigger: "when deploying to Railway"
---

## Context
Deploying {{project_name}} ({{project_type}}) to Railway.
You will follow a strict 6-phase Deployment Lifecycle Contract. 

## Instructions

Execute the following phases in order:

### Phase 1: Authentication
1. Ensure the `RAILWAY_TOKEN` environment variable is set to a valid project token.
2. If running locally, authenticate interactively with `railway login`. For automated agents, ensure the token is provided.
3. Validate by running `railway status` to confirm the active project and environment.

### Phase 2: Build
1. Railway typically handles the build process remotely using Nixpacks or a Dockerfile.
2. Ensure your `railway.toml` or `Dockerfile` is correctly configured in the project root.
3. Local building is not usually required for a standard Railway deploy, but you may run local build scripts (e.g., `npm run build`) if generating static assets before pushing.

### Phase 3: Install / Provisioning
1. Ensure the target Railway project and service exist.
2. If the project isn't linked, run `railway link` (requires interactive selection or specific project ID flags).
3. If necessary, provision databases or other services via the Railway dashboard or CLI (e.g., `railway run` for migrations).

### Phase 4: Deploy
1. Ship the artifact to Railway.
2. Run `railway up --detach` to deploy the current directory to the linked project and service. The `--detach` flag prevents the CLI from tailing logs indefinitely.

### Phase 5: Checking
1. Verify the deployment was successful.
2. Run `railway status` to check if the service is deployed and running.
3. Retrieve the public URL (often via the dashboard or `railway domain`) and use `curl -sSf <URL>` to ensure the application returns a 200 OK status code.
4. If it fails, inspect logs using `railway logs`.

### Phase 6: Update / Rollback
1. If Phase 5 fails, immediately initiate a rollback.
2. Railway supports reverting to previous deployments via the dashboard or by triggering a redeploy of an older Git commit if connected to GitHub.
3. Note the failure in the progress log.

## Validation
- [ ] Railway authentication (`railway status`) succeeds.
- [ ] Remote build succeeds (indicated by a successful deploy).
- [ ] Service is up and running.
- [ ] Health check (curl) returns 200 OK.
