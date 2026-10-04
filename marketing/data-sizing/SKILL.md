---
name: data-sizing
description: Says how much data the work needs before any of it is collected, working from the size of the difference that would matter, the variation the measure already carries and the confidence being run to. Use it when running `ref/mkt/brand-health` and 3 other reference processes.
license: CC-BY-4.0
metadata:
  agent: statistician
  agent-version: "1"
---

# Data sizing

## What it does

Says how much data the work needs before any of it is collected, working
from the size of the difference that would matter, the variation the
measure already carries and the confidence being run to.

## Where it happens

The agent does this in three activities across four reference processes.
Each one names the activity as that process words it.

- **Say How Many Interviews It Needs**
  - `ref/mkt/win-loss-analysis`, activity 4 -
    [Conduct Win/Loss Analysis](../../../../processes/marketing/win-loss-analysis.md)
- **Say How Much Data It Needs**
  - `ref/mkt/brand-health`, activity 6 -
    [Measure Brand Health](../../../../processes/marketing/brand-health.md)
  - `ref/mkt/customer-research`, activity 5 -
    [Conduct Customer Research](../../../../processes/marketing/customer-research.md)
- **Size the Test**
  - `ref/mkt/conversion-experiment`, activity 3 -
    [Run Conversion Experiment](../../../../processes/marketing/conversion-experiment.md)

## What to record

Before any data is gathered, the amount the study needs: how many
responses or how long the test has to run, what that number was computed
from, and the date it was said. Every figure with the data it was
computed from, the method it was computed with, and the range around it,
so the figure can be worked out again. Every exclusion, naming the rule
that removed the records, how many records it removed, and what the
figure looks like with them left in. Every weighting, naming which group
was weighted, to what, and against which reference. For each comparison,
a verdict saying whether the difference is larger than the noise at the
threshold the study set, with the size of the difference and the range
around it written beside the verdict. A list of every figure it could
not compute with the data it had, marked as such and carried into the
report.

That contract covers every activity this abstract agent takes on, and it
is repeated in `com.agentcatalog.agent/RECORDS.md`. What the abstract
agent does not do is in `com.agentcatalog.agent/NOT.md`.
