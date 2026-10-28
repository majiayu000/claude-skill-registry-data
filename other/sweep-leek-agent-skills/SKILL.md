---
name: sweep
description: Dig for one problem nobody has noticed yet (a latent bug, silent production error, slow path, or test gap), prove it, fix it, and open one PR per problem. Every run finds something new and never repeats earlier work.
disable-model-invocation: true
argument-hint: "[count 1-10] [focus areas, e.g. 3 refactor performance]; defaults to one cycle over every category"
---

# Sweep

Each **cycle** finds the highest-value issue you can prove, fixes its root cause, verifies the fix, and opens one PR against the default branch. One cycle, one issue, one PR.

Invoking this skill authorizes, per cycle: a branch and worktree, commits, pushing that branch, and opening and labeling its PR. It does not authorize merging, deploying, any production write, pushing to the default or a deploy branch, or deleting a pushed branch.

## Every run finds something new

The skill runs again and again on the same repo. Its PRs from earlier runs stay open for days.

- **Earlier work removes candidates. It never ends the run.** An open PR, a kept `sweep/*` branch, a leftover worktree, or a dirty main checkout is not a reason to stop or to reuse anything. Drop the candidates that earlier work covers, and keep looking.
- **Widen before you give up.** When the top candidates are all covered, go down the priority list and into code that no recent PR touched. Look again at production signals over a longer time range.
- **Never invent.** Pressure to find something new never lowers the evidence bar in [Prove one issue](#prove-one-issue). Do not reword a covered issue, split one fix into two PRs, or promote a style preference or a hypothetical risk. A run that searched widely and found nothing provable ends with no PR and a report of what it examined. That is a correct result.

## Arguments

Parse these before any discovery. On invalid input, stop and report it.

- **Count:** one whole number from 1 to 10. Without a count, run 1 cycle. A second number, `0`, a negative number, or a decimal is invalid. Treat a count above 10 as 10, and say so.
- **Focus areas:** every other token. A quoted phrase is one area: `/sweep "session notes" perf`. With no areas, every category qualifies.

| Focus area | Category |
| --- | --- |
| `bug`, `bugs`, `production` | broken production behavior, user-facing errors, wrong logic or data handling |
| `ci`, `tests`, `coverage` | CI, test, or static-analysis failures; important untested behavior |
| `ux`, `ui`, `accessibility` | interface and accessibility problems |
| `security`, `reliability` | security or reliability problems |
| `performance`, `perf` | measured performance problems |
| `observability`, `errors` | error-handling and observability gaps |
| `refactor`, `architecture`, `dry`, `tech-debt` | maintainability, layering, duplicated logic |
| `polish` | best-practice violations, code smells, minor polish |

Any other area is a **product area** (`billing`, `scheduling`). Confirm by search that it names real code (a directory, model, or domain term), otherwise stop and report it. Categories combine as a union, product areas as a union, and a category plus a product area as an intersection (`perf billing` means a performance problem in billing). Focus restricts what qualifies. It never relaxes the evidence bar.

## 1. Load context and known work

1. Read `AGENTS.md` / `CLAUDE.md`, the rule files they point to, and `.agents/domain.md` when it exists. A repo's list of usually-false review claims also rejects candidates.
2. `git fetch origin`. Resolve the default branch. Every PR targets `origin/<default>`.
3. Save the ledger of known work to a scratch file. `<scratch>` is the session scratchpad where the harness has one, otherwise `$TMPDIR`:
   ```bash
   bash <sweep-skill-dir>/scripts/known-work.sh > <scratch>/known-work.json
   ```
   It holds every open PR, every PR merged in the last 30 days (`--days N` to widen), every PR closed unmerged in the last year, the taken `sweep*` branch names, and earlier sweep findings files. It is large, so query it. Do not read it whole:
   ```bash
   jq -r --arg p <path> '.prs[] | select(.files | index($p)) | "#\(.number) \(.state) \(.title)"' <scratch>/known-work.json
   ```
4. Look at production signals, **read-only**, through whatever connectors exist (Nightwatch, PostHog, Sentry, cloud logs and metrics). Use queries, logs, metrics, and describe/list calls only. Never exec into a container, open a database session, or run anything that can write. Check the app, environment, time range, and deployed revision. A missing source does not block an issue you can prove locally. Report the access limits.

Keep discovery cheap: inventories first, then drill into strong evidence. Do not run the whole suite or every telemetry record without a reason. Baselined static-analysis errors are not failures; one qualifies only when it reflects a real defect.

## 2. Prove one issue

Priority among in-focus candidates: (1) broken production behavior, (2) CI or static-analysis failures, (3) wrong logic or data, (4) significant UX, (5) security or reliability, (6) measured performance, (7) error handling or observability, (8) high-value refactors, (9) code smells, (10) polish. Weigh impact, evidence strength, and fix scope.

**Check every candidate against the ledger** before you spend effort on it. Query each file the fix would touch, then read the title and body (`gh pr view <n>`) of each hit. A candidate is **covered** when a ledger PR addresses the same root cause or makes the same fix:

- Open, any author: covered. Do not compete with in-flight work.
- Merged: covered if current `main` already has the fix. If the problem still reproduces on `main`, the earlier fix was incomplete. Say so in the PR.
- Closed unmerged: covered. Someone declined it. Do not propose it again.

A ledger PR that touches the same file for a different reason does not cover it. A findings file from an earlier sweep is an open lead. You may take it if it still reproduces, and name its path in the PR.

Before you edit, establish all of these, or drop the candidate:

- The concrete failure, the surface it affects, and the impact.
- Evidence that it exists on current `origin/<default>`: a reproducer, a failing test, a log line, or a measured baseline. Reading code and imagining a failure is not evidence.
- The root cause, including the framework, vendor, config, and schema facts behind it.
- A bounded fix and a check that will show it worked.

Drop a candidate that is disproven, covered, speculative, or out of scope, then take the next one. For hard bugs and regressions, use the `diagnosing-bugs` loop.

## 3. Isolate, fix, verify

1. **Branch and worktree.** Name the branch `sweep/<topic>` (one or two words). It must not be in `taken_branches`, and `git ls-remote --heads origin sweep/<topic>` must print nothing (it sees branches pushed since the fetch). If either hits, choose a different word or add `-2`; a name collision never stops the cycle. Always use a worktree from the fetched base, even when the checkout is clean, so the main checkout stays untouched:
   ```bash
   git worktree add -b sweep/<topic> .claude/worktrees/sweep-<topic> origin/<default>
   ```
   From here on, start every command for this cycle with `cd <worktree path> &&` (or use `git -C <worktree path>`). Some harness shells do not keep the working directory between calls, and a bare `composer install` or `artisan make:*` then lands in the main checkout.
   In a Laravel repo, make it runnable with `laravel-herd-worktrees`' **Bootstrap a bare worktree** section before you run anything in it. A scratch database gets a name no checkout config uses, `<app db>_sweep_<topic>`, and you register it when you create it:
   ```bash
   printf '%s\t%s\t%s\t%s\n' "$(date +%s)" <pgsql|mysql|sqlite> <database> "<worktree path>" \
     >> "$(git rev-parse --path-format=absolute --git-common-dir)/scratch-databases"
   ```
   Record each resource the cycle creates (worktree, database, browser session, background process) for [Finish the run](#5-finish-the-run).
2. **Fix.** Look for an existing abstraction first, and reuse or extend it. Make the smallest change that fully fixes the root cause. Keep every edit tied to the one issue.
3. **Prove it.** For a bug, write the regression test first, through the real entry point (HTTP, Livewire, Filament, job, command, observer). It must fail before the fix and pass after; follow the `tdd` loop. For performance, compare measured query counts or timings. For UX, show the interaction on the worktree's running site with `verify`. For refactors and coverage, protect the behavior with tests. Never change production to reproduce.
4. **Checks.** Run the checks the repo requires, in its order, on the changed paths only. Report failures that existed before this change apart from regressions it caused.

**Findings outside this issue** (including severe ones out of focus): write each to the **main checkout** as `.scratch/sweep/findings/<YYYY-MM-DD>-<topic>.md`, with the frontmatter from `.agents/issue-tracker.md` when it exists (`title`, `status: open`, `triage: needs-triage`). Do not fix them, commit them, or open issues for them. `/triage` takes them from there.

## 4. Submit

Follow [references/submit.md](references/submit.md): review the diff, rerun the ledger for PRs opened during the cycle, commit, push, open the PR, label it, and wait for checks.

## 5. Finish the run

Run cycles one after another. Each cycle starts again at [step 1](#1-load-context-and-known-work), from a fresh fetch and a fresh ledger. That ledger includes the PRs earlier cycles opened, so no cycle repeats or builds on another. If a cycle fails after changing code, keep its worktree and stop the run.

At the end, stop the background processes and browser sessions the run started. Then clean up per [references/submit.md#clean-up](references/submit.md#clean-up). Report one entry per cycle: the PR link and labels, the improvement, the verification and check results, and the findings files written. For a cycle with no PR, say what it examined and why nothing qualified. For a failed cycle, say which step failed and what was kept. Start each entry with ✅ PR opened, ⚠️ no PR, or ❌ failed.

The count bounds the run. To run more, invoke `/sweep` again or put it under `/loop`.
