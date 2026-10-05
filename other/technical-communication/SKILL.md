---
name: technical-communication
description: "Before writing anything, answer three questions: who reads this, what do they"
---

# Technical Communication (Verbose)

## Core Patterns

### Audience First, Then Structure

Before writing anything, answer three questions: who reads this, what do they
have to *do*, and what do they already know? The answers change the document
completely, not just its tone.

| Reader | Wants | Leads with |
|---|---|---|
| Your on-call peer | To act, now | The symptom and the mitigation |
| Your manager | To decide or unblock | The ask and the date |
| A staff engineer reviewing design | To find the flaw | The constraints and trade-offs |
| A stakeholder outside engineering | To plan around you | Impact and timeline, no mechanism |

The same migration produces four different first sentences. Writing one document
for "everyone" produces a document that serves no one — the executive wades
through connection-pool details, and the engineer cannot find the rollback plan.

### Bottom Line Up Front

BLUF is a discipline borrowed from military briefing: the first sentence carries
the conclusion or the request, and everything after it is supporting evidence
that a reader may stop consuming at any point without missing the point.

Most engineers write in discovery order — the order they learned things — which
is exactly backwards from the order a reader needs them.

```
❌ Discovery order
"Last week we started looking into the checkout timeouts. We first tried
raising the connection pool size, which didn't help. Then Priya suggested
profiling the gateway calls, and after some digging it turned out the
retry logic is nesting. We think we can fix it in a couple of days."

✅ BLUF
"Checkout timeouts are caused by unbounded retries in the payment gateway
client. Fix is ~2 days. I need a decision by Wednesday: ship behind a flag
or wait for the Nov 12 release train.

Detail: three nested retry layers (HTTP client, gateway SDK, and our
service wrapper) compound to as many as 27 attempts per checkout. Pool
size was a red herring."
```

The test: delete everything after the first paragraph. Does the reader still
know what happened and what you need? If not, the summary is not a summary.

### The Status Update

Status updates are the most-written and worst-written artifact in engineering.
The failure mode is narrating effort instead of reporting position.

```
❌ "Making good progress on the migration. Ran into some issues with the
    legacy adapter but working through them. Should be done soon."
```

Every clause here is unfalsifiable. "Good progress" is compatible with being
90% done or 20% done. "Soon" is compatible with Thursday or next month. The
reader must now schedule a meeting to extract what a sentence could have carried.

```
✅ Migration — on track for Thu Nov 24 (was Tue Nov 22; 2-day slip)

   Done:        6 of 8 services cut over (auth, users, orders, catalog,
                notifications, search)
   Remaining:   reporting (2d), billing (1d)
   Slip cause:  legacy adapter double-encodes UTF-8 on the reporting
                payload. Fixed in PRO-455, cost 2 days.
   Risk:        billing cutover needs a 15-min write freeze; not yet
                scheduled with finance
   Need from you: approve the write-freeze window (Thu 06:00-06:15 UTC)
```

Four properties make this work: a date with a delta against the previous date, a
count rather than a percentage, a named cause for the variance, and an explicit
"need from you" line. Include that last line in every update even when the value
is "nothing" — its absence is precisely what makes people open the thread and
ask.

### The Escalation

Escalating well is a specific skill: you are transferring a decision, not a
feeling. An escalation that lacks a recommendation delegates your judgment
upward along with the problem, which is the opposite of helpful.

```
❌ "I'm getting pretty worried about the launch timeline. There's a lot
    still outstanding and I don't think people realize how much is left
    on the SSO piece. Can we talk about this?"
```

This creates work: your manager must now discover the facts you already have,
and form the opinion you already hold.

```
✅ Subject: Nov 3 launch at risk — recommend Nov 17

   Recommendation: move launch to Nov 17.

   Why: SSO integration needs ~3 weeks; 1.5 weeks remain. The vendor's
   staging environment has been down since Oct 12 (their ticket #4471,
   no ETA), so we cannot test the SAML assertion path at all.

   Options:
     A. Move to Nov 17. No scope loss. My recommendation.
     B. Launch Nov 3 without SSO. 4 enterprise accounts (~$180k ARR)
        cannot onboard; they were promised SSO at signing.
     C. Add a second engineer now. Saves ~4 days — not enough to hold
        Nov 3, and slows the current work for 2 days of ramp.

   Decision needed by Fri Oct 24. After that, A is the only option left,
   because the release train cutoff passes.

   What would change this: if the vendor restores staging before Oct 22,
   Nov 3 becomes viable at roughly 60% confidence.
```

The final line is what separates an escalation from a complaint: it tells the
reader what evidence would reverse the recommendation.

### Writing for the Skimmer

Assume your reader gives the document 15 seconds before deciding whether to
invest more. In those 15 seconds they will read headings, bold text, the first
line of each paragraph, and any table. Design for that path deliberately.

- Front-load every paragraph — the first sentence carries the claim, the rest
  supports it. A reader who stops after sentence one still gets the point.
- Cap paragraphs at about 5 lines. Longer blocks get skipped wholesale.
- Use a table whenever you have 3+ items compared on 2+ dimensions. Prose
  comparison forces the reader to build the table in their head.
- Bold the decisions and the asks, nothing else. Bolding for emphasis
  everywhere is bolding nowhere.
- Put the detail in an appendix or a collapsed section rather than deleting it.
  Skimmers skip it; the one person who needs it can still find it.

### Design Docs People Actually Review

A design doc's purpose is to get objections *before* the code exists. Most design
docs fail at this, and the failure is usually structural rather than stylistic.

What makes a doc reviewable:

- **Circulated before implementation, not after.** A doc sent alongside the PR
  is a status report. Reviewers know their objections are now expensive and
  will stay quiet.
- **Constraints stated first.** Reviewers cannot evaluate a design without the
  boundaries: what latency budget, what scale, what must not change, what team
  owns the downstream system.
- **Alternatives with real reasons for rejection.** "Considered Kafka, rejected
  it" is filler. "Rejected Kafka: we have no Kafka expertise on-call, and the
  ordering guarantee we need is per-user, which the existing queue already
  gives us" is a claim a reviewer can attack.
- **An explicit list of what you want reviewed.** "I am confident about the
  schema; I want scrutiny on the backfill strategy and the rollback path."
  Ungated docs get either no comments or comments about naming.
- **A decision deadline.** "Comments by Thu; I start Fri with whatever we have."
  Open-ended docs collect comments forever and decide nothing.
- **Length under about 3 pages** for the main argument. Longer means fewer
  readers, and the marginal reader is usually the one who spots the flaw.

### Async-First and the Written Record

In any team spanning time zones or more than a handful of people, the default
medium must be written and durable. This is not merely a convenience preference —
it changes who can participate. A decision made in a call includes only the
people in that call, and excludes everyone asleep, on leave, or hired next month.

The operating rule: **a decision that is not written down did not happen.**

Not as a moral stance, but as an accurate prediction. Six weeks later there is no
recollection of who agreed to what, the reasoning is lost, and the same argument
runs again from zero — usually with a different outcome, which is worse than
either outcome consistently applied.

So: synchronous discussion is fine and often faster for resolving a stuck
disagreement. But it is not the artifact. Within the hour, post:

```
Decision: we will use per-user ordering in the existing SQS queue rather
          than introducing Kafka.
Decided by: Priya (owner), John, Marcus — call on Oct 21.
Reasoning: our ordering requirement is per-user, not global. SQS FIFO
          with user_id as the group key satisfies it. Kafka would add
          an operational surface nobody on this on-call rota knows.
Rejected: Kafka (ops burden), Redis streams (no durability guarantee we
          can defend to compliance).
Revisit if: we need cross-user global ordering, or throughput exceeds
          3k msg/s per group (SQS FIFO limit).
```

The "revisit if" line is doing real work. It converts a decision into a standing
condition, so the next engineer knows whether the reasoning still applies rather
than either blindly following it or blindly overturning it.

### Communicating Uncertainty Honestly

A single-point estimate is a lie of precision. It silently converts your guess
into another team's commitment, and when it slips, the cost is trust rather than
just schedule.

```
❌ "Should take about a week."

✅ "3-8 days, low confidence.
    3 days if the auth layer uses the standard session middleware.
    8 days if it has the custom token handling I've heard about.
    I'll know which within a day of starting, and will update then."
```

Four components, all necessary:

| Component | Example |
|---|---|
| Range, not a point | 3-8 days |
| Confidence level | low / medium / high |
| What drives each end | standard middleware vs custom token layer |
| When it resolves | one day after starting |

The same structure works for incident impact ("between 400 and 2,000 users
affected; the range is wide because we sample request logs at 5%"), for
capacity ("this holds to somewhere between 5k and 15k RPS; untested above 5k"),
and for risk. Widening a range costs you nothing with a reader who trusts you,
and false precision is what destroys that trust.

State confidence explicitly rather than hedging with adverbs. "Probably fine"
is unmeasurable; "80% confident, and the 20% is the migration lock" is a claim
someone can plan around.

For incident-specific narrative and timelines, see `incident-timeline-creation`.

## Common Anti-Patterns

❌ **Chronological narration** — "First we tried X, then Y, then we found Z."
The reader reconstructs your week to find the conclusion.
✅ Conclusion first, evidence after. Discovery order is for your notes, not for
your reader.

❌ **The buried ask** — a request for a decision in the final paragraph of a
long thread, or implied and never stated.
✅ The ask goes in the first two lines and names a person and a date.

❌ **Unfalsifiable status** — "good progress", "some issues", "almost done",
"should be soon".
✅ Counts, dates, deltas against the last date, and a named cause for variance.

❌ **Single-point estimates** — "about a week", which becomes a committed date
in someone else's plan by the next morning.
✅ A range, a confidence level, the driver of each end, and a resolution date.

❌ **Escalating a feeling** — "I'm worried about the timeline."
✅ Escalate a recommendation with options, costs, a decision deadline, and what
evidence would change your mind.

❌ **Decisions that live only in a call or a DM** — reasoning lost, argument
repeated next quarter with a different outcome.
✅ Post decision, reasoning, rejected alternatives, and revisit-conditions to a
durable place within the hour.

❌ **The design doc sent with the PR** — reviewers understand their objections
are now expensive and stay silent.
✅ Circulate before implementation, name what you want scrutinized, set a
comment deadline.

❌ **One document for every audience** — the executive reads pool-size details,
the engineer cannot find the rollback plan.
✅ Pick one primary reader. Write a 3-line summary that serves the others and
link to the detail.

❌ **Prose comparison of many options** — three paragraphs the reader must
convert into a table themselves.
✅ Give them the table.

❌ **Hedging adverbs as risk management** — "probably", "should be fine",
"hopefully".
✅ Numbers: "80% confident; the 20% is the migration lock window."

## Communication Checklist

- [ ] Primary reader identified, and what they must do
- [ ] Conclusion or ask is in the first two lines
- [ ] Document survives deleting everything after paragraph one
- [ ] Every estimate has a range, a confidence, and a resolution date
- [ ] "Need from you" line present, even if it says "nothing"
- [ ] Dates carry a delta against the previously communicated date
- [ ] Variances have a named cause, not "some issues"
- [ ] Escalations carry a recommendation, options with costs, and a deadline
- [ ] Escalations state what evidence would reverse the recommendation
- [ ] 3+ items compared on 2+ dimensions are in a table
- [ ] Paragraphs under ~5 lines; first sentence carries the claim
- [ ] Design doc circulated before implementation, with a comment deadline
- [ ] Design doc names what specifically needs scrutiny
- [ ] Rejected alternatives include the actual reason for rejection
- [ ] Every synchronous decision written to a durable place within the hour
- [ ] Written decisions include reasoning and revisit-conditions
