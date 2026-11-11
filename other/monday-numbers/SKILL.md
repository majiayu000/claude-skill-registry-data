---
name: monday-numbers
description: "Weekly numbers review for a small business: collects sales, ad and website numbers into one table, checks the data, compares week over week, explains where a drop came from, and writes three Monday actions that each cite their number. Use when an owner asks how the week went, why sales or traffic dropped, what to focus on, or says \"monday numbers\", \"weekly numbers\" or \"what moved\". Read only: never changes data, ads or prices."
---

# Monday Numbers

Five agents that turn your sales, ad and website exports into one checked table and three actions for the week. Every number carries its source and date range; every action cites a number.

Not for tax, bookkeeping or accounting fixes.

## What you need

| Data | Best source | Fallback |
|---|---|---|
| Sales | Stripe connector (Claude.ai connector directory or Stripe MCP in Claude Code), if your plan and admin allow it | Payments CSV export, or a Google Sheet (Drive connector; if it will not open the sheet, File > Download > CSV) |
| Ad results | None needed | CSV export of the ad manager reporting table: date, campaign, ad set, ad, spend, results. Daily rows if possible |
| Website | None needed | CSV export from your analytics tool: date, page or source, visits, conversions |

Ideally 8 weeks of history so there is a baseline. With fewer than 4 weeks, the Comparer reports changes but marks every status "short history".

If a connector is missing, ask for the export or a pasted table and name the columns needed. Never stop, never guess. The report says which parts ran on pasted data.

## Setup (`start`, or when PROFILE is empty)

Ask in two rounds, accept "skip", then show PROFILE and METRICS back for confirmation.

Round 1
1. What do you sell, and how do people pay? (checkout, invoice, in person)
2. Which 3 to 8 numbers tell you how the week went? (revenue, orders, new customers, ad spend, cost per sale, visits, sign-ups)
3. Where does each live, and is it a connector or an export?
4. Week start day and the time zone your tools use.

Round 2
5. How big a change counts as "moved"? Default: 10 percent, or the biggest normal weekly swing in the last 8 weeks, whichever is bigger.
6. Revenue rule: gross or net of refunds, tax, fees?
7. Products, ads or pages to watch by name.
8. Weekly run? (see Scheduling)

## Commands and routing

| Command | Runs |
|---|---|
| `monday numbers` | 1 > 2 > 3 > 4 (once per MOVED DOWN metric) > 5, one combined report |
| `check data` | 1 > 2 |
| `compare` | 3 (needs a checked table) |
| `why <metric>` | 4 |
| `actions` | 5 |

Before acting as an agent, read its file in `agents/`. In Claude Code you can copy them to `.claude/agents/` to run each as a real subagent.

- `agents/01-data-collector.md`: exports to one WEEKLY table
- `agents/02-data-checker.md`: flags duplicates, refunds, gaps, outliers
- `agents/03-number-comparer.md`: MOVED UP / MOVED DOWN / NORMAL
- `agents/04-drop-explainer.md`: which part of a metric caused the drop
- `agents/05-action-list.md`: three actions, each citing a number

## Safety rules (every agent)

- Read only. Never refund, pause an ad, change a price or edit a sheet. Actions are for the owner.
- Never invent a number. Missing = "not available" plus what export would supply it.
- Every number shows source and date range, e.g. "Stripe payments CSV, 6 to 12 Oct".
- Compare only same source, same kind of range. Otherwise "cannot compare".
- A cause needs a breakdown that shows it; otherwise "cause unknown".
- Agents 3 to 5 use only rows the Checker passed or the owner kept.
- No customer names or emails in any output. Totals only.
- Estimates are labelled ESTIMATE with the working shown.

## Shared files

Claude Code: files in `numbers/`. Claude.ai: print updated tables at the end of each run so the owner can save them to Project knowledge.

- `PROFILE`: setup answers
- `METRICS`: metric | definition | source | how to get it
- `WEEKLY`: week | metric | value | source | rows used
- `FLAGS`: data problems and the owner's decision
- `ACTIONS`: each week's three actions and next week's result

## Scheduling (optional)

Nothing runs on its own. In Claude Code, `/schedule` a weekly routine with the prompt `monday numbers` pointed at a fixed export folder; the Claude desktop app's scheduled tasks work the same way where your plan has them. Exports from tools without a connector still have to be dropped into the folder before the run.

## End of every run

1. One line per agent that ran.
2. Numbers table.
3. FLAGS waiting for the owner.
4. Three actions.
5. Missing data and how to get it next week.
6. "Nothing was changed in any tool."

Example (fake data):

```
Ran: Collector (3 sources, 8 weeks), Checker (2 flags), Comparer, Explainer (revenue), Actions.

| Metric   | This week | Last week | Change | Status     | Source, range              |
|----------|-----------|-----------|--------|------------|----------------------------|
| Revenue  | 4,120     | 5,300     | -22%   | MOVED DOWN | payments.csv, 6 to 12 Oct  |
| Visits   | 2,950     | 3,010     | -2%    | NORMAL     | analytics.csv, 6 to 12 Oct |

Flags: F1 two duplicate transaction IDs on 8 Oct (ASK OWNER).
Revenue drop: 81% from "Starter Kit" (orders 40 > 18).
Actions: 1) Check Starter Kit checkout page (conversion 3.1% > 1.2%) ...
Missing: ad export had no ad-level rows; export with "Ad" breakdown next week.
Nothing was changed in any tool.
```
