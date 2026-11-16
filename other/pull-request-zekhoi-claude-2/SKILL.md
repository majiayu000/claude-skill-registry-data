---
name: pull-request
description: Prepare and open pull requests (GitHub) or merge requests (GitLab) with an accurate title, description, and test plan drawn from the branch's actual commits and diff. Use when the user asks to open, create, draft, or update a PR or MR, or to write its description. Do not use for reviewing someone else's PR or MR, committing, or merging.
---

# Pull or merge request

Opening a PR or MR is visible to others. Do it only when the user asked to open one; otherwise produce the title and description for them. Never merge, approve, close, or force-push unless the user explicitly asks.

## 1. Understand the branch

- Identify the current branch and its base: the user's stated target, otherwise the repository's default branch (`git remote show origin`, `gh repo view --json defaultBranchRef`, or `glab repo view`).
- Read `git log <base>..HEAD` and `git diff <base>...HEAD`. Describe what the branch actually changes, not only the latest commit.
- Check for uncommitted changes and for commits not yet pushed. Ask before committing or pushing anything on the user's behalf.

## 2. Follow project conventions

- Use the repository's PR or MR template if one exists (`.github/pull_request_template.md`, `.github/PULL_REQUEST_TEMPLATE/`, `.gitlab/merge_request_templates/`).
- Match the title style of recent merged PRs or MRs and the commit convention.
- Reference related issues using the syntax the platform understands (`Fixes #123`, `Closes group/project#123`).

## 3. Write the description

- **Summary:** what changed and why, in a few sentences.
- **Changes:** the notable changes, grouped logically. Call out breaking changes, migrations, configuration changes, and new dependencies.
- **Testing:** what was run and the result. If something was not tested, say so. Do not claim checks passed unless you ran them or saw their results.
- **Notes for reviewers:** risky areas, follow-ups, and anything intentionally out of scope.

Keep it proportional to the change. Do not pad small changes.

## 4. Open or update it

- GitHub: `gh pr create --base <base> --title ... --body ...` (add `--draft` when the work is incomplete); update with `gh pr edit`.
- GitLab: `glab mr create --target-branch <base> --title ... --description ...` (`--draft` when incomplete); update with `glab mr update`.
- If the CLI is missing or unauthenticated, or there is no remote, do not work around it. Give the user the title and description and the command to run.

## 5. Report

Give the PR or MR link, its base branch, and any checks or reviews it is waiting on.

## Examples

- Use: "Open a PR for this branch." "Write the MR description." "Update the PR description with the new changes."
- Skip: "Review PR #42." (use agent-kit:code-review) "Merge it." (requires an explicit instruction) "Commit this."
