---
name: submission-readiness-review
description: Submission-readiness review of an eCTD sequence or a portfolio — structural validation, required Module 1 coverage, shadow review, external validator posture, Part 11 release signature and the composed freeze/dispatch gates — read from the Concept2Cure connector and reported verbatim. Use when asked whether a sequence or program is ready to file, what blocks it, or to prepare a go/no-go summary.
---

# Submission-readiness review

Readiness is a verdict the platform computes. Your job is to obtain it, explain
it, and list the blockers in the order a team should clear them. You never
originate a readiness score, a blocker count or a risk level.

## The review, step by step

1. **Locate**: `c2c_list_submissions` → `c2c_list_sequences` for the
   submission under review; note the sequence status
   (`draft|assembling|validated|frozen|dispatched`).
2. **Assess**: `c2c_assess_sequence_readiness` with the `sequence_id`. Read:
   * `readiness` — structural findings (errors block; warnings and infos do not);
   * `validationErrors`, `leafCount`, required Module 1 coverage;
   * `shadowReviewRunCount` / `shadowReviewMissing` — a clear gate with no
     shadow review means "allowed, never reviewed"; say that;
   * `externalValidation.configured` / `.ran` — if no agency-grade validator
     ran, the sequence has not been validated to agency criteria; say that;
   * `releaseSignature.verdict` — `unsigned`, `awaiting`, `valid`, `invalid`,
     `revoked` or `undetermined` (undetermined is not unsigned; it means the
     lookup could not decide);
   * `freezeGate` and `dispatchGate` — `cleared` plus `blockers[]`.
3. **Structure check**: `c2c_validate_ectd_structure` with the `sequence_id`
   for the section-level detail behind the structural findings.
4. **Portfolio context** (optional): `c2c_readiness_overview` for the
   organisation-wide rollup and `c2c_search_precedents` for the precedent
   slice (report an empty corpus as empty).
5. **Deployment posture** (when the question is "can this environment file
   at all"): `c2c_ga_readiness_probe` — licensed DTDs, eSTAR templates and
   validator configuration, observed on disk.

## The go/no-go summary format

```
Sequence <number> (<region>) — status <status>
Dispatch gate: CLEAR | BLOCKED
  Blockers (engine): 1. … 2. …
Freeze gate: CLEAR | BLOCKED
Structural: <errors> errors, <warnings> warnings, <present>/<required> required sections
Shadow review: <n> run(s) | none — gate clear but never reviewed
External validation: <validator> configured: yes/no; ran: yes/no
Release signature: <verdict> (<detail>)
Next actions (in order): …
Source: c2c_assess_sequence_readiness at <timestamp>; all figures verbatim.
```

## Rules

* Quote blockers exactly as the engine words them.
* Do not soften a BLOCKED gate into "nearly ready".
* If any tool refuses (wrong organisation, sequence not found, no licence),
  the review stops there and the refusal is the finding.
* Filing, freezing and signing happen in Submission Center by a named person;
  point to the `signOff.url` the tools return.
