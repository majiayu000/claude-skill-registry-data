---
name: cx-complaints-sla
description: Use to compute and monitor regulated complaint deadlines — acknowledgement, holding response, final response — against business-day calendars, and to find cases about to breach. Trigger for "are we meeting our complaint deadlines", "complaint SLA breaches", "final response deadline", "which complaints are about to breach", complaint ageing reports, or building a complaints deadline monitor.
metadata:
  author: rulebase
  version: "1.0.0"
  archetype: analysis
---

# Complaint deadline clocks

Regulated complaint handling runs on deadlines that are not negotiable and not
business-as-usual SLAs: missing a final-response deadline is a reportable failure in
several regimes, not a dashboard amber.

The arithmetic looks trivial and is not. Almost every hand-rolled complaint clock is
wrong in at least one of the ways below, and the errors are systematically in the
optimistic direction — they make you look compliant when you are not.

## This skill does not know your deadlines

**Deadline lengths and rules vary by jurisdiction, sector, product and complaint type,
and they change.** This skill deliberately hard-codes none of them. It gives you the
clock mechanics; the deadlines come from your compliance function or the applicable
rules, as configuration.

If you do not have an authoritative source for the deadlines, that is the finding —
stop and get one. Computing precise breach counts against a half-remembered deadline is
worse than not computing them, because it produces a number people act on.

The same applies to interpretation: **whether a specific case breached, and whether a
breach is reportable, is a determination for compliance and legal.** Produce the clock
and the evidence; do not rule.

## The clock decisions that change the answer

**1. When does the clock start?** Options that all exist somewhere in practice: when
the complaint was received by anyone at the firm, when it was *identified* as a
complaint, or when it reached the complaints team. These can differ by days.

The gap between "received" and "identified" is the single most common source of
understated breach rates. A complaint expressed in an ordinary support ticket on the
3rd, recognised as a complaint on the 11th, and clocked from the 11th, understates the
age by eight days — and in most regimes the clock started on the 3rd. **Measure and
report identification lag separately**; it is both a compliance exposure and a training
finding.

**2. Business days or calendar days?** Different deadlines in the same regime often use
different units. Business-day counting needs the working-week definition *and* the
holiday calendar, per market. A multi-market operation needs one calendar per market,
and getting this wrong is worth days on every case.

**3. Does day counting start on the day of receipt or the next working day?** A
one-day systematic error across every case. State the convention.

**4. Can the clock pause?** In many complaint regimes **it cannot** — waiting for
information from the customer does not stop a final-response deadline, even though it
stops an ordinary support SLA. Do not import a pause rule from your support SLA
configuration. If your regime does permit pauses, they will have conditions attached.

**5. What satisfies the deadline?** Sent, or received? A response drafted on time and
sent late is late. A holding response may satisfy one deadline and not another.

**6. Which timezone?** Deadline arithmetic across a timezone boundary is off by a day
at the margin, and the margin is where breaches are.

## Compute it

```bash
node scripts/complaint-clock.mjs --input complaints.jsonl --config clock-config.json
```

The config carries your working week, holidays per market, and one entry per deadline —
its length, unit, what it runs from, and what satisfies it. See
[references/clock-config.md](references/clock-config.md) for the shape and the
conventions each option implies.

The script reports, per complaint and per deadline: the due date, whether it was met,
breached, or is still open, and how long is left. Open cases are bucketed by urgency so
the output is a work queue rather than a report.

## Monitoring, not reporting

A monthly breach count is an autopsy. The useful artefact is a daily queue of cases
approaching a deadline, ordered by time remaining.

- **Alert with enough lead time to act.** A final response needs drafting, review and
  sometimes approval. An alert on the due date is not a control.
- **Escalate on the approach, not the breach.**
- **Include cases with no owner.** An unassigned complaint accrues deadline the same as
  an assigned one, and unowned cases are over-represented in breaches.
- **Watch identification lag as its own metric.** It is where the hidden breaches are.

## Traps beyond the arithmetic

- **Reopened complaints.** Does a reopen restart the clock, continue it, or create a new
  complaint? A defensible answer is required and it must be applied consistently.
- **Complaints spanning several conversations.** One complaint may have three tickets.
  Clocking each separately understates age and multiplies the case count.
- **Complaints arriving through channels nobody monitors** — a review site, social,
  a regulator's portal, a letter. If they are not in the dataset they are not in your
  breach count, and their absence is not evidence of compliance. State which channels
  the data covers.
- **Complaints closed without a final response.** Check for cases closed with no
  response artefact. These are breaches that look like successes in a status-based
  report.
- **The severity of a small number.** Complaint volumes are low enough that a single
  breach can matter and percentage-based reporting hides it. **Report absolute counts,
  always, alongside any rate.**
- **Retrospective reclassification.** A case reclassified as a complaint after the fact
  inherits the original receipt date. Recompute historical breaches when
  classifications change, rather than freezing them.

## Guardrails

- **Do not assert a deadline length from memory**, in the analysis or the config. Source
  it, and record the source in the config so the next person can check it.
- **Do not determine whether a breach is reportable.** Flag it, with the evidence, and
  say the determination belongs to compliance and legal, who may have a notification
  clock of their own that starts when they are told.
- **Do not adjust a clock to avoid a breach.** Changing a start date, applying a pause
  the regime does not allow, or reclassifying a complaint to move a deadline is a
  serious matter. If the data shows any of these happening, that is a finding in itself
  and it outranks the breach count.
- **Read-only.** Do not update complaint records.
- **Cite ids; do not paste complaint content.** Complaint files contain financial
  circumstances, health disclosures and vulnerability information.

## Present results to the user

1. **The clock configuration used**, including the source of each deadline, the working
   week, the holidays, the pause rule, and the start-date definition. Everything that
   follows is conditional on this.
2. **Channel coverage** — which intake routes are in the data and which are not.
3. **Breaches, in absolute counts** as well as rates, per deadline type.
4. **Identification lag**, distributed, with the cases where it changed the deadline.
5. **The open queue**, ordered by time remaining, with owners and the unowned called out.
6. **Cases closed with no response artefact**, separately — the breaches a status report
   hides.
7. **Anything suggesting a clock was adjusted** rather than a deadline met.
8. **What needs a compliance determination** rather than an operational fix.
