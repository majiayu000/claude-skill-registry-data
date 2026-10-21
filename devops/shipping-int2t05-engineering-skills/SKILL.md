---
name: shipping
description: Prepare and execute an authorized release with a checked recovery path. Triggers on "ship", "上线".
---

# Shipping and Launch

## When to use

- Prepare and execute an authorized release with a checked recovery path.

**Not for:** ci-cd for pipeline design; git-workflow for commits.

## Steps

1. Identify artifact, environment, authority, consumers and acceptable conditions.

2. Verify builds, tests, config and migrations; define checks, stop conditions and rollback or forward recovery.

3. Choose rollout proportional to risk and traffic, without universal canary percentages or fixed monitoring windows.

4. Execute only authorized actions and inspect real health, critical flows and telemetry; recover when conditions are violated.

**Output:** Suggested paths, subject to [human audit](../../../references/human-audit.md): `docs/launch/rollback-plan.md` when a separate recovery document is useful.

## Verify

- Platform and artifact-specific recovery is concrete; actual evidence supports release claims and unexecuted actions stay explicit.

## References

- [engineering-principles.md](../../../references/engineering-principles.md) — shared decision boundaries, scope and verification.
- [human-audit.md](../../../references/human-audit.md) — document consent, readability and human review.
- [references/launch-monitoring.md](references/launch-monitoring.md) — what to monitor at launch (application p50/p95/p99, infrastructure CPU/DB-pool/disk, client Core Web Vitals/JS errors) + ErrorBoundary and error-middleware scaffolding
- [references/changelog-and-release-notes.md](references/changelog-and-release-notes.md) — commit history → categorized changelog (keepachangelog) → user-language release notes
