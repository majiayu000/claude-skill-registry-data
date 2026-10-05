---
name: cx-record-retention-audit
description: Use to compare a support data retention policy against what is actually still stored, and find both over-retention and premature deletion. Trigger for "are we deleting support data on time", "retention audit", "how long do we keep transcripts", "we still have data from 2018", conflicting retention obligations, or preparing for a data protection review.
metadata:
  author: rulebase
  version: "1.0.0"
  archetype: analysis
---

# Retention audit for support data

Support generates some of the longest-lived and least-governed personal data a company
holds. The policy usually exists. What is actually still in the systems usually differs
from it, in both directions — and the two directions are different problems with
different owners.

- **Over-retention** — data kept past its period. A data-protection exposure, and it
  expands the blast radius of any future breach.
- **Premature deletion** — data destroyed before an obligation expired. Frequently the
  more serious of the two, because it can destroy the evidence a complaint, a dispute or
  a regulator needs, and it is unrecoverable.

Most audits look only for the first. Look for both.

## Enumerate everywhere support data lives

The audit is only as good as the inventory, and the inventory is always longer than
expected. Beyond the helpdesk:

- **Call recordings and their transcripts**, often on a different system with a different
  retention period set by a different team.
- **The analytics warehouse or lake**, where support data was copied and where retention
  is frequently never configured at all. **This is the most common over-retention
  finding.**
- **QA and evaluation records**, including reasoning text that quotes the conversation.
- **Exports** — the spreadsheets, extracts and dumps people made for an analysis. Usually
  ungoverned entirely.
- **Backups and snapshots**, where deletion in the primary system does not propagate.
- **Third parties** — BPOs, transcription vendors, AI providers, survey tools. Their
  retention is your exposure.
- **Email**, where support conversations arrive and stay.
- **Ticketing attachments**, including identity documents customers sent.
- **Search and vector indexes** built from conversation content, which frequently retain
  content after the source is deleted.
- **Logs** containing message content or personal data.

For each: who owns it, what the configured retention is, whether deletion is automated,
and what actually remains.

## Test what is there, not what is configured

Configuration and reality diverge. Query the oldest records in each store.

- **Find the actual oldest record**, per store and per data type. Compare against the
  policy.
- **Check whether automated deletion is running**, and when it last ran successfully. A
  disabled or silently failing deletion job is a frequent finding and a simple one.
- **Check that deletion propagated** — primary store, replicas, warehouse, indexes,
  backups. Deletion in one system with copies elsewhere is not deletion, and search
  indexes are the usual survivor.
- **Look for exempted or held records** — anything under legal hold, in an open dispute, or
  flagged for a complaint. These *should* survive, and the audit should confirm the hold is
  recorded rather than the record merely forgotten.
- **Sample-verify a deletion.** Take records that should have been deleted and confirm they
  are gone everywhere, not just absent from the primary UI.

## The conflicts, which are the interesting part

Retention periods are set by different obligations that do not agree, and this is where an
audit adds most value:

- **Data protection** says keep it no longer than necessary.
- **Sector regulation** may require a minimum retention for records of dealings with
  customers, complaints, or advice.
- **Limitation periods** for legal claims argue for keeping evidence.
- **Tax and accounting** rules cover transaction records.
- **An open complaint, dispute or investigation** overrides a scheduled deletion.

**Where obligations conflict, the resolution is a legal determination, not an operational
one.** The audit's job is to surface the conflict precisely — this data type, this
obligation says 2 years, that one says 7 — and route it. Do not resolve it, and do not let
an operational default resolve it silently.

Also check the direction of the conflict resolution currently in place: a system deleting
at the shortest period across a conflicted data type is quietly destroying records
something else requires.

## Deletion versus anonymisation

- **Anonymisation is a defensible alternative** to deletion where the analytical value
  matters, but only if it is genuinely irreversible. Redaction of names in a support
  transcript usually is not — a conversation frequently remains identifiable from its
  content alone.
- **Do not accept "we redacted it" as "we deleted it".** Test the claim; the standard is
  whether the individual can still be identified, directly or indirectly.
- **Pseudonymised data with the key still held is still personal data.** Check where the
  key lives.

## Retention and the erasure right

These interact and are frequently confused:

- **Scheduled retention** is proactive and applies to everyone.
- **An erasure request** is reactive, individual, and may be refused where an obligation
  requires retention.

An audit should check that both mechanisms exist, that erasure requests are actually
executed everywhere the data lives, and that a refusal was recorded with its basis. The
same propagation problem applies: an erasure honoured in the helpdesk and not in the
warehouse is not honoured.

## Guardrails

- **Read-only. Do not delete anything.** Deletion is irreversible and, where a record is
  under hold or subject to a retention obligation, deleting it is the more serious
  failure. Remediation is a separate, planned, reviewed exercise with a documented basis —
  and it should be capable of being paused.
- **Do not decide the retention period.** Conflicts between obligations are a legal
  determination.
- **Flag over-retained special-category data** — health, vulnerability disclosures,
  identity documents — with higher priority than ordinary conversation content.
- **A premature-deletion finding affecting an open matter** goes to legal immediately.
- **Do not extract the over-retained data to demonstrate it exists.** Report counts, date
  ranges and store names. Copying it into an audit artefact creates another copy with its
  own retention problem.

## Present results to the user

1. **The inventory** — every store holding support data, with owner, configured retention,
   and whether deletion is automated. Including the ones nobody had on the list.
2. **Configured versus actual**, per store: oldest record found against the policy period.
3. **Over-retention**, with counts and date ranges, special-category data first.
4. **Premature deletion**, with what obligation it may have breached — usually the more
   serious finding.
5. **Propagation failures** — deleted in one place, present in another, indexes and backups
   specifically.
6. **Deletion job health** — last successful run, per store.
7. **Obligation conflicts**, stated precisely and routed to legal unresolved, plus which
   direction the current default resolves them in.
8. **Anonymisation claims tested**, not accepted.
9. **Erasure-request execution**, including propagation and recorded refusals.
10. **What requires a legal determination** versus what is an operational fix.
