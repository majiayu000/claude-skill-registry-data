---
name: run-intake
description: Reads the request that starts a run and writes down what it has to achieve, who it is for, what it may spend and when it is due. Use it when running `ref/mkt/account-based-play` and 10 other reference processes.
license: CC-BY-4.0
metadata:
  agent: campaign-manager
  agent-version: "1"
---

# Run intake

## What it does

Reads the request that starts a run and writes down what it has to
achieve, who it is for, what it may spend and when it is due. Everything
the run does afterwards is checked back against what is recorded here.

## Where it happens

The agent does this in eleven activities across eleven reference
processes. Each one names the activity as that process words it.

- **Take in the Account List**
  - `ref/mkt/account-based-play`, activity 1 -
    [Run Account-Based Play](../../../../processes/marketing/account-based-play.md)
- **Take in the Audience**
  - `ref/mkt/influencer-campaign`, activity 1 -
    [Run Influencer Campaign](../../../../processes/marketing/influencer-campaign.md)
- **Take in the Audience and the Goal**
  - `ref/mkt/display-retargeting`, activity 1 -
    [Run Display Retargeting Campaign](../../../../processes/marketing/display-retargeting.md)
- **Take in the Brief**
  - `ref/mkt/social-campaign`, activity 1 -
    [Run Social Media Campaign](../../../../processes/marketing/social-campaign.md)
- **Take in the Budget and Goal**
  - `ref/mkt/paid-search-campaign`, activity 1 -
    [Run Paid Search Campaign](../../../../processes/marketing/paid-search-campaign.md)
- **Take in the Creative and the Plan**
  - `ref/mkt/traffic-ad-creative`, activity 1 -
    [Traffic Ad Creative](../../../../processes/marketing/traffic-ad-creative.md)
- **Take in the Lapsed Segment**
  - `ref/mkt/win-back-campaign`, activity 1 -
    [Run Win-Back Campaign](../../../../processes/marketing/win-back-campaign.md)
- **Take in the Partner Agreement**
  - `ref/mkt/co-marketing-campaign`, activity 1 -
    [Run Co-Marketing Campaign](../../../../processes/marketing/co-marketing-campaign.md)
- **Take in the Question**
  - `ref/mkt/test-ad-creative`, activity 1 -
    [Test Ad Creative](../../../../processes/marketing/test-ad-creative.md)
- **Take in the Request**
  - `ref/mkt/landing-page`, activity 1 -
    [Publish Landing Page](../../../../processes/marketing/landing-page.md)
- **Take in the Targeting Need**
  - `ref/mkt/target-audience-segment`, activity 1 -
    [Build Target Audience Segment](../../../../processes/marketing/target-audience-segment.md)

## What to record

The run's plan, the CONVENED and DONE records of everything it convenes,
the launch record naming who said go, and the final report against the
brief.

That contract covers every activity this abstract agent takes on, and it
is repeated in `com.agentcatalog.agent/RECORDS.md`. What the abstract
agent does not do is in `com.agentcatalog.agent/NOT.md`.
