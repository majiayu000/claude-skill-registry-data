---
name: dependency-upgrade-demo-dependency-upgrade
description: Use when running dependency upgrade workflows for dependency-upgrade-demo.
---

# dependency-upgrade-demo-dependency-upgrade

Generated from `skillpack.yaml` by Skillpack Forge.

## Project
Dependency upgrade workflows for reviewing outdated packages, applying safe updates, and verifying compatibility.

## Workflow
- Inspect package manifests, lockfiles, current dependency versions, and available update commands
- Run the narrowest outdated or audit command first, such as npm outdated or npm audit
- Apply patch and minor updates before considering major-version changes
- Review changelog notes, migration guides, and generated lockfile diffs for risky packages
- Run focused verification, then the broader relevant suite, and document any pinned or deferred upgrades

## Commands
- install: `npm install`
- test: `npm test`
- outdated: `npm run outdated`
- deps:check: `npm run deps:check`
- deps:update: `npm run deps:update`
- deps:audit: `npm run deps:audit`

## Principles
- Review changelogs, release notes, and lockfile changes before broad upgrades
- Prefer one dependency group at a time so regressions stay attributable
- Run audit, focused tests, and the relevant full suite before reporting success
- Document skipped major versions, risky transitive changes, and follow-up work
