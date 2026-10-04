---
name: upgrade-packages
description: Upgrade all dependencies/packages to their latest versions for the detected language(s). Use when the user says "upgrade packages", "update dependencies", "bump versions", "update packages", or "upgrade deps".
argument-hint: "[--check-only] [--major] [package-name]"
---
<!-- agent-pmo:795a9c2 -->

# Upgrade Packages

Upgrade all project dependencies to their latest compatible (or latest major, if `--major`) versions.

## Arguments

- `--check-only` — List outdated packages without upgrading. Stop after Step 2.
- `--major` — Include major version bumps (breaking changes). Without this flag, stay within semver-compatible ranges.
- Any other argument is treated as a specific package name to upgrade (instead of all packages).

## Step 1 — Detect language and package manager

Inspect the repo root and subdirectories for manifest files. Identify ALL that apply:

| Manifest file | Language | Package manager |
|---|---|---|
| `package.json` | Node.js / TypeScript | npm (lockfile is `package-lock.json`) |
| `pubspec.yaml` | Dart | pub |

This repo has multiple `package.json` files — one in `too-many-cooks/` (MCP server monorepo with `packages/core` + `packages/too-many-cooks`), one in `too_many_cooks_vscode_extension/` (VS Code extension), and one in `website/` (Eleventy site) — plus `codegen/pubspec.yaml` (Dart toolkit). Process each manifest independently. Note the monorepo under `too-many-cooks/` uses npm workspaces, so run npm commands from `too-many-cooks/`.

**If you cannot detect any manifest file, stop and tell the user.**

## Step 2 — List outdated packages

Run the appropriate command to list what's outdated BEFORE upgrading anything. Show the user what will change.

### Node.js (npm)
```bash
cd too-many-cooks && npm outdated
cd too_many_cooks_vscode_extension && npm outdated
cd website && npm outdated
```

**Read the docs:** https://docs.npmjs.com/cli/v10/commands/npm-update

### Dart
```bash
cd codegen && dart pub outdated
```
**Read the docs:** https://dart.dev/tools/pub/cmd/pub-outdated

If `--check-only` was passed, **stop here** and report the outdated list.

## Step 3 — Read the official upgrade docs

**Before running any upgrade command, you MUST fetch and read the official documentation URL listed above for the detected package manager.** Use WebFetch to retrieve the page. This ensures you use the correct flags and understand the behavior. Do not guess at flags or options from memory.

## Step 4 — Upgrade packages

Run the upgrade. If a specific package name was given as an argument, upgrade only that package.

### Node.js (npm)
```bash
npm update                            # semver-compatible (within package.json ranges)
# --major flag:
npx npm-check-updates -u && npm install   # bump package.json to latest majors
```

### Dart
```bash
dart pub upgrade                      # semver-compatible
# --major flag:
dart pub upgrade --major-versions     # bump to latest majors
```

## Step 5 — Verify the upgrade

After upgrading, run the project's build and test suite to confirm nothing broke:

```bash
make ci
```

If `make ci` is not available, run whatever build/test commands the project uses (check the Makefile, CI workflow, or CLAUDE.md).

If tests fail:
1. Read the failure output carefully
2. Check the changelog / migration guide for the upgraded packages (fetch the release notes URL if available)
3. Fix breaking changes in the code
4. Re-run tests
5. If stuck after 3 attempts on the same failure, report it to the user with the error details and the package that caused it

## Step 6 — Report

Provide a summary:

- Packages upgraded (old version -> new version)
- Packages skipped (and why, e.g., major version bump without `--major` flag)
- Build/test result after upgrade
- Any breaking changes that were fixed
- Any packages that could not be upgraded (with error details)

## Rules

- **Always list outdated packages first** before upgrading anything
- **Always read the official docs** for the package manager before running upgrade commands
- **Always run tests after upgrading** to catch breakage immediately
- **Never remove packages** unless they were explicitly deprecated and replaced
- **Never downgrade packages** unless rolling back a broken upgrade
- **Never modify lockfiles manually** (`package-lock.json`, `pubspec.lock`) — let the package manager regenerate them
- **Commit nothing** — leave changes in the working tree for the user to review

## Success criteria

- All outdated packages upgraded to latest compatible (or latest major if `--major`)
- Build passes
- Tests pass
- User has a clear summary of what changed
