---
name: e10-ddf
description: "Use when produce or maintain the Design Definition File (DDF) for a space system product under ECSS-E-ST-10C clause 5.4.1.4 and Annex G: classify each DDF content item into its section (design description, budget, or interface data), compute a budget item's margin against the minimum margin required at the current review milestone, verify each interface data item declares a valid mating product, confirm every mandatory DDF section is populated for the product, and determine whether the product's DDF is ready to baseline at that milestone. Trigger: ecss, e-st-10-system-scope, design-definition-file, ddf, design-budgets, interface-data, review-milestone, baseline-readiness."
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
  tags: [ecss, e-st-10-system-scope, design-definition-file, design-budgets, interface-data, review-milestone]
  version: 0.1.0
  author: Aero Agent Skills
---

# ECSS System Engineering — Design Definition File (space-systems/ecss/e10-ddf)

Use when the task is to produce or maintain the Design Definition File
(DDF) of ECSS-E-ST-10C clause 5.4.1.4 and Annex G -- assembling, per
product, the design description, the design budgets, and the
interface data, and checking that content against the review
milestone the product is being baselined for.

## Domain quick reference

- A DDF is produced per product (configuration item), not once for
  the whole system. Every content item captured for a product's DDF
  is categorized into exactly one of three sections before it is
  reviewed: design description (functional description, physical
  description, design drivers, design solution), budget (mass, power,
  link, thermal), or interface data (physical, functional, electrical,
  thermal interface). An item type outside all three sections is
  rejected rather than silently filed.
- A budget item carries a predicted value and a maximum allowable
  value; its margin is the fraction of headroom remaining
  ((maximum - predicted) / maximum), expressed as a percent. Margin
  can be negative when the prediction already exceeds the maximum --
  that is a legitimate (non-error) outcome that the margin check must
  surface, not a computation failure.
- The margin a budget item must retain shrinks as the product design
  matures through its review milestones (SRR, PDR, CDR, QR) --
  wide headroom is expected early, and the required minimum tightens
  at each later review. A budget item's margin is checked against the
  minimum for the milestone the DDF is being assembled for, not a
  fixed threshold.
- Each interface data item must declare the product it mates with.
  A DDF is incomplete for that item if no mating product is declared,
  and inconsistent if the mating product is the product itself.
- A product's DDF is baseline-ready at a milestone only when all three
  sections have at least one item on record, every budget item meets
  its milestone margin, and every interface data item has a valid
  mating-product declaration -- any one gap keeps the DDF from being
  baselined, it does not average out against the others.

## Workflow

1. For each content item collected for a product, classify it into
   design description, budget, or interface data; reject an
   unrecognized item type before it enters the DDF.
2. Confirm the product's DDF has at least one item in every section;
   record a missing-section finding for each section with none.
3. For each budget item, compute its margin from the predicted and
   maximum values and compare it against the minimum margin required
   for the product's current review milestone; record a finding for
   any item below the minimum.
4. For each interface data item, confirm it declares a mating product
   that is not the product itself; record a finding for a missing or
   self-referential mating-product declaration.
5. Aggregate the section-completeness, budget-margin, and
   interface-linkage findings for the product; the DDF is not
   baseline-ready at that milestone until all three lists are empty.

## Pitfalls

- Treating a negative budget margin as an input error instead of a
  finding -- a prediction that already exceeds the maximum is exactly
  the condition the check exists to catch, and must be returned as a
  finding, not raised as an exception.
- Applying one fixed margin threshold across every review milestone --
  the required minimum margin tightens as the design matures, so the
  same predicted/maximum pair can pass at SRR and fail at CDR.
- Treating an interface data item with no declared mating product as
  merely incomplete metadata -- Annex G ties interface data to the
  interface control process, so a missing mating-product declaration
  is a DDF gap, not a cosmetic omission.
- Declaring a DDF baseline-ready because the budgets are all within
  margin while a mandatory section (e.g. interface data) has zero
  items on record -- section-completeness and per-item compliance are
  independent checks and both must pass.

## Behavior contract (gate 3)

The item-classification, section-completeness, budget-margin, and
interface-linkage logic is exercised by the gate 3 contract test:
scripts/test_e10_ddf.py against scripts/e10_ddf_logic.py (stdlib
unittest, offline). Run:
python3 scripts/test_e10_ddf.py

## Compliance

- ECSS standards are freely downloadable (ESA); cite the source and
  paraphrase per standards-map.yaml.
- compliance: STANDARDS-REF, gated: false.
