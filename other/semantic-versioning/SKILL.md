---
name: semantic-versioning
version: "1.0"
description: Use when committing or pushing changes and the repository needs a version bump. Analyzes commits using conventional commit prefixes to determine whether the next release is a major, minor, or patch increment. Also use when the user asks about versioning, release planning, or changelog generation.
---

# Semantic Versioning

Determine the next version from commit history when preparing a release. The highest-impact release-relevant commit drives the bump.

## When to Activate

- Before or after pushing changes (suggest the version bump)
- When the user asks "what version should this be?"
- When preparing a release or tag
- When reviewing a set of commits for release notes

## Version Rules

Follows [Semantic Versioning 2.0.0](https://semver.org):

| Bump | Trigger | Examples |
|------|---------|----------|
| **Major** (X.0.0) | Breaking change | `feat!:`, `fix!:`, `BREAKING CHANGE:` in body/footer |
| **Minor** (x.Y.0) | New feature | `feat:`, `feature:` |
| **Patch** (x.y.Z) | Everything else | `fix:`, `chore:`, `docs:`, `style:`, `refactor:`, `test:`, `ci:`, `perf:` |

The highest bump wins: if any commit is `major`, the release is major — regardless of how many patches are in the batch.

## How to Check

Run the analysis script:

```bash
uv run skills/semantic-versioning/scripts/version-bump.py [repo-path]
```

Options:
- `--apply` — update the version file after confirmation
- `--tag` — also create a git tag

## Version File Detection

The script auto-detects where the version lives:

| File | Field |
|------|-------|
| `pyproject.toml` | `[project] version = "x.y.z"` |
| `package.json` | `"version": "x.y.z"` |
| `Cargo.toml` | `[package] version = "x.y.z"` |
| `VERSION` | Plain text file |

## Workflow

1. **Analyze** — scan commits since last tag, classify each
2. **Report** — show the bump type, commit breakdown, and suggested next version
3. **Confirm** — wait for user approval before making changes
4. **Apply** (if `--apply`) — update version file and optionally tag

Never auto-apply version changes without user confirmation.

## Commit Format Guide

For best results, follow conventional commits:

```
<type>[optional scope][!]: <description>

[optional body]

[optional footer(s)]
```

If commits don't follow conventional format, fall back to keyword analysis:
- Words like "add", "new", "feature" → minor
- Words like "fix", "bug", "patch", "correct" → patch
- Words like "breaking", "remove", "drop", "rename API" → major

## Pre-1.0 Semantics

For versions `0.y.z` (pre-stable):
- API is considered unstable
- Minor bumps may include breaking changes
- Use `0.y.z` until the project declares stability

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Bumping major for every `feat!` in pre-1.0 | Pre-1.0: breaking changes go in minor |
| Forgetting to tag after version bump | Always tag: `git tag v<version>` |
| Version in multiple files getting out of sync | Use the script to update all detected version files |
| Non-conventional commit messages | Fall back to keyword analysis, but encourage conventional commits |
