---
name: vercel-deployment
description: Deep knowledge about deploying applications to Vercel (Next.js, static sites, edge functions).
type: transform
tier: library
domain: deploy
trigger: "when deploying to Vercel"
---

## Context
Deploying {{project_name}} ({{project_type}}) to Vercel.
You will follow a strict 6-phase Deployment Lifecycle Contract. 

## Instructions

Execute the following phases in order:

### Phase 1: Authentication
1. Ensure the `VERCEL_TOKEN` environment variable is set.
2. If running locally, you may authenticate interactively with `npx vercel login`. However, for automated agents, ensure the token is provided.
3. Validate by running `npx vercel whoami`.

### Phase 2: Build
1. Prepare the artifacts for deployment.
2. Typically, Vercel handles the build process on their servers based on `vercel.json` or framework detection (like Next.js).
3. If running a local preview or needing specific pre-build steps, execute your framework's build command (e.g., `npm run build`). Otherwise, this phase is implicitly handled by Vercel.

### Phase 3: Install / Provisioning
1. Ensure the target Vercel project exists.
2. If `vercel.json` is missing, you may need to configure project settings via the CLI (e.g., `npx vercel link` to link the directory to a Vercel project).
3. Set any necessary environment variables (`npx vercel env add <NAME> <ENVIRONMENT>`).

### Phase 4: Deploy
1. Ship the artifact to Vercel.
2. For a preview deployment, run `npx vercel --token $VERCEL_TOKEN`.
3. For a production deployment, run `npx vercel --prod --token $VERCEL_TOKEN`.

### Phase 5: Checking
1. Verify the deployment was successful.
2. Vercel outputs the deployment URL upon success.
3. Use `curl -sSf <URL>` to ensure the application returns a 200 OK status code.
4. Check Vercel logs (`npx vercel logs <URL>`) if the deployment fails or the health check returns an error.

### Phase 6: Update / Rollback
1. If Phase 5 fails, immediately initiate a rollback.
2. Use `npx vercel rollback <DEPLOYMENT_ID>` or revert the git commit and trigger a new Vercel deployment.
3. Note the failure in the progress log.

## Validation
- [ ] Vercel authentication (`vercel whoami`) succeeds.
- [ ] Build succeeds.
- [ ] Artifacts are deployed.
- [ ] Health check (curl) returns 200 OK.
