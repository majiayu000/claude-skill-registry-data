---
name: clean-branches
description: Use when cleaning up local branches, deleting merged branches, pruning stale or gone branches, or tidying `git branch` output. Removes branches whose work has already landed, including squash-merged PRs.
license: MIT
allowed-tools: Read Bash(git:*) Bash(gh:*) Bash(glab:*)
model: haiku
effort: low
compatibility: Requires git; `--delete-merged` needs git 2.56+. Squash-merge detection uses a GitHub (gh) or GitLab (glab) remote
metadata:
  short-description: Delete local branches that are already merged.
---

You delete local branches whose work has already landed, and leave everything else alone.

## Workflow

1. Sync remote state: `git fetch --prune`. Note the current branch and any branches checked out in worktrees (`git worktree list`) — never delete those
2. **Native pass (git 2.56+)**: preview with `git branch --dry-run --delete-merged <remote>`, then run it without `--dry-run`. It deletes branches whose tip is reachable from their still-existing upstream, and honours `branch.<name>.deleteMerged=false` opt-outs. On older git, skip to step 3
3. **Gap pass**: `--delete-merged` deliberately skips a branch whose upstream is gone and a branch with no upstream — which is where most merged PR branches end up once the host deletes the head branch. Build a candidate list from `git branch -vv` (`: gone]` upstreams and branches with no upstream), then keep a candidate only when one of these confirms it landed:
   - `git branch --merged <default-branch>` lists it (fast-forward or merge commit)
   - Its PR/MR is merged — GitHub: `gh pr list --state merged --head <branch>`; GitLab: `glab mr list --merged --source-branch <branch>`. This catches squash and rebase merges, whose commits are not reachable from the default branch
4. Show the combined list with the evidence per branch (e.g. `#93 merged`, `merged into main`) and confirm before deleting. Delete with `git branch -d`; a squash-merged branch needs `-D`, which is safe only because step 3 proved its PR merged
5. Report what was deleted and what was kept, with the reason for each kept branch — closed-unmerged PR, no PR, upstream ahead, checked out

## Keep, don't guess

A branch with a closed-but-unmerged PR or no PR at all may hold unfinished work. List it as kept and let the user decide; never delete it on age or name alone. Remote branches are out of scope — this skill only touches local refs.
