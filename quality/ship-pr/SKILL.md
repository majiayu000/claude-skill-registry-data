---
name: ship-pr
description: >-
  Merge explicitly named pull requests and land them: check mergeable and green checks, gh pr
  merge, sync the primary branch, run the validation gate, redeploy if defined, clean up. Use for
  "merge this PR", "ship this PR", "merge le chantier X", PR numbers or URLs. Never for an unnamed
  PR.
---

# Ship PR

Land one or more already-open pull requests: merge, sync, validate, redeploy, verify, clean up. `adversarial-pr-review` (or `brief-chantier`'s closing lot) gets a PR open and reviewed; this skill gets it merged and live. `commit-session-work` opens its own PR and merges it through this skill.

Invoking this skill authorizes merging the PR(s) the user names, fast-forwarding the resolved primary branch, running the repo's own redeploy script when relevant, and deleting the branches/worktrees/locks that merge made obsolete. It does **not** authorize merging a PR the user didn't name, bypassing a failing or pending required check, force-pushing, rewriting history, or touching branch-protection settings.

## 1. Resolve the target PR(s) — never guess, never scan

The user must name what to merge: a PR number (`36`), a branch name (`chantier/mcp-distant-connecteur-claude-ai`), a PR URL, a chantier slug you can match to a branch, or a list of any of these. If they say "merge the PRs for the X and Y chantiers" without numbers, resolve each via `gh pr list --head <branch>` — but if resolution is ambiguous (no match, or more than one open PR touches the name), stop and ask rather than picking one.

Never call `gh pr list` unfiltered to hunt for mergeable PRs. A PR the user didn't name stays untouched, however ready it looks.

If the user names several PRs, keep them in the order given (or ask if the order matters and isn't obvious — e.g. one PR's branch was created off another's).

## 2. Preflight each PR before merging it

For every target, `gh pr view <n> --json state,isDraft,mergeable,mergeStateStatus,statusCheckRollup,baseRefName,headRefName,headRefOid,url`. Refuse to merge — report why, touch nothing — when:

- `state` is already `MERGED` (skip it with a note, not an error) or `CLOSED` (report, stop for that PR).
- `isDraft` is true.
- `mergeable` is `CONFLICTING`, or `mergeStateStatus` shows a block (e.g. `BLOCKED`, `BEHIND` on a repo that requires being up to date).
- Any entry in `statusCheckRollup` is failing, or still pending and the user hasn't said to wait — a pending check is not a green one.

These are hard blockers, not negotiable by this skill on its own. Forcing a red check through a known flake (`gh pr merge --admin`) is the user's explicit call for that PR, never yours.

Right before each merge, run `node <ship-pr folder>/scripts/review-gate.mjs --repo <owner/name> --pr <n>`. Continue only on exit 0 with output starting `PASS` or `NOT-ENROLLED` (no reviewer calling file), and only while `gh pr view <n> --json baseRefName,headRefOid` still shows the printed `base` and `head`. Anything else blocks. Every review run and re-run of this PR on this head must be green, other PRs' runs count for nothing: only a new commit lifts a red one. A retargeted stacked PR needs a new commit (e.g. merge its base) for a new review.

If the PR's branch has a worktree, run `node <adversarial-pr-review folder>/scripts/review-run.mjs check --repo <worktree> --head <headRefOid>`: exit 1 (FAIL) and 4 (a later finding voided the PASS) mean stop unless the user says to merge anyway. Exit 3 (no verdict, or one for another head) is not a pass: say so in the report and continue.

Confirm `baseRefName` is the repo's actual primary branch (see `PRIMARY_BRANCH` resolution below) — merging into the wrong base is a mistake worth catching before it happens, not after.

## 3. Merge

For each PR that passed preflight, in order:

```
gh pr merge <n> --merge --delete-branch --match-head-commit <head printed by review-gate>
```

Default to `--merge` unless the repo's recent history shows a consistent squash or rebase convention — check `git log --oneline -20 --merges` on the primary branch: merge commits present → `--merge`; none, but PRs landed → match with `--squash` or `--rebase`. When ambiguous, `--merge`: it never rewrites what was reviewed.

`--delete-branch` removes the remote branch in the same call; that cleanup needs no separate authorization.

Record the merge commit SHA (`gh pr view <n> --json mergeCommit`) for the report and for attributing any regression.

**Multiple PRs, one at a time with a checkpoint between them.** After each individual merge, sync the primary checkout (step 4) and run at least the repo's fastest gate (typically `typecheck`) before merging the next one. This is what lets you say *which* PR broke something if one does — merge all three first and you're debugging a pile, not a diff. Stop the sequence at the first PR whose post-merge gate goes red; report it plainly, and don't merge the remaining PRs on top of a checkout you already know is broken.

## 4. Sync the primary checkout

Resolve `PRIMARY_BRANCH` the same way `commit-session-work` does: an explicit repo-policy target if one exists, else `refs/remotes/origin/HEAD`, else local `main` then `master`. Resolve the checkout that owns it via `git worktree list --porcelain`; if none does, work in a scoped `mktemp -d` integration worktree instead of inventing a checkout.

Before pulling, list dirty paths with `git status --porcelain -uall`, then `git fetch`. A dirty path *overlaps* when it is in `git diff --name-only --no-renames <PRIMARY_BRANCH> origin/<PRIMARY_BRANCH>` and its index entry is not already the incoming version (`git rev-parse :<path>` differs from `git rev-parse origin/<PRIMARY_BRANCH>:<path>`; a path absent from both the index and `origin/<PRIMARY_BRANCH>` counts as incoming; `commit-session-work` stages that version). On an overlap, stop and report it with the advice to commit those edits or move them to a work branch first, never stash it. Other dirty paths stay untouched. Then `git merge --ff-only origin/<PRIMARY_BRANCH>`.

If the fast-forward is refused because local primary holds commits origin lacks, run `git cherry origin/<PRIMARY_BRANCH> <PRIMARY_BRANCH>`. Only when every line is `-` (each local commit is patch-equivalent to merged work), `git rev-list --merges origin/<PRIMARY_BRANCH>..<PRIMARY_BRANCH>` is empty and no dirty path overlaps, run `git reset --keep origin/<PRIMARY_BRANCH>`. Otherwise, or if it refuses, stop and report. Never `merge --no-ff`, rebase, force, or push the primary branch: it was never reviewed.

## 5. Validate the integrated result

Run the repo's own validation gate on the now-synced primary branch — don't invent one. Look for it in this order: an explicit instruction in `CLAUDE.md`/`AGENTS.md` (workstation's is `bun run typecheck && bun run build && bun test`, plus a separate `bun run test:hooks` because `bun test` skips dotdirs — other repos will differ), otherwise the obvious `package.json` scripts (`typecheck`, `build`, `test`, `lint`), otherwise whatever `commit-session-work` would have used for this same repo.

A red gate here means the merge broke primary, even though each individual PR may have looked clean in isolation (two PRs can each pass alone and still conflict in combination). Stop before touching deploy — report the failure, name the PR(s) most likely responsible from the per-merge checkpoints in step 3, and leave the rest of this workflow undone rather than pushing forward on a broken build.

## 6. Redeploy, only if it's relevant and defined

Look for a deploy/redeploy convention the repo itself declares — a `redeploy` (or clearly equivalent) script in `package.json`, or a rule file like `.claude/rules/server-deploy.md`. If one exists AND the merged diff touched paths that convention cares about (workstation: `server/**`; generalize by the same logic elsewhere — front-end-only or docs-only changes don't need a server redeployed), run it. If no such convention exists, or the merge didn't touch anything deploy-relevant, skip this step outright — don't invent a deploy step for a repo that doesn't have one, and don't redeploy for a docs-only PR just because the repo happens to have a `redeploy` script.

## 7. Verify health, best-effort

If the repo's docs or rules name a health endpoint or a way to prove new code is live (workstation: `curl` the deployed URL and check for a response only the new code would produce, not just a 200), use it. Otherwise don't fabricate a check: say you redeployed but have no repo-defined way to confirm the new code is served.

## 8. Clean up

- Remote branches: already handled by `--delete-branch` in step 3.
- Local branches for the merged PR(s), if they exist in any checkout: delete them (`git branch -d`, only after confirming the merge commit is an ancestor — never `-D` a branch you haven't proven is fully landed).
- A worktree created for the branch: `git worktree remove`, then `git worktree prune`, following the same retention-proof discipline as `commit-session-work` (never force-remove a worktree with content that isn't provably retained on primary).
- A session-scoped lock file convention if one is in use for this repo (e.g. a `night-run-lock`-style file) and this invocation is the one holding it: release it. Never release a lock you don't know you're holding.

## 9. Report

For each PR: number, review verdict (PASS, FAIL, absent or stale), merge commit SHA, merge strategy used, and whether it was skipped (already merged/closed) or blocked (with the exact reason — failing check, conflict, draft, wrong base). Then: whether the primary checkout was fast-forwarded or realigned, the validation gate's verdict, whether redeploy ran and its outcome, the health-check result (or the honest "no repo-defined way to check" note), and what was cleaned up. If anything stopped the sequence early (a red gate, a blocked PR, an overlapping dirty path), say so first and plainly — a partial run that landed PR #1 but stopped before #2 is a normal, safe outcome to report, not a failure to hide.

## Hard blockers — stop without weakening safety

- A named PR is draft, has a merge conflict, has a failing/pending required check the user hasn't explicitly said to force through, or `review-gate.mjs` refuses it.
- `gh` cannot reach the repository with write permission (404, `Repository not found`). Never `gh auth switch`.
- The primary branch or its checkout can't be resolved safely.
- An overlapping dirty path (step 4).
- The fast-forward is refused and local primary holds a `+` commit in `git cherry`, a merge commit, an overlapping dirty path, or `git reset --keep` refuses.
- The post-merge validation gate is red.
- Git reports corruption or an unresolved conflict during sync.

None of these are worked around silently. Report the blocker and the safest next action; don't ask a clarifying question when the answer is really "stop and tell the user" — reserve questions for genuine ambiguity in *which* PR or *what order*, not for whether to proceed past a red gate.
