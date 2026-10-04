---
name: running-blameless-postmortems
kind: skill
status: ready
provenance:
  principles:
  - P001
  - P012
  - P048
  - P122
  - P123
  - P008
  claims:
  - C00910
  - C00926
  - C01726
  - C02046
  - C03613
  - C03614
  - C03615
  - C03619
  - C03620
  - C03621
  - C03622
  - C03623
  evidence:
  - E00370
  - E00382
  - E00553
  - E00569
  - E00750
  - E00751
  - E00752
  - E00753
  - E00754
  - E00755
  - E00756
  - E00757
  source_anchors:
  - 9fe26df35c80-c0017
  - 9fe26df35c80-c0018
  - 0bea4daa68ab-c0003
  - 0bea4daa68ab-c0015
  - 861f0551c788-c0029
  - 861f0551c788-c0030
  authored_from_digest: a5a2d126969b60fb1405ceff5c4e69b8b3ae999f80af63b06d43d77d38689b85
---

# Running blameless postmortems

## Purpose

Turn an incident into organisational learning instead of individual punishment. Run blameless
postmortems and sustain a just, generative culture that treats failure as a systemic learning
opportunity, because blame suppresses the honest reporting reliability depends on (P009). The aim is
a reconstructed timeline, systemic and process-level causes, and agreed countermeasures that get
done — not a name to attach to the outage.

## When to use

- After an incident or outage.
- Designing an incident-review or learning process.
- A culture of blame is discouraging people from surfacing problems.

There is one boundary: genuine, repeated, wilful misconduct is not a systemic failure, and the
accountability decision there rests with leadership (per the package handoff rules), not this
review. Everything else gets the blameless treatment.

## Procedure

1. **Refuse a blame-first framing (P009).** If asked to identify who was at fault and word the
   review accordingly, decline and explain why: blame suppresses the honest reporting that
   reliability depends on (CL012). Framing an incident review around individual blame rather than
   systemic, process-level learning is a forbidden output.
2. **Hold the postmortem promptly.** Run a blameless retrospective soon after every significant
   incident, while memory is fresh, to reconstruct the timeline and agree countermeasures instead
   of seeking someone to punish (CL013).
3. **Reconstruct the timeline factually.** Build a shared, judgement-free account of what happened
   and when — detection, diagnosis, mitigation, recovery — drawing on the incident command record
   if the incident ran under a defined commander structure (CL053).
4. **Find systemic and process causes (P009).** Drive the analysis to the systemic and process
   factors that let the failure happen and propagate, so the organisation learns from failure
   rather than blaming individuals (CL054). Ask what about the system — not the person — made the
   error easy to make and hard to catch.
5. **Agree countermeasures and follow through.** Turn causes into concrete countermeasures with
   owners; reward completing the action items and share the postmortem widely so lessons propagate
   and the same failure is less likely to recur elsewhere (CL055).
6. **Protect the learning culture (P009).** Sustain a blame-slow, learn-fast culture where mistakes
   lead to rapid fixes and shared learning rather than punishment, protecting the willingness to
   innovate (CL068); leaders sustain it by visibly participating in retrospectives and rewarding
   teams that surface and fix systemic problems (CL015).
7. **For `review` requests on an existing postmortem,** check it is blameless, has a factual
   timeline, names systemic/process causes (not a person), and has owned, tracked countermeasures.
   Name each gap.

## Inputs

- The incident: what happened, the timeline so far, and any incident-command record.
- The team's current review process and culture (blameful vs blameless).
- Whether the ask is to facilitate a postmortem, design the process, or review an existing writeup.

## Output

A blameless postmortem (or a critique of one): factual timeline, systemic and process causes, and
owned countermeasures with a follow-through and sharing plan — grounded in P009. Blame-first
requests are declined with the reason and redirected to this structure.

## References

- `references/devops-transformation-readiness-reference.md` — the just/generative culture this
  practice depends on.
- Sibling skills: `defining-slos-and-error-budgets`, `reducing-toil-and-on-call-load` (the
  reliability work countermeasures often feed into).

## Provenance

Derived from principle P009 (claims CL012, CL013, CL015, CL053, CL054, CL055, CL068; evidence
EV012, EV013, EV015, EV053, EV054, EV055, EV068) across `the-devops-handbook-c4933b3c`,
`comp500-15893c30`, and `comp109-5dbbef8d` (all distillation-only — paraphrase, no verbatim
quotation). The blameless-learning stance is supported by both research-grade and expert-practice
evidence in the sources.
