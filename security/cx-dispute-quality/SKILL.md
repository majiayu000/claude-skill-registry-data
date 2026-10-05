---
name: cx-dispute-quality
description: Use to audit how payment disputes, chargebacks and unrecognised-transaction claims are handled against scheme deadlines and evidence standards. Trigger for "audit our dispute handling", "chargeback quality review", "are we meeting scheme deadlines", unrecognised transaction claims, provisional credit decisions, or a customer complaining their dispute was rejected unfairly.
metadata:
  author: rulebase
  version: "1.0.0"
  archetype: analysis
---

# Dispute and chargeback handling quality

Disputes sit in an unusual place: they are support conversations governed by external
timetables and evidence rules you do not control. Miss a scheme deadline and the right is
gone regardless of the merits — **the customer loses money because of an internal process
failure, and nothing about the case file will show it as a decision.**

That asymmetry is what makes this worth auditing separately from ordinary complaint
handling.

**Scheme rules, deadlines and evidence requirements vary by scheme, region and dispute
reason, and they change.** Nothing here states one. Source them from payments or compliance
and treat them as configuration.

## Two clocks, and the internal one is the problem

**The scheme clock** — the window to raise a dispute or respond to a defence. External,
hard, and unforgiving.

**The customer clock** — any regulatory or contractual timeframe for responding to the
customer, including provisional credit where that applies.

They are different lengths and they interact badly: a case can be inside the customer
timeframe and past the scheme window, which means the customer will get an answer and no
money. Audit both, and specifically for cases where the second was met and the first was
missed.

Where a dispute arrives as an ordinary support ticket and is only later recognised as a
dispute, **the scheme clock started at first contact**. Identification lag is the single
largest cause of missed windows, and it is measurable: compare the first customer mention
against the date the dispute was formally raised.

## Evidence quality decides the outcome

A dispute succeeds or fails on the evidence submitted. Audit what was gathered:

- **Was the required evidence collected for that dispute reason?** Reasons have different
  requirements, and a generic intake form collects a generic set.
- **Was it collected at first contact**, or over several exchanges? Every extra round trip
  consumes the window and the customer's patience.
- **Was the customer asked for something unnecessary?** A common finding, and it both delays
  the case and reads as obstruction.
- **Was the customer asked for something they cannot reasonably provide**, and was that
  treated as their failure? This is where disputes get rejected for process reasons rather
  than merit.
- **Was the dispute reason coded correctly?** A miscoded reason can invalidate an otherwise
  good claim, and it is invisible unless you check.
- **Were the merchant's or acquirer's responses assessed**, or accepted by default?

## Where the unfairness usually is

The findings that matter to customers:

- **Rejections for process reasons rather than merit** — late, incomplete, miscoded, or
  evidence not gathered. Count these separately from merit rejections; they are the ones you
  can fix, and they are usually a meaningful share.
- **Provisional credit applied inconsistently** for comparable cases. Where a provisional
  credit obligation exists, check it was applied on the required basis rather than at
  discretion.
- **Credit reversed without adequate explanation**, which generates a complaint reliably.
- **Outcome variation by channel, market or agent** for the same dispute reason and evidence.
- **Outcome correlated with how hard the customer pushed**, which is the same conduct problem
  that shows up in redress generally.
- **Vulnerability not considered** — a disputed transaction can leave someone without money
  for essentials, and the handling should reflect that.
- **Repeat disputes from the same customer** treated with suspicion by default rather than on
  merit. Some are genuinely first-party fraud; treating the pattern as proof is a conduct
  problem, and the specialists decide, not the dispute handler.

## Measuring it

- **Win rate is not a quality metric.** It moves with your customer mix, your merchant mix and
  the reasons you raise. A rising win rate can mean better evidence or a decision to stop
  raising marginal cases — and the second harms customers while improving the metric. **Never
  set a win-rate target without a guardrail on cases not raised.**
- **Report deadline attainment against both clocks**, in absolute counts.
- **Report the process-rejection rate** — the number that actually indicates handling quality.
- **Report identification lag**, distributed.
- **Segment by dispute reason**, since requirements and outcomes differ substantially.
- **Report cases not raised** where the customer asked and no dispute was lodged, with the
  reason. This is where the biggest silent detriment sits and it appears in no standard
  report.

## Guardrails

- **Do not interpret scheme rules or determine whether a deadline was breached in a way that
  creates liability.** Source the rules; report the timings; route the determination to
  payments and compliance.
- **Do not determine whether a customer's claim is genuine**, and do not label a customer as
  a first-party fraud risk. That goes to the specialist team on the evidence.
- **A missed scheme window that cost a customer money is a detriment**, and whether
  remediation is required is a compliance and legal determination, not an operational
  write-off.
- **Do not use the audit to justify raising fewer disputes.** If cost reduction is the goal,
  say plainly that declining to raise a valid claim transfers a loss to the customer.
- **Vulnerability signals in a dispute conversation** go through their own route, and stay
  aggregated in any report.
- **Cite ids and aggregates.** Dispute files contain card data, transaction detail and
  financial circumstances.

## Present results to the user

1. **The rules used, and their source**, per scheme and dispute reason.
2. **Both clocks**, with attainment in absolute counts, and specifically the cases where the
   customer timeframe was met and the scheme window was missed.
3. **Identification lag**, distributed, with cases where it alone consumed the window.
4. **Process rejections versus merit rejections**, as the headline quality measure.
5. **Evidence quality per dispute reason** — what was required, what was gathered, what was
   asked for unnecessarily.
6. **Consistency checks** — provisional credit, outcome by channel, market and agent, and
   outcome against escalation intensity.
7. **Cases not raised** where the customer asked, with reasons. The silent detriment.
8. **Win rate reported with its caveat**, never as a quality target.
9. **What needs a compliance determination**, including any missed window that cost a customer
   money.
