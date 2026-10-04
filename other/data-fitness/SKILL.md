---
name: data-fitness
description: Says which of the data that arrived can be relied on and how far the figures from it can be read, covering the coverage, the duplicates, the gaps and the period the data actually spans. Use it when running `ref/mkt/analyze-customer-base`, `ref/mkt/brief-executive-leadership` and `ref/mkt/buyer-persona`.
license: CC-BY-4.0
metadata:
  agent: statistician
  agent-version: "1"
---

# Data fitness

## What it does

Says which of the data that arrived can be relied on and how far the
figures from it can be read, covering the coverage, the duplicates, the
gaps and the period the data actually spans.

## Where it happens

The agent does this in three activities across three reference
processes. Each one names the activity as that process words it.

- **Say What the Data Supports**
  - `ref/mkt/analyze-customer-base`, activity 6 -
    [Analyze Customer Base](../../../../processes/marketing/analyze-customer-base.md)
- **Say What the Numbers Carry**
  - `ref/mkt/brief-executive-leadership`, activity 5 -
    [Brief Executive Leadership](../../../../processes/marketing/brief-executive-leadership.md)
- **Say What the Responses Support**
  - `ref/mkt/buyer-persona`, activity 8 -
    [Develop Buyer Persona](../../../../processes/marketing/buyer-persona.md)

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
