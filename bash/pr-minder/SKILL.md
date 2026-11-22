---
name: pr-minder
description: >-
  One manually invoked remediation pass over the open PRs of the repo you are standing in. It moves
  each eligible PR one step toward landing or a clean exit, with remediation scaled to real
  author-activity age: nudge, repair, decide, retire. Plan-only by default; --apply updates behind
  branches, sets pr-minder's own labels and keeps one owned comment per PR. Never merges, closes,
  rebases, force-pushes or retargets. Trigger on /pr-minder, "mind the PRs", "which PRs are going
  stale", "nudge the stale PRs". Not a daemon and not multi-repo; landing stays with /merge-cleanup.
---

# pr-minder

One pass over **this checkout's** GitHub repo. No scheduler and no other repos. Run it when you want it.

```bash
python3 "$PR_MINDER" --repo-root "$PWD"              # plan only: the table; writes nothing to GitHub
python3 "$PR_MINDER" --repo-root "$PWD" --apply      # perform the eligible writes
python3 "$PR_MINDER" --repo-root "$PWD" --pr 1494    # one PR (its stack is still walked)
python3 "$PR_MINDER" --repo-root "$PWD" --explain 1494   # inputs, rung, chosen action, why
```

`$PR_MINDER` is this skill's `scripts/pr_minder.py`. It reuses two installed bundles instead of copying
them: weekly-planner's `planner_core.py` and merge-cleanup's `merge_cleanup.py`. It finds them through
`PLANNER_ENGINE` / `MERGE_CLEANUP_DRIVER` (absolute script paths), then the repo layout
(`skills/3-weekly/...`, `skills/2-daily/...`), then a flat install (`../weekly-planner/scripts`). This
matches daily-planner's drift-prevention contract.

**Always show the plan output to the operator before running `--apply`.** `--apply` writes to other
people's PRs.

## Age is author activity, not `updatedAt`

A PR's age is the time since its last commit, review, review-thread comment, or comment without the
`<!-- pr-minder` marker. Label changes and metadata edits don't count. GitHub server-side branch syncs
don't count either. A sync is a two-parent commit committed by `noreply@github.com` with headline
`Merge branch '…' into …`. Receipts are not trusted for this: an author push landing between an update-branch and the head re-read would otherwise be hidden. That predicate also
matches a human clicking "Update branch", and a web-editor conflict fix that kept the default message.
Such a PR can look staler than it is. `/daily-planner`'s Stalled report uses the same clock.

If a PR's history is incomplete or unreadable, that PR is **unknown** and gets no writes.

## The ladder

Rung floors use `S = --stale-days` (default 3). Drafts are shifted by `--draft-stale-days − S`
(default +4).

| Rung | Age ≥ | Behind, merges clean | Conflicting | Checks failing |
|---|---|---|---|---|
| 0 fresh | 0 | — | — | — |
| 1 nudge | S | `update-branch` | comment: conflict files | comment: failing check name + link |
| 2 repair | 7d | `update-branch`, label `pr-minder:stale` | label + comment with a repair command | label + comment |
| 3 decide | 14d | label `pr-minder:decide` + comment (no update-branch) | label + comment proposing a re-cut | label + comment |
| 4 retire | 30d | report only | report only | report only |

- Precedence is held > unknown > conflicting > failing > behind.
- Drift beyond `--drift-bump` (default 30 base commits) moves a PR up one rung, but never from 0 and never into 4. On a busy base, raise `--drift-bump`.
- At most one `update-branch` per PR per pass, and at most 2 per stale episode. After that the PR keeps aging.
- No `update-branch` for drafts or for fork PRs without maintainer edits. Those get the comment instead.
- One owned comment per PR (marker `<!-- pr-minder:v1 -->` **and** written by the operator running pr-minder; the marker text alone is public), edited in place. PR- or CLI-controlled text in comments (file names, commit headlines, check names, update-branch errors) is rendered only inside code spans, with backticks and newlines stripped, so it can't produce links, mentions or formatting. Check URLs are shown only if they are plain `https://`. A `pr-minder:*` label is removed only when a receipt proves pr-minder added it. A label added by hand, or from another device, is kept.
- A failed `update-branch` is not retried within the pass; the label and a comment with the failure are posted instead. Every attempt (`ok`, `failed` or `uncertain`) counts toward the 2-per-episode cap.
- New author activity resets the PR to rung 0 on the next pass. pr-minder clears its owned labels and rewrites its existing comment to "rung 0 (fresh)". A PR it never commented on gets no comment.
- **Held PRs are report-only.** Holds are the planner engine's holds, the `hold`/`parked` labels, an `owner decision: hold` body line, or merge-cleanup's `hold_label` veto. A PR stacked on a held PR is also report-only. Otherwise a stacked child is never on a lower rung than its parent.

Failing-check comments give the check name and its link, not the first log line. Downloading job logs per
PR isn't worth it when the link is one click away (GH-1498 spec deviation).

## Safety

- Report-only rows (held, stacked on held, unknown history, rung 4) get no calls at all, not even label cleanup.
- Before each PR's bundle, the PR is refreshed once. The bundle is aborted if the PR is now held (title, body or labels) or if its state, head SHA or base changed. A bundle's writes run back to back within seconds.
- Each write has its own receipt pair, and creating the label in the repo counts as a write.
- Every write records an `intent` line and a `result` line in `~/.local/state/pr-minder/<owner>/<repo>/actions.jsonl` (override with `PR_MINDER_STATE`). The result is `ok`, `failed`, `uncertain` or `aborted`.
- Kill switch: a `paused` file in that directory stops `--apply` before any write.
- One PR's failure does not end the pass. It gets a `failed` receipt, and the exit code is 1 when any write failed, came back uncertain, or was aborted (0 means a clean pass).
- Conflict files come from `git merge-tree` on fetched refs. That touches no working tree, but it does fetch into the current checkout.

## Not this skill

- **Excluded:** merging (`/merge-cleanup`), closing, conflict resolution, rebase or force-push, retargeting stacks, ledger writes, daemons, other repos.
- **Deferred (each needs an operator decision first):** merge queue / batching (#571), auto-closing retire candidates, flaky-job reruns, Jog repair dispatch, per-area PR caps, risk-tier labels.
- **Not authorized:** branch protection or rulesets, `ci.yml` triggers, `/merge-cleanup`'s landing path.
