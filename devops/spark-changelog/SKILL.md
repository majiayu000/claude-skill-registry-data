---
name: spark-changelog
description: Update the CHANGELOG.md with the description of the changes between the last released version and the new one
---

# Spark Changelog Skill

## Overview

The `.script/update-changelog.swift` script adds a new version section at the top of `CHANGELOG.md` with a placeholder:

```markdown
## [X.Y.Z]

_DD/MM/YYYY_

❗️❗️ Use the /spark-changelog skills to improve the content ❗️❗️

Release notes content
```

This skill replaces the placeholder (lines 9 to 11: the ❗️❗️ line, the empty line and `Release notes content`) with a real description of the changes.

## Prerequisites

1. `CHANGELOG.md` must contain the placeholder `❗️❗️ Use the /spark-changelog skills to improve the content ❗️❗️`. If not, stop and tell the user to run the update-changelog script first.
2. Do not mention *Claude*.

## Steps

- [ ] Read `CHANGELOG.md` and get the **new version** (first `## [X.Y.Z]` after `## [Unreleased]`).
- [ ] Find the **previous version** tag: `git tag --sort=-v:refname`, take the most recent tag lower than the new version.
- [ ] List the changes since the previous version:
  - `git log <previous-tag>..HEAD --merges --pretty=format:"%s%n%b"` to get merged pull requests (PR number + title).
  - If needed, `git log <previous-tag>..HEAD --no-merges --oneline` to complete, and `gh pr view <number>` to get more details on a PR.
  - Ignore changelog-only commits (`chore(changelog)`) and pure merges of `main`.
- [ ] Group the changes into categories (omit empty ones), in this order:
  - `### 💥 Breaking Changes`
  - `### ✨ New Features`
  - `### 🚀 Improvements`
  - `### 🐛 Bug Fixes`
  - `### 📱 Demo App Improvements`
  - `### 📚 Documentation`
  - `### 🔧 Infrastructure & CI/CD`
  - `### 🧹 Chores`
- [ ] Inside a category, use `#### <Component or topic>` sub-headers when several entries concern the same component.
- [ ] Write each entry as a short sentence starting with a past-tense verb (Added, Updated, Fixed, Removed, ...), followed by the PR link: `([#1234](https://github.com/leboncoin/spark-ios/pull/1234))`.
- [ ] Replace **only** lines 9 to 11 (the placeholder block) with the generated content. Keep the version header and the date untouched, and keep one empty line before the next `## [` section.
- [ ] Follow the same style as the previous versions already present in `CHANGELOG.md`.
- [ ] Show the generated content to the user and ask if it is OK.

## Example

```markdown
## [1.0.0]

_27/03/2025_

### ✨ New Features

#### TextEditor Component
- Added SwiftUI TextEditor component for multiline text input ([#1106](https://github.com/leboncoin/spark-ios/pull/1106))

### 🐛 Bug Fixes

- Fixed Snackbar demos to ensure proper functionality ([#1105](https://github.com/leboncoin/spark-ios/pull/1105))
```
