---
name: deploy-checklist
description: >-
  Pre-deploy and release checklist with rollback planning. Use when deploying,
  releasing, shipping, or preparing a pre-deploy review. Do not use for coding
  the feature itself or for live incident command (use incident-response).
---

# Deploy Checklist

Ship safely: verified build, observable release, reversible plan.

## Workflow

1. **Pre-flight** — complete `references/preflight.md` (quality, security, config, docs). If the release changes any externally consumed surface, confirm the `contract-guard` compatibility statement exists; for versioned releases, notes and version bump per the `release` skill.
2. **Rollback plan** — write it *before* deploy (flag kill-switch, previous artifact, migration reverse).
3. **Deploy** — prefer staged rollout (staging → canary/partial → full) when available.
4. **Watch** — first-hour checks: health, error rate, latency, one critical user flow.
5. **Decide** — advance, hold, or roll back using explicit thresholds.
6. **Close out** — changelog/notes; remove temporary flags when safe; file follow-ups.

## Constraints

- No production deploy without a stated rollback path.
- Do not treat “works on my machine / staging” as sufficient without post-deploy verification.
- Migrations: know whether they are backward-compatible with the currently running app.

## Verification

- [ ] Preflight checklist green or exceptions documented
- [ ] Rollback plan written
- [ ] Post-deploy health + critical flow verified
- [ ] Go/hold/rollback decision recorded
