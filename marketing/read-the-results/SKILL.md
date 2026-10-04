---
name: read-the-results
description: Reads what the responses say once the field is closed, and sets that reading beside the baseline and the earlier runs in the same series so that a real movement can be told from noise. Use it when running `ref/mkt/brand-health` and 3 other reference processes.
license: CC-BY-4.0
metadata:
  agent: study-manager
  agent-version: "1"
---

# Read the results

## What it does

Reads what the responses say once the field is closed, and sets that
reading beside the baseline and the earlier runs in the same series so
that a real movement can be told from noise. It also sets what people
believe against what the organization claims and against what its own
records say.

## Where it happens

The agent does this in six activities across four reference processes.
Each one names the activity as that process words it.

- **Compare with the Earlier Waves**
  - `ref/mkt/brand-health`, activity 17 -
    [Measure Brand Health](../../../../processes/marketing/brand-health.md)
- **Read What People Recognize Now**
  - `ref/mkt/brand-refresh`, activity 24 -
    [Roll Out Brand Refresh](../../../../processes/marketing/brand-refresh.md)
- **Read What People Recognize Today**
  - `ref/mkt/brand-refresh`, activity 4 -
    [Roll Out Brand Refresh](../../../../processes/marketing/brand-refresh.md)
- **Read the Result**
  - `ref/mkt/conversion-experiment`, activity 13 -
    [Run Conversion Experiment](../../../../processes/marketing/conversion-experiment.md)
- **Set Perception against the Promise**
  - `ref/mkt/brand-health`, activity 19 -
    [Measure Brand Health](../../../../processes/marketing/brand-health.md)
- **Set the Themes against the Record**
  - `ref/mkt/win-loss-analysis`, activity 17 -
    [Conduct Win/Loss Analysis](../../../../processes/marketing/win-loss-analysis.md)

## What to record

The study written down as a question before any data is gathered: what
it has to settle, the method chosen and why that method, who or what is
sampled, how many responses it needs, and the date the findings are due.
Every question and every piece of material at a version, in the order it
is put to people, with each response marked with the version it
answered. Every response as it was given, with its date, and every
response that was removed from the count, with the rule that removed it.
Each finding with the responses recorded under it, so the finding and
its evidence are read together. A comparison against the earlier studies
in the series, naming every place this study differs from the last one
and what that difference does to the reading. The count of responses
against the count the study planned for, said on the day the study
closes. The CONVENED and DONE records of everything it convenes.

That contract covers every activity this abstract agent takes on, and it
is repeated in `com.agentcatalog.agent/RECORDS.md`. What the abstract
agent does not do is in `com.agentcatalog.agent/NOT.md`.
