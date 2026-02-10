---
name: plot-release
description: >-
  Create a versioned release from delivered plans.
  Part of the Plot workflow. Use on /plot-release.
globs: []
license: MIT
metadata:
  author: eins78
  repo: https://github.com/eins78/skills
  version: 1.0.0-beta.1
compatibility: Designed for Claude Code and Cursor. Requires git and gh CLI.
---

# Plot: Cut a Release

Create a versioned release from delivered plans.

**Input:** `$ARGUMENTS` is optional. Can be a version number (e.g., `1.2.0`) or a bump type (`major`, `minor`, `patch`).

Example: `/plot-release minor`

## Setup

Add a `## Plot Config` section to the adopting project's `CLAUDE.md`:

    ## Plot Config
    - **Project board:** <your-project-name> (#<number>)  <!-- optional, for `gh pr edit --add-project` -->
    - **Branch prefixes:** idea/, feature/, bug/, docs/, infra/
    - **Plan directory:** docs/plans/
    - **Archive directory:** docs/archive/

### 1. Determine Version

Check for the latest git tag:

```bash
git tag --sort=-v:refname | head -1
```

If `$ARGUMENTS` specifies a version:
- Use it directly (validate it's valid semver)

If `$ARGUMENTS` specifies a bump type (`major`, `minor`, `patch`):
- Calculate the new version from the latest tag

If `$ARGUMENTS` is empty:
- Look at the delivered plans since the last release to suggest a bump type:
  - Any features → suggest `minor`
  - Only bug fixes → suggest `patch`
  - Breaking changes noted in changelogs → suggest `major`
- Propose the version and confirm with the user

### 2. Collect Changelog Entries

Find delivered plans since the last release:

```bash
# Get the date of the last release tag
LAST_TAG=$(git tag --sort=-v:refname | head -1)
if [ -n "$LAST_TAG" ]; then
  LAST_RELEASE_DATE=$(git log -1 --format=%ai "$LAST_TAG" | cut -d' ' -f1)
else
  LAST_RELEASE_DATE="1970-01-01"
fi

# Find archived plans newer than the last release
# (archived plans have date prefix: YYYY-MM-DD-<slug>.md)
ls docs/archive/*.md
```

For each archived plan since the last release:
1. Read the `## Changelog` section
2. Read the `## Status` section for the **Type** (feature/bug/docs/infra)
3. Collect the changelog entries

Only include feature and bug plans in the release notes (docs/infra are live when merged — they don't need release).

### 3. Compose Release Notes

Write or update `CHANGELOG.md` with the new version entry:

```markdown
## v<version> — YYYY-MM-DD

### Features

- <changelog entry from feature plan>

### Bug Fixes

- <changelog entry from bug plan>
```

If `CHANGELOG.md` doesn't exist, create it with a header:

```markdown
# Changelog

## v<version> — YYYY-MM-DD

...
```

If it exists, prepend the new version entry after the `# Changelog` header.

### 4. Bump Version

Check if `package.json` exists and update the version field:

```bash
# If package.json exists
pnpm version <version> --no-git-tag-version
```

If no `package.json`, skip this step.

### 5. Commit and Tag

```bash
git add CHANGELOG.md
git add package.json 2>/dev/null  # if it exists
git commit -m "release: v<version>"
git tag -a v<version> -m "Release v<version>"
```

### 6. Push

```bash
git push origin main
git push origin v<version>
```

### 7. Summary

Print:
- Released: `v<version>`
- Tag: `v<version>`
- Changelog updated
- Plans included:
  - `<slug>` — <type>
  - `<slug>` — <type>
- Next steps: deploy, announce, etc. (project-specific)
