---
name: cx-alert-monitor-spec
description: Use to turn a one-off support search into a standing monitor or alert that stays useful instead of being muted within a fortnight. Trigger for "alert me when a customer mentions X", "notify the team when complaints spike", "keep watching for this", "set up a daily monitor for", turning an ad-hoc sweep into something recurring, or an existing alert nobody reads any more.
metadata:
  author: rulebase
  version: "1.0.0"
  archetype: playbook
---

# Alert and monitor specs

The pattern is always the same. Someone runs a search — every conversation where a
customer threatened to go to the regulator, every ticket about a failing payment
partner — finds it valuable, and asks to be told whenever it happens again.

Almost every alert built this way is muted or ignored within two weeks, for one
reason: **it fires more often than anyone budgeted for, and nobody measured that
before shipping it.**

The good news is that you already have the data to predict it. The historical sweep
that motivated the alert *is* the volume forecast.

## Step 1: forecast the alert volume before building anything

Run the detection rule over a historical window and count how often it would have
fired, per day and per week. Then check that number against the reality of who is
meant to act on it.

Rough guidance, and worth stating to the user explicitly:

| Firing rate | Viable if |
| --- | --- |
| A few per week | A named person reviews each one. This is the sweet spot. |
| A few per day | There is a rota and a triage step. |
| Tens per day | Only as a queue or a dashboard, never as a notification. |
| Hundreds per day | Not an alert. It is a metric — chart it. |

**If the forecast is above the budget, fix the rule or change the delivery. Do not
ship it and hope.** An alert channel that people mute is worse than no alert, because
everyone believes the risk is covered.

State the forecast in the spec. It is the number that makes the alert's fate
predictable rather than a surprise a fortnight later.

## Step 2: pick the precision target deliberately

Precision and recall trade off, and the right point depends entirely on what happens
when the alert fires.

- **A human reviews each one and can dismiss it in seconds** — favour recall. A
  quarter of the alerts being irrelevant is tolerable if missing a real one is
  expensive.
- **The alert triggers a costly action** — an escalation, waking someone, contacting a
  customer — favour precision hard. Every false positive spends credibility.
- **Regulatory or safety topics** — favour recall, and route to a queue with an
  owner rather than an interrupt, so high volume does not force a precision
  compromise you cannot afford.

Measure both on a labelled historical sample rather than guessing. Take the
conversations the rule would fire on, label them by hand, and report the precision.
A few dozen labelled examples is enough to tell a 90% rule from a 50% one, and that
is the distinction that decides whether this ships.

Write the measured precision into the spec, with the sample size. It is also the
baseline for detecting decay later.

## Step 3: threshold detection or spike detection?

These are different mechanisms and people conflate them.

**Threshold** — "alert when any conversation matches X". Right for rare, individually
important events: a regulator mention, a threat to close a major account, a specific
compliance phrase. Volume scales with your traffic, so re-forecast when traffic grows.

**Spike** — "alert when complaints about X rise unusually". Right for aggregate
patterns where any single instance is unremarkable. Needs a baseline, and the baseline
needs to respect the shape of support traffic:

- **Seasonality is strong and multi-period.** Support volume has a day-of-week
  pattern and an intraday pattern, and both are large. A rule comparing this Monday
  to last Thursday will fire every week for no reason.
- **Compare like to like** — same weekday, same hour band, over several weeks — or
  use a baseline that models the periodicity.
- **Set the threshold on the historical distribution of the deviation**, not on a
  round number like "double". Report how often the rule would have fired historically
  and what was happening on those days.
- **Beware of the denominator.** A spike in the *share* of contacts about X and a
  spike in the *count* mean different things; on a quiet day the share can jump on two
  extra tickets. Alert on both together, with a minimum count floor.
- **A holiday calendar is not optional.** Public holidays break every baseline, and
  they differ per market.

## Step 4: state, dedup and escalation

The mechanics that separate a monitor from a firehose:

- **State.** The monitor must remember what it has already fired on. Alerting on the
  same conversation every run because it is still open is the fastest way to get
  muted. Persist fired ids.
- **Dedup and group.** Twelve conversations about one outage is one incident. Group by
  the underlying cause where you can, and alert once with a count and a list.
- **Cool-off.** After firing on a topic, suppress repeats for a defined window and
  report the accumulated count when it lifts.
- **A named owner, not a channel.** An alert posted to a channel with no owner is
  read by nobody. Route to a person or a rota, and say what they are expected to do
  when it fires. If nobody will own it, that is a reason not to build it.
- **What "acted on" means.** Define the closing action, so the alert can be measured
  later on whether it led to anything.
- **A kill switch, and who may use it.** Every monitor needs to be turnable off by the
  people it wakes, without a deployment.

## Step 5: schedule its own review

Monitors rot. The phrasing customers use changes, the product changes, the partner
gets fixed, and the rule quietly stops matching or starts matching everything.

Put a review date in the spec, and at review answer three questions:

1. **How often did it fire, versus the forecast?**
2. **What share of firings were acted on?** Near zero means retire it or fix precision
   — a monitor nobody acts on is a monitor nobody reads.
3. **Did it miss anything?** Look for incidents found another way that this should have
   caught. This is the only check on decaying recall, and it is the one always skipped.

A monitor with no review date is a monitor that will be wrong indefinitely.

## Never automate these

- **Replying to a customer.** Detection is not judgement. An alert may draft; a human
  sends.
- **Closing, merging or reassigning** on the strength of a detection rule.
- **Escalating to a regulator or a third party.**
- **Anything irreversible**, on any confidence level.

A monitor's job is to put the right conversation in front of the right person quickly.
The moment it acts, its false-positive rate becomes a business risk rather than an
annoyance.

## Spec template

```yaml
name: regulator-mention-monitor
owner: <person or rota>            # not a channel
purpose: <the decision this exists to enable>

detection:
  type: threshold                  # or spike
  rule: <the matching logic, precisely>
  languages: [<every language your team works in>]
  scope: <channels, queues, markets>

measured:
  window: <historical window used>
  would_have_fired: <n per week>
  precision: <x>% on <m> hand-labelled examples
  known_misses: <what the labelling found it missed>

delivery:
  mode: notify | queue | dashboard
  dedup: <grouping key>
  cool_off: <window>
  state: <where fired ids are persisted>
  expected_action: <what the owner does>
  kill_switch: <who can disable, how>

review:
  next: <date>
  retire_if: <acted-on rate below x, or purpose gone>
```

## Present results to the user

1. **The volume forecast**, first — how often this would have fired historically, per
   day and per week. This is the number that decides whether to build it.
2. **Measured precision and recall**, with the labelled sample size and examples of
   both false positives and misses.
3. **The spec**, as a file they keep.
4. **The delivery recommendation** — notify, queue, or chart — justified by the
   forecast rather than by the request.
5. **What it will miss**, stated plainly. Languages not covered, channels out of
   scope, phrasings the rule cannot catch.
6. **The review date**, and the condition under which it should be retired.
