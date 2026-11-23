---
name: pywf-oss-changelog
description: "Write or correct the section for the upcoming version in release-history.rst of a pywf open-source Python library, based on git history since the last tag. Use when the user wants to prepare release notes, update the changelog, record a change such as a dependency upgrade, or is about to publish or tag a new version."
---

Make the target version's section of `release-history.rst` accurate and complete, based on git history. Never touch the `x.y.z (Backlog)` section.

Read ../pywf-oss-base/SKILL.md, then:
- ../pywf-oss-base/references/22-versioning-and-changelog.md

## Step 1: Gather state

```bash
git status --short               # uncommitted work is invisible to git log
git describe --tags --abbrev=0   # last published tag: the baseline
grep '^version' pyproject.toml   # target version: the source of truth
```

`git log` misses uncommitted changes to code, tests, or dependencies. Show any, and ask for the user's yes to commit them first, or to include the working tree in the changelog.

## Step 2: Read the changes

```bash
git log <last_tag>..HEAD --oneline
git diff <last_tag>..HEAD --stat
git diff <last_tag>..HEAD -- '*.py'
```

- These outputs are the ground truth.
- Watch the `api.py` diff: added names are features; removed or renamed names are breaking changes.
- Classify `pyproject.toml` dependency and Python version changes with the category table in `22-versioning-and-changelog.md`.

## Step 3: Read the current file

Run `head -100 release-history.rst` to see this repo's exact formatting. Read the Backlog only to understand what the maintainer plans.

## Step 4: Write

- **The section exists:** compare it with git history. Add what is missing, remove what git does not support, and sharpen vague entries.
- **The section is missing:** insert `VERSION (YYYY-MM-DD)` with today's date directly below the Backlog block, following `22-versioning-and-changelog.md`.

Edit the file directly: it is tracked by git, so it needs no confirmation.

Next step: `pywf-oss-release`.
