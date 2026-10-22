---
name: good-skill
description: >-
  Generates the release notes of a project from its merged pull requests. Use this skill when the user asks
  for release notes, a changelog entry or a summary of what shipped since the last tag. Do not use it to
  write commit messages, that is the job of a commit skill.
license: MIT
compatibility: Requires Python 3.10+ and git.
---

# Release notes

Release notes for people who did not follow the work: what changed for them, grouped by type.

## Workflow

1. Run `scripts/collect.py --since <tag>` to list the merged pull requests as JSON.
2. Group them by type and write the notes following [the format guide](references/format.md).
3. Compare the notes with the format guide. If a section is missing or a change is listed twice, return to
   step 2.

## Gotchas

- Pull requests labelled skip-changelog stay out of the notes, even when they touch user-facing code.
- A revert cancels the change it reverts: list neither.
