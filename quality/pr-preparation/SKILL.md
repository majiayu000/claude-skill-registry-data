---
name: pr-preparation
description: Prepare or refresh a pull request from reviewed Git state with a coherent full diff, correct base/head, preserved media, accurate summary, validation evidence, migration or risk notes, and no unrelated or stale changes.
---
# Pull Request Preparation

Use when a branch or commit series is ready to be proposed for integration, or when an existing PR/MR description no longer reflects the current branch.

## Procedure
1. Verify the intended repository, base branch, head branch, remote ownership, and branch protection/review conventions before opening or updating the PR.
2. Determine whether the head branch already has a PR/MR. Update the existing review surface when it represents the same work rather than opening a duplicate.
3. Compare head against the actual target base and inspect the complete base-to-head diff/file list, not just the latest commit or current working tree.
4. Ensure commits are coherent enough for the repository's review style and that generated, lockfile, migration, vendor, media, or asset changes are intentional. Do not impose an arbitrary commit count or rewrite shared history merely for aesthetics.
5. Update from the target base according to repository policy when necessary and resolve conflicts without discarding contributor intent or unrelated work.
6. Run or gather validation appropriate to the proposed current revision and record exact commands/results or links. Do not claim checks that were not run or belong to an older head SHA.
7. Draft the title and body from the change as a whole: resulting behavior, motivation, important implementation choices, validation, migration/compatibility/rollout concerns, and known limitations where relevant.
8. When refreshing an existing PR/MR, read its current body first and preserve screenshots, videos, upload URLs, diagrams, and other intentionally attached media unless the change explicitly replaces them. Verify preserved media still exists in the new body before publishing it.
9. Link issues, tasks, designs, specifications, and related/sibling PRs when they define scope or provenance. Preserve contributor credit when the branch consolidates or carries forward another contributor's work.
10. Request reviewers appropriate to affected ownership/risk and verify after creation/update that the forge points at the intended head SHA/base and that status checks correspond to that revision.

## Decision rules
- A PR is a review surface, not a development diary.
- The complete base-to-head diff is what reviewers approve.
- Do not open a duplicate PR when an existing branch review can be refreshed accurately.
- Do not strip useful screenshots/video from an existing PR description as a side effect of rewriting text.
- Do not hide known risk or incomplete validation to make the PR appear ready.
- Reviewer selection should follow affected ownership and risk.

## Quality gate
The PR/MR is ready for review when its current full diff is coherent and scoped, base/head are correct, description and preserved media reflect the actual branch, validation evidence is truthful and revision-specific, material migration/risk/rollout information is visible, contributor provenance is preserved, and the forge confirms the intended current revision.