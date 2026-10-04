---
name: release-flow
description: Ship validated changes with repeatable release evidence — version bump, changelog, tag, and optional GitHub release
triggers:
  - release
  - bump version
  - create release
  - tag and release
  - publish version
---

# Release Flow

After verification passes, bump the version, update the changelog, tag the repo, and optionally create a GitHub release.

## Steps

1. **Confirm verification passed** — refuse to release without prior quality gate evidence
2. **Detect version source** — package.json, pyproject.toml, VERSION file, or git tags
3. **Preflight** — run the helper in verify mode to confirm git cleanliness, git identity, target tag availability, version source, changelog readiness, notes destinations, and optional `gh` readiness before any mutation
4. **Plan the release** — preview version bump level (patch, minor, major) and changelog entry
5. **Execute** — bump version, update changelog, create annotated git tag
6. **GitHub release** (optional) — validate `gh` auth, then create release with notes
7. **Report** — version, tag, changelog path, any skipped steps with reasons

## Output

```text
Version:    <old> → <new>
Tag:        v<new>
Changelog:  updated | skipped (no [Unreleased] section)
Preflight:  ready | blocked (reason)
GH Release: created | skipped (reason)
```

## Rules

- Never release without prior verification evidence
- Never invent a version file or changelog format the repo doesn't use
- Never publish artifacts without confirmed auth
- Only update changelog when it already has an `[Unreleased]` section
- Report skipped steps with reasons instead of failing silently
