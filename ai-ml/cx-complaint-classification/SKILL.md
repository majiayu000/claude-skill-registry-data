---
name: cx-complaint-classification
description: Use to design or audit complaint identification and classification in customer support, especially in regulated sectors. Trigger for "are we identifying complaints correctly", "complaint detection", regulatory complaint definition, FCA or CFPB complaint handling, vulnerable customer identification, root cause categorisation for complaints, or building an AI classifier for complaints.
metadata:
  author: rulebase
  version: "1.0.0"
  archetype: playbook
---

# Complaint identification and classification

> **This is operational guidance, not legal advice.** Complaint definitions and
> reporting duties are jurisdiction-, sector-, and licence-specific. Every
> definition and threshold here must be signed off by your compliance or legal
> function before it drives a process. Getting this wrong is a regulatory matter,
> not a data-quality one.

## The error that causes regulatory findings

**A complaint is a definition, not a feeling.**

Most support operations detect complaints by sentiment or by escalation. Both
under-identify, in the same direction, for the same reason: the regulatory
definition usually does not mention emotion at all.

| Situation | Sentiment view | Typical regulatory view |
| --- | --- | --- |
| Calm, factual "I was charged twice and I'm not happy about it" | Not a complaint | **Is a complaint** |
| Furious customer, issue resolved on the call, no allegation of loss | Complaint | Often **not** a complaint |
| "This is the third time I've had to call" | Maybe | **Usually a complaint** |
| Frustrated venting about a policy, no dissatisfaction with service | Complaint | Often **not** |

The polite, articulate customer stating a factual grievance is the one most often
missed — and the one most likely to escalate to an ombudsman when it is.

## Step 1: get the definition, in writing, from compliance

Do not draft it yourself. Obtain the definition that applies to your entity and
licence, and hold it as the single source of truth.

Most regulatory definitions are built from a similar set of elements. Use these as
a **checklist for what to ask compliance about**, not as a definition:

- An **expression of dissatisfaction** — oral or written.
- About the **provision of, or failure to provide, a service**.
- **Whether or not it is justified** — merit is irrelevant to whether it is a
  complaint.
- Often: **alleging** financial loss, material distress, or material inconvenience.
- From **or on behalf of** an eligible complainant, which can include third
  parties.

Two elements are commonly missed when teams paraphrase:

**"Whether or not justified."** A complaint you disagree with is still a complaint.
Teams that filter out "wrong" complaints under-report systematically.

**"On behalf of."** A relative, carer, solicitor, or advocate raising an issue is
usually in scope. Detection built on "the customer said" misses these entirely.

Get in writing: the definition, what is explicitly excluded, the recording
obligation, the reporting thresholds and cadence, and the clock-start rule.

## Step 2: tune for recall, not precision

This is the design decision that most distinguishes complaint detection from
ordinary classification, and it is counter-intuitive to anyone with an ML
background.

**The costs are wildly asymmetric.** A missed complaint is an unrecorded
regulatory event — potentially a reportable breach, an ombudsman referral, a
finding at your next review. A false positive costs a few minutes of human review.

So:

- **Optimise recall**, and accept precision you would never accept elsewhere.
  A precision of 0.5 with recall of 0.95 is usually the right trade.
- **Treat every model output as a candidate for human confirmation**, never as a
  finding. The model builds the queue; a person decides.
- **Report recall against a human-labelled gold set**, and never report accuracy.
  With a 3% complaint base rate, a classifier that says "no complaint" every time
  scores 97% accurate and is worthless.

Set the threshold with compliance present. This is a risk-appetite decision, not
an F1 optimisation.

## Step 3: build detection in layers

**Layer 1: structural signals.** Cheap, high-precision, no model needed.
Customer used the word "complaint" or "complain". Contacted an ombudsman or
regulator. Third repeat contact on one issue. Escalation requested. Refund or
compensation demanded. Solicitor or advocate involved.

**Layer 2: linguistic patterns** for expressions of dissatisfaction plus an
allegation of detriment. Broad by design; this is the recall layer.

**Layer 3: model classification** over the conversation, returning a verdict, the
**element(s) of the definition it believes are met**, and a **verbatim quote** for
each. Requiring a quote is what makes the verdict auditable and suppresses
confident hallucination — a verdict whose quote is not in the transcript is
rejected automatically.

**Layer 4: human confirmation** for everything the earlier layers surface.

Do not skip layer 1 in favour of a model. Structural signals are free, explainable,
and catch the clearest cases with no drift risk.

## Step 4: classify on separate axes

Once something *is* a complaint, several independent things need recording. Collapsing
them into one field is the most common structural mistake — it makes root-cause
reporting impossible.

| Axis | Records |
| --- | --- |
| **Is a complaint** | Boolean, with the definition version applied |
| **Root cause** | What went wrong (the taxonomy question — see `cx-contact-driver-taxonomy`) |
| **Product / service** | Usually required for regulatory reporting |
| **Detriment alleged** | Financial loss / distress / inconvenience |
| **Outcome** | Upheld, partially upheld, not upheld |
| **Redress** | Compensation, goodwill, correction, none |
| **Vulnerability present** | Separate duties attach |

**Root cause is not the same as product, and outcome is not the same as root
cause.** A complaint about a card decline may have a root cause of "fraud rules
mis-tuned" and an outcome of "not upheld". All three matter and they answer
different questions.

## Step 5: treat vulnerability as its own detection problem

Vulnerability signals frequently co-occur with complaints and carry **separate,
often stricter obligations**. Detect them independently rather than as a complaint
sub-category.

Common signal categories: bereavement, serious illness or disability, mental
health disclosure, financial hardship or difficulty paying, being subject to
coercion or abuse, low capability or comprehension difficulty, age-related need.

Two rules that matter more than the detection:

- **Never let a model's unreviewed verdict be the only handling.** Vulnerability
  handling is a human duty.
- **A missed vulnerability disclosure is usually more serious than a missed
  complaint.** Route it immediately, and separately.

## Step 6: build the audit trail before you need it

Regulators ask how you decided, not just what you decided. Every complaint record
should carry:

- The **definition version** applied.
- **Which elements were met**, with a verbatim quote for each.
- **Who confirmed it**, and when.
- **Detection route** — structural signal, model, agent-raised, or post-hoc audit.
- **Timestamps**, immutable, with the clock-start rule applied consistently.
- **Every state change**, retained.

If a model contributed, record the model version. Scores from different model
versions are not comparable, and "our detection improved in March" is a question
you will be asked to substantiate.

## Step 7: audit for what you missed

Precision is easy to audit — review what you flagged. Recall is the hard part and
the part that matters.

**Reverse audit.** Take a random sample of conversations **not** flagged as
complaints and have a trained reviewer apply the definition. The miss rate found
here is your recall estimate, and it is the only honest one. Run it monthly.

**Signal-based back-testing.** Search unflagged conversations for the layer-1
structural signals. Any hit is a definite miss and an immediate process failure.

**Downstream reconciliation.** Complaints that reached an ombudsman, regulator, or
social media without ever being recorded internally are your most serious misses.
Every one warrants a root-cause review of the detection itself.

Track and report the **miss rate**, not just the volume. A complaint rate that
falls is only good news if the miss rate did not rise.

## Metrics worth reporting

| Metric | Note |
| --- | --- |
| Complaints per 1,000 accounts | Normalise — raw counts track growth |
| Miss rate from reverse audit | The recall estimate; the number that matters |
| Upheld rate | A very low rate can indicate over-recording; very high, systemic failure |
| Time to resolution vs regulatory deadline | Distribution, not mean |
| Referral rate to ombudsman | Your external quality check |
| Repeat complaints on one root cause | Whether fixes actually worked |
| Share detected by each layer | If layer 1 finds most, the model is adding little |

## Present results to the user

1. **State the definition you applied and where it came from.** If it has not been
   confirmed by compliance, say so first and stop short of firm conclusions.
2. **Miss rate before complaint rate.** A clean complaint rate with an unmeasured
   miss rate is not evidence of anything.
3. **Recall and precision separately**, never accuracy, and give the base rate so
   the numbers can be interpreted.
4. **Any layer-1 structural signal found in unflagged conversations** — these are
   definite misses and should be reported as an incident, not a statistic.
5. **Root cause breakdown** with owners, since that is what reduces complaints.
6. **Vulnerability findings separately**, and immediately.
7. **The legal caveat.** Restate that definitions and duties require compliance
   sign-off, and identify which of your conclusions depend on the definition being
   right.

Do not quote complaint text into chat. Reference conversation IDs; these records
combine PII with regulatory sensitivity.

## Troubleshooting

**Complaint rate looks low and everyone is pleased** — measure the miss rate before
accepting it. Low recorded volume is the expected symptom of poor detection.

**Detection uses sentiment analysis** — this is the core error. Sentiment is
neither necessary nor sufficient under most definitions.

**Precision is poor, and there is pressure to raise the threshold** — resist, and
make the asymmetry explicit: raising the threshold trades review minutes for
unrecorded regulatory events.

**Upheld rate is near zero** — either over-recording, or complaints are being
assessed by the team that caused them. Check who decides.

**Volume jumped after a model change** — the definition did not change, the
detector did. Do not report it as a rise in complaints; report it as a change in
detection and re-baseline.

**Third-party complaints are missing** — detection assumes the customer is
speaking. "On behalf of" is usually in scope.
