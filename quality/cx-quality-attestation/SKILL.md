---
name: cx-quality-attestation
description: Use to sign off a QA period for audit or governance — stating what is being attested to, on what evidence, and with which limitations. Trigger for "sign off the QA period", "attest to our quality results", "monthly QA governance pack", "certify the quality figures", or being asked to confirm quality was assured for a period.
metadata:
  author: rulebase
  version: "1.0.0"
  archetype: playbook
---

# Attesting a QA period

Somebody senior is being asked to confirm that quality was assured for a period, and
their name goes on it. The purpose of an attestation is to make explicit what is
actually being claimed — because the implied claim ("quality was good") is almost never
what the evidence supports, and the person signing usually has not been told the
difference.

**The attestation's value is in its limitations section.** An attestation with no
limitations is not a stronger attestation; it is a less careful one, and it exposes the
signer.

## State the claim precisely

Write what is being attested to, in one paragraph, and be pedantic about the verb.
Defensible claims look like:

> "The QA programme operated as designed during the period: coverage rules were applied,
> N evaluations were completed against scorecard version V, M were reviewed by a human,
> and the results are as stated."

That is a claim about **process operation**. It is verifiable, and it is what a QA
function can actually attest to.

What a QA function cannot honestly attest to:

- **That quality was good.** That is an interpretation of a score against a standard, and
  it needs the score to be a valid measure of quality.
- **That no poor outcomes occurred.** Sampled assurance cannot support a negative across
  the population.
- **That every conversation was compliant.** Unless there was a census, which there was
  not.

If the person asking wants one of those, say which one is unavailable and what would be
needed. Signing a stronger claim than the evidence supports is the failure mode here, and
it is the signer who carries it.

## The evidence the attestation rests on

Enumerate it, with numbers:

- **Coverage** — evaluations completed, as a share of eligible conversations, broken down
  by channel, team and market. **Zero-coverage segments named individually**; they are the
  most important line in the pack, and an average conceals them.
- **Scorecard version(s) in force**, and any change during the period. A mid-period change
  breaks comparability and must be disclosed.
- **Sampling** — how conversations were selected, and whether selection was random,
  stratified or reviewer-chosen. **Reviewer-chosen selection cannot support a population
  claim** and needs saying.
- **Grader mix** — human, AI, or both, with the model version if applicable, and the
  agreement measured in the period.
- **Human review rate** on AI-graded evaluations.
- **Disputes** raised, resolved, and outstanding at period end.
- **Auto-fails** raised, and how many were closed out rather than only recorded.
- **Actions arising**, and their status.

## Limitations, written by you

Every one of these applies to most programmes. State the ones that apply to yours, with
numbers rather than adjectives:

- **Sampled, not census.** Give the coverage rate and state the obvious consequence.
- **Statistical power.** If per-agent evaluation counts are low, say what the scores can and
  cannot support — at n=10 a score carries roughly a ±19 point interval, which does not
  support ranking.
- **Instrument validity.** Whether the scorecard has been validated against an outcome. If
  it has not, the attestation is about conformity to a rubric, not about quality, and that
  distinction belongs in the document.
- **Segments where the instrument is weaker** — languages, voice, anything with materially
  lower grader agreement. Scores are not comparable across those segments.
- **Channels or queues not in scope.**
- **Data gaps** — conversations not synced, transcripts unavailable, a period with a
  different taxonomy.
- **Disputes outstanding**, which means some results in the period may change.

## Governance the attestation implies

An attestation is a control, so the control needs to work:

- **A named signer**, with the authority to sign and enough understanding to be
  accountable. Walk them through the claim and the limitations rather than sending a pack.
- **Second-line review** where the structure requires it, recorded.
- **A trail** to the underlying evidence, so the figures can be reproduced later. An
  attestation whose numbers cannot be reproduced is worse than none.
- **Consistency with prior periods**, and disclosure of any definition change that breaks
  the series.
- **Escalation of anything that would change the claim**, before signing rather than after.

## When not to attest

Say this explicitly, because it is the situation the process exists for:

- **Coverage collapsed** in the period and nobody noticed until now.
- **A whole segment has no evaluations** and cannot be assured.
- **The scorecard changed mid-period** with no versioning, so results are not comparable
  or explicable.
- **A material dispute or finding is unresolved** and would change the results.
- **The evidence cannot be reproduced.**

In these cases the right output is a **qualified attestation** — the narrower claim that
*is* supported, with the exclusion stated — or a statement that the period cannot be
attested and what is required to close it. Both are legitimate outputs and both are
better than a clean attestation that does not hold. Producing a qualified attestation is
a sign the control is working, not that it failed.

## Guardrails

- **Do not sign, and do not draft language that implies you did.** This prepares an
  attestation for an authorised signer.
- **Do not soften a limitation to make the pack read better.** The limitations are the
  protection.
- **Do not assert compliance with an obligation.** Whether the evidence discharges a
  requirement is a compliance and legal determination.
- **Do not attest across a definition change** without disclosing it, even if the numbers
  look continuous.
- **Escalate a finding that would change the claim immediately**, rather than including it
  as a caveat in a pack being signed.
- **Cite ids and aggregates; no transcripts.** Attestation packs go to audit committees and
  sometimes externally.

## Present results to the user

1. **The claim**, in one paragraph, with the verb chosen precisely — and a note of any
   stronger claim that was asked for and is not supported.
2. **The evidence table**, with coverage broken down and zero-coverage segments named.
3. **Sampling method**, and whether it supports a population claim.
4. **Grader mix and agreement**, including model version where relevant.
5. **Disputes, auto-fails and actions**, with outstanding items.
6. **Limitations**, with numbers, written plainly.
7. **Whether the period can be attested cleanly, qualified, or not at all**, and what would
   close the gap.
8. **The reproduction trail** to the underlying figures.
9. **What needs a compliance or legal view** before the signer is asked.
