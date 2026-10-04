---
name: prepare_release_notes
description: 'Prepare release notes for a new version: generate a.md from the git history since the last tag, write a release-notes summary into version.txt, let the user pick a witty title, then update the changelog. Use before creating a release, when the user asks to "prepare release notes".'
user-invocable: true
argument-hint: 'No argument needed. Run from a project whose version.txt holds an X.Y.Z-SNAPSHOT version.'
---

[Instruction](../../../instructions/prepare-release-notes.md)

Implementation is mutualized across the shared directories:

- [`../instructions/prepare-release-notes.md`](../../../instructions/prepare-release-notes.md)
  — the full workflow.
- [`../templates/prepare-release-notes.version-txt.template.txt`](../../../templates/prepare-release-notes.version-txt.template.txt)
  — the `version.txt` release-notes summary template.
- [`../scripts/prepare_release_notes.sh`](../../../scripts/prepare_release_notes.sh)
  — the release-notes script, run from the project directory.

Run before creating a release. Inputs: the project `version.txt` and the
git history since the last tag. Outputs: `a.md`, an updated `version.txt`,
and an updated `CHANGELOG.md`. The next step after this skill is for the
user to create the release with `brel`.
