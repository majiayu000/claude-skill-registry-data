---
name: finding-record
description: Files the finding with the numbers and the method underneath it, so somebody else can work it out again later and see whether it still holds. Use it when running `ref/mkt/conversion-experiment`.
license: CC-BY-4.0
metadata:
  agent: statistician
  agent-version: "1"
---

# Finding record

## What it does

Files the finding with the numbers and the method underneath it, so
somebody else can work it out again later and see whether it still
holds.

## Where it happens

The agent does this in one activity across one reference process. Each
one names the activity as that process words it.

- **Record What Was Learned**
  - `ref/mkt/conversion-experiment`, activity 16 -
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
