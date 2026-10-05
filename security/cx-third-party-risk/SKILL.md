---
name: cx-third-party-risk
description: Use to review how an outsourcer, BPO or vendor handles your customer data and meets your conduct obligations, using evidence from the work rather than from their questionnaire answers. Trigger for "review our BPO's data handling", "vendor risk assessment for our outsourcer", "are our partners compliant", third-party oversight, outsourcing due diligence, or a supplier audit of a support vendor.
metadata:
  author: rulebase
  version: "1.0.0"
  archetype: playbook
---

# Third-party risk in outsourced support

You can outsource the work. You cannot outsource the obligation — in most regulated
sectors the accountability for outcomes, and for the personal data, stays with you.

Vendor oversight is normally done through questionnaires and annual certifications, which
tell you what the vendor's policies say. This skill is about the other half: **what the
evidence from the actual work shows**, which is a much better predictor and is usually
available to you already because the conversations flow through your systems.

## Test against the work, not the questionnaire

The strongest oversight evidence comes from data you already hold:

- **Conduct patterns in their conversations.** Obstruction, pressure, misleading
  statements, unlogged complaints — run the same conduct checks you run internally, and
  compare rates against your in-house teams on comparable work.
- **Complaint identification rate.** A vendor identifying complaints at a materially lower
  rate than in-house teams on similar volume is a finding, and a common one, because
  logging a complaint often looks like admitting a failure.
- **Vulnerability recognition rate.** Same logic, higher stakes.
- **Redress consistency** between vendor-handled and in-house cases for the same failure.
  Vendors frequently have narrower authority, which shows up as customers getting less for
  the same problem — that is your finding, not theirs.
- **Access patterns.** Which records their agents opened, and whether the volume and
  pattern fit the work assigned. Bulk viewing or access outside working hours is worth
  asking about.
- **Adherence to your scripts and disclosures**, where those are required.

Compare on **like-for-like work**. A vendor given harder queues will look worse on every
measure, and an oversight report that has not adjusted for mix will be correctly
dismissed by them.

## Data protection specifics

- **Know where the data actually is.** Which country the agents work in, where the systems
  are hosted, and whether the vendor sub-contracts. **Sub-processors are the usual gap** —
  a vendor's transcription tool, AI provider or overflow partner may be processing your
  customers' conversations without ever appearing in your register.
- **Check the contract covers what actually happens.** Scope creep is normal: a vendor
  engaged for tier-1 email is doing outbound calls a year later.
- **Check the retention on their side.** Their copies, exports, recordings and local
  systems have their own retention, frequently unconfigured. Deletion on your side is not
  deletion.
- **Check what leaves your systems.** Data pushed into a vendor's own CRM, quality tool or
  workforce system is a transfer you may not have assessed.
- **Test their deletion and erasure execution**, do not accept the assertion. An erasure
  request honoured by you and not by them is not honoured.
- **Local exports and screenshots.** Agents taking screenshots or building local
  spreadsheets is common, undocumented, and hard to detect — ask specifically, and check
  whether their environment permits it.

Whether a given arrangement is lawful — the transfer basis, the contractual terms — is a
legal determination. Surface the facts precisely and route them.

## The oversight failures that recur

- **Certification as assurance.** A current certification tells you a scope was audited on
  a date. Read the scope; it frequently excludes the part you care about.
- **Questionnaire answered by the wrong person.** Sales answers optimistically; operations
  knows what happens.
- **No right to audit, or one never exercised.** An unexercised audit right provides no
  assurance. If contractual, use it.
- **Oversight only at the aggregate.** Vendor-level scores hide site-level and team-level
  problems. Segment by site, team and tenure — a vendor with three sites is three
  operations.
- **Incentives that produce the behaviour you are auditing for.** If the contract pays on
  handle time, resolution rate or a save rate, expect pressure, premature closes and
  under-logged complaints. **Check the commercial terms before concluding anything about
  the vendor's culture** — you probably bought this behaviour.
- **No exit plan.** Concentration risk, and the data-return-and-deletion question at
  termination, which is much harder to negotiate after the relationship sours.
- **Their subcontractors' subcontractors.** Ask, in writing.

## Access and joiner-mover-leaver

A recurring and easily-tested finding:

- **Are leavers' accounts disabled promptly?** Compare the vendor's roster against active
  accounts in your systems. Stale accounts are common and are a clean, undeniable finding.
- **Is access scoped to the work?** Agents with access to markets, products or record types
  outside their assignment.
- **Are shared or generic accounts in use?** They destroy attribution and every audit trail
  that depends on it.
- **Is there privileged access** — bulk export, admin — and who holds it?

## Make the oversight proportionate and repeatable

- **Scale it to the risk**: volume handled, sensitivity of the data, how regulated the work
  is, and how much discretion the vendor has over customer outcomes.
- **Fix the metrics and the cadence** so the reviews are comparable over time, and treat a
  definition change as breaking the series.
- **Share findings with the vendor** and track remediation to outcome rather than to
  response. A vendor's action plan is not a fixed problem.
- **Feed it into the commercial review.** Oversight findings that never reach the contract
  discussion do not change anything.

## Guardrails

- **Do not conclude that the arrangement is compliant.** Report evidence; sufficiency
  against an obligation is a compliance and legal determination.
- **Do not treat vendor agents worse than your own in an analysis.** Same fairness controls:
  mix adjustment, statistical power, instrument reliability, suppression of small cells. A
  finding about a named vendor agent is an employment matter for their employer, not
  material for your report.
- **A finding of actual customer harm, or of a personal-data breach on the vendor's side**,
  goes to compliance and legal immediately, and it may carry a notification clock that
  starts when you learn of it.
- **Do not extract vendor-held data to audit it** without a basis; ask for what you need
  through the contract.
- **Cite ids and aggregates; no transcripts** in a document shared with a vendor or a
  procurement function.

## Present results to the user

1. **Scope** — what the vendor does, volume, data types, sites, and how that compares to
   the contract.
2. **Sub-processors**, named, including any not previously registered. Usually the largest
   gap.
3. **Evidence from the work** — conduct, complaint identification, vulnerability
   recognition, redress consistency — mix-adjusted, against in-house comparators.
4. **The commercial terms**, and which of the observed behaviours they would predict.
5. **Data protection** — location, transfers, retention on their side, deletion and erasure
   execution tested rather than asserted, and local export practices.
6. **Access hygiene** — leavers, scope, shared accounts, privileged access.
7. **Per site and per team**, not just per vendor.
8. **Certification scope**, read and stated, rather than cited.
9. **Findings with remediation tracked to outcome**, and what belongs in the commercial
   review.
10. **What needs a legal or compliance determination**, and anything escalated immediately.
