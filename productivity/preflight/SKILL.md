---
name: preflight
description: Run periodic maintenance checks. Use /preflight to see the checklist — rows highlighted if overdue (e.g. /cleanup-dev > 30 days), then offer to run them.
purpose: Shows periodic maintenance checks, flagging any overdue.
user_invocable: true
stage: desk
composes: cleanup-dev:dispatch, daily:dispatch, triage:dispatch, nazgul:dispatch, palantir:dispatch
---

# Preflight

Runs a checklist of periodic maintenance tasks, reports which are overdue, and carries those items forward so the count stays visible at a glance.

## Workflow

### 1. Gather state

```bash
~/.claude/hooks/preflight-check.sh
```

Output is pipe-delimited `check|status|detail|flag`. `flag=warn` means the row is overdue.

### 2. Present as a table

Columns: **Check**, **Status**, **Detail**, **Action**.

- Bold the **Check** cell and prefix the **Status** cell with `⚠️ **OVERDUE**` when `flag=warn`.
- **Action** suggests the matching slash command (e.g. `/cleanup-dev`). Clean rows show `—`.
- End with a one-line summary: `N overdue / M checks`.

### 3. Carry the overdue items forward

The outcome this step owes: every overdue check leaves a standing item the user can
see after the table has scrolled away, and a check that has since been run stops
carrying one.

**Where that item lives depends on the session** — read `docs/workflow/task-surface.md` for the
convention. In short: a task-tracking tool in the roster takes the items;
absent one, the table from step 2 *is* the record — close with the one-line
summary and let step 4 act on it directly.

Where a tool is used, one item per overdue check:

- `subject`: `<key> overdue — run <action>` (e.g. `cleanup-dev overdue — run /cleanup-dev`)
- `description`: the row's detail field plus the suggested slash command
- identity: `preflight_key = <key>`, so re-runs match rather than duplicate

An overdue check whose item already stands is left alone. A check now reading
clean has its item marked complete — the self-heal. An item bearing no `preflight_key` was
not written by this skill; never touch it.

### 4. Offer to run overdue items

If any rows are flagged, use AskUserQuestion to let the user pick which overdue tasks to run now (multiSelect). Invoke the suggested slash command for each selection.

When a run finishes, the next `/preflight` invocation reads the check as clean again — and where step 3 seated an item, that run closes it via the self-heal. No per-skill coupling needed.

## Checks

| Key | Threshold | Action when overdue |
|-----|-----------|---------------------|
| `cleanup-dev` | 30 days since last run | `/cleanup-dev` |
| `daily` | not yet run today (calendar day) | `/daily` |
| `triage` | not yet run today (calendar day) | `/triage` |
| `nazgul-checks` | 30 days since last review of the rubric files | walk `skills/nazgul/checks/*.md`, then `/nazgul reviewed` |
| `palantir` | any of your PRs/MRs carries new comments since you last looked | `/palantir activity` |

Add new checks by extending `~/.claude/hooks/preflight-check.sh` and the table above.
