---
name: cloudflare-deployment
description: Deep knowledge about deploying applications to Cloudflare (Pages, Workers, Wrangler).
type: transform
tier: library
domain: deploy
trigger: "when deploying to Cloudflare"
---

## Context
Deploying {{project_name}} ({{project_type}}) to Cloudflare (Pages or Workers).
You will follow a strict 6-phase Deployment Lifecycle Contract. 

## Instructions

Execute the following phases in order:

### Phase 1: Authentication
1. Ensure the `CLOUDFLARE_API_TOKEN` environment variable is set to a valid Cloudflare API Token.
2. If running locally, you may authenticate interactively with `npx wrangler login`. However, for automated agents, ensure the token is provided.
3. Validate by running `npx wrangler whoami`.

### Phase 2: Build
1. Prepare the artifacts for deployment.
2. If Cloudflare Pages (Frontend): Run your framework's build command (e.g., `npm run build` or `yarn build`) to generate the output directory (e.g., `dist/` or `out/`).
3. If Cloudflare Workers (Backend/Edge API): Run `npm run build` if your project requires transpilation (e.g., TypeScript). Wrangler may handle this automatically if configured.

### Phase 3: Install / Provisioning
1. Ensure the target Cloudflare resources exist.
2. Check for `wrangler.toml` (for Workers) or `wrangler.json` (for modern Workers). Ensure the `name` field matches the intended project name.
3. If it's a new project, ensure the necessary Cloudflare resources (KV namespaces, D1 databases, R2 buckets) are declared and provisioned if required.

### Phase 4: Deploy
1. Ship the artifact to Cloudflare.
2. Cloudflare Pages: Run `npx wrangler pages deploy <output-directory> --project-name <PROJECT_NAME>`.
3. Cloudflare Workers: Run `npx wrangler deploy`.

### Phase 5: Checking
1. Verify the deployment was successful.
2. After a successful deploy, Wrangler outputs a URL (e.g., `https://<PROJECT_NAME>.pages.dev` or `https://<WORKER_NAME>.<SUBDOMAIN>.workers.dev`).
3. Use `curl -sSf <URL>` to ensure the application returns a 200 OK status code. If it fails, use `npx wrangler tail` to inspect logs.

### Phase 6: Update / Rollback
1. If Phase 5 fails, immediately initiate a rollback.
2. Cloudflare Workers: Rollback using `npx wrangler rollback <VERSION_ID>`. You can find versions using `npx wrangler deployments list`.
3. Cloudflare Pages: Re-deploy the previous commit hash by finding the deployment ID in the Cloudflare dashboard or checking git history and re-running the deploy command on that commit.
4. Note the failure in the progress log.

## Validation
- [ ] Cloudflare authentication (`wrangler whoami`) succeeds.
- [ ] Build succeeds.
- [ ] Artifacts are deployed.
- [ ] Health check (curl) returns 200 OK.
