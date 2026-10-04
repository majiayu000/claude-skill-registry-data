---
name: ship-it
description: Composite skill — take a merged PR all the way to production. Chains version-bump → changelog-update → ship (tag + release) → deployment-automation or vercel-deploy / cloudflare-deploy / prod-rebuild → post-deploy verify (sentry + ci-watch). Distinct from merge-confidently which stops at merge; this one ends with "live in prod, verified, no incidents."
triggers:
  - ship-it
  - post-merge-deployment
  - release-cut-requests
  - composite skill
  - ship
  - deploy
  - release
  - incident
---

# Ship It

Replaces "merged the PR, now what?" with one workflow that gets the change live and
verified. Pairs with `merge-confidently` (which ends at merge) — `ship-it` starts
where that ends.

## Auto-invocation triggers

- User says "ship to prod", "release this", "deploy to production", "cut a release"
- After `merge-confidently` returns successful merge if release/deploy is implied
- Scheduled releases (weekly/biweekly cadence)

## Workflow

### Phase 1 — Version + changelog (always)
- Invoke `version-bump` to determine semver bump (patch/minor/major from commit history)
- Invoke `changelog-update` to promote `[Unreleased]` to a versioned section
- Commit version + changelog, push to main

### Phase 2 — Tag + GitHub release (always)
- Invoke `ship` to:
  - Create the version tag
  - Cut a GitHub release with changelog excerpt
  - Verify the tag pushed cleanly

### Phase 3 — Deploy (always — pick the right deployer)
Detect deployment target from project:
- Vercel (`vercel.json`, Next.js): invoke `vercel-deploy`
- Cloudflare Workers/Pages (`wrangler.toml`): invoke `cloudflare-deploy`
- Docker on remote server: invoke `prod-rebuild`
- Generic CI/CD: invoke `deployment-automation`
- Multi-repo coordinated: invoke `chain-release`

### Phase 4 — Post-deploy verify (always)
- Wait 60s for deploy to settle
- Invoke `sentry` to check for new issue events post-deploy
- Invoke `ci-watch` to verify any post-deploy smoke checks passed
- Hit a health endpoint if known (curl `/health`, `/version` to confirm new version is live)

If Sentry shows any new issue with frequency >0 in the post-deploy window, escalate
to `production-incident` composite.

### Phase 5 — Capture (conditional)
- If release contains breaking changes: invoke `adr-write` to record migration notes
- If release is significant (minor/major): invoke `knowledge-loop` to save the
  shipping summary for future reference

## Reconciliation

```
SHIP IT — <repo> v<old> → v<new>
  Version:     <bump type>, commits since last tag: N
  Changelog:   M entries promoted from Unreleased
  Tag:         v<new> pushed
  Deploy:      <target>, took Xs
  Verify:      sentry clean, /health ok, version endpoint shows v<new>
  Captured:    ADR-NNNN (if breaking)
```

## Outputs / Evidence

- New version + tag
- Changelog entries published
- Deploy target + URL
- Post-deploy verification proof (Sentry clean, health endpoint live)
- ADR if applicable

## Failure / Stop Conditions

- Phase 1 reveals uncommitted changes → stop, commit first
- Phase 2 fails (tag conflict) → stop, investigate
- Phase 3 deploy fails → stop, surface error, do NOT auto-rollback (that's
  `production-incident` territory)
- Phase 4 finds new Sentry issues → STOP, escalate to `production-incident`
- Never use `--force-with-lease` or `--admin` to push past gates

## Memory Hooks

- Read deployment history per-repo to detect cadence patterns (e.g., "Lucky ships
  Tuesdays")
- Write release outcome to memory for trend tracking (deploy time, issue count
  post-deploy, rollback rate)
