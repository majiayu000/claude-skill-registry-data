---
name: cx-account-escalation-protocol
description: Use to design or audit the executive escalation path for a major account — intake, ownership, communication cadence and follow-through — so escalations are resolved rather than merely attended. Trigger for "design our escalation process for key accounts", "an executive escalation went badly", "customer went to our CEO", red account war rooms, or escalations that get attention and then quietly stall.
metadata:
  author: rulebase
  version: "1.0.0"
  archetype: playbook
---

# Executive account escalations

This is the path a major customer takes when the normal one has failed — a call to
their account team, an email to an executive, a threat to leave. It is distinct from
tier-2 escalation: the issue may be ordinary, and what has escalated is the
relationship.

These fail in a recognisable pattern. Attention arrives quickly, several senior people
join, the customer is reassured — and then the underlying issue returns to a normal
queue and nothing changes. The customer's second escalation is far more damaging than
the first, because they have now learned that escalating produces attention rather than
resolution.

**So the design problem is not intake. It is follow-through.**

## Define the trigger, before you need it

An escalation path with no entry criteria gets used for whoever shouts loudest, which
means it under-serves the customers least willing to shout.

Write the triggers down:

- **Customer-initiated** — an explicit escalation request, contact with an executive, a
  stated intention to leave, or a legal or regulatory threat.
- **Internally triggered** — an unresolved issue past a threshold on a named account, a
  repeat failure, a service commitment breached, a failed recovery after a previous
  escalation.
- **Severity-triggered** — anything affecting the customer's ability to operate.

**Internal triggers matter more than they look.** They are what stops the process from
serving only the vocal, and they are the ones usually missing.

## One owner, named, for the duration

Not a channel, not a team, not a rotating duty. One person who owns the outcome until it
is closed, whose name the customer knows.

- **Separate the owner from the fixer.** The owner coordinates and communicates; specialists
  fix. Making a senior engineer the owner reliably means communication stops while they
  work.
- **The owner is not necessarily senior.** Seniority helps unblock; ownership needs
  availability and follow-through. Pair a capable owner with a named executive sponsor who
  can clear obstacles.
- **Handover is explicit and told to the customer.** Silent reassignment is how these
  stall.

## Communication cadence, committed and kept

The commitment that matters is not a resolution date — you often cannot know it. It is an
**update cadence**, which you can always keep.

- **Commit to the next update, not the fix.** "I'll update you by 4pm tomorrow whether or
  not we've solved it."
- **Update even when there is nothing to report.** A no-news update on time is worth more
  than a substantive one late. Missed updates are the most common single cause of a second
  escalation.
- **One channel, one voice.** Multiple people contacting the customer independently
  produces contradictions and reads as chaos.
- **Never commit to a date the fixing team has not agreed.** Comfort dates that slip cost
  more than the honest uncertainty they were meant to avoid.

## Follow-through is the part that fails

Design it explicitly, because attention decays on its own:

- **The issue does not return to a normal queue on close of the escalation.** It stays owned
  until the root cause is addressed or a decision is taken not to address it — and that
  decision is communicated.
- **A closure conversation with the customer**, confirming *they* consider it resolved.
  Internal closure is not resolution. This single step catches most of the "we thought it
  was fixed" failures.
- **A post-escalation review**: what failed, why the normal path did not catch it, and what
  changes. Without this, the same escalation recurs on a different account.
- **A watch period.** A recurrence within weeks of closure is a different and more serious
  event; flag it as such rather than opening a fresh escalation at the same severity.

## Auditing an existing process

When the brief is "an escalation went badly", look in this order:

1. **Was the update cadence kept?** Compare committed updates against sent ones. This is
   usually the answer, and it is measurable from the record.
2. **Was there a single named owner throughout?** Count owner changes.
3. **Did anyone commit to a date that slipped?**
4. **Was the root cause addressed, or just the symptom?** Check whether the underlying
   issue recurred for this or any other account.
5. **Did the customer agree it was resolved**, or did it go quiet?
6. **Had this account escalated before?** A second escalation means the first one's
   follow-through failed, and that is the finding.
7. **Would an internal trigger have caught it earlier?** If the signals were present and
   nobody acted, the gap is detection, not handling.

Across escalations, report: time to owner assignment, update-cadence adherence, time to
resolution from the customer's *first* contact rather than from escalation, recurrence
rate, and the share that were internally versus customer-triggered. **A low
internally-triggered share means you are waiting to be told.**

## Guardrails

- **Do not let escalation become the service level.** If a meaningful share of a segment's
  issues need escalation to get resolved, the normal path is broken and the escalation
  process is masking it. Report escalation rate per account and per segment as a health
  metric on the normal path.
- **Do not buy silence.** Compensation offered in exchange for withdrawing a complaint, a
  review or a regulatory referral is a serious conduct problem.
- **A regulatory or legal threat changes the process.** It may start a formal complaint
  clock with its own obligations and it needs compliance and legal involved immediately.
  Do not handle it as a relationship matter, and do not assess the regulatory consequence
  yourself.
- **Vulnerability signals override commercial framing.** An escalation from a customer in
  distress or financial difficulty is handled under that duty first, whatever the account
  is worth.
- **Escalation priority follows severity and contract, not revenue alone.** Systematically
  resolving the same defect for large accounts and not for small ones is, in regulated
  sectors, a conduct issue.
- **Cite ids; do not paste transcripts.** Escalation reviews reach executives and sometimes
  the customer.

## Present results to the user

1. **Trigger criteria**, with internal triggers named explicitly.
2. **Ownership** — one named owner, the sponsor, and the handover rule.
3. **The cadence commitment**, and adherence measured against it.
4. **The follow-through design** — post-escalation ownership, customer-confirmed closure,
   review, and watch period.
5. **For an audit**: the seven checks in order, with the evidence for each.
6. **Programme metrics** — time to owner, cadence adherence, resolution from first contact,
   recurrence, and the internally-triggered share.
7. **Escalation rate as a health metric on the normal path**, so a well-run escalation
   process does not hide a failing one underneath.
