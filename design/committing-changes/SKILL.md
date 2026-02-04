---
name: committing-changes
description: Creates commits following project conventions. Handles Conventional Commits with project-specific scopes, PR title requirements, changesets for releases, and CI validation rules.
---

# Committing Changes

## Steps

### For Regular Commits

1. Stage changes with `git add`
2. Commit using Conventional Commits format: `<type>(<scope>): <description>`
3. If this is a release-worthy change (`feat`, `fix`, `perf`, `docs`), run `pnpm changeset`

### For PRs

1. The **PR title** is what matters - PRs are squash-merged
2. PR title must follow CC format
3. Include changeset if release-worthy

## Reference

### Scopes

Package name minus `@kitz/` prefix. Comma-separate for multiple packages. Omit for repo-level.

```
feat(core): add new utility          # @kitz/core
fix(core, arr): update shared type   # Multiple packages
ci: add Vercel Remote Cache          # Repo-level (no scope)
```

### Types

| Type | Description | Version Bump |
|------|-------------|--------------|
| `feat` | New feature | Minor |
| `fix` | Bug fix | Patch |
| `docs` | Documentation | Patch |
| `perf` | Performance improvement | Patch |
| `style` | Formatting, whitespace | None |
| `refactor` | Code change (no behavior change) | None |
| `test` | Adding/updating tests | None |
| `build` | Build system, dependencies | None |
| `ci` | CI configuration | None |
| `chore` | Other maintenance | None |
| `chore.docs` | README, guides (not code docs) | None |

### Special Rules

**`chore.docs` vs `docs`:**
- `docs(pkg)`: JSDoc, code comments → Patch release, full CI
- `chore.docs`: README, guides → No release, CI skipped

**CI Skips:** `ci:` or `chore.docs:` PR titles skip code checks (only format runs)

**Changesets:** Required for `feat`, `fix`, `perf`, `docs(pkg)`. Run `pnpm changeset` to create.

### Bypasses (edge cases only)

- `<!-- cc-bypass -->` in PR body: Skip CC validation
- `<!-- changeset-bypass -->` in PR body: Skip changeset validation

## Notes

- Individual PR commits don't matter - only the PR title affects releases
- Scopes are for changelogs, not CI filtering (Turborepo uses git diff)
- Semver rule: `feat` = "new capability", `fix` = "works better"
