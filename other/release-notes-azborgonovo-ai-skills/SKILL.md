---
name: release-notes
description: >
  The trigger for this skill covers phrasings such as "write the release notes",
  "draft a changelog", "what shipped in this version", and "summarise the commits
  since the last tag". It also covers a user who pastes a raw list of commits and
  asks what to do with them. Release notes, changelog, ship note, and version
  summary are all in range of the trigger.
allowed-tools: [Read, Write]
---

# Release Notes

Write the release notes for a version.

Think carefully before you write anything. Be thorough and accurate. Use your best judgment throughout the task.

## Gather the commits

Take the version from `$ARGUMENTS`.

Run these commands in order, and keep the output of each one:

1. `git describe --tags --abbrev=0` to find the previous tag.
2. `git log <previous-tag>..HEAD --pretty=format:'%h %s'` to list the commits.
3. `git log <previous-tag>..HEAD --pretty=format:'%an' | sort -u` to list the authors.
4. `git diff --stat <previous-tag>..HEAD` to size the release.
5. `git log <previous-tag>..HEAD -i --grep='BREAKING CHANGE'` to find the breaking changes.

Group the entries by type before you write anything.

## Commit types

| Type | Heading | Include | Order |
|---|---|---|---|
| `feat` | Added | Always | 1 |
| `fix` | Fixed | Always | 2 |
| `perf` | Improved | Always | 3 |
| `refactor` | Internal | Only when it changes a public contract | 4 |
| `docs` | Documentation | Only for user-facing documentation | 5 |
| `build` | Packaging | Only when it changes a published artifact | 6 |
| `ci` | Internal | Never | 7 |
| `test` | Internal | Never | 8 |
| `chore` | Internal | Never | 9 |
| `style` | Internal | Never | 10 |

## Write the notes

Group the entries by type, in the order that the table gives.

Open with the version and the date. Put the breaking changes first, under their own heading, with the migration step for each one.

Write one line per entry, in the past tense, and name the behavior that changed rather than the file that changed.

Credit every author in a list at the end.
