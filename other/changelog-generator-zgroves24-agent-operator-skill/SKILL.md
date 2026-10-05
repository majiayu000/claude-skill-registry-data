---
name: changelog-generator
description: Create user-facing changelogs and release notes from git history by identifying meaningful changes, filtering internal noise, grouping by user impact, and preserving an evidence trail back to commits.
---

# Changelog Generator

This skill transforms technical git commits into clear, user-facing changelogs while preserving traceability back to the underlying commits.

## When to Use This Skill

- Preparing release notes for a new version
- Creating weekly or monthly product update summaries
- Documenting changes for customers
- Writing changelog entries for app store submissions
- Generating update notifications
- Creating internal release documentation
- Maintaining a public changelog/product updates page

## What This Skill Does

1. Scans git history from a date range, tag range, or branch range.
2. Groups commits by user impact: features, improvements, fixes, breaking changes, security, docs, and internal-only work.
3. Converts implementation details into clear release-note language.
4. Filters internal noise, but keeps an evidence appendix for review.
5. Calls out uncertainty instead of inventing product impact from vague commit messages.
6. Produces copy that can be pasted into a changelog, GitHub release, app-store note, or customer update.

## How to Use

### Basic Usage

From your project repository:

```
Create a changelog from commits since last release
```

```
Generate changelog for all commits from the past week
```

```
Create release notes for version 2.5.0
```

### With Specific Date Range

```
Create a changelog for all commits between March 1 and March 15
```

### With Custom Guidelines

```
Create a changelog for commits since v2.4.0, using my changelog 
guidelines from CHANGELOG_STYLE.md
```

## Example

**User**: "Create a changelog for commits from the past 7 days"

**Output**:
```markdown
# Updates - Week of March 10, 2024

## New Features

- **Team Workspaces**: Create separate workspaces for different 
  projects. Invite team members and keep everything organized.

- **Keyboard Shortcuts**: Press ? to see all available shortcuts. 
  Navigate faster without touching your mouse.

## Improvements

- **Faster Sync**: Files now sync 2x faster across devices
- **Better Search**: Search now includes file contents, not just titles

## Fixes

- Fixed issue where large images wouldn't upload
- Resolved timezone confusion in scheduled posts
- Corrected notification badge count

## Evidence Reviewed

- `a1b2c3d` Add team workspace creation flow
- `b2c3d4e` Improve sync batching
- `c3d4e5f` Fix upload size handling
```

## Quality Bar

- Every user-facing claim must map to at least one commit, PR, issue, or release artifact.
- Do not mention internal refactors unless they changed user-visible behavior, reliability, security, or performance.
- Do not invent metrics such as "2x faster" unless the commit, benchmark, or release note source supports it.
- Keep uncertainty visible. Use "internal cleanup, no user-facing note" for ambiguous commits rather than padding the changelog.

## Tips

- Run from your git repository root
- Specify date ranges for focused changelogs
- Use your CHANGELOG_STYLE.md for consistent formatting
- Review and adjust the generated changelog before publishing
- Save output directly to CHANGELOG.md

## Related Use Cases

- Creating GitHub release notes
- Writing app store update descriptions
- Generating email updates for users
- Creating social media announcement posts
