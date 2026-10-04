---
name: edit-a-draft
description: The agent reads a draft against what was asked for and says item by item what has to be rewritten, in terms the writer can work through without coming back to ask what was meant. Use it when running `ref/mkt/announce-company-news` and 10 other reference processes.
license: CC-BY-4.0
metadata:
  agent: editor
  agent-version: "1"
---

# Edit a draft

## What it does

The agent reads a draft against what was asked for and says item by item
what has to be rewritten, in terms the writer can work through without
coming back to ask what was meant. It holds the piece at that standard
for as many rounds as it takes.

## Where it happens

The agent does this in eight activities across eleven reference
processes. Each one names the activity as that process words it.

- **Check It Once**
  - `ref/mkt/feature-release`, activity 5 -
    [Announce Feature Release](../../../../processes/marketing/feature-release.md)
- **Edit the Card**
  - `ref/mkt/competitive-battlecard`, activity 8 -
    [Refresh Competitive Battlecard](../../../../processes/marketing/competitive-battlecard.md)
- **Edit the Change**
  - `ref/mkt/website-content-update`, activity 5 -
    [Update Website Content](../../../../processes/marketing/website-content-update.md)
- **Edit the Draft**
  - `ref/mkt/customer-case-study`, activity 11 -
    [Produce Customer Case Study](../../../../processes/marketing/customer-case-study.md)
  - `ref/mkt/customer-newsletter`, activity 8 -
    [Publish Customer Newsletter](../../../../processes/marketing/customer-newsletter.md)
  - `ref/mkt/landing-page`, activity 6 -
    [Publish Landing Page](../../../../processes/marketing/landing-page.md)
  - `ref/mkt/long-form-content`, activity 7 -
    [Produce Long-Form Content](../../../../processes/marketing/long-form-content.md)
- **Edit the Entry**
  - `ref/mkt/award-entry`, activity 9 -
    [Submit Award Entry](../../../../processes/marketing/award-entry.md)
- **Edit the Release**
  - `ref/mkt/announce-company-news`, activity 7 -
    [Announce Company News](../../../../processes/marketing/announce-company-news.md)
- **Edit the Rewrite**
  - `ref/mkt/refresh-content`, activity 13 -
    [Refresh Published Content](../../../../processes/marketing/refresh-content.md)
- **Review the Cut**
  - `ref/mkt/video-asset`, activity 8 -
    [Produce Video Asset](../../../../processes/marketing/video-asset.md)

## What to record

Every edit at a version, saying what has to change and why, item by
item, in terms the writer can work through without coming back to ask
what was meant. A line for anything it flagged for another pass, naming
the agent it went to. When it holds the version, the merge, the decline
or the revision request it gave in every round, each with its reason.

That contract covers every activity this abstract agent takes on, and it
is repeated in `com.agentcatalog.agent/RECORDS.md`. What the abstract
agent does not do is in `com.agentcatalog.agent/NOT.md`.
