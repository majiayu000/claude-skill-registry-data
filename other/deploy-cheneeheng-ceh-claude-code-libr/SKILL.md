---
name: deploy
description: >-
  Load this skill when shipping a release to a running environment: building and tagging Docker
  images, promoting through staging to production, running post-deploy health and metric checks, or
  classifying a change as internal, user-visible, or breaking. Auto-load whenever a deploy pipeline
  is being run, a staging-to-production promotion is planned, or post-deploy verification is needed.
  Not for git tagging mechanics (see ceh-git-workflow/release) or incident rollback (see rollback).
compatibility: >-
  Requires a container runtime and CLI (Docker) to build and tag images, credentials for the image
  registry and the target environment, network access, and the git CLI for the release tag. None
  is assumed installed. Verification also needs an HTTP client (`curl`) to hit `/health`.
---

# Deploy Pipeline

Run after the version is tagged on `main` (see `ceh-git-workflow/release` for the tag and semver mechanics).

## Pipeline

Complete every step in order. No skipping.

1. All CI checks pass on `main`
2. `CHANGELOG.md` updated with changes since last release
3. Version tagged on `main` (semver — see `ceh-git-workflow/release`)
4. Docker images built and tagged with the version
5. Deploy to **staging** → run smoke tests
6. Staging smoke tests pass → deploy to **production**
7. Verify `GET /health` returns `200` post-deploy
8. Confirm error rate and latency metrics are at baseline within 5 minutes

**Staging must pass before production. Non-negotiable.**

## Change Classification

| Class        | Definition                                              | Additional requirement                                            |
| ------------ | ------------------------------------------------------- | ----------------------------------------------------------------- |
| Internal     | No user-visible or API change                           | None                                                              |
| User-visible | UI change, new feature, behavioral change               | PR description required                                           |
| Breaking     | API contract change, schema migration, removed endpoint | ARCHITECTURE.md Key Decisions entry + migration plan before merge |
