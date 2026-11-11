---
name: land
description: Lands a verified, reviewed branch on its base. Takes the repo lock, syncs the base, runs the project gate, merges as the project settings allow, records the merge with a read-back, waits a bounded time for the deploy, closes linked issues, and writes a report with a named verdict. Takes the branch to land (default the current one). Use when asked to "land this branch" or "merge it", or when ship routes a verified, reviewed branch here; not for opening or describing a pull request.
argument-hint: "[branch]"
---

# Land

Take a branch that has passed verify and review onto its base, and end with one verdict a later reader can trust: `landed`, `gate failed`, `not merged`, or `deploy did not run`. Every step either leaves evidence (a sha, a read-back, a probe result) or stops the line and says what it needs.

The agent may start this skill (from `ship` or on the user's ask), because nothing irreversible happens before the merge gate: the reads, the sync push to the branch itself, and the gate run are safe to repeat. The merge itself waits for the user's yes unless the project settings grant `merge: auto`; the always-ask list (public posts, deletes, money, facts about the user) is never granted, so this skill deletes no branch or record (only its own lock file) and posts nowhere public.

## Inputs

- **The branch**: the argument, else the current branch. Its base: the settings, else the remote's default branch, else whichever of `main` or `master` exists.
- **Entry evidence**: the verify report `live-verify-<branch>.md` under `.claude/shipyard/reports/` (a `/` in the branch name becomes `-`, as in every report path) with `Result: pass` and a `Commit:` equal to the branch HEAD at entry, before the sync (an older commit counts as not verified; the gate in step 3 covers the synced tree), unless the settings skip verify for this change (for a change to prompt, skill, or instruction text, the `eval-loop-<branch>.md` report with `Result: pass` for the same commit, when the settings make it the verify evidence); and a clean review: a `pr-review` the user ran and reports clean (or an approved pull request) when the settings name `pr-review` as the review station, or nothing yet when they name the project gate, because step 3 is then the review.
- **Project settings**: on every invocation, read `.claude/shipyard/land.md` in the project root if it exists; its settings win over the defaults here. It names the base and remote, the review station, the gate command, whether merging is `auto`, the merge strategy, where to record the merge, the deploy probe and wait, the manual deploy command, external records to sync, and the issue tracker. Its shape is in [references/overlay-example.md](references/overlay-example.md). Without a gate command, a probe, or a record, the matching step is reported as `not configured`, never improvised.

## Output

The report `land-<branch>.md` under `.claude/shipyard/reports/` (a `/` in the branch name becomes `-`) in the shape of [references/report-template.md](references/report-template.md): the verdict first, then one line per step with its evidence, `Checked:` / `Not checked:`, and `next:`. The same text is the reply.

## Rules

- **One land per repo.** Take the lock (`.git/shipyard-land.lock`, holding the branch, the time, and the session) before anything else and release it on every exit, including failures. Two lands in one checkout race on fetch and push and produce wrong merges; a held lock stops this run with the holder named, and a stale lock (default: older than 30 minutes, no land running) is reported and removed only after a `STOP — WAIT` the user answers.
- **Plain git, clear failures.** Sync, merge, and read-back use plain git as in [references/git-steps.md](references/git-steps.md), never a helper only one host or machine has, so the skill works in any checkout. Each failure the reference lists is reported as symptom, cause, and the exact fix (a missing git identity names the two `git config` commands).
- **The gate runs on the synced tree, and the base must not have moved under it.** After the gate, fetch the base again; if it moved, re-sync and rerun the gate, at most 2 times (settings may change the cap), then stop with `not merged` and say the base keeps moving. A gate run on a stale base proves nothing about the merge result.
- **Merge needs a yes unless the settings say `merge: auto`.** `STOP — WAIT` with the branch, the base, the strategy, the gate result, and the merge sha it will produce or the command it will run. A pick in a menu is not a yes; the user replies to that text.
- **Every write is read back.** The merge: fetch the base and confirm it is the merge sha. The record: read the row or line back. An external record: compare its hash to what was sent. A mismatch is an andon (`H5`): report it, change nothing more, and hand the user the record and the difference.
- **Deploy wait ends in a verdict.** Poll the settings' probe at its interval until it succeeds or the wait `T` (default 10 minutes) elapses; one bounded loop, never an open-ended watch. At `T`, the verdict is `deploy did not run`, the report hands the user the settings' manual deploy command, and this skill does not run that command itself: a deploy that did not start is the human's call.
- **Issues close explicitly.** A `Closes #a, #b` line in a merge message closes one issue on some hosts and none on others, so each linked issue is closed through the tracker's CLI or API, one call each, and the report lists what closed and what did not.
- **An honest stop is the safe outcome.** A conflict, a failed gate, a refused push, or a missing tool ends with its verdict and the evidence; nothing is bare force-pushed (a `rebase` sync pushes with `--force-with-lease` against the sha it fetched, as git-steps shows), retried past the caps, or fixed under the user's name.

## Steps

```
- [ ] 1 Read settings, check entry, take the lock
- [ ] 2 Sync the base into the branch
- [ ] 3 Run the gate; re-sync if the base moved (max 2)
- [ ] 4 Merge (gate)
- [ ] 5 Record the merge and read it back
- [ ] 6 Wait for the deploy, up to T
- [ ] 7 Sync external records, close issues
- [ ] 8 Write the report and release the lock
```

Steps are agent-owned unless marked.

1. **Read settings, check entry, take the lock.** Read the settings. Confirm a clean working tree, a git identity, and the remote (git-steps lists the checks and their fixes). Check the verify report is a pass for HEAD and the review is clean; a gap stops here with the gap named and `next:` the stage that fills it. Then take the lock.
2. **Sync the base into the branch.** Fetch; record the base sha; bring the base into the branch with the settings' strategy (merge by default, rebase when the strategy is `rebase`), in the checkout when it is on the branch and clean, otherwise in a temporary worktree; push the branch so the pull request shows the synced tree. A conflict is `not merged`, `next:` implement, with the conflicting files listed.
3. **Run the gate** from the repo root with the settings' command; capture its exit code and the last lines of its output (complete when it fails, since the reader needs the failure whole). Exit 0 and a base that has not moved: continue. Exit non-zero: verdict `gate failed`, `next:` implement with the output. Base moved: step 2 again, counting toward the cap.
4. **Merge.** `STOP — WAIT` unless the settings say `merge: auto`. Then merge through the code host when a pull request is open and its CLI is signed in (branch protection may require that path), else with plain git in a temporary worktree, pushing the result to the base; a push the remote rejects as not fast-forward means the base moved and counts toward the re-sync cap. Read the base back: it must equal the merge sha.
5. **Record the merge** where the settings say, read it back, and quote the read-back in the report. With no record configured, the report is the record.
6. **Wait for the deploy, up to T**, polling the probe. Success: note the time to live. `T` reached: verdict `deploy did not run`; `HUMAN TRIGGER`: the report hands the user the manual deploy command, step 7 is skipped (records and issues follow a live change), and the run goes to step 8.
7. **Sync external records** the settings list (one call each, hash compared after) and **close each linked issue** (from the pull request, the plan file `.claude/shipyard/plans/<branch>.md`, and the settings) with one call each, reading the state back. Report each as closed, failed, or `not configured`.
8. **Write the report**, then release the lock. The reply is the report.

## Handoff

`next:` `gate failed`, or `not merged` on a conflict or a moving base, goes back to the implement stage with the report's reason; `not merged` because the user declined goes to the pull request's human reviewers; after `landed`, the demo stage when the settings name one, else done; `deploy did not run` is an andon (H5) with the manual deploy command.
