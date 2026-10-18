---
name: roblox-release-operations
description: Run Roblox release operations. Use for pre-publish checklists, smoke tests, release notes, staged rollout thinking, rollback plans, live issue response, release gates, version readiness, and post-release monitoring.
---

# Roblox Release Operations

## Goal

Ship updates with confidence and a clear recovery path.

## Pre-Release Gate

Verify:

- Core loop smoke test passes.
- Mobile layout and controls are usable.
- Save/load and valuable grants are checked.
- Purchases are server-authoritative.
- Console has no new errors.
- Performance risks are known.
- Update notes and player-facing promise match the build.

## Release Notes

Include:

- New content.
- Balance changes.
- Bug fixes.
- Known issues when necessary.
- Return hook or event deadline.

## Rollback Thinking

- Know which changes are data-schema-sensitive.
- Avoid irreversible migrations without fallback.
- Stage risky economy or persistence changes behind server flags where possible.
- Keep manual admin recovery steps for grant/data issues.

## Post-Release Watch

Track:

- Error spikes.
- Purchase/grant failures.
- Save/load failures.
- Funnel drop-offs.
- Economy inflation.
- Community reports.

## Output

Return:

- Release readiness status.
- Blocking issues.
- Smoke test plan.
- Rollback or mitigation plan.
- Post-release watchlist.

## Next

After release, watch metrics with `roblox-analytics-instrumentation` and player sentiment with `roblox-community-ops`; hand any live bug to `roblox-debugging-bugfix`.

