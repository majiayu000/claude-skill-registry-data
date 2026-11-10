---
name: azure-devops-worktree-cleanup
description: Use when the user says Azure DevOps work is already merged or complete and wants to safely clean up the local feature branch and worktree.
---

# Azure DevOps Worktree Cleanup

## Scope

Clean up only the local branch, local worktree, the remote source branch
confirmed in step 6, and confirmed runtime resources covered by
`../worktree-runtime-cleanup/SKILL.md` after Azure DevOps work is complete.

Read `../azure-devops-common/references/context.md` before checking PR status.

## Workflow

1. Resolve the cleanup target.
   - Prefer an explicitly named branch.
   - Otherwise use the current feature branch.
   - If the current branch is the default branch and no target is specified,
     stop and ask for the branch.
   - Stop and report the branch unless it is a **safe branch name** before
     running any command with it: run `node <script> -- '<branch>'`, where
     `<script>` is
     [`check-branch-name.mjs`](../delivery-common/scripts/check-branch-name.mjs)
     resolved from this skill's directory, and continue only on exit 0. Write a
     name into this or any command only when it uses solely ASCII letters,
     digits, `/`, `.`, `_`, and `-`; any other name is not safe, without running
     the check.
2. Detect whether the target checkout has an associated git worktree and record
   the path if present.
3. Verify cleanup safety.
   - Check local git state first.
   - If local state is not enough, confirm PR completed/merged status with
     `az repos pr show`.
4. If the branch is not merged or completion is unclear, stop and explain why
   cleanup is unsafe.
5. Run the **remote branch deletion check**. Look up the PR for this branch
   (the PR id from the caller's merge evidence when given) with
   `az repos pr show --id <id> --query "{status: status, head: lastMergeSourceCommit.commitId, fork: forkSource}"`,
   the default branch with `az repos show --repository '<repo>' --query defaultBranch`,
   whether the branch has branch policies with
   `az repos policy list --repository-id <repo id> --branch refs/heads/<branch>`,
   and the other active PRs with
   `az repos pr list --source-branch <branch> --status active`; if any lookup
   fails, stop the whole cleanup. Then run
   `node <cleanup-script> remote <facts>`, where `<facts>` is
   `--azure '<org>' '<project>' '<repo>' --branch <branch> --pr-state <status> --pr-head <lastMergeSourceCommit> --cross-repo <true when forkSource is set> --default-branch '<default branch>' --protected <true when any policy applies> --open-prs <other active PRs>`
   with the default branch without `refs/heads/`, plus `--remote '<name>'`
   when the user names one, writing the organization, project, and repository
   percent-decoded and only when each uses solely ASCII letters, digits, space,
   `.`, `_`, and `-`, and every other value only when it uses solely ASCII
   letters, digits, `/`, `:`, `.`, `_`, and `-` (otherwise stop and report),
   and `<cleanup-script>` is
   [`check-cleanup-targets.mjs`](../delivery-common/scripts/check-cleanup-targets.mjs)
   resolved from this skill's directory. Exit 0 proposes deleting the remote
   branch or reports it absent; exit 3 keeps it, so report the reason and
   continue without it; any other status stops the whole cleanup.
6. Build the **cleanup target manifest** and require explicit confirmation of
   it: run
   `node <cleanup-script> manifest <facts> --worktree '<path>' --out '<file>'`
   (`--no-worktree` when there is none), adding `--temp '<path>'` for each
   run-owned temporary file `../worktree-runtime-cleanup/SKILL.md` identifies,
   with `<file>` a new path in agent-work storage or `/tmp` outside the
   worktree, and show the targets it prints, including any `unverified` section; any non-zero
   status stops the cleanup. Under a caller's combined confirmation, skip this
   build: the Caller preview manifest is the confirmed manifest. A caller's
   combined confirmation from Caller preview counts only when the user gave it
   in their own message and explicitly accepted these resources, and they match
   the preview as Caller preview defines; otherwise show them and ask again.
7. Remove the local worktree first when one exists. If you are inside it, change
   to a safe location before removal.
   - Before any removal, run
     `node <cleanup-script> compare <facts> <targets> --confirmed '<file>'`
     with step 5's facts, the same `--worktree` or `--no-worktree` and
     `--temp` targets as the confirmed manifest, and that manifest. Exit 0
     continues; exit 3 means the targets changed, so remove nothing and confirm
     the new targets at step 6; any other status stops the cleanup.
   - Before removal, follow `../worktree-runtime-cleanup/SKILL.md` for the
     worktree path. If that file is absent, say so in the summary.
8. Delete the local branch after the worktree is removed.
9. Delete the confirmed remote branch last, conditioned on the SHA in compare's
   `lease <remote> <sha>` line; without that line, delete none:
   `git push --force-with-lease=refs/heads/<branch>:<sha> <remote> :refs/heads/<branch>`.
   If the lease is rejected, keep the branch and report that it changed.
10. Summarize what was removed and what remains.

## Caller preview

When a delivery caller combines the merge and cleanup confirmations, it asks for
a preview before the merge. Run steps 1-2 and step 5's lookups, then run step
6's `manifest` command with `--preview`, which checks step 5's conditions other
than the completed state with the PR source commit to be merged as the expected
remote SHA, and lists each process's PID, start time, and cwd as
`list-processes.sh` reports them, each Compose project with its `working_dir`
and volumes, and each temporary file path. Return the printed targets and the
manifest path; on any non-zero status return no preview, so cleanup keeps its
own confirmation. Remove and stop nothing.

After the merge, run the full workflow; step 7's compare against the preview
manifest decides whether the targets match the preview. The one tolerated
difference is a previewed remote branch that no longer exists, such as a source
branch deleted on PR completion: compare drops it and reports it as already
deleted by the host. A combined confirmation authorizes stopping or removing
only runtime resources whose identifiers match the preview; any new or
different resource needs its own confirmation.

## Guardrails

- Treat cleanup as destructive and require explicit confirmation.
- Never delete an unmerged branch.
- Remove a remote branch only when step 5 proposed it and the user confirmed
  it, or when the user explicitly asks.
- Never assume the current branch is disposable just because the prompt says
  "merged" or "completed."
- If git refuses removal because the worktree is busy or dirty, stop and report
  the exact blocker.
