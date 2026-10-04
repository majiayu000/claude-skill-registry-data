---
name: release-ops-demo-release-automation
description: Use when running release automation workflows for release-ops-demo.
---

# release-ops-demo-release-automation

Generated from `skillpack.yaml` by Skillpack Forge.

## Project
Release automation workflows for changelogs, tags, packages, and CI checks.

## Workflow
- Inspect git status, recent commits, package metadata, and release history
- Run tests and package dry-run checks
- Prepare release notes from concrete changes
- Publish only after verifying the target registry or GitHub release state

## Commands
- install: `npm install`
- test: `npm test`
- build: `npm run build`
- release: `npm run release`
- check: `npm run check`

## Principles
- Verify a clean worktree and passing checks before release steps
- Keep version, tag, package, and release notes aligned
- Treat publish credentials and tokens as sensitive
