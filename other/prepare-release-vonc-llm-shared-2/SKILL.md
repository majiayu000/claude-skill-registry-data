---
name: prepare-release
description: 'Finish a feature by returning its exact range to its umbrella-slug integration branch, or to generic integration for a standalone topic, then stop with the next umbrella requirement from pw skill. When the umbrella is exhausted, continue through the Diataxis wiki audit and release preparation. Stop before brel and never push.'
user-invocable: true
metadata:
  - "Feature mode may stop after the destination merge and umbrella handoff without touching release artifacts; a full release stops before brel, never creates the tag, and never pushes."
  - "Step 1-2: find the last tag (git describe --tags --abbrev=0) and detect a development effort (a commit since the tag touching docs/{feature,issue,design,plan}.*). With none, stop with 'release already done' (HEAD on a tag) or 'nothing to release yet'."
  - "Step 3: resolve an umbrella-slug integration branch before planning, then classify on-main, integration, or feature mode; recover the actual feature fork and stop when Git evidence is ambiguous."
  - "Apply gitworkflow topic graduation (one word, not GitFlow): collection topics return to their umbrella branch; standalone topics use generic integration when present, otherwise main."
  - "Before mutation, automatically locate and run prepare_release_plan.bat for deterministic topology and Git 2.50+ merge-tree conflict evidence; never ask the user to run it. Preview merges once and feature rebases commit by commit, stopping at the first predicted conflict."
  - "Step 4-5: make the current worktree clean and bring main plus the feature destination current; never rebase integration; replay a stale exact feature range on a temporary landing branch, verify with range-diff, then run ghog day."
  - "Step 6-7A: merge --no-ff into the destination, reword with Why:/What:, then call pw skill --after-merge. A pending item stops with process-draft based on its slug; prepare-release means the collection is exhausted and the full release may continue."
  - "Step 8: when wiki/ or docs/wiki/ exists, call review-and-update-project-docs for every existing root against the complete last_tag..HEAD release range; stop on uncovered topics, and commit reviewed wiki changes before release notes."
  - "Step 9-13: set version.txt to X.Y.Z-SNAPSHOT, call prepare_release_notes for the summary and changelog, pause for notes review, update pyproject.toml and uv when present, then make one chore(release): prepare for vX.Y.Z release commit."
  - "Step 14: report a summary and tell the user to review and run brel. It uses the flag file a.prepare-release.active in the review artifact home (.reviews; deleted at start, created before each sub-skill call, removed on exit) so the called skills return control to it."
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
