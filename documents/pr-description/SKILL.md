---
name: pr-description
description: Draft a pull request description from the current branch diff plus rolling-wave project context. Use when the user wants PR body text, changes, potential risks, or reviewer notes for a branch, especially after completing a rolling-wave slice. Defaults to the Git Town parent branch when no base branch is named.
---

# PR Description

## Purpose

Draft a concise PR description from:

- the current branch changes compared to a requested base branch
- the rolling-wave project artifact
- the currently finished or most relevant completed slice

Do not open a PR, post to GitHub, stage files, commit, or edit project files unless the user explicitly asks.

## Inputs

- Base branch: use the branch named by the user. If none is named, use the Git Town parent branch. If Git Town cannot resolve a parent, fall back to `main`, then `origin/main`.
- Rolling-wave project: use the project named by the user, or the single project under `docs/rolling-wave/` when only one exists.
- Finished slice: prefer the slice named by the user. Otherwise use the most recently updated slice with status `done`. If no done slice exists, use the most relevant active slice and clearly say the PR description is based on an unfinished slice.

## Workflow

1. Resolve the base branch.
   - Run `CURRENT_BRANCH=$(git rev-parse --abbrev-ref HEAD)`.
   - If the user named a base branch, use it.
   - If the user did not name a base branch, run `git-town config get-parent "$CURRENT_BRANCH"` and use the returned branch.
   - If Git Town does not return a parent branch, fall back to `main`, then `origin/main`.
   - Compute `BASE=$(git merge-base HEAD "$BASE_BRANCH")`.
   - If the base cannot be resolved, stop and ask for a valid base branch.

2. Read branch changes.
   - Use:

```bash
git diff --stat "$BASE"...HEAD
git diff --name-status "$BASE"...HEAD
git diff -U10 "$BASE"...HEAD
git log --oneline "$BASE"..HEAD
```

   - Read changed files only as needed to understand user-visible behavior, contracts, migrations, tests, docs, and risk.
   - Do not include unrelated local worktree changes unless the user explicitly asks. This skill describes the branch diff.

3. Read rolling-wave context.
   - Read `docs/rolling-wave/{project}/project.md`.
   - Read the selected finished slice file under `docs/rolling-wave/{project}/slices/`.
   - Use the project finish line, success criteria, cross-slice decisions, potential risks, and review notes as context.
   - Use the slice original contract, implementation notes, review notes, and completion learnings to decide what reviewers need to know.

4. Synthesize, do not dump.
   - Focus on changes a reviewer needs to understand before reviewing the PR.
   - Prefer behavior, API/contract, data/model, migration, permission, testing, and rollout implications over file-by-file summaries.
   - Mention implementation details only when they materially affect review.
   - Combine project-level and slice-level risks. Do not invent risk to fill the section.
   - If project docs and branch diff disagree, call out the mismatch in review notes.

5. Draft the PR body.
   - Use this exact section order:

```markdown
## Changes

- ...

## Potential Risks

- ...

## Review Notes

- ...
```

   - Omit `Review Notes` only when there is genuinely nothing special human reviewers need to know.
   - Keep bullets concise but specific.
   - Avoid generic bullets like "updates tests" unless the test change is itself important to review.
   - Do not include marketing prose, long background, or a full implementation plan.

6. Apply the user's voice with `ghostwriter`.
   - Use the `ghostwriter` skill as the final drafting pass.
   - Treat the synthesized facts, risks, and reviewer notes from steps 1-5 as fixed source material.
   - Preserve the required section order and bullet-list structure.
   - Preserve technical claims, uncertainty, and risk framing; do not let voice polish soften or invent facts.
   - Match the user's default PR-description tone: direct, technical, concise, candid about constraints, and useful to reviewers.

## Output Rules

- Output only the PR description plus a short one-line context note if needed, such as the base branch and slice used.
- Do not claim tests passed unless the diff or user-provided context proves it.
- Do not include unresolved speculation as fact. Phrase uncertain items as risks or review notes.
- If the branch has no diff against the base, say so and do not fabricate a PR description.
