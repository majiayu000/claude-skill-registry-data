---
name: cx-case-timeline
description: Use to reconstruct what actually happened to one customer across every conversation, channel and handoff, for an escalation, complaint, post-mortem or goodwill decision. Trigger for "build a timeline for this customer", "what happened on this case", "summarize the back-and-forth before I decide", "when were they first told", escalation summaries, complaint investigations, or a case spanning several tickets.
metadata:
  author: rulebase
  version: "1.0.0"
  archetype: playbook
---

# Case timelines

Someone needs to decide something — a goodwill credit, a complaint response, whether
an agent misinformed a customer — and the facts are spread across several tickets,
two channels, a phone call, and a third-party thread. The deliverable is a timeline
someone can act on and, if it comes to it, defend.

**A case is not a ticket.** Almost everything that goes wrong in this task comes from
treating a ticket id as the boundary of the case.

## Step 1: anchor on the customer, not the ticket

Start from the ticket you were given, then widen. The case includes:

- **Earlier conversations from the same customer** about the same issue, often with
  no link between them. The first contact is usually the one that matters most and is
  the one nobody finds.
- **Channel switches.** A customer who chatted, then called, then emailed has three
  records and one problem.
- **Reopens and re-raises.** A closed ticket followed by a new one two days later is
  one case with a gap in the middle, and that gap is frequently the finding.
- **Merged and duplicate records.** Follow duplicate pointers in both directions. A
  merged ticket can look abandoned while the work continued under another id.
- **Internal-only threads** — escalations to a back-office queue, a tracker issue, a
  third-party investigation. The customer-facing record often goes quiet precisely
  while these are running, and a timeline without them shows unexplained silence.

Search on every identifier the customer has: account id, email, phone, company, and
the name as agents typed it. Report which identifiers you searched and which you
could not.

## Step 2: order by event time, not by record time

The single most common defect in a reconstructed timeline is wrong ordering, and it
comes from sorting on the wrong timestamp.

- **Event time** is when the message was actually sent in the source system.
- **Record time** is when it landed in whatever you are querying.

Backfills, sync lag and re-imports make these diverge by hours or months. Sorting a
timeline by record time produces a confident, plausible, wrong story — and it is
wrong in the most damaging way, because it can reverse cause and effect.

Sort on event time, fall back to record time only where event time is absent, and
**mark every entry where you fell back.** Where a timeline is used to establish who
knew what when, an entry with an uncertain timestamp is an entry that cannot support
that conclusion.

Normalise timezones and say which one the timeline is rendered in. Business-hours
context matters too: a nineteen-hour gap over a weekend is not the same neglect as a
nineteen-hour gap on a Tuesday.

## Step 3: separate three different things

Keep these in separate columns. Collapsing them is how a timeline becomes an
argument rather than a record.

1. **What the customer was told.** Customer-visible messages only.
2. **What actually happened internally.** Internal notes, status changes,
   escalations, third-party responses.
3. **What the record asserts.** Evaluation summaries, dispositions, tags, and the
   case's own status history.

The divergence between these is usually the finding. A case where the customer was
told "we're processing it" three times while the internal record shows no action
between them is a specific, defensible finding that no single column reveals.

## Step 4: attribute every turn correctly

- **A bot reply is not "we responded".** Automated acknowledgements, AI agent
  replies, and out-of-office autoresponders all look like agent messages in most
  data models. Label them, and never count them as a human response in a
  responsiveness finding.
- **Name the human who acted**, per turn, and note reassignments. A case handled by
  five people with no handoff notes is a routing finding.
- **Check for the customer's follow-ups.** A second unanswered message is much
  stronger evidence than a long first wait.

Do not trust a single author-type field in either direction; validate against the
message content on a sample before building attribution on it.

## Step 5: mark the gaps explicitly

**A timeline with an unmarked gap is worse than no timeline**, because the reader
assumes completeness and decides on it.

State plainly:

- Conversations you know exist but could not retrieve, by id.
- Channels not covered — a phone call with no recording, a chat that was not synced,
  an in-person branch visit.
- Periods with no records at all, distinguishing "nothing happened" from "we have no
  data".
- Content unavailable: transcripts that failed to load, redacted messages, deleted
  records.

Say which of your conclusions would change if a gap turned out to contain something.

## Template

```
Case timeline — <customer/account> — prepared <date>
Rendered in <timezone>. Ordered by event time; ~ marks an estimated timestamp.

Conversations in scope: #<id> (email), #<id> (chat), #<id> (voice), #<id> (internal)
Identifiers searched: <account id, email, phone, company>
Not retrievable: #<id> (<reason>)

  <date time>  <channel>  <actor: customer | agent name | BOT | third party>
               Customer-visible: <what was said, minimally quoted>
               Internal:         <note / status change / escalation>

  ...

Key findings
  - <what the customer was told vs what happened>
  - <unexplained gap of N business hours between X and Y>
  - <first point at which the issue was known internally>

Gaps and their effect
  - <gap> -> <which finding would change>
```

## Guardrails

- **Cite ids; quote minimally.** Support transcripts carry names, addresses, card
  fragments, and financial and health disclosures. Quote only the specific sentence a
  finding rests on, redact the customer's identifying details, and say you redacted.
- **Never reconstruct content you could not read.** If a transcript failed to load,
  the entry is "content unavailable", not a paraphrase from an evaluation summary.
  This is the one failure that destroys the credibility of the whole document.
- **Do not attribute intent.** Record what was said and done. "The agent did not
  check the account" is a finding; "the agent did not care" is not.
- **A timeline is not a decision.** If the request is a goodwill credit or a complaint
  outcome, present the facts and the options; the decision belongs to the person with
  the authority for it.
- **Expect this document to be read by someone outside the team.** Complaints and
  escalations get shared with regulators, legal, and sometimes the customer. Write it
  so that is fine.

## Present results to the user

1. **Scope** — conversations included, identifiers searched, timezone, ordering
   basis.
2. **The timeline**, in the template above.
3. **Findings**, each tied to specific entries.
4. **Gaps**, and which findings they could change.
5. **What this does not establish**, said plainly. Ordering uncertainty, missing
   channels, unretrievable content.
