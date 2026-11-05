---
name: fly-deployment
description: Deep knowledge about deploying applications to Fly.io (MicroVMs, Docker).
type: transform
tier: library
domain: deploy
trigger: "when deploying to Fly.io"
---

## Context
Deploying {{project_name}} ({{project_type}}) to Fly.io.
You will follow a strict 6-phase Deployment Lifecycle Contract. 

## Instructions

Execute the following phases in order:

### Phase 1: Authentication
1. Ensure the `FLY_API_TOKEN` environment variable is set to a valid token.
2. If running locally, authenticate interactively with `fly auth login`. For automated agents, ensure the token is provided.
3. Validate by running `fly auth whoami`.

### Phase 2: Build
1. Prepare the artifacts for deployment.
2. Fly.io uses a `fly.toml` configuration file and a `Dockerfile` (or buildpacks) to build your application on their builders.
3. Ensure the `Dockerfile` builds successfully locally (`docker build .`) to catch any errors early.
4. If your project requires generating static assets before pushing, run your framework's build command (e.g., `npm run build`).

### Phase 3: Install / Provisioning
1. Ensure the target Fly.io application exists. If not, initialize it using `fly launch --no-deploy`.
2. Check the `fly.toml` file to ensure the application name, regions, and environment variables are correctly configured.
3. Ensure required secrets are set using `fly secrets set KEY=value`.
4. If your application requires a database (Postgres, Redis), ensure it's provisioned via `fly postgres create` or `fly redis create` and attached to the app.

### Phase 4: Deploy
1. Ship the artifact to Fly.io.
2. Run `fly deploy` to build and deploy your application. You can append `--remote-only` to force the build on Fly's remote builders.
3. Use `--detach` if you do not want to wait for health checks to pass in the foreground (not recommended for automated agents unless monitoring separately).

### Phase 5: Checking
1. Verify the deployment was successful.
2. Run `fly status` to check the application's instances and their health status.
3. Retrieve the public URL using `fly info` and use `curl -sSf <URL>` to ensure the application returns a 200 OK status code.
4. Check logs via `fly logs` if the deployment fails or instances are crashing.

### Phase 6: Update / Rollback
1. If Phase 5 fails, immediately initiate a rollback.
2. Fly.io supports rolling back to previous deployments. Identify the previous image or release version and run `fly deploy -i <previous-image-ref>`.
3. Note the failure in the progress log.

## Validation
- [ ] Fly.io authentication (`fly auth whoami`) succeeds.
- [ ] Build succeeds (locally or remote).
- [ ] Application instances are running (`fly status`).
- [ ] Health check (curl) returns 200 OK.
