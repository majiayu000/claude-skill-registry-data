---
name: cx-emerging-harm-scan
description: Use to scan support conversations for a harm nobody has categorised yet — a new failure mode, a scam pattern, or a product change hurting a group of customers before it shows in any metric. Trigger for "is anything new going wrong", "scan for emerging issues", "early warning from support", horizon scanning, a new scam pattern, or preparing for a question about what you might be missing.
metadata:
  author: rulebase
  version: "1.0.0"
  archetype: analysis
---

# Scanning for harm you have no category for

Every monitoring system in a support operation looks for things someone already thought
of. Tags, alerts, complaint categories and QA criteria all encode last year's known
failures.

Emerging harm is by definition outside that. It arrives as conversations that do not fit
existing categories, gets tagged "Other", and is discovered months later — often by a
regulator, a journalist, or a customer forum.

This is the deliberately open-ended counterpart to categorised monitoring. It is
exploratory, it will produce false leads, and it is worth running anyway because the
alternative is finding out from outside.

## Where uncategorised harm actually shows up

Six places, roughly in order of yield:

**1. The "Other" bucket and its growth rate.** The most reliable single indicator. A
rising Other rate in a stable taxonomy means something is arriving that the taxonomy
cannot describe. Read a sample of Other every period — not the aggregate, the actual
conversations.

**2. Long conversations with no clean resolution.** Novel problems take longer and end
ambiguously, because nobody has a script. Sort by turn count and look at the tail.

**3. Agent uncertainty.** Internal notes asking colleagues, escalations with no
destination, "has anyone seen this before". **Agents notice new failure modes weeks
before any metric moves**, and this signal is usually sitting in internal notes that
nothing analyses.

**4. Conversations that escalate without a policy hook.** An escalation is a human
judging something serious; one with no matching policy or category is a strong candidate.

**5. New vocabulary.** Terms appearing in customer language that were not there before —
a new third party, a new scam framing, a new device or app, a new regulation customers
have heard about. Term-frequency change over time surfaces these without any prior
hypothesis.

**6. Clusters with no tag.** Semantic clustering over recent conversations, filtered to
clusters that do not map to an existing category. Useful where available, and the
clusters need reading rather than counting.

## Method

1. **Fix the window and the baseline.** Something is "emerging" relative to a prior
   period, so you need both.
2. **Run several passes.** Other-bucket sampling, long-tail reading, internal-note
   search, unhooked escalations, vocabulary change, and clustering if available. Each is
   blind to what the others find — that is the point of running all of them.
3. **Read the candidates.** This step cannot be skipped or delegated to a metric.
   Emerging harm is identified by a human recognising that something is wrong, and the
   analysis's job is to put the right twenty conversations in front of them.
4. **Characterise each candidate**: what happens to the customer, what causes it, who is
   affected, whether it is growing.
5. **Size it from operational data**, not from conversation volume. Complaint and contact
   volume are a weak proxy for how many customers are affected — and for a new harm the
   contact rate is usually low precisely because customers do not yet understand what
   happened to them.
6. **Triage by severity, not volume.** A harm affecting twenty customers badly outranks a
   mild annoyance affecting two thousand. This inverts normal contact-driver
   prioritisation, and it is the correct inversion for this exercise.

## What to look for specifically

Categories of emerging harm worth an explicit pass, because they recur across
industries:

- **A new scam or fraud pattern** targeting your customers, especially one that uses your
  brand or your product's mechanics. Customers describe these before your fraud systems
  see them, and the description is often the only early evidence.
- **A product or pricing change producing an unintended outcome** for a subset — legacy
  plans, edge-case configurations, customers mid-process when something changed.
- **An automation or AI agent behaving badly** in a case nobody tested.
- **A third-party failure** you are carrying — a partner, a payment provider, a courier —
  where customers experience it as your failure.
- **A group struggling with something new** — a redesign, a new verification step, a
  channel closure — where the difficulty is concentrated and invisible in the average.
- **A regulatory or external change** customers are reacting to before you have a position.

## Expect false positives, and say so

This scan trades precision for recall deliberately. A candidate list of fifteen where
two are real is a success, and framing it that way protects the exercise — a scan
presented as fifteen findings will discredit itself on the thirteen.

- **Present candidates as candidates.** Distinguish "worth investigating" from
  "confirmed".
- **Rule out the boring explanations first**: a taxonomy change, a routing change, a
  campaign, a backfill landing old conversations, a channel newly connected, a seasonal
  pattern.
- **Confirm with a second source** before escalating anything — operational data, product
  telemetry, or another channel showing the same thing.
- **Keep a register of dismissed candidates** with the reason. Some come back, and a
  second appearance is much stronger evidence than a first.

## Cadence

Run it periodically rather than continuously — this is a review, not a monitor. Once a
candidate is confirmed, it graduates: it gets a category, a monitor with a volume
forecast, and an owner. **The scan's output is new categories and new monitors**, which
is how the categorised system stops being last year's.

Also run it after any significant change — a launch, a pricing change, a migration, an
automation deployment — where the specific value is finding the unintended consequence
before the retrospective does.

## Guardrails

- **A candidate is not a finding.** Do not brief an unconfirmed pattern as a known harm;
  the credibility cost of one wrong escalation is high.
- **A confirmed harm goes to its escalation route immediately**, not into the next
  periodic report. If it involves customer detriment, whether it is reportable is a
  compliance and legal determination with its own clock.
- **A suspected scam pattern goes to fraud and security now**, and the pattern details
  should not circulate widely — attack details in a broadly-shared document are a
  liability.
- **Vulnerability and safeguarding signals** found incidentally go through their own
  route, at aggregate level in any report.
- **Cite ids, quote minimally, redact.** These reports reach senior audiences and travel.
- **Do not let the scan become a metric.** Counting candidates found rewards volume and
  destroys precision.

## Present results to the user

1. **What was scanned** — window, baseline, which passes were run, languages and channels
   covered.
2. **Candidates, explicitly labelled as candidates**, ranked by potential severity rather
   than volume.
3. **For each: what happens to the customer, the suspected cause, who is affected, and
   whether it is growing.**
4. **Boring explanations ruled out**, per candidate.
5. **Confirmed harms, separately**, with the escalation already made rather than
   recommended.
6. **Population estimates from operational data**, with the caveat that contact volume
   understates a new harm.
7. **Graduations** — candidates now confirmed and needing a category, a monitor and an
   owner.
8. **Dismissed candidates and why**, kept as a register for next time.
9. **What the scan could not see** — passes not run, languages not covered, channels
   outside the data.
