---
name: set-up-the-send
description: Assembles the message in the sending system from copy and design that have already been signed off, loads the audience, sets the schedule, and sends proof copies so the people who have to read the message before anyone else see it exactly as a recipient would. Use it when running `ref/mkt/churn-risk-play` and 4 other reference processes.
license: CC-BY-4.0
metadata:
  agent: email-producer
  agent-version: "1"
---

# Set up the send

## What it does

Assembles the message in the sending system from copy and design that
have already been signed off, loads the audience, sets the schedule, and
sends proof copies so the people who have to read the message before
anyone else see it exactly as a recipient would.

## Where it happens

The agent does this in six activities across five reference processes.
Each one names the activity as that process words it.

- **Build the Issue**
  - `ref/mkt/customer-newsletter`, activity 9 -
    [Publish Customer Newsletter](../../../../processes/marketing/customer-newsletter.md)
- **Build the Send**
  - `ref/mkt/onboarding-email-program`, activity 8 -
    [Run Onboarding Email Program](../../../../processes/marketing/onboarding-email-program.md)
- **Prepare the Send**
  - `ref/mkt/churn-risk-play`, activity 8 -
    [Run Churn-Risk Play](../../../../processes/marketing/churn-risk-play.md)
- **Proof the Issue**
  - `ref/mkt/customer-newsletter`, activity 11 -
    [Publish Customer Newsletter](../../../../processes/marketing/customer-newsletter.md)
- **Set up the Practical Side**
  - `ref/mkt/customer-reviews`, activity 9 -
    [Solicit Customer Reviews](../../../../processes/marketing/customer-reviews.md)
- **Set up the Sending**
  - `ref/mkt/win-back-campaign`, activity 12 -
    [Run Win-Back Campaign](../../../../processes/marketing/win-back-campaign.md)

## What to record

Each message at a version, with the proof record naming who was sent a
proof, when it went, and what they said. The audience at a version, with
the count before the consent, opt-out and suppression rules were
applied, the count after, and the rule behind every removal. The
schedule as it was set, including the send-time windows and any wait
between batches. The send record naming the version that went, the time
it fired, and the person who said go. The delivery report, with what was
delivered, what bounced hard, what bounced soft, who complained, who
unsubscribed, and who the sending system suppressed on its own. Anything
it could not verify before the send is recorded as unverified instead of
being left out.

That contract covers every activity this abstract agent takes on, and it
is repeated in `com.agentcatalog.agent/RECORDS.md`. What the abstract
agent does not do is in `com.agentcatalog.agent/NOT.md`.
