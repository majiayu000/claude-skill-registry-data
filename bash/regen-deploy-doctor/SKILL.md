---
name: regen-deploy-doctor
description: Diagnose Railway deploy failures for regencivics.earth, especially FAILED deploys where the CLI shows no logs. Use whenever a deploy lands FAILED or CRASHED, when railway logs come back empty, when a build dies in under 30 seconds, or when two sessions pushed at nearly the same time.
---

# ReGen Deploy Doctor

Mined 2026-07-17 from repeated diagnosis sessions (viem/pkg.pr.new incident 2026-07-15, concurrent-push double failures). Hours were lost polling a CLI that will never show the reason. This is the checklist.

## Always first

```bash
railway status
```

If it prints anything other than `Service: ReGenCivics.Earth`, re-link with `railway service "ReGenCivics.Earth"`. Every other command needs the `-s "ReGenCivics.Earth"` pin (the `pnpm railway:*` scripts already carry it).

## Failure triage

**1. FAILED with empty CLI logs.** `railway logs --build` only returns the latest COMPLETED build, and `railway logs -d <id>` shows nothing for a build-stage failure. Do not keep polling. Go straight to the dashboard deployment card via Claude in Chrome:

```
https://railway.com/project/1b47f872-03c6-4c22-9ab7-a42c81d11e51/service/f99fd8fb-acf9-4a8f-97de-20514d1669f8?environmentId=517c3df8-e298-4c1b-8e8b-6a4ec1c738c0
```

The error text renders inline on the FAILED card.

**2. Instant failure (under ~30s, no logs).** Historically this is `pnpm install` dying, not code. Grep the lockfile for ephemeral tarball URLs first:

```bash
rg 'pkg\.pr\.new|tarball' pnpm-lock.yaml
```

2026-07-15 precedent: viem 2.51.0 depended on `ox` via a pkg.pr.new preview tarball that expired; every uncached build died with ERR_PNPM_FETCH_404. Fix was `pnpm update viem`.

**3. Two deployments seconds apart, both red.** Concurrent sessions pushed retrigger commits simultaneously. Before retriggering anything:

```bash
git fetch && git log origin/main --oneline -5
```

Retrigger once, from one session.

**4. Build green locally, red on Railway (or the reverse).** Local `pnpm build` failing on a workbox `maximumFileSizeToCacheInBytes` error over PNGs in `client/public/core/raw/` is local-only; those assets are gitignored and Railway never sees them.

## After the fix

Push, then poll `pnpm railway:deploys` until the newest deployment reaches SUCCESS. Report commit, deploy status, and root cause. If the incident was security-relevant, append to `.ai/docs/security/OPS-PLAYBOOK.md`.
