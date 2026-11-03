---
name: deploy
description: Production deployment workflow with preflight checks, release execution, smoke tests, and rollback discipline. Use when you need to ship safely and verify the target environment still works.
origin: Betopia
slash: /deploy
order: 30
---

# Deploy

Ship safely with a strict preflight and post-deploy verification loop.

## When to Activate

- Preparing a production release
- Verifying a release candidate
- User says "deploy", "ship", or "release"

## Inputs to Collect

- Target environment or deployment URL
- Project-specific build and deploy commands
- Any required env vars, secrets, or migration steps
- Scope of the release that is supposed to go out

## Workflow

### 1. Build first

- Run the project build
- Stop immediately if the build fails
- Do not proceed with a broken build

### 2. Test the release

- Run the relevant test suite
- Stop on any failing test
- Prefer the narrowest test set that still proves the change

### 3. Check environment and migrations

- Confirm required env vars and secrets exist
- Check whether migrations are needed
- Run migrations in the correct order if the project requires them

### 4. Review the release scope

- Review the final diff of what is actually being deployed
- Confirm the release matches the intended change
- Do not ship unrelated edits by accident

### 5. Deploy

- Execute the deploy command
- Watch logs for runtime, infra, or config errors
- Keep the deployment state explicit if the result is uncertain

### 6. Smoke test

- Hit the critical pages or endpoints after deploy
- Confirm the app works in the target environment
- Use the smallest set of checks that proves the release is healthy

### 7. Roll back if needed

- If verification fails, stop immediately
- Revert or roll back before retrying
- Investigate the failure before starting a second deploy

## Quality Rules

- Never ship with a failing build or test suite
- Never skip the smoke test
- Never hide an uncertain deploy state
- Prefer the smallest safe release window

## Examples

- "deploy this to production"
- "ship the release candidate after tests pass"
- "smoke test the staging deploy"

## Output Standard

Report:

- deploy command used
- target environment or deployment URL
- build/test status
- smoke test result
- rollback status if anything failed
