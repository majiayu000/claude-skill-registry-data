---
description: Check release readiness, preview changelog, and validate publishability. Use when preparing a release or checking version status.
trigger: /release
---

# Release Check

Run the following checks to validate release readiness:

## Steps

1. **Current version**: Read `Cargo.toml` and report the current version
2. **Git tag check**: Run `git tag --list 'v*' --sort=-version:refSort` to see existing tags
3. **Unreleased commits**: Run `git log $(git describe --tags --abbrev=0 2>/dev/null || echo HEAD~10)..HEAD --oneline --no-decorate` to show commits since last tag
4. **Conventional commit validation**: Check that recent commits follow conventional commit format (feat:, fix:, docs:, etc.)
5. **Changelog preview**: If `git-cliff` is available, run `git-cliff --unreleased` to preview the next changelog entry. Otherwise, summarize commits manually.
6. **Publish dry-run**: Run `cargo publish --dry-run 2>&1` to verify the package is publishable

## Output

Report a summary:
- Current version: `x.y.z`
- Commits since last release: N
- Suggested next version based on conventional commits (patch/minor/major)
- Any issues found (missing fields, build errors, etc.)
- Dry-run result (pass/fail)

## Notes

- The actual release process is automated via release-plz (GitHub Actions)
- This skill is for local validation before pushing to main
- To publish: push conventional commits to main, release-plz will create a release PR
