---
name: operating-vitest-agent
description: How to drive the vitest-agent MCP tools correctly — the non-obvious operational facts (run_tests scoping, why subset runs "fail" coverage, the consoleLeaks signal, the VITEST_AGENT_CONSOLE escape hatch, auto-recovered attribution) that otherwise cost trial-and-error.
when_to_use: |
  Load when operating a project through the vitest-agent MCP tools. Trigger phrases: "run the tests via run_tests", "run_tests filter", "how do I scope a run", "why does my single-file run fail coverage", "coverage threshold on a subset run", "consoleLeaks", "stray console output in tests", "VITEST_AGENT_CONSOLE", "how do I run one test file with vitest-agent", "run_tests return shape", "no-match result", "which tests classified as flaky". Also load at the start of an agent session driving a vitest-agent project, before the first run_tests call.
model: sonnet
effort: medium
---

# Operating vitest-agent as an Agent

Read this first when you are an agent driving a project that uses
`@vitest-agent/*`. It front-loads the handful of facts that otherwise cost
trial-and-error. For the full `run_tests` reference (scoping, return shape,
coverage-in-subset, the `consoleLeaks` signal), see
[references/running-tests.md](references/running-tests.md).

## The facts that save the most time

1. **Run tests with `run_tests`, not Bash `vitest`.** `run_tests` persists
   results, classifications, coverage, and history and fires the post-tool-use
   hooks. Shelling out to `vitest` bypasses all of that.
2. **`run_tests` has no `filter` parameter.** Scope with `project` (the Vitest
   project name), `files` (globs), or `tags`. An unknown key like `filter` is
   rejected with an error naming the offending key and the accepted params —
   fix the call and re-run. The `ok` result echoes the resolved `scope`
   (`project`, `files`, `tags`) so you can confirm what actually ran.
3. **Subset runs no longer "fail" coverage thresholds (issue #160).** A
   scoped call (`files`, `project`, or `tags` supplied) is detected as
   partial and the plugin's reporter neutralizes Vitest's native
   `coverage.thresholds` check for that run before it can flip the exit
   code — thresholds compared against the whole-project denominator are
   meaningless against a subset of files. The `ok` result carries
   `scopedNote` (also folded into the text summary) explaining that
   thresholds were skipped and how many of the project's test files
   actually ran; the persisted `test_runs.scoped` flag and
   `report.coverage.scoped` reflect the same signal. Full (unfiltered)
   runs are unaffected — thresholds still enforce and baselines still
   ratchet. The `--coverage.enabled=false` workaround is no longer
   needed for this purpose.
4. **Concurrent Vitest runs no longer clobber each other's coverage
   temp files (issue #194).** Two runs sharing `coverage.reportsDirectory`
   used to `rm -rf` each other's `coverage/.tmp` mid-run — the v8
   provider's `clean: true` default — producing an unhandled rejection or
   a silent exit-0 with no summary. `run_tests` was always isolated (each
   call gets its own `mkdtemp` directory); `AgentPlugin`'s plain-CLI path
   (`vitest run` from the terminal or a script) now isolates too, for the
   `agent` executor only — a human's `./coverage` output and CI's
   configured directory are never relocated. Two env vars tune it:
   `VITEST_AGENT_COVERAGE_DIR_ISOLATION=off|0|false` opts out entirely
   (back to the shared, collision-prone directory); `VITEST_AGENT_COVERAGE_DIR=<path>`
   pins an explicit directory verbatim (no mkdtemp, no cleanup) so an
   orchestrator running several agents can point each one at a directory
   it collects afterward. Persistence (`file_coverage`, coverage
   thresholds/trends) is unaffected either way — it reads the in-memory
   istanbul `CoverageMap`, never the on-disk report.
5. **Stray `console.*` is surfaced by `run_tests` as a signal, not raw logs.**
   The `ok` result's `report.consoleLeaks` field lists writes by file with
   counts, optional per-test attribution, and a truncated sample. `total` /
   `byFile` count only writes from tests that did NOT fail — writes logged
   inside a failing test are excluded from the leak signal and summarized
   separately in `fromFailingTests`, so a red run whose assertion failures
   route through a console-backed logger doesn't look like a leaking green
   run. `run_tests` still null-routes Vitest's stdout; the signal captures
   what was printed without forwarding raw log lines into agent context. To
   see the raw output for a flagged file, run Vitest on the CLI:
   `VITEST_AGENT_CONSOLE=passthrough pnpm test`. Details in
   [references/running-tests.md](references/running-tests.md).
6. **Session attribution is recovered for you.** The SessionStart hook writes
   the `VITEST_AGENT_*` identity into the environment and the SDK recovers it —
   you never set those vars by hand. Beyond identity, the behavioral knobs are
   `VITEST_REPORTER_LOG_LEVEL`, `VITEST_REPORTER_LOG_FILE`, `NO_COLOR`, and
   the `VITEST_AGENT_CONSOLE` output override documented below.
7. **Stale counts mean tests were not re-run**, not a warm cache. Discovery
   re-walks per Vitest run; the MCP serves counts from the database.
8. **Some "leaks" are guardrail tests** that assert on their own output. Do not
   silence output a test captures and `expect`s on.

## Results that lie

- Judge a run by the collected count, never by `0 failed` alone. When
  `collectedModules` is known and nonzero, the totals line carries
  `across N files` — a lower N than you expected means files failed to
  load or were never collected, not that fewer tests existed.
- `0 tests collected` is a warning, not a pass. The agent-facing render
  says so explicitly: *"0 tests collected. A zero-test run usually means
  a wrong working directory, a filter that matched nothing, or a
  load-time error — verify before trusting it."*
- Suite/hook errors (an `afterAll` throw) and load-time collection
  failures now fail the `AgentReport`: `failedFiles` is non-empty and
  `reason` coerces to `"failed"` even when every individual `it` block
  passed. A green summary with a non-empty `failedFiles` means the
  report predates this fix — rerun on a current build.
- Each project's `test_runs.reason` is now derived from that project's
  own report, not the whole-process outcome — one failing project no
  longer marks every project in a `triage_brief` as failed.
  `"interrupted"` still passes straight through as a global outcome (a
  killed run is killed for everyone).
- If stderr shows `vitest-agent: persistence failed — results above
  were rendered but NOT recorded: <error>`, the rendered output you're
  looking at is real but nothing reached SQLite for that run —
  `test_status` / `test_history` will not reflect it until the next
  successful run.
- Always invoke vitest from the absolute repo root in the same command
  (`cd /abs/repo && pnpm vitest run --project …`) — a `cd` for one tool
  silently poisons the next command's project filter.
- Never pipe a vitest invocation whose exit code you intend to read
  (`vitest run … | tail` reports tail's exit code, always 0). Use
  `run_tests`' structured return, or the JSON reporter's `outputFile`,
  for machine-readable results.

## Environment, briefly

You do not configure vitest-agent through environment variables. The
`VITEST_AGENT_*` vars (chat id, conversation id, agent ids, project dir,
sidecar bin) are attribution plumbing written by the Claude Code plugin's
SessionStart hook and recovered automatically. The vars you might set:

- `VITEST_REPORTER_LOG_LEVEL` / `VITEST_REPORTER_LOG_FILE` — diagnostic
  logger (separate from the console reporter).
- `NO_COLOR` — disables ANSI color in rendered output.
- `VITEST_AGENT_CONSOLE=<value>` — overrides the resolved console mode for
  the active executor on a CLI `vitest` run. Console output inside tests
  is swallowed by design; this is the escape hatch to see it raw when
  investigating a file flagged by `report.consoleLeaks`. The accepted
  values are per-executor-slot literal unions (verbatim from
  `packages/sdk/src/schemas/Common.ts`):
  - `human` executor: `passthrough` | `silent` | `stream` | `agent`
  - `agent` executor: `passthrough` | `silent` | `agent`
  - `ci` executor: `passthrough` | `silent` | `ci-annotations`

  A value invalid for the active executor's slot warns to stderr
  (`[vitest-agent:plugin] ignoring invalid VITEST_AGENT_CONSOLE="…" for
  <executor> executor` — `packages/plugin/src/plugin.ts`) and is ignored;
  the plugin falls back to that slot's normal default. This only changes
  what gets *printed* — `console.log` inside a test is still swallowed by
  design in every mode except `passthrough`, so **assertions
  (`expect(...)`), not `console.log`, are the reliable way to read a
  value out of a probe test.**

## Where to go next

| You want to… | Read |
| --- | --- |
| Scope a run, read the return shape, understand coverage-in-subset | [references/running-tests.md](references/running-tests.md) |
| Read the full console-mode matrix (human prose) | <https://vitest-agent.dev/guide/console-modes> |
| The human-facing version of this page | <https://vitest-agent.dev/guide/operating-as-an-agent> |
