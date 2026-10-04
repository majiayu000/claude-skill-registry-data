---
name: open-a-run
description: Takes in what starts a run for one customer, which is either a new customer with what they bought and when they started, or a signal that fired on an account with the date it fired. Use it when running `ref/mkt/churn-risk-play` and `ref/mkt/onboarding-email-program`.
license: CC-BY-4.0
metadata:
  agent: lifecycle-manager
  agent-version: "1"
---

# Open a run

## What it does

Takes in what starts a run for one customer, which is either a new
customer with what they bought and when they started, or a signal that
fired on an account with the date it fired.

## Where it happens

The agent does this in two activities across two reference processes.
Each one names the activity as that process words it.

- **Take in the New Customer**
  - `ref/mkt/onboarding-email-program`, activity 1 -
    [Run Onboarding Email Program](../../../../processes/marketing/onboarding-email-program.md)
- **Take in the Signal**
  - `ref/mkt/churn-risk-play`, activity 1 -
    [Run Churn-Risk Play](../../../../processes/marketing/churn-risk-play.md)

## What to record

For each customer, the run at a version: the date they entered, the
condition that put them in, the goal the run is trying to reach, every
step they were given with the date and the reason it was chosen, and
every step that was skipped with the reason it was skipped. A dated line
each time the path changed, naming what changed and what the customer
did or failed to do that changed it. Every commitment made to the
customer, naming who made it, what was promised, when it is due, and the
date it was met. The handover record when a person takes over, saying
what that person is being asked to do and everything the customer has
already been sent. The closing record, saying whether the goal was
reached, what the customer did, and the date the run ended.

That contract covers every activity this abstract agent takes on, and it
is repeated in `com.agentcatalog.agent/RECORDS.md`. What the abstract
agent does not do is in `com.agentcatalog.agent/NOT.md`.
