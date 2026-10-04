---
name: release
description: Bump version, generate changelog draft, tag, and deploy a release.
allowed-tools: Bash(git *), Bash(gh *), Bash(pnpm check *), Bash(pnpm test *), Bash(node *), Read, Edit, Write, AskUserQuestion
---

# Release

Bump version, generate a changelog draft, open a release PR, and create a GitHub Release after merge.

## Usage

```
/release [patch|minor|major]   (default: minor)
```

## Process

### 1. Determine version

- Read the latest git tag: `git tag --sort=-v:refname | head -1`
- If no tags exist, this is the first release — use `0.1.0`
- Apply bump type (patch/minor/major) to compute next version
- Confirm with user: "Release v{version}?"

### 2. Pre-flight checks

- Must be on `main` branch with clean working tree
- `pnpm check` and `pnpm test` must pass
- If checks fail, stop and report

### 3. Generate changelog draft

- Skip this step for the first release (no prior tag to diff against)
- Collect commits since last tag: `git log v{prev}..HEAD --format='%s'`
- Group by type prefix (feat → Added, fix → Fixed, perf → Performance, refactor/style → Changed, docs → Documentation)
- If `CHANGELOG.md` doesn't exist, create it with the [Keep a Changelog](https://keepachangelog.com/) header
- Insert a new section at the top with the draft entries
- **Ask the user to review and edit** the changelog draft before proceeding
  - User rewrites technical commit messages into user-facing descriptions
  - Wait for explicit confirmation before continuing

### 4. Version bump

- Update `version` in `package.json`

### 5. Create release PR

```bash
git checkout -b release/v{version}
git add package.json CHANGELOG.md
git commit -m "chore: release v{version}"
git push -u origin release/v{version}
gh pr create --title "chore: release v{version}" --body "Version bump and changelog for v{version}."
```

- Show the PR URL to the user

### 6. Done

- After merge, CI automatically:
  1. Deploys to Cloudflare Pages
  2. Creates a GitHub Release with tag (extracts notes from CHANGELOG.md)
- The CI auto-tag step triggers on merge commits containing "release v" in the message
- No manual action needed after merge

## Safety

- Never skip pre-flight checks
- Never auto-generate final changelog text — always show draft and wait for user edit
- First release (v0.1.0): version bump + tag only, no changelog
- Always use PR flow — never commit directly to main
