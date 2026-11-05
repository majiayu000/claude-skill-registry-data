---
name: tk-merge
description: Open the merge stage -- per PR in dependency order, fast-forward master onto the reviewed green head, push it, retarget stacked children, delete the branch, close the issue and delete its plan. Invoked by the owner after reviewing the diffs; the invocation is the owner's yes on the code.
disable-model-invocation: true
argument-hint: "[#n ... , issues or PRs to merge; empty means every PR of this session's unit]"
---

# /tk-merge -- the merge stage

Run `/tk-workflow` first. An argument, when the owner gave one, is:

<issues>
$ARGUMENTS
</issues>

The PRs to merge are those of the issues the argument names (an issue
number or a PR number), else those the build-stage message of this session
names. With neither, stop and ask.

## Entry check

Current branch: !`git branch --show-current`

Working tree (empty means clean):

!`git status --short`

Master vs origin, commits ahead / behind (0 0 means in sync):

!`git fetch -q origin 2>/dev/null; git rev-list --left-right --count master...origin/master`

Plans on this machine:

!`grep -H -E -r --include='*-plan.md' '^(Issue|Branch|Base|Thread|Status):' .plans 2>/dev/null || echo none`

Open pull requests, with the head SHA and the state of each check on it:

!`gh pr list --state open --json number,headRefName,baseRefName,headRefOid,statusCheckRollup --jq '.[] | "#\(.number) \(.headRefName) -> \(.baseRefName) \(.headRefOid[0:12]) \([.statusCheckRollup[]? | "\(.name)=\(.conclusion // .status)"] | join(" "))"' 2>&1 || true`

CI workflows in the tree (empty means no CI):

!`ls .github/workflows/ 2>/dev/null || true`

The tree is clean, master is in sync with origin, and for each PR to merge:
it is open; its head SHA on GitHub is the local branch's head (`git
rev-parse <slug>`); and with CI in the tree, every check on that head is
`SUCCESS`, `SKIPPED` or `NEUTRAL`. The checks are read from the list above
or from `gh-watch.sh <sha>` (exit 0), never from the conversation: a
build-stage message that says green is a claim, and GitHub is the evidence.
Anything else (a dirty tree, a head that differs, a check `IN_PROGRESS`,
`QUEUED` or `FAILURE`, a PR whose base is a branch not being merged in this
run) is a stop for that PR and for every PR stacked on it; say which, and
the owner decides. The others proceed.

## Step by step

For each PR, in landing order (a PR after the PR its base branch belongs
to):

1. Make it a fast-forward. When master moved since the branch was cut (an
   independent PR merged before it), `git merge-base --is-ancestor master
<slug>` fails: rebase it onto master (`git rebase master <slug>`), then
   `git range-diff master <old head> <slug>` must show every commit
   unchanged in content. A conflict, or a commit whose content changed, is
   a stop: the reviewed code is no longer the code that would merge.
   Otherwise `git push --force-with-lease`, and with CI wait for the new
   head with `gh-watch.sh` (exit 0; exit 3 means rerun with the same SHA)
   before going on. A stacked PR whose
   parent was fast-forwarded in this run is already a fast-forward.
2. Fast-forward and publish, with the github skill's "Fast-forward merge":

   ```
   git checkout master
   git merge --ff-only <slug>
   git push origin master
   ```

   No merge commit, ever. A rejected push (origin moved, a ruleset that
   wants checks this head lacks) is a stop: report it; never force.

3. Verify: `gh pr view <n> --json state -q .state` is `MERGED`. When it is
   not, report it and leave the PR, the branch and the issue as they are.
4. Retarget every open PR whose base is this branch, before the branch
   goes: `gh pr edit <child> --base master`.
5. Delete the branch locally and on origin: `git branch -d <slug> && git
push origin --delete <slug>`.
6. Close the issue: `gh issue close <issue> -c "Landed in #<n>"`.
7. Delete the plan: `rm .plans/<slug>-plan.md`. Every reason it carried is
   in the code or the documents; the build stage's check made sure of that.

Close with one line per PR: `<slug>: #<pr> merged, <n> commits, <first
sha>..<last sha>, issue #<issue> closed`, plus "rebased first" when step 1
rebased, and one line per PR that stopped, with the reason.

Correct: logging (#20) and metrics (#21, stacked on logging) are green and
approved. You fast-forward master to logging's head, push, see #20 MERGED,
retarget #21 to master, delete `server-logging`, close #12, delete its
plan; metrics is now a fast-forward of master, so you merge it the same
way.

Incorrect: you delete `server-logging` before retargeting #21, and GitHub
closes #21. Or: the build-stage message said green, the list shows a check
`IN_PROGRESS`, and the merge runs on the message. Or: the push is rejected
and you retry with `--force`.
