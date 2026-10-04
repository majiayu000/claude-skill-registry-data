---
name: agree-a-deal
description: Makes the approach to a creator, finds out whether they are interested, and works through the terms until both sides hold the same deliverables, dates, usage rights, disclosure wording and fee. Use it when running `ref/mkt/influencer-campaign`.
license: CC-BY-4.0
metadata:
  agent: creator-relations
  agent-version: "1"
---

# Agree a deal

## What it does

Makes the approach to a creator, finds out whether they are interested,
and works through the terms until both sides hold the same deliverables,
dates, usage rights, disclosure wording and fee. Every exchange lands in
the contact log on the day it happened.

## Where it happens

The agent does this in two activities across one reference process. Each
one names the activity as that process words it.

- **Approach the Creators**
  - `ref/mkt/influencer-campaign`, activity 7 -
    [Run Influencer Campaign](../../../../processes/marketing/influencer-campaign.md)
- **Settle the Terms**
  - `ref/mkt/influencer-campaign`, activity 8 -
    [Run Influencer Campaign](../../../../processes/marketing/influencer-campaign.md)

## What to record

For each creator, the record holds the audience figures with the date
they were read and the source they came from, what the authenticity
check found, and what the history check found in the creator's past
publishing. For each deal, it keeps what was agreed at the version it
was agreed: every deliverable, the date each one is due, the channels
the work may run on, how long the organization may use it, what the
disclosure has to say, and the fee. Every approach lands with its date,
what was offered, and the answer that came back, including the creators
who declined and the reason they gave. When a creator publishes, the
agent records what went out, where it went out, and on what date. When a
check finds a problem, the agent records the finding, what it asked the
creator to do, the date it asked, and what the creator did.

That contract covers every activity this abstract agent takes on, and it
is repeated in `com.agentcatalog.agent/RECORDS.md`. What the abstract
agent does not do is in `com.agentcatalog.agent/NOT.md`.
