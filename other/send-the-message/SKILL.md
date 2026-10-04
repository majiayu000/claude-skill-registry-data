---
name: send-the-message
description: Fires a prepared send once the named owner says go, and keeps the record of what went out to whom. Use it when running `ref/mkt/account-based-play` and 11 other reference processes.
license: CC-BY-4.0
metadata:
  agent: email-producer
  agent-version: "1"
---

# Send the message

## What it does

Fires a prepared send once the named owner says go, and keeps the record
of what went out to whom. The same work covers a single message, a step
in a sequence, a reminder to the people who have not answered, a notice
that has to be provable, and a statement that goes out on every channel
at once.

## Where it happens

The agent does this in thirteen activities across twelve reference
processes. Each one names the activity as that process words it.

- **Deliver the Intervention**
  - `ref/mkt/churn-risk-play`, activity 9 -
    [Run Churn-Risk Play](../../../../processes/marketing/churn-risk-play.md)
- **Issue the Response**
  - `ref/mkt/crisis-communication`, activity 11 -
    [Manage Crisis Communication](../../../../processes/marketing/crisis-communication.md)
- **Open Recruitment**
  - `ref/mkt/channel-program`, activity 11 -
    [Launch Channel Program](../../../../processes/marketing/channel-program.md)
- **Publish It on the Owned Channels**
  - `ref/mkt/announce-company-news`, activity 14 -
    [Announce Company News](../../../../processes/marketing/announce-company-news.md)
- **Send the Ask**
  - `ref/mkt/customer-reviews`, activity 10 -
    [Solicit Customer Reviews](../../../../processes/marketing/customer-reviews.md)
- **Send the Issue**
  - `ref/mkt/customer-newsletter`, activity 13 -
    [Publish Customer Newsletter](../../../../processes/marketing/customer-newsletter.md)
- **Send the Pre-Read**
  - `ref/mkt/advisory-board`, activity 9 -
    [Convene Customer Advisory Board](../../../../processes/marketing/advisory-board.md)
- **Send the Reminder**
  - `ref/mkt/customer-reviews`, activity 11 -
    [Solicit Customer Reviews](../../../../processes/marketing/customer-reviews.md)
- **Send the Sequence**
  - `ref/mkt/win-back-campaign`, activity 14 -
    [Run Win-Back Campaign](../../../../processes/marketing/win-back-campaign.md)
- **Send the Step**
  - `ref/mkt/onboarding-email-program`, activity 9 -
    [Run Onboarding Email Program](../../../../processes/marketing/onboarding-email-program.md)
- **Serve the Notice**
  - `ref/mkt/pricing-change`, activity 10 -
    [Launch Pricing Change](../../../../processes/marketing/pricing-change.md)
- **Start the Touches**
  - `ref/mkt/account-based-play`, activity 14 -
    [Run Account-Based Play](../../../../processes/marketing/account-based-play.md)
- **Tell the Customers Who Have It**
  - `ref/mkt/feature-release`, activity 7 -
    [Announce Feature Release](../../../../processes/marketing/feature-release.md)

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
