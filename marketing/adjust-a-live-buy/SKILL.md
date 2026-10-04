---
name: adjust-a-live-buy
description: Changes a buy that is already running. Use it when running `ref/mkt/paid-search-campaign` and 3 other reference processes.
license: CC-BY-4.0
metadata:
  agent: media-buyer
  agent-version: "1"
---

# Adjust a live buy

## What it does

Changes a buy that is already running. It moves money between lines and
systems, resets daily limits so each flight lands on its date, moves
bids, swaps out creative that has gone stale, and turns wasted terms and
unwanted inventory into exclusions.

## Where it happens

The agent does this in five activities across four reference processes.
Each one names the activity as that process words it.

- **Apply the Exclusions**
  - `ref/mkt/verify-ad-placement`, activity 10 -
    [Verify Ad Placement Quality](../../../../processes/marketing/verify-ad-placement.md)
- **Correct the Pacing**
  - `ref/mkt/reallocate-media-spend`, activity 11 -
    [Reallocate Media Spend](../../../../processes/marketing/reallocate-media-spend.md)
- **Move the Money in the Platforms**
  - `ref/mkt/reallocate-media-spend`, activity 10 -
    [Reallocate Media Spend](../../../../processes/marketing/reallocate-media-spend.md)
- **Optimize**
  - `ref/mkt/social-campaign`, activity 11 -
    [Run Social Media Campaign](../../../../processes/marketing/social-campaign.md)
- **Tune the Bids and Terms**
  - `ref/mkt/paid-search-campaign`, activity 10 -
    [Run Paid Search Campaign](../../../../processes/marketing/paid-search-campaign.md)

## What to record

Every campaign configuration at a version, every budget move with the
number, the direction, and the reason, and the stop record when the buy
comes off.

That contract covers every activity this abstract agent takes on, and it
is repeated in `com.agentcatalog.agent/RECORDS.md`. What the abstract
agent does not do is in `com.agentcatalog.agent/NOT.md`.
