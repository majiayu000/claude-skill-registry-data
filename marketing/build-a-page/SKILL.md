---
name: build-a-page
description: Assembles approved copy and approved design into a working page, using the templates and components the site already has, and wires up whatever the page needs to do its job, such as a form or the tracking behind it. Use it when running `ref/mkt/account-based-play` and 9 other reference processes.
license: CC-BY-4.0
metadata:
  agent: web-producer
  agent-version: "1"
---

# Build a page

## What it does

Assembles approved copy and approved design into a working page, using
the templates and components the site already has, and wires up whatever
the page needs to do its job, such as a form or the tracking behind it.

## Where it happens

The agent does this in six activities across ten reference processes.
Each one names the activity as that process words it.

- **Build the Page**
  - `ref/mkt/customer-case-study`, activity 16 -
    [Produce Customer Case Study](../../../../processes/marketing/customer-case-study.md)
  - `ref/mkt/landing-page`, activity 7 -
    [Publish Landing Page](../../../../processes/marketing/landing-page.md)
  - `ref/mkt/long-form-content`, activity 11 -
    [Produce Long-Form Content](../../../../processes/marketing/long-form-content.md)
- **Build the Pages and the Notice**
  - `ref/mkt/account-based-play`, activity 13 -
    [Run Account-Based Play](../../../../processes/marketing/account-based-play.md)
- **Build the Partner Portal**
  - `ref/mkt/channel-program`, activity 8 -
    [Launch Channel Program](../../../../processes/marketing/channel-program.md)
- **Build the Registration Page**
  - `ref/mkt/co-marketing-campaign`, activity 9 -
    [Run Co-Marketing Campaign](../../../../processes/marketing/co-marketing-campaign.md)
  - `ref/mkt/webinar`, activity 4 -
    [Produce Webinar](../../../../processes/marketing/webinar.md)
- **Open Registration**
  - `ref/mkt/field-event`, activity 8 -
    [Host Field Event](../../../../processes/marketing/field-event.md)
  - `ref/mkt/user-conference`, activity 7 -
    [Host User Conference](../../../../processes/marketing/user-conference.md)
- **Ready the Landing Pages**
  - `ref/mkt/paid-search-campaign`, activity 5 -
    [Run Paid Search Campaign](../../../../processes/marketing/paid-search-campaign.md)

## What to record

The page at a version, with the preview link that shows it. The publish
record naming the version, the time, and the person who said go. Every
redirect it set, with the address it came from and the address it now
points at. The rollback record when a page comes down, saying what is in
its place.

That contract covers every activity this abstract agent takes on, and it
is repeated in `com.agentcatalog.agent/RECORDS.md`. What the abstract
agent does not do is in `com.agentcatalog.agent/NOT.md`.
