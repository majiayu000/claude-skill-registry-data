---
name: repo-cleanup
description: "Manually invoke repo-cleanup to tidy a local Git repository: remove branches fully merged into main and their clean worktrees, inspect working directories, propose atomic commits, and review Git stash and IntelliJ IDEA shelves. Run only when the user explicitly invokes this skill; never select it automatically during development or after another task."
disable-model-invocation: true
---

# Repository Cleanup

Run only on the user's explicit invocation. Scope the run to the selected repository and its linked
worktrees. A normal invocation authorizes the eligible local branch and worktree removals below;
announce the concrete candidates and proceed without another confirmation. `audit`, `dry-run`, or
`report only` means inspection and proposals only, with no fetch or other mutations.

Creating commits, applying or deleting stash/shelf entries, deleting remote branches or tags, and
discarding files require separate explicit instructions. Propose atomic commits by default.
Never turn a request to create or edit this skill into a cleanup run.

## Establish scope and baseline

1. Resolve the repository root, common Git directory, current worktree and branch. Read repository
   guidance and any branch retention rules. Record the initial status, branch tips and worktree paths
   so the final report can distinguish existing work from cleanup actions.
2. Use `refs/heads/main` as the integration target unless the user specifies another branch. If it is
   absent, resolve the intended target from repository guidance or ask; do not silently use `HEAD`.
   Record its full commit ID. Protect the target, the current branch, the remote default branch's local
   counterpart, branches used as upstreams by retained local branches, and documented long-lived
   branches such as release/maintenance branches. Do not infer obsolescence from age or branch name.
3. Inspect the target's upstream and remote configuration. In cleanup mode, fetch the relevant remote
   target without pruning refs/tags, recursing into submodules, or updating local branches. Avoid
   arbitrary configured refspecs that write local heads. Do not pull, merge, rebase, switch branches,
   or push. Report ahead/behind/divergence between local main and its upstream. Require candidates to
   be contained in both local main and the refreshed upstream when one exists. A behind main may
   leave extra candidates for a later run; do not update it just to make cleanup succeed.
4. If a configured upstream cannot be refreshed or resolved, history is shallow/incomplete, objects
   are missing, or inspection fails, report the limitation and keep affected candidates. A repository
   with no remote can be checked against local main; label that scope. In audit mode, label cached
   remote information as unrefreshed.

## Inventory before deleting anything

Use `git worktree list --porcelain -z` and `git for-each-ref` to enumerate worktrees, local branch refs,
full tips and upstreams. Preserve paths with spaces/newlines using NUL-aware parsing; do not parse
human-oriented `git branch` output or pipe names into `xargs` for deletion. Quote arguments, use fully
qualified refs for revision checks, and use `--` where supported.

Inspect every accessible worktree, including the current one:

```sh
git -C "$worktree_path" status --porcelain=v1 -z --untracked-files=all --ignore-submodules=none
git -C "$worktree_path" diff --no-ext-diff --stat
git -C "$worktree_path" diff --no-ext-diff --cached --stat
git -C "$worktree_path" ls-files --others --ignored --exclude-standard -z
```

Read relevant staged and unstaged diffs and untracked files to understand their purpose. Inspect the
directory itself for local artifacts, nested repositories, submodules and IDEA shelves. Ignored files
may include `.env`, local databases, patches and shelves; a clean ordinary status is insufficient.
Do not expose secret values in the report. Check in-progress merge/rebase/cherry-pick/revert/bisect
state using Git-resolved paths, not an assumed `.git/` directory. Treat active sessions, locks and
evidence of concurrent changes as reasons to retain a worktree. If tracked paths use
`assume-unchanged` or `skip-worktree` and their on-disk state cannot be verified, retain that worktree.

Finish the stash and shelf inventory below before removing directories. A failure to read a directory
or inspect its shelf is an unknown state, not evidence that it is empty.

## Decide and perform eligible cleanup

A local branch is eligible only if its tip is an ancestor of the target and it has zero commits outside
the target. For recorded commit IDs, check:

```sh
git merge-base --is-ancestor "$branch_oid" "$target_oid"
git rev-list --count "$target_oid..$branch_oid"
```

Require exit status 0 from the ancestry check and a successful count of `0`. Repeat for the refreshed
upstream target when applicable. A nonzero ancestry status may be an error; do not hide it. PR merge
status, a deleted upstream, identical file trees, or patch equivalence alone do not meet this rule.
Squash/rebase merges can leave original commits outside main: report them as possible integrated
changes requiring a separate decision, and retain them under this skill's default criterion.

Remove a linked worktree only when its branch is eligible and it has no staged, unstaged, untracked
or ignored files, unresolved inspection, in-progress operation, active use, nested repository or
submodule needing preservation. Retain the main worktree, current worktree (including an ancestor of
the invocation directory), locked worktrees and detached-HEAD worktrees. List regenerable ignored
build output as an optional follow-up; do not silently discard it to qualify a worktree as clean.

Before mutations, show a compact list of exact branch names, tips, target ID and worktree paths, with
reasons for keeping others. In audit mode stop at the report. Otherwise:

1. Re-read refs, worktree registrations, status, ignored files, shelf state and activity immediately
   before each removal. If a tip, target or relevant state changed, skip that candidate and report it.
   Do not race another worker or IDE that is actively writing there.
2. Remove eligible worktrees individually with `git worktree remove -- "$worktree_path"`. Do not
   use `--force`, unlock them, or fall back to `rm -rf`. A refusal leaves that candidate retained.
3. Recheck reachability and that a branch is no longer checked out in any worktree, then use
   `git branch -d -- "$branch_name"`. Its own safety check uses the branch's upstream or HEAD,
   so it does not replace the main check above. If it refuses, report the reason and keep the branch;
   do not bypass it with `-D`, `update-ref -d`, or temporary tracking changes.
4. Preview stale worktree metadata with `git worktree prune --dry-run --verbose`. Prune only if every
   entry the command would remove is verified abandoned: no temporarily unmounted drive, moved
   checkout, locked entry, or unpreserved worktree-specific state. Otherwise report the preview and
   leave metadata intact. Never manually delete Git administrative files or lock files.

Do not delete remote branches, prune tags, run `git clean`, reset working copies, expire reflogs, or
run aggressive GC as routine cleanup. Remote-tracking refs with missing upstreams can be reported
as a separate optional prune; their absence says nothing about whether local work was merged.

## Propose atomic commits

For each dirty worktree, group changes by one related behavior or intent per commit. Keep supporting
tests/docs and required generated files with their change. Split unrelated changes in the same file
by hunks; do not group solely by directory or file extension. Preserve existing staging boundaries
while inspecting, and point out when staged changes mix unrelated intents.

Give each proposed commit a message, exact files or hunks, purpose, dependencies/order, and suitable
verification. Include untracked files and deletions; identify local-only artifacts that should remain
uncommitted. If ownership or intent is unclear, mark that group unresolved rather than guessing.
Do not stage, unstage, rewrite, stash, or commit anything unless the user requests execution of the
concrete plan. Existing explicit authorization in the conversation counts; do not ask again.

## Review Git stash

Inspect the repository's shared stash once, not once per worktree. Record each entry's selector, full
object ID, date, message, base commit, changed paths, and staged/unstaged/untracked content when
present. `git stash show --include-untracked --stat` and targeted patch inspection are starting
points; inspect the index parent separately when staging distinctions matter.

Recommend keep, recover into a dedicated worktree, split into atomic commits, or consider dropping
after review. Compare content with current main/work where useful; age and the source branch having
been merged do not prove that a stash is redundant. Preserve binary and untracked payloads in any
recovery proposal. Do not apply/pop/clear/drop during an inspection. If the user later authorizes
specific drops, re-resolve the selectors against recorded object IDs first: stash indices shift.

## Review IntelliJ IDEA shelf

Look for `.idea/shelf` in every worktree and inspect project shelf configuration (including
`ShelfManager` settings when present) for a custom location. Resolve project macros and relative
paths before using them. Restrict discovery to this project and referenced locations; do not scan
unrelated home directories. If the location cannot be resolved, report that and ask for the Shelf
location from the IDE when necessary; absence of `.idea/shelf` alone does not prove no shelves exist.

Inventory shelf metadata, patch files and binary companions, including recycled/already-unshelved
entries that still preserve data. Record description, date, paths, storage location and recoverability.
Flag missing payloads or unresolved references. Recommend keep, recover, compare with current work,
or consider deleting after review, using the same content-based reasoning as stash.

Never unshelve, edit shelf XML or delete shelf files during routine cleanup. Any shelf payload inside
a candidate worktree blocks its removal even when Git ignores it. An external shelf must remain
intact, including any payload references back into a candidate directory. Moving or deleting shelves
is a separately authorized operation through the IDE where possible; verify the complete payload at
its new location before removing any original.

## Final report

Re-enumerate refs/worktrees and recheck status. Confirm the current branch/HEAD, index and working
files, protected refs, stash object IDs and shelf contents were preserved unless separately authorized.
Report actual removals, retained candidates with reasons, target freshness, atomic commit proposals,
stash/shelf recommendations and any incomplete checks. Include deleted branch names and recorded
tips so they can be recreated while those commits remain reachable from main. Do not report a
repository as clean when unresolved or unreadable state remains. A second unchanged run should have
no further eligible removals.

Reference semantics when needed: [Git branches](https://git-scm.com/docs/git-branch),
[worktrees](https://git-scm.com/docs/git-worktree), [stash](https://git-scm.com/docs/git-stash), and
[IDEA shelving and custom locations](https://www.jetbrains.com/help/idea/shelving-and-unshelving-changes.html).
