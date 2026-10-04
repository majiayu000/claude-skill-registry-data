---
name: release-acceptance
description: Use for release, deployment, migration, or production acceptance; distinguish deploy success from user-visible production success and require exact revision, smoke, observability, rollback, and dependency evidence.
---
# Release / Production Acceptance

1. Run workspace hygiene, identify a clean candidate revision, migrations, feature flags, dependencies, and rollback/recovery path.
2. Run required CI/build/security/data checks on the candidate revision.
3. Deploy only through approved mechanisms.
4. Confirm the deployed revision, not merely that the deployment command returned success.
5. Run production/staging smoke on the real URL and the separate critical user flow.
6. Inspect health, errors, logs/metrics, auth/private boundary, and critical external dependencies.
7. Close verified candidate evidence with `.ai/scripts/close_task.py`; reject any later product-source drift.
8. Record both `production-smoke` and `production-critical-flow` evidence for release tasks.
9. Verify the exact deployed revision marker. Make post-closure revision probes ephemeral to avoid a commit/deploy loop.
10. Run `.ai/scripts/accept_release.py` only after both production checks are fresh for the deployed closure revision.
11. Do not say `production accepted` when only `deployed` is known.
