---
name: cx-flow-efficiency
description: Use to analyse touch time vs elapsed time across the resolution path — queue wait, customer wait, back-office wait, and where elapsed time hides real delay. Trigger for "flow efficiency", "touch time vs elapsed time", "where is the time going", "customers waiting on us", back-office bottlenecks, idle time in cases, or end-to-end time much longer than handle time.
metadata:
  author: rulebase
  version: "1.0.0"
  archetype: analysis
---

# Flow efficiency

Handle time is what agents work. Elapsed time is what customers wait. They diverge —
often by an order of magnitude — and most CX reporting only tracks the shorter one.

**Flow efficiency** (in the lean sense) is the ratio of touch time — value-adding work —
to total elapsed time from first contact to resolution. Support operations rarely measure
it directly, but the decomposition answers the question leadership actually asks: *why
did this take a week when the call was ten minutes?*

The analysis maps where elapsed time accumulates when nobody is actively working the
case, and which buckets you can influence.

## Touch time vs elapsed time

| Term | Meaning | Typical owner |
| --- | --- | --- |
| **Touch time** | Agent (or system) actively working — talk, chat, research, wrap | Agent, tooling, knowledge |
| **Queue wait** | Customer waiting for first or next agent | Staffing, routing |
| **Internal wait** | Case idle while waiting on another team, approval, or system | Process, escalation design |
| **Customer wait** | Case open pending customer reply or action | Process, clarity of request |
| **External wait** | Third party, carrier, bank, vendor | Different remedy than internal |
| **Elapsed time** | Wall-clock first contact to resolution | All of the above |

For async channels, **resolution time** is elapsed time; **handle time** summed across
segments is touch time. A ticket with nine minutes of handle and six days elapsed is
low flow efficiency — and may still meet SLA if SLA measures first response only.

Declare which clock anchors the analysis: **customer-first-contact** is the default for
customer-visible flow.

## Decompose before diagnosing

Build a timeline per case or per cohort:

1. First customer contact
2. First agent engagement (queue wait ends)
3. Each transfer, escalation, or status change
4. Each outbound request to customer or third party
5. Each inbound response
6. Internal resolution (work done, customer not yet told)
7. Customer notified / case closed

Sum durations between events into buckets. Report **share of elapsed time in each
bucket** for the cohort — not only averages on one bucket.

The bucket with the largest share names the lever. Averages hide when a minority of
cases spend days in internal wait while most resolve same day; report p50 and p90
elapsed by bucket.

## Where elapsed time hides

**Waiting in queue** — visible on voice and chat; often invisible on async if "received"
timestamp is first scan not first action.

**Waiting on customer** — legitimate when the request was clear; failure mode when the
agent asked for information already provided, or sent a template that did not match the
issue. High customer-wait share with low response rate may mean requests are unclear or
channels are wrong (email ask on a phone-only customer).

**Waiting on back-office** — escalation accepted but not started, work done but not
communicated, ticket linked to external tracker with no sync back. Often the largest
hidden bucket. Measure **acceptance lag** (escalated → first action by receiver) and
**return lag** (internal resolution → customer notified) separately.

**Waiting on approval / authority** — distinct from back-office if the blocker is a
person or policy gate, not a work queue.

**Reopen and ping-pong** — elapsed time resets partially; multiple segments stack.
Multi-segment cases need segment-level decomposition, not one elapsed number.

**Scheduled or deferred work** — callback promised for Thursday counts as elapsed wait
from the customer's view even if touch time on Thursday is short.

## Flow efficiency without fake precision

Classic lean flow efficiency = touch time ÷ elapsed time. In support, touch time is
often incomplete in data (after-contact work in another system, manager approvals offline).

Use a **defensible partial decomposition**:

- Report **known active time** vs elapsed, and list **unallocated elapsed** explicitly
- Never imply unallocated time is zero
- Where only total elapsed and total handle exist, report **handle-to-elapsed ratio**
  as a lower bound on efficiency, with the caveat that handle may exclude wrap and
  internal notes

Compare cohorts: same contact driver, different elapsed — the bucket diff names process
variant or team behaviour.

## Reading the pattern table

| Dominant bucket | What it usually means | First question to ask |
| --- | --- | --- |
| Queue wait | Staffing or routing | Is volume staffed to interval? |
| Customer wait | Pending input | Was the request necessary and clear? |
| Internal wait | Handoff or capacity | Who owns the idle period? |
| External wait | Dependency | Is status visible to customer? |
| High touch, high elapsed | Rework or complexity | Repeat contacts within case? |
| Low touch, high elapsed | Process lag | Work happened elsewhere unlogged? |

Cross with **contact driver**. One driver with 80% internal wait is an escalation design
problem; another with 80% customer wait may be correct for document collection.

## Link to outcomes

Long elapsed with short touch correlates with repeat contact, complaint, and survey
dissatisfaction even when handle-time QA scores are high — the customer experienced
the idle periods, not the ten active minutes.

Report flow decomposition alongside **repeat contact and CSAT** by driver where sample
allows. Efficiency without outcome context optimises the wrong bucket (e.g. pressuring
agents to close while internal wait unchanged).

## Traps

- **SLA on first response only** — team hits target while elapsed runs to days. Report
  SLA attainment with elapsed p90 for the same cohort.
- **Status fields as proxies for buckets** — "pending" may mean customer, internal, or
  forgotten. Validate statuses against event log on a sample.
- **Merge external and internal wait** — remedies differ; one bucket hides vendor delay
  as "our backlog".
- **Single elapsed metric on reopened tickets** — use case identity across segments.
- **Attributing internal wait to the last assigned agent** — idle during back-office
  queue is organisational.
- **Invented benchmarks** for "good" flow efficiency percentage. Report your own
  distribution and trend; compare drivers internally.

## Present results to the user

1. **Data coverage** — which intervals are observed, which are inferred, which are
   unallocated; clocks used (first contact vs ticket creation).
2. **Elapsed vs touch summary** — p50/p90 for each, and handle-to-elapsed ratio as lower
   bound where full touch is incomplete.
3. **Bucket share of elapsed time** — queue, customer, internal, external, active touch;
   p50 and p90 where distribution is skewed.
4. **Acceptance and return lag** — for escalated cohorts, if applicable.
5. **Driver-level breakdown** — top drivers by total customer-days waited (volume ×
   elapsed), not only by median elapsed.
6. **Pattern diagnosis** — table matched to this operation's dominant buckets.
7. **Outcome link** — repeat contact or satisfaction where available, with sample caveats.
8. **Ranked levers** — each names a process, routing, or staffing change; not "agents
   should work faster" when internal wait dominates.
