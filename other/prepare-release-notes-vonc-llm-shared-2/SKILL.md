---
name: prepare_release_notes
description: 'Prepare release notes for a new version: generate a.md from the git history since the last tag, write a release-notes summary into version.txt, let the user pick a witty title, then update the changelog. Use before creating a release, when the user asks to "prepare release notes".'
user-invocable: true
metadata:
  - "This skill prepares release notes for a new version of the project, and must be run before creating a new release."
  - "Step 1: call the prepare_release_notes.sh script from llm-shared/scripts, run from the project directory; its output is a.md in the project directory."
  - "Step 2: analyse a.md and write a release-notes summary into version.txt, following the template under ../templates."
  - "Step 3: pause to let the user choose one of the three witty titles, then finalize version.txt."
  - "Step 4: call tools/dev_workflow/update-changelog.bat to update the changelog; the next step for the user is to run 'brel'."
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
