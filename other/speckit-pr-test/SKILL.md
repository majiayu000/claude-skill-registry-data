---
name: "speckit-pr-test"
description: "Test and review a ready PR like a QA engineer before it merges: run the pr-tester subagent, which tests the PR head on GitHub Actions (the PR QA workflow) and reviews it here, post its review and the agent-review commit status, move the story's tracker issue to QA, and drive the fix-and-retest loop until agent-review is success or the repair cap blocks the run. Mandatory between 'mark ready' and 'merge' (Constitution VII); /speckit-auto and /speckit-review run it."
argument-hint: "<PR number> [--dry-run] [--local]"
compatibility: "Requires gh and Node 26; the boot and sweep run on GitHub Actions. --local also needs Playwright's Chromium and Docker or local PostgreSQL/Redis binaries"
metadata:
  author: "george-hutanu"
  source: "project-local — QA step of the PR lifecycle"
user-invocable: true
disable-model-invocation: false
---

## User Input

```text
$ARGUMENTS
```

The first number is the PR. `--dry-run` posts nothing to GitHub or the tracker: use
it for a PR another session owns. `--local` boots the PR on this machine
instead of GitHub Actions: only when Actions is unavailable, or for a PR whose
tester change cannot yet run there. It waits for a `scripts/heavy.sh` slot.
`--run <id>` reviews a PR QA run already dispatched for the head and
finished (the hand-off note's `QA run:` line) instead of dispatching one.

## Why

CI proves the code compiles and its own tests pass. Nobody has yet booted the
change and used it. This step does, on every PR, before it merges. It starts
as soon as the PR is ready and runs beside CI, not after it: the two check
different things, and the merge gate waits for both. It leaves the unit
suites to CI's jobs and the end-to-end suite to its on-demand run and the
release's core flows, rather than running them a second time. Its
verdict is a commit status the merge gate (`pre:bash:merge-gate`) and the Stop
gate (`stop:pr-lifecycle`) read. A push after it ran leaves the new head
without a status, so the test runs again.

## Procedure

1. **Tracker → QA** (skip on `--dry-run`): `speckit-tracker-sync qa`, which also
   sets the PR's one stage label to `QA`. Marking the PR ready already moved
   both to QA (there is no In review stage), so this normally reports
   `unchanged` and only catches a PR that skipped that step. The story and its
   timeline row stay QA for the whole loop.
2. **Carry** (skip on `--dry-run`, or pass it on): when the head differs from
   the last commit with an `agent-review` success by documentation only, the
   verdict carries and no lap runs:

   ```bash
   node .claude/scripts/pr-test/carry.mjs <n>   # 0 carried, 1 needs a real lap (reason on stderr), 2 gh failed
   ```

   Exit 0 set `agent-review` success on the head (`carried from <sha>:
   docs-only change`) and noted it in the PR's Agent review section: go to
   step 5. "Documentation only" is `scripts/docs-only.ts`, the definition CI's
   docs-only skip uses (Markdown outside `.claude/`, `.specify/` and
   `.github/`, or `docs/`). It never carries past a failing verdict, onto a
   head that already has a status, or over any other file, and the merge gate
   re-checks every carry against GitHub before it merges. Exit 1 or 2: go on.
3. **Lap**: `node .claude/scripts/run-state.mjs show --json` — the lap is
   `repair_iterations + 1`.
4. **Test**: invoke the `pr-tester` subagent (Agent tool,
   `subagent_type: pr-tester`) with `PR`, `LAP`, `DRY_RUN` when asked,
   `LOCAL` for `--local` and `RUN` for `--run <id>`. Within the lifecycle the
   run is always given: the agent that marks the PR ready, or pushes a fix,
   dispatches it with `dispatch.mjs <n> --no-wait` and ends, and the tail
   brings `RUN` once the run has finished, whatever CI's state (speckit-auto "The wait"),
   so no agent sleeps on a run. With `RUN` the tester downloads that run
   (`dispatch.mjs <n> --run <id>`) and checks that the flows sent with it
   cover the spec's. Without it, by hand, it dispatches `.github/workflows/pr-qa.yml`
   through `.claude/scripts/pr-test/dispatch.mjs` (`gh workflow run`, the
   run found by the nonce in its title, then `gh run watch`): a GitHub runner boots the PR head with PostgreSQL, Redis
   and MinIO from the PR's own compose file, sweeps the screens, runs its flows
   and the API calls (the unit suites are CI's; the integration suite runs on demand and at release; the end-to-end suite runs on demand and, its core flows, at release), and uploads the
   report and screenshots as an artifact. The
   agent downloads it into its `--out` (through a fresh folder of its own, so
   re-running a lap into the same `--out` is never refused), reviews the diff against the spec and the constitution
   here from the packet `.claude/scripts/pr-test/packet.mjs` writes into
   `--out` as `packet.md` (changed files, requirements touched, the run's
   findings and readiness, the previous lap's marked new, persisting or
   resolved, and only the screenshots that differ from the baseline run),
   which replaces its own reading of the report and the spec: it reads the
   code diff per changed file beside it (targeted `git diff` calls batched
   in one turn, never one whole-PR diff file), and posts with
   `post.mjs`; no secret or LLM step runs in CI. With
   `LOCAL` it runs `.claude/scripts/pr-test/run.mjs` on this machine instead
   (`--local`: one heavy slot, teardown always). QA in CI holds no heavy slot,
   so ready PRs are not queued behind the laptop. Read its report; check the
   status yourself:

   ```bash
   gh api repos/{owner}/{repo}/commits/<sha>/status --jq '.statuses[] | select(.context=="agent-review") | .state'
   ```

5. **Success**: return to the caller, which merges on green CI
   (`node .claude/scripts/pr-test/ci-wait.mjs <n>` with `run_in_background`,
   which prints only the checks that did not pass, then
   `gh pr merge <n> --merge`, then `speckit-tracker-sync finish`). The merge
   gate refuses while any check is failing, running or missing.
6. **Failure**: the implementing agent fixes every blocking finding — a failing
   test first that reproduces it (`/speckit-tests` rules), then the fix — commits,
   pushes, and counts the lap:

   ```bash
   node .claude/scripts/run-state.mjs repair   # exits 1 past SPECKIT_MAX_REPAIR_ITERATIONS (10)
   ```

   Then dispatch the new head's run with `dispatch.mjs <n> --no-wait` and
   end (speckit-auto "The tail"); the next tail comes back to step 2 with its
   `RUN`. A medium or low finding whose fix is small or medium is fixed the
   same way in the lap (test first, counted as a lap), pre-existing or
   adjacent ones included, even when `agent-review` passed; only a large fix
   by the size test in AGENTS.md ("Technical debt a review defers") goes to
   `specs/<feature>/deferred.md`, and every deferred bullet is filed as a
   tracker issue (`speckit-tracker-sync debt`).
   On success, file the lap's deferred findings the same way before merging,
   in the order `/speckit-auto`'s "The tail" step 4 gives (commit the task URLs,
   which step 2 carries without a lap; the new head's own findings, if a lap
   ran, go to the tracker directly).
7. **Cap reached** (`repair` exits 1): the run is blocked with
   `repair-loop-exceeded`. Run `speckit-tracker-sync blocked` with the reason
   (open findings, laps used), comment the same on the PR
   (`gh pr comment <n> --body …`), leave `agent-review` at failure, and stop.
   The PR is never merged at the cap.

## Evidence

Copy `report.md` and `report.json` from the tester's `--out` directory into
`specs/<feature>/pr-review/lap<n>/` and commit them to the private specs
repository (`node .claude/scripts/specs-repo.mjs commit "chore(specs): ST-<n> QA lap <n>" -- <feature>/pr-review`),
failing and passing laps alike: it is not the PR's branch, so the commit makes
no new head and no new lap. Never commit the screenshots: they stay in
`--out`, outside the repo, and in the run's `pr-qa-<n>` artifact (kept 7
days); the report names them and gives the run's URL. The specs repository's
`.gitignore` refuses them under `pr-review/`.

## Never

- Never post on, push to, or set a status on a PR you were asked to dry-run.
- Never set `agent-review` by hand; only the PR QA workflow sets it, from
  its run (the only writer in a cloud session), `post.mjs`, from a report,
  and `carry.mjs`, from a verified docs-only carry. The merge gate traces
  who wrote it (`provenance.mjs`): a PR that changes `pr-qa.yml` needs a lap
  dispatched on `main` from the laptop.
- Never merge with `agent-review` missing or failing on the head commit.
