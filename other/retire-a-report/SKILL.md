---
name: retire-a-report
description: Reads what each report costs and what depends on it, freezes it so it stops moving, and switches off the feeds behind it. Use it when running `ref/rev/retire-a-report`.
license: CC-BY-4.0
metadata:
  agent: data-steward
  agent-version: "1"
---

# Retire a report

## What it does

Reads what each report costs and what depends on it, freezes it so it
stops moving, and switches off the feeds behind it.

## Where it happens

The agent does this in four activities across one reference process.
Each one names the activity as that process words it.

- **Find What Depends on Each One**
  - `ref/rev/retire-a-report`, activity 7 -
    [Retire a Report](../../../../processes/revenue-operations/retire-a-report.md)
- **Freeze the Report**
  - `ref/rev/retire-a-report`, activity 11 -
    [Retire a Report](../../../../processes/revenue-operations/retire-a-report.md)
- **Read What Each One Costs**
  - `ref/rev/retire-a-report`, activity 3 -
    [Retire a Report](../../../../processes/revenue-operations/retire-a-report.md)
- **Switch Off the Feeds**
  - `ref/rev/retire-a-report`, activity 13 -
    [Retire a Report](../../../../processes/revenue-operations/retire-a-report.md)

## What to record

Per definition: the request and who made it, who reads the object today
and what counts off it, the sentence saying what the object is and what
it is not, every field with its fill rate and whether anything reads it,
the required list with the reason each field is required, the allowed
values with what each one means, the uniqueness key written as fields
rather than as a feeling, and where every field's value comes from. Then
the count of records already held that would fail, the reports and
integrations that read a changed field, the signed version with its
signer and date, and the backfill deadline with its owner and the count
still failing when the run closed. Per correction: the old value, the
new value and the reason, for every record touched. Per failure: the
source named with the evidence that it was that one, and a failure that
could not be traced recorded as unexplained rather than as fixed. Per
merge: the surviving id with the reason it was chosen, the winning value
per field naming the record it came from, and every value that did not
survive, stored against the survivor and dated.

That contract covers every activity this abstract agent takes on, and it
is repeated in `com.agentcatalog.agent/RECORDS.md`. What the abstract
agent does not do is in `com.agentcatalog.agent/NOT.md`.
