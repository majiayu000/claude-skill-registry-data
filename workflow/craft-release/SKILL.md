---
name: craft-release
description: Crafting a release pipeline. One action, full pipeline.
---

# Skill: Craft Release

> "A release should be one click, not a checklist."

## The Standard

1. **GitHub Release triggers everything**: Create a release on GitHub. The changelog updates. Packagist picks up the tag. One action, full pipeline.
2. **Semver strictly followed**: Major for breaking changes. Minor for new features. Patch for fixes. No exceptions, no "we'll bump major just in case."
3. **Consistent tag prefix**: Pick one convention and stick with it. Taylor's first-party packages use `v` prefix (`v7.1.0`). Spatie omits it (`7.1.0`). Both work with Packagist. Consistency matters more than the choice.
4. **CHANGELOG.md auto-updated**: The `update-changelog.yml` workflow uses `stefanzweifel/changelog-updater-action` + `git-auto-commit-action`. Commits directly to `main`. No manual changelog edits.
5. **GitHub auto-generated release notes**: PR-based entries, contributor attribution, compare links. Low maintenance, high value.
6. **Packagist webhook**: Configure once on the GitHub repo. Tag creation triggers package update automatically. No manual publishing.

## The Pipeline

One human action: create the GitHub release. Everything else is automated.

1. Merge PRs to main
2. CI validates (tests, PHPStan, style)
3. Create GitHub release with auto-generated notes
4. `update-changelog.yml` fires -- CHANGELOG.md updated, committed to main
5. Packagist webhook fires -- package version published
6. Dependabot handles downstream updates for consumers

## Version Support Policy

State your support window explicitly in README or SECURITY.md. Three tiers:

| Tier        | Bug Fixes | Security Patches | Example                    |
|-------------|-----------|------------------|----------------------------|
| Active      | Yes       | Yes              | Current major              |
| Maintenance | No        | Yes              | Previous major (12 months) |
| End of Life | No        | No               | Everything else            |

Laravel's window: 18 months bug fixes, 24 months security. For community packages, match your capacity — but be explicit. Undocumented support policy is no support policy.

## The Anti-Patterns

| Don't                              | Do                          | Why                                                |
|------------------------------------|-----------------------------|----------------------------------------------------|
| Manual changelog updates           | Auto-changelog on release   | Humans forget. Automation does not                 |
| Inconsistent tag prefix            | Pick one, be consistent     | Taylor uses `v`, Spatie omits. Both valid          |
| Manual Packagist publishing        | Packagist webhook           | One-time setup, zero ongoing cost                  |
| Squash without meaningful messages | Meaningful PR titles        | PR titles become changelog entries                 |
| Release branches                   | Release from `main`         | One branch, one pipeline, one truth                |
| Manual release notes               | GitHub auto-generated notes | PR-based, contributor-attributed, link-rich        |

**See also:** craft-ci (CI workflows that gate releases), craft-deprecation (sunset lifecycle before major releases).

## Real-World Examples

See [examples.md](examples.md).
