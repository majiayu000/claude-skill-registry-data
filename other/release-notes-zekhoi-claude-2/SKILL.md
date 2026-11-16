---
name: release-notes
description: Write release notes or a changelog entry from the commits and merged pull or merge requests since the previous release, grouped for users and following the project's existing changelog format. Use when the user asks for release notes, a changelog entry, a "what changed since vX" summary, or to update CHANGELOG.md before a release. Do not use for tagging, publishing, or creating the release itself, for pull request descriptions (use agent-kit:pull-request), or for general documentation (use agent-kit:documentation).
---

# Release notes

## 1. Find the range and the format

- Find the previous release: the latest tag (`git describe --tags --abbrev=0`), the last version in `CHANGELOG.md`, or the version the user named. Confirm the range when it is ambiguous.
- Read the existing changelog and follow its format, headings, and tone (Keep a Changelog, Conventional Changelog, a custom layout). Note how versions are numbered.

## 2. Collect the changes

- List commits in the range (`git log <prev>..HEAD --no-merges`) and the merged pull or merge requests where the forge CLI is available. Read the diffs of commits whose messages are unclear instead of guessing.
- Drop changes users do not see (internal refactors, test-only and CI-only changes) unless the project's changelog includes them. Merge commits that belong to one change.

## 3. Write

- Group entries the way the project does, typically: breaking changes first, then added, changed, fixed, deprecated, removed, and security. Write each entry from the user's point of view: what changed and what they need to do.
- Every breaking change needs migration steps. Link pull requests or issues the way existing entries do. Do not invent impact or credit.
- If the version number is not decided, suggest one from the changes (semantic versioning: breaking means major, features mean minor) and mark it as a suggestion.

## 4. Report

Show the draft or the edited changelog section, the range used, entries that were left out and why, and open questions. Do not create tags or releases or publish packages unless the user explicitly asks.

## Examples

- Use: "Write release notes for v2.3.0." "Update the changelog with everything since the last tag."
- Skip: "Tag and publish the release." "Write the description for this PR." (agent-kit:pull-request)
