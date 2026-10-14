---
name: q20-qap-drd
description: "Generate and assess the quality assurance plan of ECSS-Q-ST-20C Annex A against its document requirements description: build the numbered DRD outline the contract level owes, decide whether each section carries the subjects the DRD names, confirm the organisation section states a quality function independent of the line that builds the product, reconcile the task provisions with the level's set, resolve every procedure the plan cites against its own reference list, and refuse a tailoring declaration on scope or organisation. Use when a quality plan is drafted, tailored or reviewed before submission. Trigger: ecss, q-st-20c-annex-a, quality-assurance-plan-drd, qa-plan-section-order, qa-plan-task-provisions, qa-plan-independence-statement, qa-plan-tailoring-justification."
license: Apache-2.0
compliance: STANDARDS-REF
standards:
  - id: ecss
    reference-only: true
gated: false
domain: space-systems
pack: space-systems
compatibility: "agentskills.io SKILL.md; any SKILL.md host (Claude Code, Hermes, OpenClaw)"
metadata:
  domain: space-systems
  subdomain: ecss
  tags: [ecss, q-st-20c-quality-assurance-scope, q20-qap-drd, quality-assurance-plan-drd, qa-plan-drd-section-order, qa-plan-organization-independence, qa-plan-task-provisions, qa-plan-documentation-and-records, qa-plan-drd-tailoring-justification]
  version: 0.1.0
  author: Aero Agent Skills
---

# ECSS Quality Assurance Plan DRD (space-systems/ecss/q20-qap-drd)

Use when the task is the Annex A document requirements description of
ECSS-Q-ST-20C: a quality assurance plan is being written, tailored or
reviewed, and the question is whether it contains what the DRD asks of it
rather than whether it reads well.

## Domain quick reference

- The DRD is a content list, not a template. Scope, the applicable and
  reference documents, the organisation and its responsibilities, the
  quality task provisions, the documentation and records, and how the plan
  itself is kept current -- a plan is graded on whether each of those
  actually says something, in that order.
- A section heading is not a section. The DRD names subjects inside each
  one, and the organisation section is the clearest case: a reporting line
  and a resource statement without an independence statement leaves the
  quality function reporting into the organisation it is supposed to be
  able to stop.
- The task provisions are level-dependent. Every plan commits to
  procurement, inspection and test, nonconformance, metrology, handling
  and records control. A prime adds supplier surveillance, the customer
  interface and its own audit programme; a subcontractor adds surveillance
  and flow-down verification; a supplier adds flow-down verification
  alone. Writing a supplier plan and submitting it at prime level is how
  the audit programme goes missing.
- Tailoring is legitimate and reviewable. Where a section may be dropped
  it carries a justification and a customer approver, which is what makes
  the omission a decision instead of an oversight. Scope and organisation
  are refused outright: without them the plan does not state what it
  covers or who is accountable.
- A plan that cites a procedure it never lists is a plan whose commitments
  cannot be followed. The citation and the reference list are checked
  against each other, not read separately.
- A section nobody asked for is not a defect. It is reported as an extra,
  because it usually signals a plan carried over from another contract.

## Workflow

1. Resolve the contract level, refusing a level outside the recognised set
   rather than falling back to a generic task list.
2. Build the numbered outline: sections in DRD order, subjects numbered
   within their section, and the level's task set attached to the task
   provisions section.
3. Normalise the submitted plan: one entry per section, subjects on
   anything not tailored out, and a justification and approver on anything
   that is.
4. Decide each section: complete, validly tailored out, incomplete against
   its named subjects, or absent.
5. Apply the tailoring rules, refusing scope and organisation outright.
6. Reconcile the declared task provisions with the level's set, reporting
   a task beyond the level as an extra rather than a finding.
7. Resolve the cited documents against the reference list, then report the
   conformance fraction and the verdict.

## Pitfalls

- Grading the table of contents. Every DRD section can be present and the
  plan still silent on independence, retention or approval authority.
- Reusing a plan across contract levels. The base task set is identical,
  so the copy looks complete while the level-specific provisions are the
  ones that were needed.
- Accepting a tailoring line because it is plausible. Without a
  justification and a customer approver it cannot be reviewed, and on
  scope or organisation no justification is sufficient.
- Treating extras as findings. A leftover section is a signal about where
  the plan came from, not a reason to reject it.
- Reading the reference list on its own. Its job is to make the citations
  resolvable, so the two are compared rather than checked for existence.

## Behavior contract (gate 3)

The level task resolution, the numbered outline generation, the
per-section subject grading, the tailoring admissibility rules including
the scope and organisation refusal, the task provision reconciliation, the
citation resolution and the conformance fraction are exercised by the gate
3 contract test: scripts/test_q20_qap_drd.py against
scripts/q20_qap_drd_logic.py (stdlib unittest, offline). Run:
python3 scripts/test_q20_qap_drd.py

## Compliance

- ECSS standards are freely downloadable (ESA); cite the source and
  paraphrase per standards-map.yaml.
- compliance: STANDARDS-REF, gated: false.
