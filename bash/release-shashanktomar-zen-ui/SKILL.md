---
name: release
description: Create a new zen-ui release with proper version bump, build, tag, and GitHub release with HACS-compatible asset. Use when the user says "make a release", "cut a release", "bump version", "publish a new version", "release X.Y.Z", or anything about releasing/publishing zen-ui.
---

# Release

Create a release using the justfile recipes. The release script handles: version bump in package.json, lint/format/test checks, build, git commit + tag, push, and GitHub release creation with the built `zen-ui.js` asset (required for HACS installs).

## Workflow

### Step 1: Determine the version

If the user provided a version (e.g., "release 1.3.0"), use it.

If not, check the current version and recent changes to suggest one:

```bash
just version
git log --oneline $(git describe --tags --abbrev=0)..HEAD
```

Based on commits since last tag, suggest a version following semver:
- **patch** (1.2.x): bug fixes only
- **minor** (1.x.0): new features, backwards compatible
- **major** (x.0.0): breaking changes

Ask the user to confirm the version before proceeding.

### Step 2: Verify clean state

```bash
git status --short
```

If there are uncommitted changes, warn the user and ask whether to proceed or stash first. The release script commits only `package.json`, so other changes won't be included in the release commit but could cause confusion.

### Step 3: Run the release

```bash
just release <version>
```

This runs `scripts/release.sh` which does everything: version bump, checks, build, commit, tag, push, and `gh release create` with `dist/zen-ui.js` attached.

### Step 4: Verify

After the release completes, confirm success:

```bash
gh release view v<version> --json tagName,assets --jq '{tag: .tagName, assets: [.assets[].name]}'
```

Verify that `zen-ui.js` appears in the assets list — this is critical for HACS installs. If the asset is missing, notify the user immediately. Do not attempt to fix it automatically.
