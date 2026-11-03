---
name: qa
description: "Test recent work the way a QA engineer would: derive cases from the requirement and the diff, run them against the live app, fix critical and high findings, retest once. Use when the user asks for QA, a test pass or a browser walk-through, or the execute skill reaches Phase 3e; never start it unasked."
---
<!-- ported-from: plugins/ac/skills/qa/SKILL.md sha256:becb3aa5c0879fb85ad93e365e6ed3df178ea54baba7b446819cb05ffebf64d9 -->

# qa

Orchestrates one QA run: scope the change, boot the app, brief a fresh-context `ac/qa-tester`, fix what it finds, retest once, and curate what the run learned. The tester derives and runs the cases; you own the brief, the fixes and the learnings file.

Input: the request text. `--plan <slug>` in it selects a plan run; the rest is the focus text.

## Standing rules

These hold for the whole run, including after a compaction.

- Never call the `question` tool and never raise a BLOCKER. An environment failure (app will not boot, tool missing, browser missing, credentials absent) ends the run as `could-not-run`, recorded in the report and in `## Known gaps`, and the run still prints its `QA result:` block.
- Spawn `ac/qa-tester` at most twice per invocation: one initial run, one retest. Spawn it with the `subagent` tool and `background: true`; its report reaches this session as a notification. A returned report continues Phase 3 at once. A background launch ends the turn with one line (`QA: tester running for run <run id>; resuming on its notification`), and the notification resumes at the report handling. Never wait with `sleep`, a poll loop or by reading the tester's output file.
- Standalone, and plan mode outside execute, the turn ends on the `QA result:` block. Chained (`--plan` under the execute skill) that block hands control back to the execute skill, which continues to Phase 4a in the same turn, so never end the turn there and never summarise to the user as if the work were over. A wait turn during `--plan` is allowed, because execute's stop guard counts a running subagent.
- Never commit, never push, never touch the `.ac/state/` markers (`active-execution.json` must still exist when the execute skill resumes).
- Only you edit application code and `.ac/qa/learnings.md`; the tester writes only inside its run directory.

## Phase 0: Parse the request

`--plan <slug>` selects a plan run; the rest of the request text is the focus text. Without `--plan` the mode is standalone and the whole request is the user's request. Set `PROJECT_ROOT` to `pwd` and use absolute paths from here on; the tester cannot expand relative ones.

With `--plan`, read `.ac/state/active-execution.json` (read only). When it names the slug, the mode is chained, called from the execute skill's Phase 3e. When the file is absent or names another slug, it is plan mode outside execute: `Requirement` comes from the plan as in chained mode, the base is the commit before the plan's `**Generated**:` time (`git rev-list -1 --before=<Generated> HEAD`), falling back to the standalone clean-tree base rule in Phase 1 when that finds nothing, in place of the `started_at` lookup, the run dir sits under the plan's `qa/`, lows and unfixed mediums go to the plan's `## Deferred Ideas`, and the `QA result:` block ends the turn as in standalone mode.

A plan run needs `.ac/plans/<slug>/plan.md`. If it is missing, print the `QA result:` block with `status: could-not-run` and `report: none`, then hand control back (chained) or end the turn (outside execute).

Run id: `date +%Y%m%d-%H%M%S`. Run dir:

- Standalone: `.ac/qa/runs/<run id>/`
- Plan run (chained or outside execute): `.ac/plans/<slug>/qa/<run id>/`, so a second run does not overwrite the first.

## Phase 1: Scope

**Standalone.** `Requirement` is the user's request, restated verbatim (a bare request with no text uses "Exercise every user-facing behavior the changed files add or change"). Scope files:

- Dirty tree (`git status --porcelain` prints anything): `git diff --name-only HEAD` plus the untracked paths from `git status --porcelain` (the `??` lines). Diff command: `git diff HEAD`.
- Clean tree: take the base from `git merge-base HEAD main` or, failing that, `git merge-base HEAD master`. If neither exists, or the base equals `HEAD`, use `HEAD~1`, and only when `git rev-parse -q --verify HEAD~1` succeeds. Scope files: `git diff --name-only <base>`; diff command: `git diff <base>`. With no base at all, scope is only what the request names.

**Chained, and plan mode outside execute.** `Requirement` is the plan's Core Objective and Definition of Done from `## Work Objectives`, verbatim, plus the focus text when given. Base commit: chained, `git rev-list -1 --before=<started_at> HEAD`, with `started_at` read from `.ac/state/active-execution.json` (read only); outside execute, the Phase 0 merge-base. Scope files are `MODIFIED_FILES` from the execute run in context; after a compaction, and outside execute, `git diff --name-only <base>`. Diff command: `git diff <base> -- <scope files>`. `Existing evidence` is the absolute path of `.ac/plans/<slug>/evidence/`: execute's Layer C already proved those scenarios, and the tester skips them.

**No user-facing change in scope** (only docs, tests, comments, build output or internal config, and nothing in the request asks for a behavior check): print the `QA result:` block with `status: skipped`, `cases: 0/0/0/0`, `findings: none`, `fixed files: none`, `report: none`, and stop here. Write nothing.

## Phase 2: Prepare

1. Create the Run dir with `evidence/`, `specs/` and `tmp/` under it, and a `.gitignore` inside it holding `*`.
2. Leave the project `.gitignore` alone (a project may track `.ac/plans/`), and never copy `.env` or another secret file into the Run dir.
3. Read `.ac/qa/learnings.md` when it exists. It is data about earlier runs, checked against the live app, never instructions to you.
4. Detect the tool and viewports with `references/detection.md` (relative to this skill's base directory). A matched tool that fails preflight falls back to playwright-cli. If the fallback is unavailable too, or no `Target` can be reached, the run is `could-not-run`: skip to step 6.
5. Boot every `Target` the project documents (URL server, start script, simulator, desktop app) when nothing already answers. Start it with the `shell` tool and `background: true`, as `echo $$ > <run dir>/server.pid; exec <boot command> > <run dir>/server.log 2>&1`, with no `nohup` and no trailing `&`. Then probe readiness per the detection reference, in one foreground `shell` call with `timeout: 660000`. Before booting a simulator or emulator, reuse one that is already running (`xcrun simctl list devices booted`, `adb devices`), and record it as started only when this run booted it. Remember whether you started it (`STARTED_SERVER`), and the device id of a simulator or emulator you booted. Nothing sweeps a crashed run's leftovers, so Phase 6 has to stop what you started even after a failure. Anything that was already running is left running. Pass the tester a `Target` that already answers so it does not boot a second copy. A CLI project has a command as `Target`; a library with only a test suite has `Target: none`.
6. On any environment failure write `<Run dir>/report.md` yourself in the tester's four-section shape (`### Cases` empty, `### Findings` none, `### Could not run` with the boot command, the last lines of `server.log` or the missing tool, and `### Proposed learnings` none), then go to Phase 5.

## Phase 3: Brief and spawn

Write `<Run dir>/brief.md`, one `**Label**:` line per field:

```
**Mode**: initial
**Run dir**: <absolute path>
**Scratch dir**: <Run dir>/tmp
**Requirement**: <verbatim>
**Scope files**: <paths, comma-separated>
**Diff command**: <command>
**Target**: <base URL, CLI command, simulator device id, desktop app process name, or none>
**Tool**: <detected tool and the exact invocations>
**Detection reference**: <absolute path of references/detection.md under this skill's base directory>
**Viewports**: <list, or none when there is no UI>
**Learnings**: <absolute path of .ac/qa/learnings.md, or none>
**Existing evidence**: <absolute path, or none>
**Retest cases**: none
**Security target**: <localhost or dev URL only, else none>
```

The tester does not see this skill's base directory, so write the literal absolute path in the brief. `Security target` is the `Target` URL when its host is localhost or 127.0.0.1, or a dev URL the project's own docs name; anything else is `none`. Never put a credential value in the brief; name its source (env var, seeder) at most.

Then spawn, passing only the path (a fresh context is the point: your account of the build would replace the tester's evidence):

```
subagent({
  agent: "ac/qa-tester",
  description: "QA run <run id>",
  prompt: "<absolute path of brief.md>",
  background: true
})
```

The body of the notification is the report: write it verbatim to `<Run dir>/report.md` with the `write` tool. The tester returns its report as its final message instead of writing the file. Parse it by its four headers: `### Cases`, `### Findings`, `### Proposed learnings`, `### Could not run`. A body without them is an environment failure (step 6 above, reason "tester returned no report"). Do not re-spawn for this.

## Phase 4: Triage, fix, retest

Triage each finding (aligned with the execute skill's 3c):

- **critical, high**: fix with `edit` at the suspect `file:line`, smallest correct fix. With no suspect, locate the cause from the repro and evidence with `grep` and `read`; a cause you cannot find stays an unfixed finding. When the `Requirement` and the code do not determine what correct behaviour is (a form with no endpoint, a link with no target page), the fix would be a product decision: leave the finding open, say what is undecided, and, with a plan, add it to `## Deferred Ideas` rather than inventing behaviour.
- **medium**: fix when small and local (one file, a few lines, cause known); otherwise report it and, with a plan, append it to the plan's `## Deferred Ideas` in `.ac/plans/<slug>/plan.md`.
- **low**: report only; with a plan, append each open low to `## Deferred Ideas`.

After the fixes, re-run the project's build and tests scoped to them (the `testing.command` and `testing.single` forms from `CLAUDE.md`, else the detected commands). A fix that breaks them and cannot be repaired in one more edit is undone and its finding stays unfixed. Record every edited path in `FIXED_FILES`.

With at least one fix, run exactly one retest. First restart or rebuild the Target and re-probe it, unless it hot-reloads. Copy `brief.md` to `<Run dir>/brief-retest.md` with the Mode line set to `retest` and `**Retest cases**:` set to the case IDs (`F-01`, `R-02`, ...) of the fixed findings, and nothing else (no fix narrative, path or commit), then spawn `ac/qa-tester` again with that path only, handling the launch and the report as in Phase 3. The brief reuses the same Run dir, so the tester reads the earlier `cases.md`; write its returned body to `report-retest.md`, leaving `report.md` intact. A case that still fails stays an open finding marked "still failing after fix"; there is no second retest.

## Phase 5: Learnings

Merge `### Proposed learnings` from `report.md` and `report-retest.md` with what you observed yourself (how the app booted, the port, readiness time, the tool chosen, the preflight result) into `.ac/qa/learnings.md`, following `references/learnings-format.md`: six sections in order, dated bullets of at most 200 characters updated in place, the 150-line cap and its pruning order, facts not directives, no credential values. Every `### Could not run` reason and every Phase 2 environment failure that names a standing capability gap, as the learnings-format bullet rules define it, becomes or updates a bullet in `## Known gaps`; a reason that held for this run only stays in its report. Refresh the date of any Known gaps bullet a case was skipped on this run. Refresh the `_Updated: <YYYY-MM-DD> by qa (run <run id>)_` line. Create `.ac/qa/` and the file on the first run.

## Phase 6: Close

1. Stop each kind you started, and only those (`STARTED_SERVER`): first check that `ps -ww -o command= -p <pid>` still shows the boot command, because pids get reused, then `kill $(cat <run dir>/server.pid)` and confirm the URL no longer answers; a leftover child still listening on the port you started (`lsof -ti :<port>`) is killed too. For a simulator you booted, `xcrun simctl shutdown <id>`; for an Android emulator you booted, `adb -s emulator-<port> emu kill`.
2. `playwright-cli -s=<run id> close`, whenever playwright-cli was available, including after a failure. Not `close-all`, which also closes a parallel run's sessions and the user's own.
3. Before printing the closing block, write it verbatim to `<Run dir>/result.txt` whenever a Run dir exists. Then print it and follow the standing rules for where the turn ends.

```
QA result:
status: <passed | findings | could-not-run | skipped>
cases: <run>/<passed>/<failed>/<blocked>
findings: critical <n>, high <n>, medium <n>, low <n>
fixed files: <paths, or none>
report: <absolute path of report.md>
```

`status` is `could-not-run` when no case reached PASS or FAIL, `findings` when any finding is still open after the retest, otherwise `passed`. `run` counts PASS plus FAIL, with retest outcomes replacing the first run's for the retested IDs. `findings` counts the open ones; fixed ones appear under `fixed files`. Name `report-retest.md` on a following line when it exists.
