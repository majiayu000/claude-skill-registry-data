---
name: release-readiness
description: Use before tagging, publishing, or promoting PubTator-Link builds.
---

# Release Readiness

Follow `AGENTS.md` first.

## Workflow

1. Confirm the worktree only contains intended release changes.
2. Run `make ci-local`, then any `docker-*-config` validation targets the Makefile exposes.
3. Build the release image with the same Dockerfile used in CI.
4. Confirm container scan and SBOM artifacts are generated; current policy is advisory unless the release checklist says otherwise.
5. Check README, changelog, MCP safety language, and deployment docs for user-visible drift.
6. Record residual risks and any deferred release controls before handoff.
