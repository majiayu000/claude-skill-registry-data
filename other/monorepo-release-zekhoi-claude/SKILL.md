---
name: monorepo-release
description: Prepare per-package versions and changelogs in a monorepo using the workspace's release tooling (Changesets, Nx release, Lerna, release-please, uv or Cargo workspaces, Go module tags), including changeset files, version bumps for changed packages and their dependents, and per-package changelog entries, without publishing. Use when the user asks to version, bump, add a changeset, prepare a release, or write changelogs for packages in a monorepo. Do not use for single-package repositories (use agent-kit:release-notes), for code changes (use agent-kit:monorepo-change), or to publish, tag, or push, which need an explicit instruction.
---

# Monorepo release

Do not publish packages, create or push tags, create releases, or push commits unless the user explicitly asks; prepare the changes and give the commands.

## 1. Learn the release setup

- Find the tool and its configuration: `.changeset/config.json` (fixed or linked groups, `updateInternalDependencies`, ignored packages), `nx.json` `release`, `lerna.json` (fixed or independent mode), `release-please-config.json`, Cargo `workspace.package.version`, or Go module tags of the form `path/to/module/vX.Y.Z`. Follow it; do not switch tools.
- Determine which packages changed since their last release: existing changesets, tags per package, or `git log <last-tag>..HEAD -- <package path>`. Ignored packages are skipped; private packages are versioned but not published by default (Changesets `privatePackages`). Follow the config.

## 2. Decide the bumps

- For each changed package, pick major, minor, or patch from what changed for its users: breaking API changes are major, compatible features minor, fixes patch. Read the diffs when commit messages are unclear.
- Account for dependents: internal dependents get bumps according to the tool's rules (Changesets bumps dependents whose dependency range would no longer match; fixed groups move together). Note when a major bump of a shared package forces major bumps elsewhere.

## 3. Prepare

- With Changesets, write `.changeset/*.md` files (frontmatter listing packages and bump types, then a user-facing summary), and run `changeset version` only if the user asked to apply versions. With other tools, use their dry-run or version commands (`nx release --dry-run`, `lerna version --no-push --no-git-tag-version`; release-please computes versions in its pull request, so only prepare the conventional commits and config it reads).
- Per-package changelog entries describe changes for that package's users and include migration steps for breaking changes.
- For Go modules, list the tags to create (the module's directory relative to the repository root, such as `lib/strutil/v1.2.0`, with a `/vN` import path for majors from v2) instead of creating them.

## 4. Report

List each package with old and new versions and the reason, dependents bumped, the changeset or changelog files written, packages left out and why, and the exact publish and tag commands for the user to run.

## Examples

- Use: "Add a changeset for my change to packages/ui." "Prepare the next release of the packages." "What versions should bump after these commits?"
- Skip: "Write release notes for this single-package CLI." (agent-kit:release-notes) "Publish everything to npm now." (needs an explicit instruction; prepare and confirm first)
