---
name: hotfix
description: 'Composite skill — emergency bypass of the release branch when production is broken and waiting for the next release-cut is not viable. Chains incident scoping → branch from main (NOT release) → minimal fix → pr-merge-readiness → merge to main → patch-version tag → deploy → cherry-pick to release branch → post-deploy verify (sentry + ci-watch). Use ONLY for production-impacting breakage; routine "small fix" work belongs in /pr-to-release.'
user-invocable: true
auto-invoke: '"prod is broken", "hotfix", "emergency fix", "users can''t X right now", urgency markers'
metadata:
  owner: global-agents
  tier: contextual
  canonical_source: ~/.claude/skills/hotfix
---

# Hotfix

The ONLY acceptable bypass of the `release` branch cadence. Used when:
- Production is degraded or broken
- A security vuln is being actively exploited or disclosed within 24h
- Customer-blocking bug with no viable workaround

If the work does not meet this bar, refuse and route to `/pr-to-release` instead.

## Auto-invocation triggers

- "prod is down", "users can't X", "hotfix", "emergency fix", "P0", "SEV-1/2"
- Sentry alert with new high-frequency issue post-deploy
- Manual: explicit `/hotfix` invocation

## Severity gate (always first)

Ask one clarifying question if not obvious from context:
> "Is this prod-impacting and unable to wait for the next `/release-cut`? (y/N)"

If `n` or no clear urgency: STOP and recommend `/pr-to-release`.

## Workflow

### Phase 1 — Scope (always)
- Identify exact failure mode, blast radius, and which version regressed it
- Capture evidence: Sentry issue URL, customer report, reproducer
- Decide: is a revert safer than a forward-fix? If yes, prefer revert.

### Phase 2 — Branch from main
```bash
git fetch origin
git switch main && git pull --ff-only
git switch -c hotfix/<short-slug> main
```

**Never** branch from `release`. The hotfix must rejoin `main` directly; it
will be back-merged to `release` in Phase 8.

### Phase 3 — Minimal fix
- Smallest change that solves the immediate problem
- No drive-by refactors, no unrelated cleanup, no dependency bumps
- Tests: at minimum, one regression test that fails without the fix

### Phase 4 — Open PR against main
- Base: `main` (NOT release)
- Title: `hotfix: <subject>`
- Body must include: incident link / Sentry URL, blast radius, why this can't wait
- Label: `hotfix`
- Reviewers: page on-call reviewer (do not wait for full async review)

### Phase 5 — Gate
Invoke `pr-merge-readiness`. For hotfixes the bar is:
- Required CI checks green
- At least one human approval OR explicit user override "I am the only reviewer available"
- No CHANGES_REQUESTED outstanding

Automated reviewer suggestions (CodeRabbit, Greptile) are advisory only — do not
block the merge on them during a hotfix.

### Phase 6 — Merge to main
- Method: **squash merge** for traceability
- Refuse `--admin` and `--no-verify` unless the user explicitly types the
  override phrase `BYPASS BRANCH PROTECTION` (then log the bypass in the PR comment)

### Phase 7 — Patch version + tag
- Invoke `version-bump` to bump **patch only** (e.g., 1.4.2 → 1.4.3)
- Invoke `changelog-update` to add the hotfix under a new `[X.Y.Z+1] - YYYY-MM-DD` section directly (no `[Unreleased]` involvement — this version exists outside the release-branch batch)
- Invoke `ship` in tag-only mode: tag `vX.Y.Z+1`, push, create GitHub release marked `--latest`

### Phase 8 — Deploy
Invoke `/ship-it` starting from Phase 3 (deploy) — version, changelog, tag are
already done. Watch deploy logs in real time; do not move on until the deploy
is verified live.

### Phase 9 — Post-deploy verify (always, full pass)
- Wait 60s for deploy to settle
- Hit health endpoint to confirm new version is live
- Invoke `sentry` to confirm the original issue is no longer firing
- Invoke `ci-watch` for any post-deploy smoke checks
- If a new Sentry issue appeared post-deploy: escalate to `production-incident`

### Phase 10 — Cherry-pick back to release (always)
```bash
git fetch origin
git switch release && git pull --ff-only
git cherry-pick <merge-sha-on-main>
# Resolve any conflict — release may contain unreleased work that touches the same area
git push origin release
```

If cherry-pick conflicts cannot be auto-resolved: open a follow-up PR
`chore: backport hotfix vX.Y.Z+1 to release` and surface to user. Never leave
`release` without the hotfix — the next `/release-cut` would otherwise
re-introduce the regression.

### Phase 11 — Capture (always, lightweight)
- Invoke `adr-write` only if the fix changes architectural assumptions
- Otherwise: invoke `knowledge-loop` to save a "what broke / what fixed it / how detected" note for future reference
- If the root cause is a class of bug: queue `/security-sweep` or
  `/test-cleanup` for the next session

## Stop / escalation conditions

- Fix is not actually trivial (touches >5 files or crosses module boundaries) →
  escalate to user; this is no longer a hotfix
- Cherry-pick to `release` fails and the conflict requires nontrivial work →
  surface to user
- Post-deploy verification fails (Sentry still firing the issue OR new issues
  appeared) → invoke `/production-incident`; do not declare done
- Severity gate not met → refuse and redirect to `/pr-to-release`

## Reconciliation

```
HOTFIX — <repo> v<X.Y.Z> → v<X.Y.Z+1>
  Severity:      <SEV / incident link / Sentry URL>
  Fix:           <PR # squashed at SHA>
  Tag:           vX.Y.Z+1 pushed, GitHub release published as :latest
  Deploy:        <target>, verified at <health URL>
  Sentry:        original issue cleared, no new issues post-deploy
  Backport:      cherry-picked to release@<SHA>
  Captured:      <ADR | knowledge note | none>
```

## Outputs / Evidence

- Hotfix PR # + merge SHA on `main`
- New patch tag + GitHub release URL
- Cherry-pick SHA on `release`
- Sentry before/after evidence
- Health-endpoint verification

## What this composite is NOT

- Not for routine bugs that can wait → `/pr-to-release`
- Not for new features framed as urgent → `/pr-to-release`
- Not a deploy-only workflow → use `/ship-it` directly if you don't need the version+merge flow

## Pairs with

- `/pr-to-release` — default flow; this is the exception
- `/release-cut` — the cherry-pick keeps release ready for the next batch
- `/production-incident` — escalation target if post-deploy verification fails
