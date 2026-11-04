---
name: release-changelog
description: Write LocalPilot changelog entries and prepare a release (version bump, CHANGELOG promotion, VSIX check). USE WHEN a user-visible change is finished and needs a CHANGELOG.md entry, or when asked to release, bump the version, or package the extension.
---

# Changelog and releases

## Changelog entries

Every user-visible change gets an entry under `## Unreleased` in `CHANGELOG.md` ([Keep a Changelog](https://keepachangelog.com/) style). Use the `### Added`, `### Changed` or `### Fixed` subheadings and create one only if it isn't there yet.

Style (match the existing entries):
- Start with a **bold one-line summary** that a user would recognise, then explain in plain sentences what changed and why it matters to them.
- Name the command (**LocalPilot: Do X**) or setting (`localpilot.x.y`) and its default, so users can find it.
- Describe behaviour, not implementation: "The queue resumes after a reload", not "TaskQueue.load() resets running tasks".
- For fixes, describe the symptom the user saw, then what happens now.
- No internal refactors, test-only changes or file lists.

## Releasing

Releases are usually automatic: the Release workflow bumps the version on pushes to `main` with releasable commits (`scripts/auto-bump.js`). To choose a version yourself:

```bash
npm run release -- patch --dry-run   # print the plan, change nothing
npm run release -- minor             # or patch | major | 1.2.3; --no-push to commit only
```

The script updates `package.json`, `package-lock.json` and `docs/_config.yml`. It promotes `## Unreleased` to `## X.Y.Z — date`, generating entries from conventional commits if the section is empty. It runs `check:version`, compile, smoke and VSIX packaging, then commits `release: vX.Y.Z` and pushes. CI tags, builds and publishes to the Marketplace and Open VSX.

**Pushing publishes the extension.** Run `--dry-run` and confirm with the user before any real release, and never push without being asked.

To build the VSIX locally without releasing:

```bash
npx @vscode/vsce package --no-dependencies --readme-path MARKETPLACE.md
```

`npm run check:version` reports a mismatch between `package.json`, the lockfile, `docs/_config.yml` and the CHANGELOG heading. Fix the files, not the check.
