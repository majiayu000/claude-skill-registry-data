---
name: consolidate-git
description: "Consolidate and prune stale branches."
version: 1.0.0
allowed-tools: ["Read","Write","Edit","Bash","Grep","Glob","Agent","Skill","AskUserQuestion","TaskCreate","TaskUpdate","TaskGet","TaskList"]
---

# Consolidate Git — Branch + Worktree Cleanup

## Overview

Reduce branch and worktree sprawl to a single clean workstream branch. Every branch and worktree
is inventoried for you (ownership, unique-commit evidence, absorb/delete sequencing).
Unconditional directives (no-unique-commit deletes, clean-worktree removal, prune) execute as you
reach them. Yours to decide: supersession verdicts, conflict resolution, the locked/dirty worktree
pause, and the merge-ready call.

**Consolidation and shipping are separate decisions — this skill never merges to main.** It leaves
one current branch holding all of *my* in-flight work, no sibling branches, no stale worktrees;
shipping is `/merging-to-main`'s call (optionally offered via `merge-ready`).

**Announce at start:** "Using coordinator:consolidate-git to consolidate branches and worktrees
into the current branch; merge to main is separate."

## Compute the Inventory

**On a PowerShell host, use the `.exe` launcher through the call operator** (Shape W), never the
`${...}` POSIX-shell form shown below. Ladder and shapes: `${CLAUDE_PLUGIN_ROOT}/snippets/resolve-coordinator-bin.md`.

`consolidate-assemble brief` (per `${CLAUDE_PLUGIN_ROOT}/snippets/resolve-coordinator-bin.md`)
returns the current-user + branch inventory (ownership category per branch and worktree),
unique-commit evidence per stale branch, absorb/delete directives, and the judgment points below.
It is READ-ONLY — every mutating action surfaces as a directive or a judgment point, never fires
silently.

**Worktrees are not exempt.** One whose tip is reachable from main or the current branch is stale
(a lock is a stale signal, not a veto); a dirty one is a genuine pause.

**Candidates are branches/worktrees owned by the current git identity, plus `cloud-session`
branches** (tip authored by `noreply@anthropic.com`). An `Operator:` trailer equal to your git
email makes it `mine-stale`; without it, or another operator's, it is `cloud-session`, usually the
operator's own in-flight work — absorbing it is this skill's point. Every other owner's branch is
reported under `gates` and never touched.

## Resolve the Judgment Points

**Re-verify against origin before the first mutating action.** `consolidate-assemble brief` is a
snapshot; a concurrent `git reset` can fork local from origin invisibly to a tree-diff. If either
side holds a commit the other lacks (`<branch>` vs `origin/<branch>`), the brief is stale — re-run
it before absorbing, deleting, or merging.

**A commit that looks orphaned mid-run can be a transient merge-base read.** Re-run the
merge-base check after the tree settles and look for a recovering merge commit before treating it
as lost; try the cherry-pick first — an empty result means already applied, never force it.

Each judgment point below carries its own evidence and per-option guidance in the decision
object — decide from it, never invent a verdict the evidence doesn't support.

**`j-delete-<branch>` — zero-unique-commit `cloud-session` branch.** **delete** once its tip is
reachable from main or the current branch and it heads no open PR, which you check with `gh pr list`.
Otherwise **keep**. Before any remote delete, run `git merge-base --is-ancestor <remote tip> origin/<base>`; "a PR merged" is not evidence. A tip with commits outside the base is kept; report its count and SHA. `mine-stale` branches with zero unique commits delete unconditionally; a
`cloud-session` branch always gets a verdict, because its owner is inferred, not proven.

**`j-absorb-<branch>` — supersession verdict.** You get the unique-commit list plus a
`git show --stat` per commit; nothing labels a commit "superseded" for you. Before
choosing **skip**, name the file(s) on the current branch that supersede each commit — "current
branch has a newer version" without a path is a guess, not evidence, and any commit touching a
file the current branch never touched must be absorbed, not skipped. Choosing **absorb** applies
the computed cherry-pick/merge selection (cherry-pick for small counts, merge for large)
via the closed CLI table — you are not hand-choosing the git verb.

**A ref can exist to hold objects rather than changes.** Never resolve a `backup/`- or
`pre-*`-named ref on unique-commit count: name what it insures against, and if unknown, report and
leave it. "Merged into HEAD" is not "safe to lose".

**Conflict resolution (surfaces mid-directive-apply, not as a separate judgment point).**
Inspect conflicting files — if the current branch already supersedes the change, abort and skip
(note it in the report); if needed, resolve and continue. Never force through conflicts blindly.

**Post-absorb re-verify on conflict-resolved shared infra.** For a conflict-resolved file with a
known specific change, confirm its canonical phrase survived; if missing, re-apply it in a
follow-up commit. Weight toward shared files touched by multiple branches.

**`j-worktree-dirty-<path>`.** Worktrees are forbidden, so a dirty one is stray debris to drain,
never state to keep; the question is how to remove it without destroying uncommitted work. Surface
it, never remove silently. **rescue** saves the state (stash or throwaway-branch commit) before
removal; **proceed** discards it when genuinely disposable. Default is pause for a decision.

**`j-behind-main`.** Fires only when the current branch is behind main. **merge-main-first**
ensures the final state includes everything before absorbing; **proceed-anyway** is the branch's
call if a stale main is expected.

**`j-merge-ready`.** Fires whenever any directive or judgment point exists. Offer
**chain-to-merge** only when the branch looks ship-ready (finished, reviewed, no unresolved skips
or flagged dirty worktrees) — otherwise **stop-here**. Phrase it as a recommendation with evidence.

## Report

Summarize per the `branches`/`worktrees` gates: absorbed, skipped (with the
superseding evidence named), deleted (branches + worktrees), and left untouched (other owners).
Close with current branch, ahead-of-main count, and the merge-ready disposition.

## Edge Cases

**On main with no other branches:** abort early — nothing to consolidate.

**Remote branches with no local counterpart:** fetch first, so their commits are inspected
before a remote delete is proposed.

**Cross-device branch reconciliation:** merge, never cherry-pick; verify the merged tree against
EACH parent from a pre-merge baseline.

## What This Does NOT Do

- **Merge to main.** Consolidation lands everything on the current branch and stops; shipping is
  `/merging-to-main`, invoked separately by the PM (optionally recommended via `j-merge-ready`).
- **Rebase** — merges and cherry-picks only.
- **Touch other repos** — scoped to the current repository only.
- **Delete main** — always preserved as the merge target.
- **Force-delete branches** — safe delete (`-d`) only; `-D` needs explicit PM approval if `-d`
  refuses.
- **Touch other people's branches or worktrees** — ownership is tip-commit-author-scoped; every
  non-owned branch/worktree except `cloud-session` is reported, never modified.
