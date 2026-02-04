---
name: release-npm-trustme
description: Release automation for npm-trustme. Use when asked to cut a new npm-trustme version, run the release script, or tag/publish a new release.
---

# release-npm-trustme

## Overview

Run `scripts/release.ts` to bump the version, build, tag, and push a release for npm-trustme.

## Workflow

- Open the repo: `cd ~/projects/npm-trustme`
- Ensure the working tree is clean (the script will refuse to run otherwise).
- Pick the version bump: `patch` | `minor` | `major` or a specific semver.
- Run: `pnpm tsx scripts/release.ts <bump>`
- The script builds, commits, tags, pushes, and (if `gh` is installed) creates/updates a GitHub Release.

## Examples

```
pnpm tsx scripts/release.ts patch
pnpm tsx scripts/release.ts minor
pnpm tsx scripts/release.ts 0.2.0
```

## Notes

- The script pushes to the current branch and tags; confirm the branch before running.
- Release notes use `CHANGELOG.md` if present. Set `GH_NOTES_REF` to override the changelog section.
