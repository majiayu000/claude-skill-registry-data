---
name: prepare-release
description: 'Finish a feature by returning its exact range to its umbrella-slug integration branch, or to generic integration for a standalone topic, then stop with the next umbrella requirement from pw skill. When the umbrella is exhausted, continue through the Diataxis wiki audit and release preparation. Stop before brel and never push.'
user-invocable: true
argument-hint: 'Explain the context from main, integration, or any feature branch. Feature mode returns a collection topic to its umbrella-slug branch; ambiguous ancestry pauses for a parent branch or boundary commit.'
---

[Instruction](../../../instructions/prepare-release.md)

Implementation is mutualized across the shared directories:

- [`../instructions/prepare-release.md`](../../../instructions/prepare-release.md)
  — the full workflow.

This skill calls the `group-commits-msg`, `update-merge-commit-msg`,
`review-and-update-project-docs`, and `prepare_release_notes` skills, and runs
the `ghog day` groundhog loop when it rebases the branch or merges a stale
base, using the flag file
`a.prepare-release.active` in the review artifact home (`.reviews`) so the called skills return control
to it instead of ending standalone. It readies every release artifact and
stops at the `chore(release): prepare for vX.Y.Z release` commit; the next
step is for the user to review and run `brel` to build and tag. The skill
never creates a tag and never pushes to a remote.
