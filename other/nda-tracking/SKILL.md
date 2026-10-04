---
name: nda-tracking
description: Tracks NDA status across every counterparty in a live deal, use it when multiple parties are signing and accessing confidential information.
---

# NDA Tracking Agent

## When to use
Use this when a sell-side or buy-side process has multiple parties signing confidentiality agreements and requesting access to information at different times. As the counterparty list grows, verbal recall of who signed what, and when, breaks down. This agent keeps a single source of truth for NDA status so no party gets access before their agreement is executed.

## What it does
It produces an NDA status log that tracks every counterparty from first contact through executed agreement, including access tier granted and expiry, so the deal team always knows exactly who is cleared for what and which items still need chasing.

## Method
1. List every counterparty in the outreach, one row each.
   - Capture legal entity name, party type (strategic buyer, sponsor, lender, adviser), and primary contact plus their adviser.
   - Assign a stable counterparty ID so the same party is not double-counted across an affiliate and its fund.

2. Record the NDA version sent to each party.
   - Track whether it is the standard form or a marked-up variant, with a version number so redline rounds do not get confused.
   - Note who holds the pen on the current draft (company counsel or counterparty counsel).

3. Log the key dates per party: sent, returned with comments, countersigned, and full execution.
   - Flag any party stuck between sent and returned beyond your target turnaround (commonly three to five business days).
   - Common pitfall: a party is verbally agreed but unexecuted; keep it out of the executed bucket until signatures are in.

4. Capture the material terms per party.
   - Record confidentiality period, standstill provision and its duration, non-solicit and non-hire scope, and any residuals or clean-team carve-outs.
   - Highlight where a party negotiated a term below standard, since that becomes a precedent others may demand.

5. Map the access tier granted once executed.
   - Tiers run teaser only, CIM, round-one data room, round-two data room, confirmatory.
   - Access must never precede execution, so tie the tier date to the execution date, not the request date.

6. Track expiry and renewal.
   - Note when each NDA lapses relative to the expected deal timeline, and flag any that expire before signing so extensions are requested early.
   - Good looks like: zero agreements silently expiring while a party is still active in the process.

7. Maintain a follow-up status column.
   - Values: with counsel, awaiting signature, executed, access granted, expiring soon, expired, dropped out.
   - Sort so open and overdue items surface at the top of the log.

8. Produce a short exceptions summary on every update.
   - List parties past turnaround, non-standard terms accepted, and NDAs expiring within the next 30 days.

## Inputs
- The counterparty list with entity names, party types, and contacts
- The standard NDA form and any negotiated markups per party
- Key dates on record: sent, returned, countersigned, executed
- Standstill duration, non-solicit scope, and confidentiality period standards
- Your target signing turnaround in business days
- The access-tier structure and the gating between rounds
- Which parties have dropped out or are inactive

## Output format
- Status log: a row per counterparty described in prose, each stating entity name, party type, NDA version, sent and executed dates, standstill and non-solicit terms, access tier granted, expiry date, and current follow-up status.
- Exceptions summary: overdue signatures, non-standard terms accepted, and agreements expiring within 30 days.
- Sorting note: open and overdue items appear first.
- Describe the log as structured text, never as a rendered markdown table.

## Example
Northwind Logistics sell-side, latest update. Meridian Capital (sponsor): NDA v2 with a marked-up 12-month standstill and a 24-month non-solicit, sent 04 Mar, executed 09 Mar, granted round-one data room access, expires 09 Mar next year, status executed and access granted. Cascade Freight Group (strategic): NDA v1 standard form, sent 04 Mar, returned with comments 07 Mar, not yet countersigned, status with counsel and one day past the five-day turnaround, flagged. Summit Rail Partners: dropped out after the teaser, no data room access, removed from the active list. Exceptions summary: one signature overdue (Cascade Freight Group); one non-standard term accepted (Meridian 12-month standstill vs the 18-month standard, likely to be cited by other bidders); no agreements expiring within 30 days.
