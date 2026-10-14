---
name: e10-pum-drd
description: "Use when produce or review a Product User Manual against the ECSS-E-ST-10C Annex P Document Requirements Definition: confirm the manual declares the product configuration it describes and that it matches what was delivered, confirm every required section is present and not empty, confirm procedure steps are numbered contiguously without repeats, confirm every hazardous step carries its warning ahead of the step, and confirm each maintenance task states its interval and required resources. Trigger: ecss, e-st-10-system-scope, product-user-manual, pum, annex-p-drd, operating-procedures, hazard-warnings, maintenance-interval, configuration-match."
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
  tags: [ecss, e-st-10-system-scope, product-user-manual, annex-p-drd, operating-procedures, hazard-warnings, maintenance-interval]
  version: 0.1.0
  author: Aero Agent Skills
---

# ECSS System Engineering — Product User Manual DRD (space-systems/ecss/e10-pum-drd)

Use when the task is to produce or check the Product User Manual of
ECSS-E-ST-10C Annex P -- the document delivered with a product so that
someone who did not build it can operate, maintain and handle it safely.

## Domain quick reference

- A manual is written against one configuration of one product and must
  say which. A manual whose declared configuration differs from what was
  delivered is not a documentation defect to be corrected in review --
  it describes a different article, and the operator following it is
  working from the wrong book.
- A declared-but-absent configuration and a mismatched one are separate
  findings, because they are fixed differently: one is filled in, the
  other means the wrong manual shipped.
- The required sections are fixed. An empty section and an absent one
  are the same defect -- there is nothing to read either way -- so the
  check looks at content, not at headings.
- Operators follow procedures by step number. A duplicate number or a
  gap in the sequence is an execution hazard, not a typographic one:
  under load, the reader jumps to a number that is ambiguous or absent.
- A hazard warning must precede the step it protects. A warning placed
  after has already failed, because the operator reads it having
  already acted. Position is the substance of the check, not presence.
- Hazard classes are a closed set. An unrecognized class cannot be
  matched to a warning convention, so it stops the review.
- A maintenance task needs both an interval and its required resources.
  Without an interval it is never scheduled; without stated tooling or
  consumables it cannot be prepared for, and both turn planned
  maintenance into unplanned downtime.

## Workflow

1. Confirm the manual declares a product configuration and that it
   matches the delivered article.
2. Check every required section for real content, reporting empty
   sections alongside absent ones.
3. For each procedure, check step numbering for duplicates and for a
   sequence that does not run contiguously from one.
4. For each hazardous step, confirm its warning is placed before the
   step; reject an unrecognized hazard class outright.
5. For each maintenance task, confirm both the interval and the
   required resources are stated.
6. The manual may ship only when the finding list is empty.

## Pitfalls

- Checking that section headings exist rather than that they contain
  anything. A manual of empty headings passes a structural check and
  helps nobody.
- Accepting a hazard warning anywhere in the procedure. Placed after
  the step, it documents the accident rather than preventing it.
- Treating step numbering as formatting. It is the operator's index
  into the procedure, and a repeat or a gap is read under time pressure.
- Shipping a manual whose configuration was never updated after a
  design change. It looks complete, and every limit in it may belong to
  a different build.
- Recording a maintenance task with a resource list but no interval, so
  it is well specified and never scheduled.
- Silently accepting a hazard class the warning convention does not
  cover, which lets an unanalyzed hazard through with no warning rule
  applied to it.

## Behavior contract (gate 3)

The section-completeness, configuration-match, step-numbering,
hazard-warning-placement and maintenance-task logic is exercised by the
gate 3 contract test: scripts/test_e10_pum_drd.py against
scripts/e10_pum_drd_logic.py (stdlib unittest, offline). Run:
python3 scripts/test_e10_pum_drd.py

## Compliance

- ECSS standards are freely downloadable (ESA); cite the source and
  paraphrase per standards-map.yaml.
- compliance: STANDARDS-REF, gated: false.
