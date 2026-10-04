---
name: go-live
description: Starts the run on the date that was agreed, once the person who owns it says go, and confirms that what should be running is running, whether that is a set of campaigns at their opening bids, the ads, the posts, the messages or the variants of a test at their split. Use it when running `ref/mkt/account-based-play` and 7 other reference processes.
license: CC-BY-4.0
metadata:
  agent: campaign-manager
  agent-version: "1"
---

# Go live

## What it does

Starts the run on the date that was agreed, once the person who owns it
says go, and confirms that what should be running is running, whether
that is a set of campaigns at their opening bids, the ads, the posts,
the messages or the variants of a test at their split.

## Where it happens

The agent does this in eight activities across eight reference
processes. Each one names the activity as that process words it.

- **Build the Campaigns and Launch**
  - `ref/mkt/paid-search-campaign`, activity 8 -
    [Run Paid Search Campaign](../../../../processes/marketing/paid-search-campaign.md)
- **Launch**
  - `ref/mkt/social-campaign`, activity 8 -
    [Run Social Media Campaign](../../../../processes/marketing/social-campaign.md)
- **Launch the Campaigns**
  - `ref/mkt/display-retargeting`, activity 13 -
    [Run Display Retargeting Campaign](../../../../processes/marketing/display-retargeting.md)
- **Launch the Joint Campaign**
  - `ref/mkt/co-marketing-campaign`, activity 12 -
    [Run Co-Marketing Campaign](../../../../processes/marketing/co-marketing-campaign.md)
- **Launch the Test**
  - `ref/mkt/test-ad-creative`, activity 13 -
    [Test Ad Creative](../../../../processes/marketing/test-ad-creative.md)
- **Send the Sequence**
  - `ref/mkt/win-back-campaign`, activity 14 -
    [Run Win-Back Campaign](../../../../processes/marketing/win-back-campaign.md)
- **Start the Touches**
  - `ref/mkt/account-based-play`, activity 14 -
    [Run Account-Based Play](../../../../processes/marketing/account-based-play.md)
- **Switch the Ads On**
  - `ref/mkt/traffic-ad-creative`, activity 15 -
    [Traffic Ad Creative](../../../../processes/marketing/traffic-ad-creative.md)

## What to record

The run's plan, the CONVENED and DONE records of everything it convenes,
the launch record naming who said go, and the final report against the
brief.

That contract covers every activity this abstract agent takes on, and it
is repeated in `com.agentcatalog.agent/RECORDS.md`. What the abstract
agent does not do is in `com.agentcatalog.agent/NOT.md`.
