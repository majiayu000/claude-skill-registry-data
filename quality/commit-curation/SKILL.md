---
name: commit-curation
description: Curate repository changes into coherent commits by inspecting exact diffs, separating unrelated work, preserving authorship/context, validating staged state, and writing messages that describe the resulting repository change.
---
# Commit Curation

Use when a working tree contains one or more completed changes that need to become reviewable, recoverable Git commits.

## Procedure
1. Inspect branch, HEAD, worktrees, status, staged/unstaged/untracked paths, and relevant diffs before staging anything. Identify changes owned by other work and preserve them.
2. Group changes by one coherent outcome or dependency. Files may belong in the same commit when they are required to make one change correct and understandable; split changes that can be reviewed/reverted independently.
3. Review generated, lockfile, vendor, schema, migration, or asset changes carefully so automatic output does not hide unrelated modifications.
4. Stage exact intended paths or hunks using the safest available mechanism. Avoid broad `git add .` or equivalent when unrelated work is present or the set of reviewed files is known.
5. Inspect the staged diff and staged file list after staging. The index, not the working tree, is the content that will become the commit.
6. Run or verify the validation appropriate to the staged result. If validation depends on unstaged changes, make that dependency explicit rather than pretending the commit is independently proven.
7. Write a commit message that describes the resulting behavior or repository state. Use project conventions and include rationale/body only when it adds durable context.
8. Create the commit, then verify the new commit's diff/tree and remaining working-tree state. Confirm unrelated modifications remain untouched.
9. For multi-commit series, review the sequence as a reader would encounter it. Each commit should build sensibly on its parents without relying on later commits for basic validity unless the project deliberately accepts that style.

## Decision rules
- Commit boundaries are review/recovery boundaries, not arbitrary file-count limits.
- Do not rewrite, squash, or attribute another contributor's work without authority.
- A clean working tree is not a reason to combine unrelated changes.
- The staged diff is the source of truth for what is about to be committed.
- Never discard uncommitted work merely to make commit curation easier.

## Quality gate
The commit is ready when its staged content has been reviewed exactly, unrelated work is excluded and preserved, the change is coherent and appropriately validated, the message describes the resulting change, and post-commit repository state matches the intended split.