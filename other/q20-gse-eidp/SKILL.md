---
name: q20-gse-eidp
description: "Produce the end item data package a delivered piece of ground support equipment owes under ECSS-Q-ST-20C clause 5.8.4.1: derive the package sections from the item's own states instead of a standing table, refuse a section still in draft or marked approved with nobody behind it, force every open nonconformance into the package the receiving side accepts the item with, compute the approved fraction of the required set and decide whether the package may be released. Use when GSE is about to change hands and its data package has to be assembled or audited. Trigger: ecss, q-st-20c-clause-5-8-4-1, gse-end-item-data-package, gse-eidp-section-derivation, gse-eidp-approval-state, gse-open-nonconformance-carry-over, gse-data-package-release."
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
  tags: [ecss, q-st-20c-quality-assurance-scope, q20-gse-eidp, gse-end-item-data-package, gse-eidp-section-derivation, gse-eidp-approval-state, gse-open-nonconformance-carry-over, gse-data-package-release]
  version: 0.1.0
  author: Aero Agent Skills
---

# ECSS GSE End Item Data Package (space-systems/ecss/q20-gse-eidp)

Use when the task is the clause 5.8.4.1 end item data package for ground
support equipment in ECSS-Q-ST-20C: a GSE item is being delivered, the package
content follows the corresponding Annex B document requirements definition, and
the question is whether what has been assembled may travel with the item.

## Domain quick reference

- The package is derived from the item, not chosen from a standing table. A
  pressurised system owes its pressure certification, a lifting fixture its
  proof-load certificate, a software-driven controller its build record, a
  measuring chain its calibration certificate, a safety-critical duty its
  assessment record, and an item with limited-life parts its list of them.
- A section that exists is not a section that counts. Draft is not delivered,
  superseded is not current, and an approved section with no approver named is
  a page nobody stood behind.
- The data package is how the receiving side learns what it is taking on.
  Every nonconformance still open against the item belongs in it; one left out
  is accepted by someone who was never told it existed.
- Completeness is a fraction of the required set, not a count of pages. Ten
  approved sections against a set of fourteen is a package at five sevenths,
  and the number is reported so the gap can be sized.
- Release is the conjunction of two separate facts: the required set is fully
  approved, and no finding stands anywhere in the package. Either alone lets
  an incomplete package through.
- An extra section is not a defect. A spares list nobody asked for adds
  nothing to the gap, and a gate that reports it wastes the reviewer's attention.

## Workflow

1. Validate the GSE item: an identifier, a designation, and each package-driving
   state stated as a boolean rather than assumed absent.
2. Derive the mandatory section set from those states and keep it ordered so
   the reviewer reads the base package before the conditional additions.
3. Validate the assembled sections, refusing a duplicated section name, an
   unknown release state and a missing state field.
4. Name each gap separately: section absent, section in draft, section
   superseded, section approved with no approver.
5. Reconcile the open nonconformance list against what the package carries and
   name every one that is not carried.
6. Compute the approved fraction of the required set, counting a section only
   when it is approved and has an approver.
7. Release the package only when the fraction reaches unity within the named
   tolerance and no finding stands.

## Pitfalls

- Assembling the same package for every GSE item. The pack that is right for a
  plain trolley is three certificates short the moment the item lifts, holds
  pressure or measures anything.
- Reading a section's presence as its approval. A draft acceptance test report
  in the binder is the report not yet agreed, and it delivers nothing.
- Approving a section without naming who approved it. The signature is the
  point of the approval; without it the state is a claim about itself.
- Leaving an open nonconformance out of the package. The receiving side
  accepts the item as it stands, and what it is not told it cannot accept.
- Reporting a page count instead of a fraction of the required set. Extra
  sections inflate a count and hide the two certificates that are missing.
- Releasing on completeness alone. A fully populated package with a superseded
  section in it is complete and still wrong.

## Behavior contract (gate 3)

The item validation, state-derived section set, section validation, the
draft, superseded and unapproved findings, the open-nonconformance carry-over
check, the approved fraction and the release decision are exercised by the
gate 3 contract test: scripts/test_q20_gse_eidp.py against
scripts/q20_gse_eidp_logic.py (stdlib unittest, offline). Run:
python3 scripts/test_q20_gse_eidp.py

## Compliance

- ECSS standards are freely downloadable (ESA); cite the source and
  paraphrase per standards-map.yaml.
- compliance: STANDARDS-REF, gated: false.
