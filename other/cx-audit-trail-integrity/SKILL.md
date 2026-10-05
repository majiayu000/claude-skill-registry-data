---
name: cx-audit-trail-integrity
description: Use to verify that the chain from conversation to evaluation to decision is complete and reconstructible, so a QA score or a customer outcome can be explained months later. Trigger for "can we prove why this decision was made", "is our audit trail complete", "reconstruct how this score was produced", evidencing an AI-assisted decision, or an auditor asking how a conclusion was reached.
metadata:
  author: rulebase
  version: "1.0.0"
  archetype: analysis
---

# Audit trail integrity

Someone asks why a specific customer got a specific outcome, or why an agent received a
specific score, and the answer has to be reconstructible from records — not from
somebody's memory of a meeting.

This is a distinct problem from having data. Most support stacks record plenty and still
cannot answer "on what basis was this decided", because the pieces exist in different
systems with no reliable link and no version history.

**Where a decision was AI-assisted, the bar is higher.** In several regimes a
substantially automated decision affecting a person carries a specific explainability
obligation, and "the model scored it 62" is not an explanation.

## The chain, link by link

Pick a decision and try to walk it backwards. Each link is a place trails break:

1. **The conversation.** Is the full content still retrievable, including internal notes,
   attachments and the parts that were redacted?
2. **The evaluation or assessment.** Which rubric version, which criteria, which reasoning,
   which grader — human or model, and which model version.
3. **The inputs the assessor actually saw.** This is the link that almost always breaks.
   If a grader assessed a transcript that has since been redacted, or a knowledge article
   that has since changed, the assessment cannot be reproduced and you cannot show what it
   was based on.
4. **Human review.** Who reviewed, when, what they changed, and why. Overrides need a
   recorded reason or the trail explains nothing.
5. **The decision.** What was decided, by whom, under what authority, on what date.
6. **What the customer or agent was told**, and when.

Report which links are complete and which are not, per decision type rather than
overall. A trail that is complete for complaints and broken for QA is two different
findings.

## The failures that break reconstruction

**Version amnesia.** A scorecard, policy or knowledge article that changed after the
decision, with no way to retrieve what it said at the time. This silently invalidates
every historical assessment — the score is there, the standard it was measured against is
gone. Check whether your rubric and policy artefacts are versioned and whether an
assessment records the version it used, not just its own timestamp.

**Overwrite instead of append.** A record updated in place, so the earlier state is
gone. Status histories, field changes and reassignments frequently work this way. If the
only evidence of a change is that the current value differs from what someone remembers,
there is no trail.

**Broken joins.** The evaluation references a conversation id that no longer resolves —
merged, deleted, migrated. Sample and test the joins; do not assume referential
integrity holds across systems.

**Redaction after the fact.** Necessary for data protection and destructive for
reconstruction. If redaction removes the basis of an assessment, you need a documented
position on how the assessment remains explainable — this is a real tension, not an
oversight, and it should be a recorded decision rather than an accident.

**Retention mismatch.** The decision record outliving the evidence, or the evidence
outliving its lawful retention. Both are problems. Check the retention periods of every
artefact in the chain against each other; they are usually set independently and are
rarely consistent.

**Unrecorded human judgement.** An override with no reason, a manual adjustment with no
author, a decision taken verbally. The most common single gap, and the cheapest to fix
going forward.

**No model provenance.** For AI-assisted assessments: which model, which version, which
prompt, which retrieved sources, and what it actually output before any post-processing.
A prompt or model change is a change to the decision basis, and if it is not versioned
the trail cannot survive it.

## Test it, do not assess it from documentation

Sample real decisions and attempt reconstruction end to end. This is the whole method,
and it produces findings that a documentation review never will.

- **Stratify toward the consequential**: complaints, redress decisions, adverse outcomes
  for agents, anything AI-assisted, anything affecting a vulnerable customer.
- **Include some old ones.** Trails break with age — versions rotate, retention expires,
  systems migrate. A trail that works for last week and not last year is a finding.
- **Have someone else attempt the reconstruction** from the records alone, with no access
  to the people involved. If it needs a conversation with the analyst, it is not a trail.
- **Time it.** How long reconstruction takes is itself the finding when the answer is
  needed under a deadline.
- **Report completion rate per link**, so the weakest link is visible rather than averaged
  away.

## Guardrails

- **This is read-only.** Do not create records to fill a gap you find. Back-filling a trail
  is a serious matter — a reconstructed record presented as contemporaneous is falsified
  evidence, whatever the intent.
- **Where a gap is found, the honest remediation is forward-looking**: fix the recording
  so future decisions are traceable, and state plainly that historical decisions in that
  period cannot be fully reconstructed. Say the second part out loud; it is what people
  want to leave out.
- **A gap affecting decisions already relied on** — an agent dismissed, a customer refused
  redress — is a matter for compliance, legal and HR. Flag it; do not assess the
  consequence.
- **Do not conclude that a trail is adequate.** Adequacy is measured against an obligation,
  which is a compliance and legal determination. Report completeness; let them judge
  sufficiency.
- **Cite ids; do not reproduce content** in the audit output.

## Present results to the user

1. **What was sampled** — decision types, how they were stratified, and the age spread.
2. **Reconstruction success rate**, and per-link completion so the weak link is named.
3. **Time to reconstruct**, distributed.
4. **Version integrity** — whether rubric, policy and knowledge artefacts are versioned and
   whether assessments record the version used. Usually the largest finding.
5. **AI provenance**, where decisions were model-assisted: model, version, prompt,
   retrieved sources, raw output.
6. **Unrecorded human judgement**, counted.
7. **Retention consistency** across the artefacts in the chain.
8. **Decisions that cannot be reconstructed**, with the period and type affected — stated
   plainly, not softened.
9. **What needs a compliance, legal or HR determination**, kept separate from the
   forward-looking fixes.
