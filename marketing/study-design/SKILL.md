---
name: study-design
description: Settles how a study or a read will be done before any data is gathered, which means the method and why that one, who is sampled or who counts, what gets asked, the period and the markets covered, and which wording carries over unchanged from the last time so the two can be compared. Use it when running `ref/mkt/analyze-customer-base` and 4 other reference processes.
license: CC-BY-4.0
metadata:
  agent: statistician
  agent-version: "1"
---

# Study design

## What it does

Settles how a study or a read will be done before any data is gathered,
which means the method and why that one, who is sampled or who counts,
what gets asked, the period and the markets covered, and which wording
carries over unchanged from the last time so the two can be compared.

## Where it happens

The agent does this in five activities across five reference processes.
Each one names the activity as that process words it.

- **Carry the Questions Forward**
  - `ref/mkt/brand-health`, activity 11 -
    [Measure Brand Health](../../../../processes/marketing/brand-health.md)
- **Choose the Method**
  - `ref/mkt/customer-research`, activity 3 -
    [Conduct Customer Research](../../../../processes/marketing/customer-research.md)
- **Design the Buyer Study**
  - `ref/mkt/map-buyer-journey`, activity 4 -
    [Map Buyer Journey](../../../../processes/marketing/map-buyer-journey.md)
- **Plan the Study**
  - `ref/mkt/buyer-persona`, activity 5 -
    [Develop Buyer Persona](../../../../processes/marketing/buyer-persona.md)
- **Set the Scope of the Read**
  - `ref/mkt/analyze-customer-base`, activity 2 -
    [Analyze Customer Base](../../../../processes/marketing/analyze-customer-base.md)

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
