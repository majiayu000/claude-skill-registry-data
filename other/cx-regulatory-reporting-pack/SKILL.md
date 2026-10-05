---
name: cx-regulatory-reporting-pack
description: Use to assemble a pack of support evidence for a regulator, auditor or supervisory request, at the standard of reproducibility those audiences apply. Trigger for "the regulator has asked for", "prepare an audit pack", "evidence request from compliance", supervisory information request, s166-style review support, or assembling complaint and QA evidence for an external body.
metadata:
  author: rulebase
  version: "1.0.0"
  archetype: playbook
---

# Assembling an evidence pack for an external body

An information request from a regulator or auditor is not a reporting task. The
difference is the standard: every number has to be reproducible by a stranger, every
definition stated, and every gap disclosed by you rather than discovered by them.

**The most damaging outcome is not a bad number. It is a number that cannot be
reproduced, or a gap they find that you did not mention** — because both convert a
question about the data into a question about your control environment, which is a much
worse conversation.

## Read the request as written

Requests are drafted precisely and read loosely. Before extracting anything:

- **Define every term the request uses in your own data**, and write down where the
  request's language and your system's language differ. "Complaint" in the request may
  not equal your `complaint` tag. "Customer" may mean account, contact, or legal entity.
  This mapping is usually the most contentious part of the pack and it belongs in it
  explicitly.
- **Pin the period, and the date field.** A request for a calendar quarter needs to say
  whether membership is by event date, receipt date, or resolution date. Pick, state,
  and be consistent across every table.
- **Note what is not asked for.** Do not volunteer additional analysis into an evidence
  pack; it invites scope you were not asked about. Answer the question.
- **Identify what you cannot answer**, early, and raise it with whoever owns the
  relationship. A late-discovered gap is worse than an early-declared one.
- **Check who is asking and through whom.** Responses to regulators are usually
  channelled through compliance or legal. **Do not send anything directly**, and do not
  assume the requester in your inbox is the right recipient.

## The standard for every figure

For each number in the pack, record — in the pack, not in a side document:

1. **The definition**, in plain language.
2. **The population and the exclusions**, with counts for each exclusion.
3. **The source systems**, and the extract date.
4. **The query or method**, reproducible.
5. **The figure**, with absolute counts alongside any percentage.
6. **Known limitations.**

Then verify: **have a second person reproduce the figure from the written method
alone.** If they cannot, the method is not written well enough, and that is far better
to discover now. This step catches more errors than any amount of re-checking by the
original analyst.

## Reconcile to the systems of record before submitting

Every figure that also exists elsewhere must tie to it, or the difference must be
explained in the pack:

- Complaint counts against the complaints system.
- Customer and account counts against the CRM or ledger.
- Any financial figure against finance's own numbers.
- Any figure previously reported to the same body, in any prior submission.

**An inconsistency with something you have previously said is the finding they will pull
on.** Check the prior submissions specifically, and if a number has legitimately
changed, disclose the change and its reason rather than hoping nobody compares.

## Disclose the gaps yourself

The section that most improves how a pack is received, and the one most often left out.
Be specific:

- **Channels not covered** — complaints arriving by post, social, review sites, a
  regulator's own portal.
- **Records not retrievable** — deleted, redacted, outside retention, lost in a migration.
- **Periods with a different definition, system or taxonomy**, and what that does to
  comparability.
- **Known data quality issues** in the fields you relied on.
- **Manual steps** in the extraction, and who performed them.

Where a gap materially affects a figure, say what the figure would look like at both
plausible bounds rather than presenting the convenient one.

## Handle the material properly

- **Evidence must be as-at, not as-of-now.** If a status has changed since the period,
  present the position at the period end and note the subsequent change separately.
  Silently reflecting today's state misrepresents the period.
- **Freeze the extract.** Take a dated snapshot, keep it, and record its hash or a
  version reference. A pack whose underlying data has moved on cannot be defended, and
  you will be asked about it months later.
- **Keep a working file separate from the submission.** Drafts, hypotheses and internal
  commentary should not travel with the pack.
- **Preserve the chain.** Record who extracted what, when, and from where. If the pack's
  provenance is questioned, this is the answer.
- **Expect follow-up questions** months later and expect to have to reproduce the pack
  exactly. Store the method and the frozen extract together.

## Redaction and minimisation

- **Provide what was asked for, at the granularity asked for.** Volunteering full
  transcripts where a summary was requested expands the disclosure and the customer data
  you have shared, and it cannot be undone.
- **Where customer-level detail is required**, follow the instruction from legal on
  redaction and on whether identifiers are needed. Do not decide this yourself.
- **Do not include agent names** unless specifically requested; where they are, flag it,
  because it may engage employment and data-protection considerations.
- **Special-category data** — health, vulnerability disclosures — needs an explicit
  decision before it goes anywhere.

## Guardrails

- **Do not submit anything directly to an external body.** Compliance or legal owns the
  channel, the covering language and the timing.
- **Do not interpret the regulation, and do not characterise your own compliance.**
  Present evidence. "We complied" is not an analytical output, and asserting it in a pack
  is a specific risk.
- **Do not adjust a definition to produce a better figure.** If two defensible definitions
  give different answers, present the one that matches the request and disclose the other.
- **Do not omit an unfavourable figure that was asked for.** If a number is bad, it goes in
  with its explanation and the action taken.
- **Flag anything that looks like a reportable matter** discovered during preparation,
  immediately and separately. It may carry its own notification clock that starts when
  someone is told.
- **Do not speculate in writing.** Anything in the pack may be read literally and quoted
  back.

## Present results to the user

1. **The request, restated**, with every term mapped to your data and the mismatches named.
2. **The pack**, figure by figure, each with definition, population, exclusions, source,
   method, and absolute counts.
3. **Reconciliation** to systems of record and to prior submissions, with differences
   explained.
4. **The gaps section**, written by you, with bounds where a gap moves a figure.
5. **The frozen extract reference** and the provenance record.
6. **Second-person reproduction result** — who reproduced which figures from the method
   alone.
7. **What could not be answered**, and what would be needed to answer it.
8. **Anything requiring a compliance or legal decision** before submission: redaction,
   agent names, special-category data, and any suspected reportable matter.
