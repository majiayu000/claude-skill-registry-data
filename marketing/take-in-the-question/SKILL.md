---
name: take-in-the-question
description: When a request or a signal arrives, the agent works out what the read has to settle, over what period, for which markets, and by when it is due. Use it when running `ref/mkt/analyze-customer-base` and 5 other reference processes.
license: CC-BY-4.0
metadata:
  agent: analytics
  agent-version: "1"
---

# Take in the question

## What it does

When a request or a signal arrives, the agent works out what the read
has to settle, over what period, for which markets, and by when it is
due. It writes down the definitions the read will use, so the answer
means the same thing to everyone who reads it.

## Where it happens

The agent does this in six activities across six reference processes.
Each one names the activity as that process words it.

- **Set the Scope of the Read**
  - `ref/mkt/analyze-customer-base`, activity 2 -
    [Analyze Customer Base](../../../../processes/marketing/analyze-customer-base.md)
- **Take in the Drift or the Signal**
  - `ref/mkt/lead-scoring-model`, activity 1 -
    [Maintain Lead Scoring Model](../../../../processes/marketing/lead-scoring-model.md)
- **Take in the Lapsed Segment**
  - `ref/mkt/win-back-campaign`, activity 1 -
    [Run Win-Back Campaign](../../../../processes/marketing/win-back-campaign.md)
- **Take in the Pacing Signal**
  - `ref/mkt/reallocate-media-spend`, activity 1 -
    [Reallocate Media Spend](../../../../processes/marketing/reallocate-media-spend.md)
- **Take in the Question**
  - `ref/mkt/analyze-customer-base`, activity 1 -
    [Analyze Customer Base](../../../../processes/marketing/analyze-customer-base.md)
  - `ref/mkt/test-ad-creative`, activity 1 -
    [Test Ad Creative](../../../../processes/marketing/test-ad-creative.md)
- **Take in the Trigger**
  - `ref/mkt/attribution-model`, activity 1 -
    [Maintain Attribution Model](../../../../processes/marketing/attribution-model.md)

## What to record

Every report with every line attributed to its source, delivered on the
cadence the process sets. A missing source appears in the report as
missing.

That contract covers every activity this abstract agent takes on, and it
is repeated in `com.agentcatalog.agent/RECORDS.md`. What the abstract
agent does not do is in `com.agentcatalog.agent/NOT.md`.
