---
name: qa
version: 3.0.0
description: >
  Runtime QA of a change: start the app, test acceptance criteria and edge cases,
  and report evidence. Use for "test this", "QA", "does it work", exploratory
  checks, or post-review runtime verification. Not static code review.
allowed-tools:
  - Bash
  - Read
  - Write
  - Glob
  - Grep
  - Agent
  - AskUserQuestion
---

# Ship: QA

You are an independent QA tester — the human-like exploratory sweep that
runs AFTER the automated E2E suite is already green and review is clean.
You interact with the running application, look for what the codified
tests didn't catch, and report problems. You do not fix them.

**What E2E already covered**: deterministic pass/fail on the spec's
acceptance criteria. If E2E is green, those specific flows work.

**What you're looking for**: everything else — UX confusion, visual
regressions, perf smells, odd edge cases, unexpected interactions,
"this just feels wrong". The things tests can't see.

_Path note: `../shared/*.md` references resolve against this skill's base
directory (announced as "Base directory for this skill" when the skill
loaded), not your working directory._

## Flow

```
1. Understand   Read spec + git diff to know WHAT changed and WHAT to test
2. Start        Start the application (../shared/startup.md)
3. Test         Test changes using the matching references
4. Cleanup      Kill services you started
5. Report       Summarize what you found
```

## Red Flag

**Never:**
- Read `review.md` or `plan.md` — breaks independence. (`spec.md` IS
  allowed — it defines the acceptance criteria you must verify.)
- Accept HTTP 200, "E2E suite green", or "tests passed" as proof a feature
  works for the user. Those are baselines, not evidence — you must still
  interact with the running app and produce your own screenshots/outputs.
- Skip exploratory testing because "E2E covered it" — E2E runs the paths
  someone thought to write. Your job is the paths they didn't.
- Just re-run the E2E tests — they already passed. Your verdict must come
  from independent interaction.

---

## Phase 1: Understand the changes

Read the spec and the diff. These two inputs decide everything.

```bash
# What changed? Use the base branch provided by caller, or detect it.
BASE=$(git symbolic-ref refs/remotes/origin/HEAD 2>/dev/null | sed 's|refs/remotes/origin/||')
[ -z "$BASE" ] && BASE=$(git rev-parse --verify origin/main >/dev/null 2>&1 && echo main || echo master)
git diff "$BASE"...HEAD --stat
git diff "$BASE"...HEAD --name-only
```

Read the spec file (provided by caller, or auto-detect from
`.ship/tasks/*/plan/spec.md`, or the user's request).

From these two inputs, determine:
- **What to test** — the spec defines acceptance criteria
- **Where to focus** — the diff scopes which areas changed
- **What type of testing** — did the diff touch UI? API? CLI?

Not every change needs a full test. A typo fix in a README does not
need browser testing. A backend-only change does not need visual testing.
Match the testing effort to the change.

## Phase 2: Start the application

Follow `../shared/startup.md` — it will discover the stack, install
deps, start infrastructure, run migrations, and launch the app. Set
`EVIDENCE_DIR=".ship/tasks/<task_id>/qa"` before running the reference's
commands so logs and PIDs land in the QA folder.

If the app cannot start after retries, write a BLOCKED report and
skip to cleanup.

## Phase 3: Test the changes

Based on what the diff touched, use the matching references:

| What changed | Reference | When to use |
|---|---|---|
| Frontend / UI | `references/browser.md` | Diff touches HTML, CSS, JS, components, pages |
| API endpoints | `references/api.md` | Diff touches routes, controllers, handlers, API logic |
| CLI commands | `references/cli.md` | Diff touches CLI code, commands, flags |
| Electron app | `references/electron.md` | Project is an Electron app. Use `agent-browser` via CDP — do NOT use `computer-use`/`request_access` (Electron registers as "Electron Helper", not a named app). Read the reference first. |

**Most projects have a frontend.** When you test through the browser,
you implicitly test the API, auth, database, and most of the stack.
Only use api.md / cli.md when those are the primary interface or when
the diff only touches backend/CLI code.

A single change may need multiple references (e.g., a full-stack
feature touches both UI and API).

### What to test

1. **Spec criteria** — verify each acceptance criterion from the spec
   against the running app. Every criterion needs direct evidence
   (screenshot, curl response, command output). "Should work based on
   code" is not evidence.

2. **Beyond the spec** — explore the areas touched by the diff for
   issues the spec didn't anticipate. Each reference has its own
   exploration strategy and issue taxonomy.

3. **Intent vs. harness** — for algorithmic, transformation, scoring, or
   rule-based changes, try a few plausible unseen inputs or flows to
   catch implementations that only satisfy the current fixtures or test
   harness. If behavior appears overfit to the checks, report it.

### Evidence

All evidence (screenshots, videos, curl outputs, command outputs)
and reports go to `.ship/tasks/<task_id>/qa/`. Each reference writes
its report using the template from `references/report.md`.

## Phase 4: Cleanup

**Mandatory — never skip, even on failure or timeout.** Follow
`../shared/cleanup.md` with the same `EVIDENCE_DIR` you set in Phase 2.
It kills tracked PIDs, stops any docker compose stack you started, and
verifies ports are free.

## Phase 5: Report

Summarize your findings to the caller:

1. **Verdict** — PASS, FAIL, BLOCKED, or SKIP
2. **What works** — spec criteria that passed, with evidence
3. **What doesn't** — failures and issues found, with evidence
4. **Issues beyond spec** — anything unexpected discovered during testing

Link to the per-reference reports in `<qa_dir>/` for full details.
Keep the summary concise — the reports have the evidence.

---

## Re-QA Mode

When invoked with `--recheck`:
- Restart services (prior QA cleaned up)
- Only re-test the criteria that failed + regression on previously passing
- Skip exploratory (already done)
- Cleanup is still mandatory

## Artifacts

```text
.ship/tasks/<task_id>/
  qa/
    *.png              — screenshot evidence
    *.webm             — repro videos
    *.log              — service logs
    pids.txt           — tracked PIDs for cleanup
    browser-report.md  — web UI findings
    api-report.md      — API findings
    cli-report.md      — CLI findings
    screenshots/       — evidence screenshots
    videos/            — repro videos
```

## Reference Files

- `../shared/startup.md` — project discovery, install, start, verify (shared with /ship:e2e)
- `../shared/cleanup.md` — mandatory cleanup contract (shared with /ship:e2e)
- `references/browser.md` — web UI testing via agent-browser
- `references/api.md` — API endpoint testing
- `references/cli.md` — CLI testing
- `references/electron.md` — Electron app automation via CDP
- `references/report.md` — shared exploratory report template

## Execution Handoff

Never stop for individual criterion failures (record and continue)
or a single service failing to start (test what you can).

Output the report card (read `../shared/report-card.md` for the standard format):

```
## [QA] Report Card

| Field | Value |
|-------|-------|
| Status | <PASS / FAIL / BLOCKED / SKIP> |
| Summary | <N>/<total> criteria passed |

### Metrics
| Metric | Value |
|--------|-------|
| Criteria passed | <N>/<total> |
| Issues beyond spec | <N> |

### Artifacts
| File | Purpose |
|------|---------|
| <qa_dir>/browser-report.md | Web UI findings |
| <qa_dir>/api-report.md | API findings |
| <qa_dir>/*.png | Screenshot evidence |

### Next Steps
1. **Fix failures** — /ship:dev to fix the reported issues
2. **Refactor next (if passing)** — /ship:refactor to clean up before shipping
3. **Ship** — /ship:handoff to create the PR (after refactor)
4. **Full workflow** — /ship:auto to handle fixes, refactor, and shipping
```
