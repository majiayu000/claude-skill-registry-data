---
name: build-ci
description: Build scripts, CI pipelines, and versioning for the .NET 8 WPF widget host app. Use when setting up build workflows, CI checks, packaging gates, or semantic versioning rules.
---

# Build CI

## Overview

Automate builds, tests, and versioning for consistent releases.

This skill also defines “quality gates” expectations typically enforced in CI.

## Workflow

1. Define build steps (restore, build, test, pack).
2. Configure CI pipeline stages and caching.
3. Add versioning strategy (semver, git tags).
4. Publish artifacts to CI outputs.

## Definition of done (DoD)

- Local build script parity is maintained (prefer using `build.ps1` when applicable)
- CI steps are deterministic (no environment-dependent behavior)
- Minimum gates exist for relevant changes: build + nearest tests
- Packaging/signing steps are separated from compile/test steps

## Guidance

- Keep CI deterministic and fast.
- Fail on warnings for release branches.
- Store build scripts in repo for local parity.

## Quality gates (recommended)

- Restore/build/test are separate and cacheable
- Test runs are scoped (run the nearest test project(s) when possible)
- Security/quality scanning is additive (warn first, then enforce)

## References

- `references/pipelines.md` for CI flow.
- `references/versioning.md` for version rules.
- `references/build-scripts.md` for local build scripts.
