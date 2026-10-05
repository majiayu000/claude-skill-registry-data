---
name: cx-disclosure-audit
description: Use to check that required disclosures, consents and notices were actually given in support conversations — the right wording, at the right point, through a channel the customer could act on. Trigger for "did we give the required disclosure", "are we capturing consent properly", "recording notification audit", "check our mandatory notices", disclosure compliance, or a complaint that a customer was not told something.
metadata:
  author: rulebase
  version: "1.0.0"
  archetype: analysis
---

# Auditing disclosures and consent

Some things have to be said, in a particular way, at a particular point, before something
else happens: a recording notification, a right-to-cancel notice, a risk warning, a fee
disclosure, a data-sharing consent, a notice that the customer is talking to a machine.

Whether they were said is checkable from conversation data. Almost nobody checks, and the
usual assumption — that the script contains it, therefore it happened — fails in three
predictable ways.

## Timing is part of the requirement

A disclosure given after the thing it relates to is usually not a disclosure. Check the
**sequence**, not just the presence:

- Was the recording notification given **before** recording began, or read out three
  minutes in?
- Was the fee disclosed **before** the customer committed, or in the confirmation?
- Was consent captured **before** the data was used, or afterwards to tidy up the record?
- Was the cancellation right explained **at the point it applied**?

Presence-only checking is the most common defect in a disclosure audit and it produces a
comfortable, wrong answer. Compare the disclosure's timestamp against the triggering event
in the same conversation.

## The three ways script-based assurance fails

**1. The channel exception.** The script covers voice and the same requirement applies to
chat, or the disclosure lives in an email template and the conversation happened in
messaging. Enumerate every channel the requirement applies to and test each separately.
This is the most productive single check.

**2. The path exception.** A disclosure in the main flow, absent from the transfer, the
callback, the escalated path, the after-hours route, or the automated one. Trace the paths a
conversation can take, and test each. **Automated and bot-handled paths are the routine gap
now**, because they were built after the script was written.

**3. Wording drift.** Where specific wording is required, paraphrase does not satisfy it.
Agents summarise, shorten, and personalise — reasonably, and it may break the requirement.
Test for the required elements rather than an exact string, and report both the presence
rate and the intact-wording rate.

## Detect on required elements, not on a phrase

An exact-string match under-reports, because legitimate variations exist. A loose keyword
match over-reports, because a fragment matches.

Decompose the disclosure into its **required elements** — the fee amount, the timeframe, the
right, the consequence — and check for each. Then report:

- **Fully present** — all elements.
- **Partially present** — some elements, which is a failure with a different remedy from
  total absence, and it is where most cases land.
- **Absent.**
- **Present but late.**

Search in every language the requirement applies in. A disclosure audit run in one language
against a multilingual operation produces a compliance conclusion about one market and
implies it about all of them.

For voice, transcription quality bounds what you can conclude. A disclosure recorded as
absent may have been said and mis-transcribed — so **verify a sample against the audio**
before reporting a voice failure rate, and state the transcription-quality caveat per
language.

## Consent has extra requirements

Where the audit concerns consent rather than notification, presence is not sufficiency:

- **Was it freely given?** Consent obtained as a condition of getting help is not freely
  given.
- **Was it specific?** Bundled consent covering several purposes usually fails.
- **Was it informed?** The customer needs to have been told what they were agreeing to.
- **Is it recorded**, with what they were told at the time, in a form that survives a policy
  change? A consent record that points to "the current privacy notice" cannot show what was
  consented to.
- **Can it be withdrawn**, and is withdrawal actually honoured downstream? Test the
  execution, not the mechanism — this is where it usually breaks.

**Consent is frequently the wrong lawful basis** for support processing, and a firm relying
on it where another basis applies has created an obligation it did not need. That is a
finding worth surfacing, and the determination is legal's.

## Sampling and reporting

- **Risk-weight the sample** toward the conversations where the requirement bites, but keep
  a **random core** — you will be asked for a population rate, and only the random core
  supports one. Never pool them.
- **Report absolute counts.** A 2% failure rate on a mandatory disclosure is a number of
  specific customers who were not told, and the count is what determines whether it is a
  reportable matter.
- **Segment by channel, path, market, language and team**, since that is where the failures
  concentrate.
- **Rank by consequence, not frequency.** A rare missed risk warning may outrank a common
  missed courtesy notice.

## Guardrails

- **Do not determine whether a failure is a breach or reportable.** Produce the evidence
  and the counts; the determination is compliance and legal's, and it may carry a
  notification clock that starts when they are told.
- **Do not conclude compliance from a clean sample.** State the sensitivity: a sample of 200
  cannot detect a failure affecting 30 customers.
- **Do not treat a detected absence as proven**, especially in voice. Verify a sample against
  the source.
- **Route individual findings to process, not to people**, unless the pattern is genuinely
  individual — a channel-wide or path-wide gap is a design failure and coaching agents will
  not fix it.
- **Cite ids; quote only the disclosure text**, not surrounding conversation.

## Present results to the user

1. **The requirement, decomposed into elements**, with the timing rule stated and its source.
2. **Which channels and paths the requirement applies to**, and which you tested — including
   automated paths.
3. **Presence, partial presence, absence and lateness**, as four numbers, in absolute counts
   as well as rates.
4. **Intact-wording rate**, separately from presence, where specific wording is required.
5. **By channel, path, market and language**, since this is where the gaps are.
6. **Consent-specific findings**, where applicable: freely given, specific, informed,
   recorded, withdrawable — and whether withdrawal is honoured downstream.
7. **Verification of a sample against source audio**, for any voice finding.
8. **Detection sensitivity**, so a clean result is not read as proof.
9. **What needs a compliance determination**, with the affected customer count attached.
