---
name: cx-pii-redaction-audit
description: Use to check whether a conversation export, dataset or AI pipeline is leaking personal data that should have been redacted, and to measure how well the redaction actually works. Trigger for "is this export safe to share", "check our redaction", "can we use support transcripts for training", sending transcripts to a vendor or model, "is there PII in this dataset", or before opening support data to a wider audience.
metadata:
  author: rulebase
  version: "1.0.0"
  archetype: analysis
---

# Auditing PII redaction

Support transcripts are among the densest personal data a company holds. In a single
thread you can find a name, an email, a postal address, a phone number, a partial card
number, a date of birth, an account balance, a reason for a payment, a health condition
explaining a refund request, and a photograph of a document.

That makes a redaction audit the gate before support data moves anywhere: to a vendor,
into an analytics warehouse, into a model's context, or to a wider internal audience.

**This audit does not make data safe. It measures how unsafe it still is**, so someone
with the authority can decide. Do not present a clean result as clearance to share.

## Establish the purpose and the standard first

Redaction is only meaningful against a stated purpose. "Enough for internal analytics"
and "enough to send to a third-party model provider" are very different bars.

Write down:

- **Who will see the data**, and under what agreement.
- **What the data will be used for**, and whether that use is compatible with why it was
  collected. This is a legal question in most jurisdictions, and it is not one you
  answer — flag it.
- **Whether re-identification matters.** Removing names does not anonymise a dataset. A
  conversation is often uniquely identifying from its content alone: a specific
  transaction, an unusual complaint, a distinctive combination of dates and amounts.
  **Redaction is not anonymisation**, and claiming otherwise is the most consequential
  error in this area.
- **Retention** — how long the redacted copy lives, and who deletes it.

## Where the leaks actually are

Redaction is usually applied to the obvious field and not to the others. Check every
one of these; each has been a real source of leakage:

- **Message bodies** — the field everyone redacts.
- **Subjects and titles**, which regularly contain names, account numbers and order ids.
- **HTML bodies alongside plain text.** Where both are stored, redaction is often
  applied to one. Check both independently — and check which one your export actually
  reads, because they can differ.
- **Quoted and forwarded text**, including full email signature blocks with direct
  numbers and addresses.
- **Attachment filenames** — `passport_scan_jane_doe.pdf` needs no opening.
- **Attachment contents**, if they travel with the export. Images of documents are
  invisible to text redaction entirely.
- **Custom fields and metadata**, which are frequently free text.
- **Internal notes**, which are often blunter about customers than public replies.
- **Voice transcripts**, where spoken card numbers and addresses appear as digit strings
  that pattern matchers written for formatted numbers will miss.
- **URLs** with identifiers, tokens or emails in query strings.
- **Customer and requester objects** — the actual point of many exports, and easy to
  forget when auditing the messages.
- **Bot and system messages**, which echo back what the customer typed.

## Measure both error directions

Redaction has two failure modes and reporting only one is misleading:

**Under-redaction (leaks).** The dangerous direction. Estimate it by hand-reviewing a
random sample of redacted records and counting the identifiers that survived. Report it
as a rate with a confidence interval and as an absolute count — "0.4% of messages" reads
as small until you multiply by two million.

**Over-redaction.** Destroys the analytical value and pushes people to work around the
redacted copy, which is how the unredacted one gets copied somewhere. Measure how much
of the substance survives, and report it, because a redaction pipeline nobody can use is
a redaction pipeline nobody uses.

**Stratify the sample.** Uniform random sampling under-represents the categories where
leaks concentrate — voice transcripts, long threads, forwarded email, non-English text,
attachments. Over-sample those and weight back.

## What pattern matching reliably misses

Regex-based redaction is a floor, not a solution. It systematically misses:

- **Names**, which have no pattern. This is the largest gap by volume.
- **Addresses** written conversationally.
- **Unformatted numbers** — a card or account number typed without separators, or
  spoken and transcribed as words or spaced digits.
- **International formats** — phone numbers, postcodes, and national identifiers vary by
  country, and a matcher tuned for one market silently fails on the rest. Check per
  market.
- **Non-Latin scripts**, where matchers written against Latin text often do nothing at
  all.
- **Contextual disclosures** — "I've been off work since my diagnosis" is sensitive
  personal data with no pattern, and no redaction system will catch it.
- **Indirect identifiers** — the combination that identifies someone without naming
  them.

Test each of these categories deliberately rather than trusting an aggregate pass rate.
And report the *categories* that failed, not just a number: "phone numbers leak in three
markets" is actionable in a way that "97.1% redaction accuracy" is not.

## Consistency, if you preserve structure

If redaction replaces values with tokens rather than removing them, check:

- **The same person maps to the same token within a conversation**, or the transcript
  becomes unreadable.
- **Tokens are not reversible** without the key, and the key is stored separately from
  the data. A "pseudonymised" dataset shipped alongside its mapping table is not
  pseudonymised.
- **Cross-conversation linkage is intentional.** Stable tokens across conversations
  enable per-customer analysis and materially raise re-identification risk. Decide
  deliberately.

## Guardrails

- **Do not paste examples of leaked PII into chat, a report, or a ticket.** Cite the
  record id, the field, and the *category* of identifier. Keep any excerpt in a
  restricted annex. An audit report that reproduces the leak it found has made the
  problem worse and will be forwarded widely.
- **Do not fix leaks by editing production records** as part of an audit. Report;
  remediation is a separate, planned, bounded change.
- **A confirmed leak in already-shared data is a potential incident** with its own
  reporting clock. Say so immediately and separately rather than filing it in the
  findings.
- **Do not advise on the legal position.** Flag that the purpose, the lawful basis,
  cross-border transfer and retention need a decision from whoever owns data protection.

## Present results to the user

1. **Purpose and standard** — who sees it, for what, and the bar being audited against.
2. **Coverage** — every field and artefact checked, and, explicitly, the ones not
   checked. Attachments are the usual omission.
3. **Leak rate**, by identifier category, with sample size, interval, and the absolute
   count across the full dataset.
4. **The categories that failed**, ranked by sensitivity rather than by frequency.
5. **Over-redaction**, and whether the data is still usable for its purpose.
6. **Re-identification risk**, stated plainly, with the reminder that redaction is not
   anonymisation.
7. **A clear verdict for the decision-maker** — what is safe for what audience — and an
   explicit statement that the decision is theirs, not yours.
