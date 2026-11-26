---
name: deploy-without-fear
description: Check everything before and after a production deploy, with a rollback plan and clear rollback triggers. Use when the user is about to deploy or just deployed, or says "is it safe to deploy", "pre-deploy check", "post-deploy check" or "we're going to prod". Not for committing, opening PRs or app store releases.
---

# Deploy without fear

The code is merged; this is about getting it live safely. Check each item yourself where you can (CI, configs, endpoints, logs) and ask the user only for what you can't see.

## Before
- CI is green on exactly the commit or tag being deployed.
- Every env var and secret the new code reads exists in the target environment.
- Migrations: reviewed, tried on staging, and any that can't be undone named out loud.
- Rollback plan written down: what to revert, how, and how long it takes. If a migration can't be undone, the plan says what happens to data.
- Feature flags set for this release.
- Anyone downstream told if an API, event or schema they use changed.
- Not at peak traffic, and someone is around for the next hour. Avoid Friday evenings unless it's a fix.

If anything here fails, say so and stop. Don't deploy around it.

## During
Watch the deploy logs live. Unexpected errors at startup mean stop and roll back, not wait.

## After
- Health check returns 200.
- Smoke test the flows that make money or that users hit first, for real.
- Error rate, latency and slow queries normal against the hour before.
- No new alerts.
- Release notes out and tickets closed.

## Roll back now if
- Errors rise above 1% of requests.
- p95 latency more than doubles.
- Any sign of wrong or lost data.
- A main flow returns 5xx.

Finish with one line: deployed what, when, healthy or rolled back, and anything left to watch.
