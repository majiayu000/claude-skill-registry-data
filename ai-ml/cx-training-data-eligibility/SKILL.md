---
name: cx-training-data-eligibility
description: Use to assess whether support conversations can be used to train, fine-tune or evaluate a model, and to build a filtered dataset if they can. Trigger for "can we train on our support data", "use transcripts to fine-tune a model", "build an eval set from real conversations", "is it ok to send our tickets to a model provider", or preparing support data for machine learning.
metadata:
  author: rulebase
  version: "1.0.0"
  archetype: playbook
---

# Using support conversations as training data

Support transcripts are the most valuable training and evaluation data a customer-service
AI could have, and the most legally and ethically loaded. The request usually arrives as an
engineering task and it is not one — the gating questions come first, and if they fail, no
amount of filtering fixes it.

**This skill does not determine lawfulness.** It structures the assessment, surfaces the
decisions someone else has to make, and — if they clear it — builds the dataset properly.

## The gating questions, before any data moves

Work through these in order and stop at the first unresolved one:

**1. What is the purpose, precisely?** Training a production model, fine-tuning, building
an evaluation set, or prompt examples. These carry very different risk: an eval set of 200
hand-reviewed conversations is a different proposition from fine-tuning on two million.

**2. Is it compatible with why the data was collected?** Customers contacted support to get
help. Whether using that to train a model is compatible with that purpose — and on what
lawful basis — is the central question and it is legal's to answer.

**3. Where will it go?** In-house training on your own infrastructure, a provider's
fine-tuning API, or a third party's platform. Each is a different transfer and processor
question, and a provider's *default* terms on retention and training use frequently differ
from the negotiated ones — only the configured arrangement matters.

**4. Is it reversible?** **Largely not.** A model trained on data cannot straightforwardly
have that data removed, which collides with erasure rights and with retention deletion.
Establish the position on this before training, not after the first erasure request. Keeping
the training set separately identifiable, so you know whose data is in it, is usually the
minimum.

**5. What must be excluded outright?** See below.

Do not skip to filtering because filtering feels like progress. A well-filtered dataset
assembled without an answer to question 2 is a liability with good hygiene.

## Exclude these before anything else

- **Special-category content** — health disclosures, vulnerability, anything about someone's
  circumstances that carries heightened protection. Detection is imperfect, so **exclude
  conservatively at the conversation level rather than trying to strip the sentence.**
- **Children's data**, wherever your product or context makes it plausible.
- **Conversations under an open complaint, dispute, investigation or legal hold.**
- **Anyone who has objected, opted out, or requested erasure.** This needs a mechanism to
  check, and one that keeps working — a customer who opts out after training has a
  reasonable expectation that something happens.
- **Anything outside its retention period.**
- **Conversations containing another customer's data**, which also flags a separate problem.
- **Agent-side content where employee monitoring rules apply**, and where staff have not been
  informed.
- **Payment credentials, credentials, and identity documents** — including in attachments and
  spoken on calls.

Report exclusions with counts. The proportion excluded is itself informative: a very small
exclusion rate usually means the detection is not working rather than that the corpus is
clean.

## Redaction is necessary and not sufficient

Redaction reduces risk; it does not make a support conversation anonymous.

- **A conversation is frequently identifiable from its content alone** — a specific
  transaction, an unusual complaint, a distinctive combination of dates and amounts. Removing
  names does not change that.
- **So "we redacted it, therefore it's anonymous, therefore the rules don't apply" is
  wrong**, and it is the most common reasoning error in this area. Treat the dataset as
  personal data unless someone competent has assessed otherwise.
- **Audit the redaction rather than trusting it**, on the fields that are always missed:
  HTML bodies alongside plain text, quoted and forwarded text, signature blocks, attachment
  filenames, custom fields, internal notes, and voice transcripts where numbers appear as
  spoken digit strings.
- **Memorisation is a real risk.** Models can reproduce distinctive training strings, so a
  rare identifier that survived redaction can surface in an output. Test for it after
  training by probing with fragments from the training set.

## Building the dataset, if it is cleared

- **Sample deliberately.** For an eval set, stratify toward the cases where being wrong is
  expensive and include the hard ones — ambiguous requests, out-of-scope asks, requests for
  a human. For training, representativeness matters more.
- **Keep provenance per record** — which conversation, which date, which exclusion checks it
  passed. Without this you cannot honour an erasure request against the dataset, or
  reconstruct what a model was trained on.
- **Version and freeze it.** A dataset that changes silently makes every model comparison
  meaningless.
- **Keep eval data out of training data.** Contamination inflates every subsequent
  measurement, and it is easy to do accidentally when both come from the same corpus.
- **Store it as the sensitive asset it is** — restricted access, encrypted, with its own
  retention, and inside your data map rather than on someone's laptop.
- **Document the whole chain**, because you will be asked what a production model was trained
  on, possibly by someone external.

## Bias, which is a separate obligation

A model trained on your historical conversations learns your historical behaviour,
including the parts you would not defend:

- **Where past handling differed by market, language, channel or customer group**, the model
  inherits it and applies it at scale.
- **Where past redress correlated with who escalated loudest**, a model trained on those
  outcomes learns to reward escalation.
- **Where transcription quality is worse for some accents**, training on transcripts
  encodes that as a quality signal.

Check the training corpus's composition against the population it will serve, and report
the gaps. This is not a legal question — it is a straightforward quality one that becomes
an ethical one at scale.

## Guardrails

- **Do not move data to a provider before the assessment is done.** Sending conversations to
  an external API to see whether the idea works is itself the processing that needed
  approving, and it cannot be undone.
- **Do not assert that a redacted dataset is anonymous.**
- **Do not train on data you cannot enumerate.** If you cannot say whose data is in the set,
  you cannot honour an erasure request or answer a regulator.
- **Do not use vulnerability or special-category signals as features**, even where the
  conversation is otherwise eligible.
- **The lawful basis, the compatibility assessment and the erasure position are legal
  determinations.** Surface them; do not resolve them.
- **Cite ids and counts. Do not paste conversation content** into an assessment document.

## Present results to the user

1. **The five gating questions**, answered or explicitly open, with the open ones routed. If
   any is open, say the dataset should not be built yet.
2. **Provider terms as configured** — retention and training use — for anything leaving your
   infrastructure.
3. **The exclusion list applied**, with counts and the exclusion rate, plus a note on whether
   the rate suggests detection is working.
4. **Redaction audit results** on the fields that are always missed, rather than an assertion.
5. **The reversibility position** — what happens on an erasure request after training.
6. **Dataset construction** — sampling, provenance, versioning, train/eval separation, storage
   and retention.
7. **Composition against the served population**, with inherited-bias risks named.
8. **What is legal's to decide**, listed separately and unresolved.
