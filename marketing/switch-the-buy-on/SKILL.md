---
name: switch-the-buy-on
description: Starts the buy once the named owner says go, at the bids, caps and splits already set, and confirms that everything named is serving. Use it when running `ref/mkt/account-based-play` and 4 other reference processes.
license: CC-BY-4.0
metadata:
  agent: media-buyer
  agent-version: "1"
---

# Switch the buy on

## What it does

Starts the buy once the named owner says go, at the bids, caps and
splits already set, and confirms that everything named is serving.

## Where it happens

The agent does this in five activities across five reference processes.
Each one names the activity as that process words it.

- **Build the Campaigns and Launch**
  - `ref/mkt/paid-search-campaign`, activity 8 -
    [Run Paid Search Campaign](../../../../processes/marketing/paid-search-campaign.md)
- **Launch the Campaigns**
  - `ref/mkt/display-retargeting`, activity 13 -
    [Run Display Retargeting Campaign](../../../../processes/marketing/display-retargeting.md)
- **Launch the Test**
  - `ref/mkt/test-ad-creative`, activity 13 -
    [Test Ad Creative](../../../../processes/marketing/test-ad-creative.md)
- **Start the Touches**
  - `ref/mkt/account-based-play`, activity 14 -
    [Run Account-Based Play](../../../../processes/marketing/account-based-play.md)
- **Switch the Ads On**
  - `ref/mkt/traffic-ad-creative`, activity 15 -
    [Traffic Ad Creative](../../../../processes/marketing/traffic-ad-creative.md)

## What to record

Every campaign configuration at a version, every budget move with the
number, the direction, and the reason, and the stop record when the buy
comes off.

That contract covers every activity this abstract agent takes on, and it
is repeated in `com.agentcatalog.agent/RECORDS.md`. What the abstract
agent does not do is in `com.agentcatalog.agent/NOT.md`.
