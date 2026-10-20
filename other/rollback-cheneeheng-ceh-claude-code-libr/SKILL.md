---
name: rollback
description: >-
  Load this skill when deciding whether to roll back a deployment, executing an application
  rollback, or planning recovery from a failed migration. Auto-load whenever a deployment fails its
  health check, error rates spike post-deploy, P95 latency triples within 10 minutes of a release,
  or any data integrity issue is detected after deploying. Not for forward-fix deploys (see deploy).
compatibility: >-
  Requires access to the deploy environment and its CLI, plus the previously published container
  image still present in the registry - a rollback cannot rebuild it. An HTTP client (`curl`) is
  needed to verify `/health`. None of these is assumed installed.
---

# Rollback

## When to Roll Back

Roll back **immediately** (before root cause analysis) when any occur within 10 minutes of deploy:

- `GET /health` returns anything other than `200`
- Error rate > 5× the pre-deploy baseline
- P95 latency > 3× the pre-deploy baseline
- Any data integrity issue detected

## Application Rollback Procedure

1. Re-deploy the previous Docker image tag
2. Verify `GET /health` returns `200`
3. Confirm error rate and latency return to baseline within 2 minutes
4. Open a P1/P2 incident if production was impacted
5. Document the rollback in the Decision Log (default `.agents_workspace/DECISION_LOG.md`, overridable per project)

## Database Rollback Considerations

- **Additive migrations** (new columns, new tables): roll back the application; leave the schema change. The old application ignores unknown columns.
- **Destructive migrations** (drops, renames): cannot be automatically rolled back. This is why the two-step process is mandatory. If a destructive migration was applied prematurely, a forward-fix is required — not a rollback.
