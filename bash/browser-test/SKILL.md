---
name: browser-test
description: Test a web app from a start URL and a plain-language prompt. A planner splits the prompt into cases, cheap parallel browser workers run them, and you get one verdict table plus any page errors. Read-only unless the prompt asks for a write and you confirm it.
disable-model-invocation: true
argument-hint: "<start-url> <what to test> (e.g. https://app.test/invoices filters and pagination work)"
allowed-tools: "Bash(agent-browser *)"
compatibility: "Needs the agent-browser CLI and python3 on PATH"
model: sonnet
effort: medium
---

# Browser Test

You coordinate. A planner turns the prompt into cases, and workers drive the browser. You
never click through the app yourself, except to help the user sign in. Nothing changes
data unless the user confirms that exact write in this run.

- Arguments: `$ARGUMENTS`. The first `http(s)` token is the start URL, and the rest is
  the prompt. With no URL or no prompt, ask for the missing one and stop.

## 1. Start the run

From the project root, run `bash ${CLAUDE_SKILL_DIR}/scripts/start-run.sh <start-url>`.
It prints `run_id`, `run_dir`, `origin`, `state` (the auth file for this host), and
`state_exists`. The run directory also holds `scope.json`, which the read-only guard
reads. Sessions are `bt-<run_id>-<tag>`: `plan`, `login`, or the case number.

## 2. Plan

Send the planner this brief, with `STATE` set to the `state` path when `state_exists` is
true, otherwise `none`:

```
START_URL: <start-url>
PROMPT: <prompt, verbatim>
SESSION: bt-<run_id>-plan
STATE: <path | none>
```

In Claude Code with this plugin, dispatch `subagent_type=leek-skills:browser-test-planner`.
Elsewhere, use a sub-agent on a mid-tier model with the rules in that agent's file (and
`verify`'s [Process](../verify/SKILL.md#process) for grouped UI, state reversal, and
calculated reports), or plan inline.

**`NEEDS LOGIN`:** tell the user a browser window will open for them to sign in. Run
`agent-browser --session bt-<run_id>-login --headed open <start-url>`, and wait for the
user to say they are signed in. Then run `agent-browser --session bt-<run_id>-login state save <state>`
and `agent-browser --session bt-<run_id>-login close`, and re-plan with `STATE` set. The
auth file lives outside the repo and never goes in a report. If the re-plan still says
`NEEDS LOGIN`, stop and say so.

## 3. Confirm writes (only when the plan has any)

If no case is `MODE: write`, go straight to step 4; read-only runs never pause.
Otherwise show the user each write case with its `WRITES` lines verbatim, and ask
(`AskUserQuestion` where available, otherwise in chat): **Run with these writes**, **Run
read-only** (every case becomes `read`; its writes are dropped), or **Cancel**. Only an
explicit yes in this run allows a write. A `WRITE CANDIDATE` line is never run; it goes
in the report.

## 4. Dispatch

One worker per case, all in **one message** so they run in parallel (at most 5 at a
time). Each brief is exactly:

```
CASE: <the planner's case block, verbatim>
WRITES: <the confirmed WRITES lines; write cases only>
SESSION: bt-<run_id>-<case n>
STATE: <path | none>
SHOT_DIR: <run_dir>
```

In Claude Code with this plugin, dispatch `subagent_type=leek-skills:browser-tester` for
`read` cases and `subagent_type=leek-skills:browser-writer` for confirmed `write` cases.
A plugin hook blocks every non-read-only command from `browser-tester`. Elsewhere there
is no hook: use sub-agents on the cheapest model with the rules from those agent files,
or run the cases inline one by one, and hold them to the read-only rules yourself.

Distrust thin evidence: a worker with fewer than 5 tool uses cannot have run its case.
Report it as `INCOMPLETE (no evidence)`. Re-dispatch a worker that returned `INCOMPLETE`
at most once.

## 5. Settle UNSURE checks

For each `UNSURE` check, read its screenshot and decide PASS or FAIL. Mark it
`(from screenshot)`. If the screenshot cannot settle it either, it stays `UNSURE`. Never
read the screenshots of checks that already passed or failed.

## 6. Report

Return only this:

```
Browser test <run_id> — <origin> — <n> cases — <PASS | n failed, n unsure, n incomplete>
<any DATA CHANGED line from a worker, verbatim, in bold>
<any WROTE line from a writer, verbatim>

| case | check | verdict | evidence | screenshot |
|------|-------|---------|----------|------------|

| case | page | kind | detail | screenshot |
|------|------|------|--------|------------|
```

The second table holds the errors the workers saw (5xx and error screens first, then
page and js errors, then 4xx, blank, and slow). Collapse one error seen on several pages
into one row. Omit the table when it has no rows. After the tables, add one line per
`INCOMPLETE` case saying what it could not reach, and one line per `WRITE CANDIDATE` or
`UNPLANNABLE` note. No advice and no fixes.

Mark the headline result and each verdict cell, in front of the word: ✅ PASS, ❌ FAIL,
⚠️ UNSURE or INCOMPLETE. No other marks.
