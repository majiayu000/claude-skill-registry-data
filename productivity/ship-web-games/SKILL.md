---
name: ship-web-games
description: Prepare web games for release through source verification, builds, gameplay QA, asset and configuration checks, approval gates, production proof, and rollback planning. Use when a browser game or major gameplay update is ready for release review.
engines: [AGNOSTIC]
---

# Ship Web Games

## When to use

- Preparing a web-game release candidate.
- Validating that a gameplay or content update is deployable.
- Collecting review evidence before a PR or production action.

## Workflow

1. Define the release scope, version policy, target environment, player-visible changes, dependencies, and rollback boundary.
2. Run targeted gameplay tests, full tests, build, lint, asset checks, configuration validation, and performance gates.
3. Verify licenses, source-to-runtime asset integrity, routes, caching, save compatibility, observability, and failure handling.
4. Generate PR-readiness evidence and follow the applicable Hephaera mode gate before pushing or opening a PR. Normal task and Gauntlet promotion PRs stop for human approval; explicit Goal tasks and approved Gauntlet progress PRs use their scoped automatic-publication records.
5. Deploy only when separately authorized through the repository's normal workflow.
6. After a confirmed deployment, verify the production route, version, core loop, console health, and rollback signal.

## Output

- A release-readiness summary with pass or fail status.
- Validation commands, evidence paths, configuration and migration notes.
- Deployment and rollback checks with residual risk.

## Guardrails

- Do not commit, push, open a PR, deploy, or publish without the applicable Hephaera gate.
- Do not describe a local build as production proof.
- Do not release with unknown save compatibility or unverified required assets.
