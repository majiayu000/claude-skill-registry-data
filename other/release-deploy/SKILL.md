---
name: release-deploy
description: >-
  Release and deploy via GitHub tags and GitHub Actions (not every commit).
  Creates production releases from main and beta releases from staging using
  the GitHub CLI. Use when the user asks to release, ship, deploy, cut a
  version, tag a release, publish beta/production, create a GitHub Release,
  or bump a semver tag. On first use in a project, run the setup interview
  and write a project-specific config under projects/.
user-invocable: true
disable-model-invocation: false
version: "1.1.0"
author: "Ali Farahat"
tags: ["release", "deploy", "semver", "github", "changelog", "beta", "production"]
when_to_use: |
  USE WHEN:
  - The user asks to release, ship, deploy, cut a version, or tag a release.
  - The user asks to publish beta or production, create a GitHub Release, or
    bump a semver tag.
  - First release in a repo (run the setup interview and write projects/).

  DO NOT USE WHEN:
  - The user only wants a normal commit or PR with no release/tag.
  - The user explicitly says not to create a release yet.
  - Changelog notes are missing or ambiguous and the user has not updated them.
---

# Release & Deploy (GitHub Tags)

> **Leading words:** commits ≠ deploys; branch → channel; tag triggers ship;
> changelog is truth; interview once; never guess channel.

## Core model

- **Commits ≠ deploys.** Only a **git tag + GitHub Release** triggers deployment (via GitHub Actions or project-specific release jobs).
- **Branch → channel**
  - `main` → **production** release
  - `staging` → **beta** release
- **Tags**
  - Production: `vMAJOR.MINOR.PATCH` (e.g. `v1.4.0`)
  - Beta: `vMAJOR.MINOR.PATCH-beta.N` (e.g. `v1.4.0-beta.1`)
- **Release notes** come from the project's maintained `CHANGELOG.md` (do not invent a changelog). See [references/versioning.md](references/versioning.md).

## Before every release

1. **Load project config**
   - Look for `projects/<repo-slug>.md` next to this `SKILL.md` (slug = GitHub `owner/repo` with `/` → `-`, e.g. `acme-web-app`).
   - If missing → run the **first-time interview** in [references/interview.md](references/interview.md), write the file from [references/project.template.md](references/project.template.md), then continue.
2. **Confirm channel** with the user: beta (`staging`) or production (`main`). Never guess.
3. **Verify git state** (PowerShell-safe; run as separate commands):
   - Correct branch checked out (`staging` or `main`)
   - Working tree clean (or user explicitly accepts dirty)
   - Branch is up to date with its remote
   - HEAD is the commit they intend to ship
4. **Determine next version** from existing tags + user intent. Follow [references/versioning.md](references/versioning.md).
5. **Extract notes** from `CHANGELOG.md` for that version (or `[Unreleased]` if they are cutting that section into a version). If changelog is missing/ambiguous → stop and ask.

## Release workflow

Follow [references/gh-release.md](references/gh-release.md). Summary:

1. Ensure on the correct branch at the intended commit.
2. Create annotated tag locally (optional if `gh release create` will create it).
3. `gh release create` with tag, title, notes from changelog, and `--target` set to the branch (or SHA).
4. Watch the project's release/deploy workflow (from project config) until green or report failure.
5. Summarize: tag, release URL, channel, deploy target/URL from project config.

## Hard rules

- Never tag production from `staging`, or beta from `main`, unless the project config explicitly documents a different branch map **and** the user confirms.
- Never force-push tags or delete remote tags without explicit user request.
- Never skip the interview on a first release in a repo.
- Never fabricate changelog entries; only use `CHANGELOG.md` (or ask the user to update it first).
- Prefer `gh` over raw API calls. Prefer project config over inventing deploy steps.

## Platform-specific behavior

After the interview, project config names the stack. Read the matching reference only when needed:

- Cloudflare Workers/Pages → [references/platforms/cloudflare.md](references/platforms/cloudflare.md)
- Desktop apps (installers, auto-update, signed builds) → [references/platforms/desktop.md](references/platforms/desktop.md)
- Generic / other → rely on `projects/<slug>.md` workflow names and URLs

## Additional resources

- [references/interview.md](references/interview.md) — first-time setup questions
- [references/project.template.md](references/project.template.md) — config file shape
- [references/versioning.md](references/versioning.md) — semver + changelog rules
- [references/gh-release.md](references/gh-release.md) — GitHub CLI commands
