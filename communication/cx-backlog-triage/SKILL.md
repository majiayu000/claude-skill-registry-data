---
name: cx-backlog-triage
description: Use to analyse a support backlog and find the conversations actually at risk — never-touched tickets, work stalled on your side, customers stranded with a bot, and unassigned open work. Trigger for "report on our open tickets", "daily outstanding tickets report", "how many tickets have we not responded to", "find tickets waiting on us", "customers stuck with a bot and no human", aging backlog, or a backlog that keeps growing.
metadata:
  author: rulebase
  version: "1.0.0"
  archetype: analysis
---

# Backlog triage

"How many open tickets do we have" is the wrong question, and the number that
answers it is close to meaningless. An open-ticket count mixes together work that is
legitimately parked, work waiting on the customer, spam that will never close, and
a small number of genuinely abandoned customer requests that are the entire reason
anyone asked.

The useful question is: **which conversations have a customer waiting on us, and how
long have they been waiting?**

## Why the naive count misleads

- **It counts work waiting on the customer.** In most helpdesks a large share of
  "open" work is parked awaiting a reply. Including it makes the backlog look
  frightening and hides the part that is actionable.
- **It counts spam and automation.** Notification emails, no-reply bounces,
  accounts-payable traffic and marketing blasts open tickets that nobody will ever
  work. On a real backlog these can dominate the "never touched" bucket entirely,
  which is why the untouched count on its own convinces nobody.
- **It has no age distribution.** A thousand tickets a day old and a thousand a
  month old are different situations with the same count.
- **It measures a stock, not a flow.** A stable backlog with high throughput is
  healthy. Report arrivals, closures and the resulting net change alongside the
  level, or the number cannot be interpreted.

## The four segments that matter

Segment by **who owes the next action**, and age from **the last action on your
side** — not from ticket creation. Creation age is dominated by long-parked work
and tells you nothing about neglect.

**1. Never touched.** No human agent action, ever. The highest-severity segment and
the one most contaminated by noise, so it needs the filtering below before it means
anything.

**2. Stalled on us.** A customer action is the most recent event, and no agent has
responded since. This is the real backlog. Age from the customer's last message.

**3. Waiting on customer.** We acted last and are waiting. Report it separately.
Worth checking for a follow-up policy: work parked indefinitely with no chase is
functionally abandoned even though the status looks correct.

**4. Bot-only, human never involved.** The customer has exchanged messages with an
automated agent and no human has ever replied. Escalate the subset where the
customer explicitly asked for a human, or expressed frustration, and did not get
one. This segment does not appear in any status-based view, and it is where the
worst customer experiences hide.

## Separating dropped requests from noise

This is the analytical work in backlog triage, and skipping it is why untouched-
ticket reports get dismissed.

For the never-touched population, classify rather than count:

- **Tag signals.** Find the tags that mark automation, spam, notifications and
  bulk traffic in this account, and quantify each. Do not assume tag names — derive
  the most common tags on untouched work and inspect them.
- **Customer linkage.** An untouched conversation linked to a known customer or
  company account is far more likely to be a real dropped request than one from an
  unrecognised sender. This is usually the strongest single signal.
- **Subject and first-message shape.** Sample subjects across the untouched set and
  characterise them. Auto-generated subjects cluster hard and are easy to name.
- **Channel.** Untouched voice and chat mean something different from untouched
  email — an abandoned chat may be a customer who left, which is a routing or
  staffing finding rather than a neglect finding.

Report the untouched count **twice**: raw, and after exclusions, with the exclusion
rules named. The gap between them is usually large, and stating both is what makes
the filtered number credible.

## Data required, and the traps in it

- **Status semantics are not portable.** "Pending" means awaiting-customer in some
  helpdesks and awaiting-agent in others; "on hold" and "solved-but-reopenable" vary
  the same way. Derive who-owes-the-next-action from **message events**, not from
  the status field, and use status only as a cross-check. Where you must use status,
  state the mapping you assumed.
- **Internal notes are actions.** A ticket where an agent left an internal note has
  been touched, even though the customer saw nothing. Whether that counts as a
  response depends on the question: for "did we neglect this" it counts; for "did
  the customer hear from us" it does not. Decide, and say which.
- **Business hours, not calendar hours**, for anything framed as a service
  expectation. A Friday-evening arrival is not eight hours late on Saturday morning.
  Get the schedule and the holiday calendar; if you cannot, report calendar hours
  and label them.
- **Timezones.** Aging arithmetic across a timezone boundary is off by hours, which
  matters enormously at short thresholds and not at all at long ones.
- **Bot and system accounts look like agents.** If an automated replier counts as
  an agent action, your untouched count collapses to almost nothing and the report
  is wrong in the reassuring direction. Identify these accounts explicitly and
  validate against a sample rather than trusting a single author-type field.
- **Merged and duplicate conversations.** A merged ticket can look abandoned while
  the work continued elsewhere. Resolve duplicate pointers before reporting age.

## Ranking by risk, not by age

Age alone puts the oldest parked spam at the top. Rank the "stalled on us" segment
by a combination of:

- **Time waiting**, in business hours, against the expectation for that queue
- **Whether the customer has followed up** — a second unanswered message is a much
  stronger signal than a long first wait
- **Explicit escalation language**, a complaint, a regulator mention, or a
  cancellation threat
- **Customer value or tier**, if available
- **Whether anyone owns it** — unassigned work has nobody to chase

Unassigned + open + customer-waiting is the highest-yield single filter in most
backlogs, and it is usually a routing rule failure rather than an agent problem.
Check whether the unassigned population clusters on a queue, a tag or a time of day
before concluding anything about people.

## Present results to the user

1. **The level and the flow** — backlog size, arrivals, closures, net change over
   the window. A level without a flow cannot be interpreted.
2. **The four segments**, with counts and the who-owes-next-action rule you used.
3. **Never-touched, raw and filtered**, with the exclusion rules and what the
   excluded traffic actually was.
4. **The ranked action list** — the specific conversations with a customer waiting,
   worst first, by id, with time waiting and why each ranks where it does. This is
   the part someone will work from, so keep it short enough to work through today.
5. **Bot-only strandings**, separately, with the subset that asked for a human.
6. **Systemic findings** — unassigned clusters, queues with no owner, follow-up
   policies not firing, integrations creating ticket noise. These fix the backlog;
   the action list only drains it.
7. **What you could not determine** — status mappings assumed, business hours
   unavailable, accounts you could not classify.

Cite ids and counts. Do not paste conversation text into chat.
