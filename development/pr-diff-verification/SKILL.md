---
name: pr-diff-verification
description: Check that a branch's actual diff matches what its commit messages and any subagent report claim, before the commits leave the machine. Use before `git push` of a feature branch, before `gh pr create` or `gh pr merge`, after a subagent reports "committed N files", after an amend / rebase / force-push, or when a verification report's headline count looks off. Catches "commit log wrote but code didn't make it" accidents. Does NOT read the diff for correctness (that is a Code Reviewer's job) nor own gh / PR mechanics (github-contribution-workflow).
allowed-tools: Bash(git show *) Bash(git diff *) Bash(git log *) Bash(git reflog *) Bash(git rev-parse *)
---

# PR Diff Verification

## When to invoke

Before:
- `git push` of a feature branch (especially after subagent return)
- `gh pr create`
- `gh pr merge` (final sanity)
- Force-push (`--force-with-lease`) of a rebased branch

Skip when: pushing a single trivial commit you authored line-by-line in the current session and didn't amend.

## The pattern (3-step verify)

### Step 1 — read the commit message claims

For the HEAD commit (or all commits on the branch since base), extract concrete claims:
- "modifies X" → look for X in the diff
- "adds Y" → look for `create mode 100644 Y` in the `--summary` output
- "deletes Z" → look for `delete mode 100644 Z` in the `--summary` output
- "renames A → B" → look for `rename dir/{A => B} (NN%)` in the `--summary` output
- "fixes N+M lines" → diff total should be in that ballpark

### Step 2 — compare against actual diff

```bash
git show --stat --summary HEAD                    # for single commit
git diff --stat --summary origin/main...HEAD      # for branch cumulative
git log --oneline origin/main..HEAD               # for commit count
```

`git diff` takes three dots (`origin/main...HEAD`, diff against the merge base — otherwise
commits landed on `origin/main` since the branch forked also show up in the stat);
`git log --oneline` keeps two dots (`origin/main..HEAD`, commits reachable from HEAD but not
from `origin/main`).

Plain `--stat` only prints `path | N +-` per file; the `create mode` / `delete mode` /
`rename A => B (NN%)` lines only appear with `--summary` added.

For each concrete claim, grep the stat output. If the claim mentions a path that doesn't appear in the stat, that's a discrepancy — investigate before push.

### Step 3 — surface discrepancies

| Symptom in stat | Likely cause | Recovery |
|---|---|---|
| Total LOC far off the claim (e.g. `+50/-3` vs "1-line fix") | `git commit --amend` or a rebase squashed the wrong content | Inspect `git show` on the commit; re-amend or split it |
| File count doesn't match (`0 files changed` vs "refactored X module") | A worktree wipe lost commits before push | Restore from reflog (`git reflog \| grep <SHA>`); re-dispatch if truly unrecoverable |
| A named file (e.g. `Foo.swift:42`) is missing from the stat | Subagent's report claimed work that never got committed | Cherry-pick from a sibling branch, or re-apply the edit manually |
| `git log --oneline` shows a different commit count than expected | Unintended squash, or a force-push from another branch overwrote this branch's commits (the "push wrong ref" footgun) | Re-dispatch the subagent with explicit recovery instructions |

## Failure modes seen in practice

**"Commit log claims work, diff doesn't show it" (general pattern)**: this class of mistake recurs when (a) `git commit --amend` after partial revert loses hunks but keeps the original message, (b) force-push from a stale branch overwrites newer commits, (c) subagent returns a structured "I committed X" report but the commits never made it to the branch ref due to worktree wipe before push. Each failure mode is caught by the same single check: `git show --stat --summary HEAD` vs. the commit body.

**Real-world example — wrong ref pushed**: a subagent reported "1 commit a547d70 with all the changes"; Leader pushed `worktree-agent-XXX:feat/feature-phase1` and discovered post-push that the wrong ref was pushed (the worktree-agent ref was at main SHA; the actual feature commits were on a different local branch). Required force-push recovery from reflog.

## Anti-pattern this prevents

- **Lying commit log + invisible diff**: code review reads the message and assumes the code matches. Trust is misplaced; defects ship.
- **Force-push wrong ref**: `git push origin worktree-agent-X:feat/Y` pushes worktree-agent-X's HEAD to remote feat/Y. If worktree-agent-X doesn't have the commits (because they were committed to a different local branch by the subagent), remote feat/Y gets reset to whatever worktree-agent-X is at — usually main SHA.

## Integration with commit discipline

This skill starts after commits exist; it does not prescribe commit granularity. It is the POST-commit verification step — confirms the commits that survived actually contain what the message claims.

## Heuristics for "what to check"

The four symptom patterns are in the Step 3 table above — those are the cheap signals to
scan for. Don't deep-read diffs as part of this skill — that's Code Reviewer's job. Just
confirm the SHAPE matches the claims.

**A verification/acceptance report's own summary numbers need the same check.** This failure
mode recurs often enough to warrant its own check: a report's headline count ("N items
verified", "M files changed") doesn't match its own itemized table below it. Before trusting
or forwarding such a report, re-count its table rows yourself and compare against the summary
line it prints — don't take the summary number on faith just because it's inside a
"verification" document.

## Example application

```
Subagent returns: "3 commits, 11 files, +265/-272 LOC, all 7 wiring tests pass"

Leader runs:
  git log --oneline origin/main..HEAD   # should show 3 commits
  git diff --stat origin/main...HEAD    # should show ~11 files, ±540 line tags

If git log shows 1 commit (subagent squashed without saying) → OK if intentional
If git log shows 0 commits (commits lost to worktree wipe) → STOP, recover, re-push
If git diff --stat shows different file count → investigate
```

## Related skills

- `github-contribution-workflow` — routes diff-vs-commit verification here before push/PR; that skill owns the gh CLI mechanics, this one owns the post-commit sanity check.
- Official sources: when verifying or updating a factual or version-sensitive claim, read `references/official-docs.md`.
