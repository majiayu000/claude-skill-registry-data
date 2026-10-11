---
name: autopilot
description: Orchestrate unattended resolution of open GitHub issues - triage by complexity, dispatch parallel worker agents into isolated worktrees, review their diffs, open PRs, and monitor CI and CodeRabbit until green. Use when asked to work through open issues autonomously or put Claude on auto-pilot.
---

# Autopilot

You are the orchestrator. You run on Opus, in the main thread. Workers run on Sonnet,
reviewers on Haiku.

**Structural constraint: subagents cannot spawn subagents.** Workers therefore do not
review their own work and do not open PRs. Review and shipping happen here.

**You never merge.** Autopilot ends with green PRs awaiting human review.

## Phase 1 - Triage

```bash
gh issue list --limit 60
```

Read the candidates. Rank by implementation complexity, not by label. Write the ranked
queue to `<repo root>/.claude/temp/autopilot-queue.md` - that directory is tracked and
always exists, so write to it directly rather than creating it (a relative `mkdir` from the
nested project root would make a second, wrong `.claude/`):

| # | Issue | Title | Complexity | Files | Backwards-compat risk |

Defer, with a stated reason, anything that:
- needs a product or design decision the issue does not settle
- cannot preserve backwards compatibility
- depends on an open PR landing first
- is a research question rather than a change

Good autopilot candidates: a reproducible bug with a clear expected behaviour, a missing
test, a documented helper that does not exist yet, a mechanical refactor with tests
already covering it. Bad candidates: anything whose first step is "decide how X should
work".

## Phase 2 - Plan

For the top 3, write a concrete plan each:

- the success criterion - what is observably true when done
- **the failing test to write first**, named, and where it goes
- files to touch
- backwards-compatibility risk, explicitly
- anything the worker should stop and ask about

A worker with a vague plan produces vague work. Be specific enough that it never has to
guess.

## Phase 3 - Dispatch

Workers run in parallel, so each needs its **own checkout** - three agents cannot share one
working tree. Create a worktree per issue, in a directory *outside* the repository so the
build trees and scratch files never collide with it:

```bash
git worktree add <worktrees-dir>/<short-name> -b <type>/<slug> <base>
```

Use the worktree root the user names. If none was given, default to a sibling of the
repository (e.g. `../<repo-name>-worktrees/`) and say which you chose. `<base>` defaults to
`origin/main` unless told otherwise - record whichever value you used, since Phase 5 needs
the same one for `gh pr create --base`. Record the mapping of issue to worktree so you can
find each one again in Phase 4.

Spawn 3 Sonnet agents in parallel, one issue each. Give each: the issue body, its plan, its
worktree path, and its branch name (already created - the worker works in place).

Instruct each worker to follow `work-an-issue` **steps 1 and 3-6 only** - understand, failing
test, instrument, implement, build and test. Skip step 2; its branch already exists. Then
report back with:

- the full diff
- test results with counts
- anything it had to assume

Tell it explicitly: do not review, do not touch docs, do not commit, do not push, do not
open a PR. Those are the orchestrator's.

Builds run at `--parallel 4` (the `build-and-test` skill enforces this). Three unbounded
C++ builds on one machine would thrash every core.

## Phase 4 - Review

For each worker that reported back:

1. Dispatch a **Haiku** agent pointed at the worker's worktree, running
   `project-code-review`. Give it the worktree path, not just diff text -
   `project-code-review` requires searching `tools/` for helper reuse and checking
   `tests/CMakeLists.txt` for registration, neither possible from a diff alone.
2. Dispatch a **Haiku** to run `docs-check` the same way, in the same worktree.

If either turns up findings, send them to the **owning worker** via `SendMessage` rather
than spawning a new agent - the worker still holds all the context about why it wrote
what it wrote, so a fresh agent would just re-derive it at full cost.

Loop until the diff is clean. If a worker cannot resolve a finding after two rounds,
stop on that issue and record it for the report rather than burning turns.

## Phase 4b - Performance check (serialized)

Only for worktrees whose diff touches the simulation hot path (`src/elements/`, `src/simulation/`,
`src/tools/`, `include/tools/math.h`, `include/tools/fft_convolution.h`,
`include/tools/simd_dispatch.h`). Skip the rest and say so.

**Run these one at a time, with every other worker idle.** Three parallel workers make wall-clock
measurement worthless - this is the one phase that cannot be parallelised, and running it
concurrently produces confident nonsense rather than an error.

For each qualifying worktree, use the `perf-regression-test` skill. Because the machine is running
agents, treat the result as advisory: note any delta over 5% in the PR body, and stop on the issue
only past 15% - a delta that large is a real regression regardless of the noise.

An inconclusive result goes in the PR body as unverified. Do not re-run in a loop chasing a clean
number.

## Phase 5 - Ship

Once a diff is clean, from the worker's worktree:

```bash
git add -A && git commit -m "<type>: <lowercase summary>"
git push -u origin <branch>
gh pr create --base <base> --title "<type>: <summary>" --body "<what / why / how to verify>

Closes #<N>"
```

`gh pr create --base` takes a branch name, not a ref - `main`, not `origin/main`. Use
whichever branch Phase 3's `<base>` pointed at.

## Phase 6 - Monitor

Poll each open PR:

```bash
gh pr checks <N>
gh pr view <N> --comments
```

Expect these jobs: `build-and-test-linux` (plus coverage, headless example smoke-run and a
single-process order-dependence check), `sanitizers-linux` (asan-ubsan and tsan),
`build-and-test-windows`, macOS, and `clang-tidy` from Static Analysis. This is not fast -
check roughly every 5-8 minutes rather than tight-looping.

Address failures and CodeRabbit comments by messaging the owning worker. A CI failure that
reproduces locally is a real bug in the change; one that does not is worth reporting rather
than patching blind.

If CodeRabbit hits its rate limit, note it in the report and move on - do not block.

**Stop when checks are green and review comments are resolved. Do not merge.**

## Phase 7 - Report

- PRs opened, with URLs and one line each on what they do
- for each PR: perf verdict from Phase 4b - checked / skipped (with the reason) / inconclusive /
  regression (with the delta)
- issues deferred, each with the reason
- anything that needs a human decision
- anything left mid-flight, and its exact state

Report honestly. A PR that is green because a test was weakened is worse than no PR, and
saying "3 issues done" when one is half-finished wastes more time than it saves.
