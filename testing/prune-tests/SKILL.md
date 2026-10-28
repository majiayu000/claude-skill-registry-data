---
name: prune-tests
description: Delete low-signal tests (tests that restate the code, always pass, or break on every refactor) one test area at a time, keeping coverage, and open one PR per area. Every run takes an area no earlier run touched.
disable-model-invocation: true
argument-hint: "[count 1-10] [test paths or product areas]; defaults to one cycle on the weakest area found"
---

# Prune Tests

Each **cycle** takes one test **area** (a test directory, or the tests for one module), deletes every test in it that would not catch a real bug a stronger test misses, proves coverage held, and opens one PR. One cycle, one area, one PR.

The goal is a smaller suite that protects behavior, not a large suite that protects coverage numbers. A test stays only when it passes the value gate in `tdd`'s [testing best practices](../tdd/references/testing-best-practices.md). That file is the one source for what a good test is. Read it before the first cycle.

Invoking this skill gives the same authority as `sweep`, per cycle: a branch and worktree, commits, pushing that branch, and opening and labeling its PR. It does not authorize merging or pushing to the default branch.

## Every run finds new ground

Runs repeat on the same repo, and earlier PRs stay open for days. Treat earlier work as `sweep` does: an open, merged, or declined `prune-tests/*` PR rules out its files. It never ends the run. Move on to the next area.

**The keep rule beats the quota.** A test that passes the value gate stays, however short of the target the cycle falls. An area whose tests all earn their place ends with no PR and a report of what was examined. That is a correct result.

## Arguments

Parse these before any discovery. On invalid input, stop and report it.

- **Count:** one whole number from 1 to 10. Without a count, run 1 cycle. Treat a count above 10 as 10, and say so.
- **Areas:** every other token. A path restricts cycles to tests under it. Any other word is a product area (`billing`): confirm by search that it names real code, otherwise stop and report it. With no areas, every test qualifies.

## 1. Load context and known work

1. Read `AGENTS.md` / `CLAUDE.md` and the rule files they point to. Find the test runner, how the repo runs coverage, and its test layers (unit, integration, feature, E2E).
2. `git fetch origin`. Resolve the default branch.
3. Save the ledger, then query it by path, never whole (`<scratch>` is the session scratchpad, otherwise `$TMPDIR`):
   ```bash
   bash <this-skill-dir>/../sweep/scripts/known-work.sh --prefix prune-tests > <scratch>/known-work.json
   ```
   Query it the way `sweep`'s step 1 shows.

## 2. Pick one area

Rank the in-scope test files by smell density: mock-heavy setups, assertion-free tests, snapshot or copy assertions, tests named after methods rather than rules, many tests on one small class, unit tests for code a feature test already drives. Take the densest area that no ledger PR touches (an open PR on any of its files covers it). Keep the area reviewable: up to about 40 test files.

## 3. Baseline

Work in a worktree from the fetched base, per `sweep`'s step 3.1, with the branch `prune-tests/<area>` (not in `taken_branches`).

1. Run the area's tests. **A failing test is never deleted.** Write it to `.scratch/prune-tests/findings/<YYYY-MM-DD>-<topic>.md` in the main checkout as a possible product bug, and leave it alone.
2. Measure coverage of the area's **production owners** (the code its tests exercise). Run the full suite, or, when that is too slow, the area plus every test file that names an owner. Use the same test set again in step 5. Record the number and the command. Without a coverage driver, say so and record covered lines from the runner's own output, or the owners' line list, instead.

The baseline is done when you have the test count, the pass/fail list, and the coverage number with its command.

## 4. Audit every test

Give every test in the area a disposition from the value gate: **Keep**, **Rewrite**, **Move**, or **Delete**, with one line of evidence. A Delete names its reason. When it duplicates a stronger test, it names that test by `file:line`. Read each test and its production owner. A test's name is not evidence. Before you mark a test Delete because it asserts presentation, run `git log` on it: a test that a fix commit added guards that bug, and it stays.

Fan the audit out when the area has more than about 10 files. In Claude Code, dispatch the `leek-skills:test-auditor` agent, one per batch of about 8 files, in parallel. In Codex, use `spawn_agent` with the same brief, then `wait_agent`. Otherwise audit inline. The brief: the batch, the area's other test layers to search for stronger tests, and the value gate file. Check each returned Delete yourself before acting on it. A Delete whose stronger test you cannot find becomes a Keep.

The audit is done when every test in the area has a checked disposition.

## 5. Prune and verify

1. **Delete** each Delete. Remove what only those tests kept alive: fixtures, helpers, test-only exports or wrappers in production code. Record each production line removed.
2. **Rewrite** only when it is small and stays in the area (a circular oracle becomes a literal, a mock of an owned class becomes the real class). Break the behavior it claims in production code, watch it go red, then restore the code. Note a larger rewrite or any **Move** as a findings file instead.
3. Run the area and the whole suite. Every test that passed at baseline still passes.
4. Measure coverage again with the same command. It must stay within 2 percentage points of the baseline. If it falls further, find the lines that lost coverage first. A real branch that a deleted test hit only by accident gets its own test now. For the rest, restore deleted tests, the weakest-reasoned first, until it holds. A restored test is a sign that the test protected something; say so in the PR.

**Target:** remove at least 20% of the area's tests. When the value gate keeps more, the PR says why per kept group, never "they looked fine".

## 6. Submit and finish

Follow `sweep`'s [references/submit.md](../sweep/references/submit.md) with `prune-tests/<area>` for `sweep/<topic>` and `--prefix prune-tests` on every ledger run. The PR's label is `test`. The body adds a table of removed tests, each with its reason, plus coverage before and after, with the command, and production lines removed.

Run cycles one after another, each from a fresh fetch and ledger. Clean up per `sweep`'s [Clean up](../sweep/references/submit.md#clean-up), with `.scratch/prune-tests/findings/` kept.

At the end, check the repo's `AGENTS.md` for the rules in [references/agents-rules.md](references/agents-rules.md). If no rule of that kind is there and no ledger PR adds one, open one more PR, `prune-tests/agents-rules`, that adds them. It does not count toward the cycle count.

Report one entry per cycle: the PR link, tests removed and kept (with the kept reasons), production lines removed, coverage before and after, checks, findings files, and anything you were unsure about. For a cycle with no PR, say what it examined and why nothing qualified. Start each entry with ✅ PR opened or ⚠️ no PR.
