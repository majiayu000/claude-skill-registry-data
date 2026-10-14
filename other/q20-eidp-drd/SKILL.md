---
name: q20-eidp-drd
description: "Structure and assess the end item data package of ECSS-Q-ST-20C Annex B against its document requirements description: emit the numbered table of contents the DRD fixes, group every submitted document under the design, manufacturing, test or acceptance data it belongs to, raise a document filed under the wrong category as its own finding, name what each category is short of, list an unrecognised document as an extra instead of failing on it, and return the per-category and whole-package completeness. Use when a data package is compiled, indexed or reviewed before handover. Trigger: ecss, q-st-20c-annex-b, eidp-drd, eidp-document-categories, eidp-table-of-contents, eidp-design-data, eidp-manufacturing-data, eidp-acceptance-data."
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
  tags: [ecss, q-st-20c-quality-assurance-scope, q20-eidp-drd, eidp-drd-document-set, eidp-drd-document-categories, eidp-drd-table-of-contents, eidp-design-data-category, eidp-manufacturing-data-category, eidp-test-data-category, eidp-acceptance-data-category]
  version: 0.1.0
  author: Aero Agent Skills
---

# ECSS End Item Data Package DRD (space-systems/ecss/q20-eidp-drd)

Use when the task is the Annex B document requirements description of
ECSS-Q-ST-20C: a data package is being built or indexed, and the question
is whether its document set is grouped and ordered the way the DRD asks
rather than whether each individual record is approved.

## Domain quick reference

- The DRD makes the package an ordered set, not a pile. Design data,
  manufacturing data, test data and acceptance data, in that order, and
  every recognised document belongs to exactly one of them. The order is
  part of the content: a reviewer opening the package expects to move from
  what was designed, to what was built, to what was demonstrated, to what
  was accepted.
- The two configuration lists are the pair most often swapped. The
  as-designed list is design data and the as-built list is manufacturing
  data; filing one under the other hides the whole point of holding both,
  which is that they can be compared.
- A document filed under the wrong category is a finding in its own right,
  separate from a gap. Nothing is absent, so a completeness count alone
  reports a whole package while the reviewer cannot find the record where
  the DRD says it will be.
- A category is graded on its own. Reporting a single package fraction
  lets a complete acceptance section mask an empty test section, which is
  the section a delivery is usually short of.
- An unrecognised document is not a defect. It is reported as an extra,
  because it usually signals an index carried over from another contract
  or a supplier's own paperwork travelling with the package.
- A document without an identifier and an issue cannot be pointed at.
  Those are validated on entry rather than graded later, because an index
  line with neither is not a reference to anything.

## Workflow

1. Hold the DRD assignment of each recognised document to its category,
   and build the reverse lookup once.
2. Emit the table of contents: categories in DRD order, documents numbered
   inside their category, so the index is generated rather than typed.
3. Normalise the submission: one entry per document, an identifier and an
   issue of at least one on every entry, refusing a duplicate outright.
4. Group each document under the category the DRD assigns it, collecting
   the unrecognised ones separately.
5. Compare the declared category with the assigned one and raise each
   disagreement as a misfiling finding.
6. Name what each category is short of, compute the per-category fraction
   and the whole-package fraction, then return the verdict.

## Pitfalls

- Grading the package on a single completeness number. It hides which
  category is empty, and the categories fail unevenly.
- Reading the as-built and as-designed lists as interchangeable. They sit
  in different categories precisely so the difference between them is
  visible.
- Letting an extra document fail the package. It is a provenance signal,
  not a gap, and treating it as one buries the real findings.
- Accepting an index line with no issue. Without it the package cannot say
  which version of the document it carries.
- Checking only that a document is present. The DRD also says where it
  goes, and a misfiled record is as unfindable as an absent one.

## Behavior contract (gate 3)

The category assignment and reverse lookup, the numbered table of contents
generation, the submission validation including the identifier and issue
rules, the grouping of documents under their DRD category, the misfiling
findings, the per-category and whole-package completeness and the verdict
are exercised by the gate 3 contract test: scripts/test_q20_eidp_drd.py
against scripts/q20_eidp_drd_logic.py (stdlib unittest, offline). Run:
python3 scripts/test_q20_eidp_drd.py

## Compliance

- ECSS standards are freely downloadable (ESA); cite the source and
  paraphrase per standards-map.yaml.
- compliance: STANDARDS-REF, gated: false.
