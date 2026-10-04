---
name: maker-brief
description: Puts the same request in front of everyone who has to build a piece of the measurement at the same time, so nobody works from an older version of it. Use it when running `ref/mkt/conversion-experiment` and 3 other reference processes.
license: CC-BY-4.0
metadata:
  agent: conversion-tracker
  agent-version: "1"
---

# Maker brief

## What it does

Puts the same request in front of everyone who has to build a piece of
the measurement at the same time, so nobody works from an older version
of it.

## Where it happens

The agent does this in one activity across four reference processes.
Each one names the activity as that process words it.

- **Brief the Makers**
  - `ref/mkt/conversion-experiment`, activity 5 -
    [Run Conversion Experiment](../../../../processes/marketing/conversion-experiment.md)
  - `ref/mkt/landing-page`, activity 4 -
    [Publish Landing Page](../../../../processes/marketing/landing-page.md)
  - `ref/mkt/nurture-sequence`, activity 6 -
    [Build Nurture Sequence](../../../../processes/marketing/nurture-sequence.md)
  - `ref/mkt/win-back-campaign`, activity 7 -
    [Run Win-Back Campaign](../../../../processes/marketing/win-back-campaign.md)

## What to record

A measurement plan at a version, naming every conversion, what counts as
one, and where it fires. For each conversion, a dated test record
showing a real submission arriving in the CRM. The tracking parameters
it handed to each paid channel, recorded against the page they belong
to. Anything it could not verify is recorded as unverified rather than
left out.

That contract covers every activity this abstract agent takes on, and it
is repeated in `com.agentcatalog.agent/RECORDS.md`. What the abstract
agent does not do is in `com.agentcatalog.agent/NOT.md`.
