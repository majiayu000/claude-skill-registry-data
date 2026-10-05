---
name: cx-data-minimisation-review
description: Use to find personal data support collects and stores that nothing actually uses, and to stop collecting it. Trigger for "do we collect too much data", "which fields do we actually use", data minimisation review, "why do we ask customers for this", reducing breach exposure, or a form that grew a field every quarter.
metadata:
  author: rulebase
  version: "1.0.0"
  archetype: analysis
---

# Data minimisation in support

Support forms and ticket schemas grow. Every incident adds a field, every integration adds
a property, every team adds a custom attribute — and nothing is ever removed, because
removing a field feels riskier than keeping it.

The result is a system holding personal data with no current purpose. That is both a
compliance problem and, more concretely, **the single cheapest way to reduce the impact of
a future breach**: data you do not hold cannot be exposed.

This is the least glamorous analysis in the compliance set and one of the highest
return-on-effort, because the findings are usually uncontroversial once someone actually
looks.

## Inventory, then test for use

List every field where personal data can land:

- Ticket and conversation fields, standard and custom
- Contact and customer record fields
- Intake and contact-form fields, per form and per channel
- Fields populated by integrations
- Fields populated by automation
- Free-text fields, which can contain anything
- Attachments, and what customers are asked to attach

Then, for each, establish **whether anything uses it**:

- **Is it populated?** A field empty in 95% of records is either unused or inconsistently
  used, and both are findings.
- **Is it read?** Query it in reports, dashboards, automations, routing rules, exports and
  integrations. **A field written by everyone and read by nothing is the target.**
- **Is it read by a human?** A field displayed on a screen nobody looks at is not used.
- **When was it last used?** A report that has not run for a year does not justify a field.
- **Who asked for it, and is that need current?** Fields frequently outlive the incident or
  the person that prompted them.

The pattern to look for is a field that is required at intake, populated for every customer,
and read by nothing. Those are pure liability.

## The categories that recur

- **Identity documents collected "in case"** — the highest-risk holding and frequently
  unnecessary once verification is done. Ask whether the *document* needs retaining or
  whether the *verification outcome* is sufficient. Almost always the latter.
- **Full card numbers or bank details** in free-text or attachments, where a reference or last
  four would do. Also a payment-security matter.
- **Date of birth**, collected for verification and retained indefinitely.
- **Full addresses**, where a postcode or a country would serve the purpose.
- **Phone numbers on channels that never call.**
- **Health information** collected once for a specific accommodation and retained afterwards.
- **Optional demographic fields** nobody analyses.
- **Free-text "additional information"** boxes, which reliably accumulate whatever the
  customer felt like sharing and are almost never read.
- **Duplicated fields** — the same data in three places because three integrations each
  created their own.

## Collection, not just retention

Retention review asks how long you keep it. Minimisation asks whether to collect it at all,
and that is the more effective intervention because it removes the data from every
downstream system at once.

For each intake field:

- **Is it required?** A required field forces every customer to provide it, including the
  large majority whose case does not need it. **Conditional collection — asked only when the
  case needs it — is usually the right answer** and is rarely how forms are built.
- **Is it asked before it is needed?** Collecting verification data before establishing that
  verification is necessary.
- **Is it asked because a small fraction of cases need it?** Ask that fraction.
- **Does the customer know why?** A field with no explanation gets junk answers as well as
  being a transparency problem, so this finding usually improves data quality too.

## Free text is the hard part

You cannot minimise what customers volunteer, and support conversations are free text by
nature. What you can do:

- **Do not prompt for more than you need.** A field labelled "please describe your medical
  circumstances" will produce special-category data at volume. Rewording the prompt is the
  cheapest control available anywhere in this area.
- **Do not require detail the case does not need**, since customers will over-share to be
  helpful.
- **Know what accumulates**, by sampling free-text fields for the categories of sensitive
  data present. This informs handling and retention even where collection cannot be reduced.
- **Handle attachments deliberately.** Asking a customer to "send a screenshot" reliably
  produces screenshots containing far more than the issue.

## Removing a field safely

The reason nothing gets removed is that removal feels risky. Make it a bounded change:

1. **Confirm nothing reads it** — reports, automations, routing rules, integrations, exports,
   and any warehouse model. Check for reads you did not build.
2. **Stop collecting it first**, and leave the historical data in place. This captures most
   of the benefit for new records with almost no risk.
3. **Then decide about the history**, which is a retention question with its own obligations
   — and possibly a reason to keep it.
4. **Check nothing broke**, over a period long enough for monthly processes to run.
5. **Deleting a field's data is usually irreversible**, and it may destroy something an
   obligation requires. Treat it as a reviewed change with a plan, not a cleanup — and get a
   documented basis before deleting rather than after.

## Guardrails

- **Do not delete fields or data.** This produces a proposal. Deletion is irreversible and
  may remove records something requires.
- **Do not remove a field that a retention obligation or an open matter depends on.** Check
  before proposing, and route the question rather than assuming.
- **Identity documents and payment data findings** carry higher priority and involve
  security as well as privacy.
- **Special-category data found in free text** is a handling and retention finding as well as
  a minimisation one. Do not quote it; report categories and counts.
- **Whether a purpose justifies a field is a legal determination** where the answer is
  contested. Provide the usage evidence.
- **Do not extract the data to prove it exists.** Field names, population rates and counts
  are sufficient.

## Present results to the user

1. **The field inventory**, with population rate and evidence of whether anything reads it.
2. **Collected-but-unread fields**, ranked by sensitivity then by population — the primary
   finding.
3. **Required-at-intake fields that most cases do not need**, with a conditional-collection
   proposal.
4. **High-risk holdings** — identity documents, payment data, date of birth, health — with
   whether the outcome could replace the artefact.
5. **Free-text and attachment findings**, including prompts that invite sensitive data, with
   the rewording proposal.
6. **Duplicated fields** across systems.
7. **A removal plan per field**: stop-collecting first, read-dependency check, verification
   period, and the separate historical-data decision.
8. **What needs a legal determination** or a retention check before anything is removed.
