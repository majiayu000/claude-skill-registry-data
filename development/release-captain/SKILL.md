---
name: release-captain
description: Prepare software releases, changelogs, release notes, semantic version decisions, migration notes, publish checklists, and GitHub release drafts. Use when the user asks to cut a release, tag a version, publish a package, summarize changes since the last release, or verify release readiness. Do not use for unrelated marketing copy or routine docs edits.
---

# Release Captain

Make releases boring, traceable, and reversible.

## Workflow

1. Identify the release target, previous tag, versioning scheme, package names, and publish destination.
2. Compare commits since the previous release and group changes by user impact.
3. Check readiness: tests, build, docs, migrations, compatibility, security notes, and rollback path.
4. Decide version bump from public API or user-visible behavior, not commit count.
5. Draft release notes with install/upgrade instructions.
6. Do not publish, tag, or mutate package registries unless the user explicitly approves that final action.

## Release Notes Shape

```text
Title:
Summary:
Highlights:
Breaking changes:
Migration notes:
Fixes:
Verification:
Rollback:
Links:
```

## Checklist

- Version number matches project conventions.
- Changelog and README links are current.
- Generated artifacts are intentionally included or ignored.
- Package lockfiles match manifests.
- CI or local verification is recorded.
- Secrets and local paths are absent from notes.
- Release URL, tag, and commit SHA are captured after publishing.
