---
name: git-release
description: "Cut releases safely: semver, tags, changelogs, staged rollouts, rollback, monitoring. Faster is safer only with gates."
---

# git-release

A release is a verified artifact plus a way back.
## Inspection

Confirm what's shipping (diff since last tag), migration/compat notes, rollout plan, monitors, and who is on call.

## Decision rules

Semver from change content; annotated tags; changelog + migration guide for breaking changes; staged rollout with halt criteria; rollback artifact ready.


## Activate when

- Tagging, versioning, changelogging, rolling out, or rolling back a release.

## Do NOT activate for

- CI config (devops/github-actions) or routine PRs (git-workflow).

## Procedure

1. Version: semver bump from change content (breaking → major); tag annotated (`git tag -a`), pushed explicitly.
2. Notes: changelog entry (features, fixes, migrations, deprecations); migration guide for breaking changes.
3. Gates: required checks green, staged rollout (canary → percentage → full) with health/error-budget watches.
4. Rollback: artifact from the previous release deployable in one step; rollback drill before you need it.
5. Tool gates: IF hosting CLI exists use it for release creation; ELSE use the UI. Monitor via project observability (see architecture/observability).
6. Verify: installed artifact smoke-tested, notes published, monitors quiet, rollback path confirmed available.

## Failure modes

Floating tags moved silently; breaking change without migration notes; big-bang rollout without canary; rollback never drilled.

## Escalation

CI mechanics → devops/github-actions; deploy health → backend/production-readiness.
