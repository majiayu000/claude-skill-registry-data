---
name: release
description: Run pre-release validation and execute the release process via release.sh
user-invocable: true
argument-hint: "[version|--major|--minor|--patch]"
allowed-tools: Bash, Read, Grep, Glob
---

# Release

Run pre-release checks then cut a new bashdep release via `release.sh`.

## Arguments

- `$ARGUMENTS` - Optional. Either an explicit version (`0.5.0`) or a
  bump flag (`--major`, `--minor`, `--patch`). Default:
  `release.sh` auto-bumps the **minor** version.

## Current State

- Current version: !`grep -o 'BASHDEP_VERSION="[^"]*"' bashdep | cut -d'"' -f2`
- Branch: !`git branch --show-current`
- Working tree: !`git status --short`
- Unreleased changes: !`awk '/^## \[Unreleased\]$/,/^## \[/' CHANGELOG.md | head -40`

## Instructions

### 1. Pre-flight validation

Run `/pre-release` first, or replay the critical checks here:

```bash
make test
make sa
make lint
grep -nE 'declare -A|mapfile|\$\{[A-Za-z_][A-Za-z0-9_]*,,\}' bashdep || echo "Bash 3.2+: OK"
gh run list --limit 3 --branch main
git status --short
git branch --show-current
```

If ANY check fails, **stop and report**. Do NOT proceed to release.

### 2. Confirm with user

Show a summary:
- Current version → target version (resolved from `$ARGUMENTS`)
- Key entries from `CHANGELOG.md` `## [Unreleased]` (abbreviated)
- All checks passed

Ask the user to confirm before running `release.sh`.

### 3. Dry-run the release

Always preview first - `release.sh` is idempotent in dry-run mode:

```bash
./release.sh $ARGUMENTS --dry-run
```

Show the user the proposed:
- Version bump
- CHANGELOG diff (renamed `[Unreleased]` section + new compare links)
- Tag name

Ask for explicit confirmation before the real run.

### 4. Execute release

```bash
./release.sh $ARGUMENTS
```

`release.sh` will:
1. Validate the version is semver and greater than current
2. Confirm clean `main`, tag does not exist
3. Bump `BASHDEP_VERSION` in `bashdep`
4. Roll `CHANGELOG.md`: rename `[Unreleased]` → `[X.Y.Z] - YYYY-MM-DD`
    and refresh compare links
5. Run `make test sa lint` as a release gate
6. Commit `chore(release): X.Y.Z` and tag `X.Y.Z`
7. Push commit + tag to the remote
8. Create the GitHub release via `gh release create` and attach the
    `bashdep` script as the downloadable asset

The release URL is printed at the end.

### 5. Post-release verification

```bash
git log --oneline -1
git tag --list --sort=-v:refname | head -1
gh release view "$(git tag --list --sort=-v:refname | head -1)"
```

Verify:
- Latest commit is `chore(release): X.Y.Z`
- Latest tag matches the target version
- GitHub release page lists the `bashdep` asset

Report the release URL to the user.

## Useful flags

```
./release.sh --dry-run          # preview, no changes
./release.sh --patch            # auto-bump patch
./release.sh --major            # auto-bump major
./release.sh 0.5.0              # explicit version
./release.sh --no-gh            # skip GitHub release (still push tag)
./release.sh --force            # skip "Release X.Y.Z?" prompt (CI)
```

## Example Usage

```
/release
/release --patch
/release 0.5.0
```
