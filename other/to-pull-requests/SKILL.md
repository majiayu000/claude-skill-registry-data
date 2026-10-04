---
name: to-pull-requests
description: Prepare and open a pull request for an already pushed issue branch. Use after `/implement` offers it, or when the developer explicitly asks to open a PR.
disable-model-invocation: true
---

# To Pull Requests

Create the pull request for the named ticket. This is a manual command: never run it merely because `/implement` completed.

1. Resolve the ticket and its exact PR target branch from the ticket's `## Integration Branch` section, its parent epic, or `base_branch` for an epic-less ticket. If this cannot be resolved, stop and ask the developer.
2. Verify that the current branch matches `branch_pattern`, is neither `base_branch` nor `integration/*`, has no uncommitted changes, and has no commits absent from its upstream branch. If the branch has not been pushed, stop and ask the developer to return to `/implement`. Fetch its upstream and require `git rev-parse HEAD` to equal the upstream branch SHA; if it differs, fast-forward the clean local branch before continuing.
3. For a valid `backend-orchestration` opt-in, resolve the full current SHA with `git rev-parse HEAD` after that synchronization and validate it before any PR action:
   `python .harness/orchestration/coordinator.py --repo . qa evidence --ticket "#<ID>" --branch "<current-issue-branch>" --candidate-commit "<full-current-SHA>"`.
   The CLI selects the unique batch with accepted QA evidence for that SHA, so abandoned historical
   batches with the same ticket and branch do not matter. If more than one batch accepted that exact
   SHA, stop and repeat the command with its explicit `--batch <batch-id>`. Stop if the command rejects
   missing, unaccepted, or SHA-mismatched evidence, UNLESS the ticket is explicitly labeled `pipeline::fast`. For `pipeline::fast` tickets, bypass the coordinator evidence check.
   Do not rerun `/qa-gate` when coordinator validation succeeds. If the project is not a valid opt-in, or if the ticket is `pipeline::fast`, run `/qa-gate` if this repository provides it and
   stop on failure.
4. Prepare the PR body using `docs/agents/git-workflow.md` §3. Store it only at `.harness/.sandboxes/pr_body/pr-body-<issue>-<slug>.md`, never in `docs/tasks/`. A developer may manually run `pr-composer` in the coding application; otherwise fill in the template directly. Resolve the repository default branch and use `Closes #<ID>` only for that target, otherwise `Related to #<ID>`.
5. Ask the developer for explicit confirmation that the branch is ready to become a PR. Stop for their answer.
6. After approval, open the PR/MR with the tracker CLI and `--body-file <path>`. Delete the `.harness/.sandboxes/pr_body/` body file only after that command succeeds; on failure, retain it for retry. If the ticket carries `task-report::required`, publish its completion report on the ticket, unless the developer asked to skip it.
7. Return the PR/MR link in the primary session and ask whether the developer wants to review it. Never merge it. After the developer confirms the merge, close a `Related to #<ID>` ticket explicitly; for `Closes #<ID>`, verify that the tracker closed it.
8. **Unblock dependencies — mandatory after every close, in the same session.** Leave the closed ticket's own `status::in-progress` label as is: the closed state is its terminal `done`. Then find every open ticket this one blocked and move each one whose blockers are now all closed:
    - **GitHub:** list open `status::blocked` issues (`gh issue list --state open --label status::blocked --json number`). For each, read its native blockers (`gh api repos/<owner>/<repo>/issues/<n>/dependencies/blocked_by --jq '[.[] | select(.state=="open")] | length'`) and any `Blocked by:` line in its body. If both show no open blocker, run `gh issue edit <n> --remove-label status::blocked --add-label status::ready`.
    - **GitLab:** the same check through native blocking links (`glab api projects/:id/issues/:iid/links`) and the `Blocked by:` line; swap with `glab issue update <n> --unlabel status::blocked --label status::ready`.
    - **Local tracker** (`.scratch/<feature>/issues/*.md` or `docs/tasks/*.md`): check `**Blocked by:** #<ID>` and set `**Workflow:** status::ready` once every listed blocker is resolved.
    - Report which tickets moved to `status::ready` and which stay blocked, and by what.
9. **Cleanup:** After confirming the PR is merged and the ticket is closed, clean up the local environment to prevent garbage accumulation. Switch out of the worktree if necessary, remove the worktree using `git worktree remove <path>`, and delete the local branch using `git branch -d <branch-name>`.
