---
name: release
description: Bump version, commit, tag, and create a GitHub release
disable-model-invocation: true
---

# Release

Automate the qsv-stats release workflow.

## Arguments

The user should provide the new version number (e.g., `0.47.0`). If not provided, ask for it.

## Workflow

1. **Verify clean state**: Run `git status` to ensure the working tree is clean
2. **Bump version**: Update the version in `Cargo.toml` on the line marked with `#:version`
   - The line looks like: `version = "0.46.0"                                            #:version`
   - Only change the version string, preserve the comment marker and alignment
3. **Generate release summary**: Run `git log --oneline` from the last tag to HEAD and categorize commits:
   - `perf:` — Performance improvements
   - `feat:` — New features
   - `fix:` — Bug fixes
   - `refactor:` — Refactoring
   - `chore:` — Maintenance
   - `docs:` — Documentation
4. **Commit**: Create a commit with message `v X.Y.Z release`
5. **Tag**: Create a git tag `X.Y.Z` (no `v` prefix — matches existing tag convention)
6. **Push**: Push the commit and tag with `git push && git push --tags`
7. **GitHub release**: Create a release via `gh release create X.Y.Z --title "X.Y.Z" --notes "<release summary>"`

## Notes

- Check existing tags with `git tag --sort=-v:refname | head -5` to confirm the naming convention
- If there are uncommitted changes, warn the user and stop
- Always show the release summary for user review before creating the GitHub release
