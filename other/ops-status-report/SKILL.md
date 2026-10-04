---
name: ops-status-report
description: Generate a recurring status snapshot of a folder-based workspace (clients, pipeline files, recent activity, command health checks) ending in an Attention Needed section that surfaces what is stalled or overdue. Read-only except for the report file. Use when the user says "status report", "weekly report", "what's going on in this workspace", or "ops snapshot".
---

# Ops Status Report

A workspace full of markdown and folders holds an honest status report nobody compiles. This skill compiles it: what is active, what is overdue, what went quiet. The Attention Needed section is the whole point; everything else is supporting evidence.

## Step 0: Load the report config (once)

Look for an `ops-report.config.md` file in the project root. If it does not exist, interview the user about what "status" means in their workspace, then offer to save it. The config defines a list of sections, each one of these shapes:

```
FOLDER_SCAN     A folder where each subfolder or file is a tracked item,
                plus which line or frontmatter key holds its status
FRONTMATTER_TALLY  A folder of markdown files, which keys to tally
                (e.g. status), and which date key flags overdue items
RECENT_ACTIVITY A folder to check for files created or modified in the
                last N days
COMMAND         A read-only command whose output summarizes a tool
                (e.g. a CLI status command), and what failure means
REPORTS_FOLDER  Where finished reports are saved
```

## Step 1: Collect (read-only)

Run every configured section. Rules of collection:

- Missing files or folders are findings ("item X has no status file"), not errors to silently skip.
- Dates that cannot be parsed are listed as-is, never guessed.
- A COMMAND that fails gets one line with the reason ("not run: missing .env"), and the report continues.

## Step 2: Write the report

Save to `REPORTS_FOLDER/ops-report-<YYYY-MM-DD>.md`:

```markdown
# Ops Report: <date>

## <One section per config entry>
Tables for tallies, lists for activity, short summaries for commands.

## Attention needed
Three to five bullets maximum, ordered by cost of ignoring them:
overdue items first, then untracked items, then things that went quiet.
```

If everything is genuinely fine, Attention Needed is one line saying so. Invented urgency kills trust in the report faster than a missed item.

## Step 3: Deliver

Show the Attention Needed section in chat with the report path. If the user wants this on a schedule, suggest their scheduler of choice run the skill weekly.

## Rules

- Read-only except the report file itself. The report never fixes what it finds; it names it.
- Numbers come from counting, not estimating. If something could not be counted, the report says so.
- No em dashes in any output.

## Output

A dated ops report file plus the Attention Needed highlights in chat.
