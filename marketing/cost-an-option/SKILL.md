---
name: cost-an-option
description: The agent works out what a proposed option would take in money and in people over its whole life, including what it would cost to leave it, and says what the department would have to give up to carry it. Use it when running `ref/mkt/brand-refresh` and 3 other reference processes.
license: CC-BY-4.0
metadata:
  agent: budget-keeper
  agent-version: "1"
---

# Cost an option

## What it does

The agent works out what a proposed option would take in money and in
people over its whole life, including what it would cost to leave it,
and says what the department would have to give up to carry it.

## Where it happens

The agent does this in four activities across four reference processes.
Each one names the activity as that process words it.

- **Check What Each Option Would Take**
  - `ref/mkt/develop-marketing-strategy`, activity 8 -
    [Develop Marketing Strategy](../../../../processes/marketing/develop-marketing-strategy.md)
- **Check What the Department Can Carry**
  - `ref/mkt/brand-refresh`, activity 9 -
    [Roll Out Brand Refresh](../../../../processes/marketing/brand-refresh.md)
- **Cost Each Way of Closing the Gap**
  - `ref/mkt/plan-marketing-capacity`, activity 9 -
    [Plan Marketing Capacity](../../../../processes/marketing/plan-marketing-capacity.md)
- **Work out the Whole Cost**
  - `ref/mkt/select-marketing-technology`, activity 15 -
    [Select Marketing Technology](../../../../processes/marketing/select-marketing-technology.md)

## What to record

It leaves the budget at a version for the year, with one line per
function carrying what was allocated, what was already committed against
it before the year began, what has been drawn, and what is left. Every
change to an allocation goes in as a new version naming who approved it,
on what date, and which line the money moved from and to, and the
version it replaces stays where it was. Every draw is recorded against
the allocation it came from and the run that made it. The uncommitted
remainder is restated whenever a draw or a change lands. Once the
reconciliation for a period closes, that period's figures are frozen, so
a question about it a year later gets the same answer it got on the day.

That contract covers every activity this abstract agent takes on, and it
is repeated in `com.agentcatalog.agent/RECORDS.md`. What the abstract
agent does not do is in `com.agentcatalog.agent/NOT.md`.
