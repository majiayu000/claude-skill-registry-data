---
name: edit-a-draft
description: The agent reads a draft as an editor and says what has to be rewritten, naming each thing rather than quietly rewriting it. Use it when running `ref/mkt/landing-page` and `ref/mkt/website-content-update`.
license: CC-BY-4.0
metadata:
  agent: copywriter
  agent-version: "1"
---

# Edit a draft

## What it does

The agent reads a draft as an editor and says what has to be rewritten,
naming each thing rather than quietly rewriting it.

## Where it happens

The agent does this in two activities across two reference processes.
Each one names the activity as that process words it.

- **Edit the Change**
  - `ref/mkt/website-content-update`, activity 5 -
    [Update Website Content](../../../../processes/marketing/website-content-update.md)
- **Edit the Draft**
  - `ref/mkt/landing-page`, activity 6 -
    [Publish Landing Page](../../../../processes/marketing/landing-page.md)

## What to record

Every draft at a version, and the DONE records of the patterns it works
inside. A claim it uses cites the register entry it came from.

That contract covers every activity this abstract agent takes on, and it
is repeated in `com.agentcatalog.agent/RECORDS.md`. What the abstract
agent does not do is in `com.agentcatalog.agent/NOT.md`.
