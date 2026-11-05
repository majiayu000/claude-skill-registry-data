---
name: netlify-deployment
description: Deep knowledge about deploying applications to Netlify (static sites, edge functions, serverless functions).
type: transform
tier: library
domain: deploy
trigger: "when deploying to Netlify"
---

## Context
Deploying {{project_name}} ({{project_type}}) to Netlify.
You will follow a strict 6-phase Deployment Lifecycle Contract. 

## Instructions

Execute the following phases in order:

### Phase 1: Authentication
1. Ensure the `NETLIFY_AUTH_TOKEN` environment variable is set to a valid Netlify Personal Access Token.
2. If running locally, you may authenticate interactively with `npx netlify login`. However, for automated agents, ensure the token is provided.
3. Validate by running `npx netlify status`.

### Phase 2: Build
1. Prepare the artifacts for deployment.
2. Run your framework's build command (e.g., `npm run build` or `yarn build`) to generate the output directory (e.g., `dist/` or `build/`).
3. If using Netlify Functions, ensure they are compiled or placed in the designated functions directory (e.g., `netlify/functions`).

### Phase 3: Install / Provisioning
1. Ensure the target Netlify site exists.
2. Check for `netlify.toml` in the project root. This file should define build commands and publish directories.
3. Ensure the site is linked to the current directory by running `npx netlify link` or explicitly providing the `NETLIFY_SITE_ID` environment variable.

### Phase 4: Deploy
1. Ship the artifact to Netlify.
2. For a draft/preview deployment, run `npx netlify deploy --build --site $NETLIFY_SITE_ID`.
3. For a production deployment, run `npx netlify deploy --prod --build --site $NETLIFY_SITE_ID`.

### Phase 5: Checking
1. Verify the deployment was successful.
2. After a successful deploy, Netlify outputs a Draft URL or a Live URL.
3. Use `curl -sSf <URL>` to ensure the application returns a 200 OK status code. If it fails, check build logs using `npx netlify build:logs` or the dashboard.

### Phase 6: Update / Rollback
1. If Phase 5 fails, immediately initiate a rollback.
2. Netlify supports atomic deploys. You can rollback to a previous successful deploy via the Netlify dashboard or by triggering a redeploy of an older Git commit.
3. Note the failure in the progress log.

## Validation
- [ ] Netlify authentication (`netlify status`) succeeds.
- [ ] Build succeeds.
- [ ] Artifacts are deployed.
- [ ] Health check (curl) returns 200 OK.
