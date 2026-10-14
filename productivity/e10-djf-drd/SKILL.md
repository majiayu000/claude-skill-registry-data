---
name: e10-djf-drd
description: "Use when assemble or review a product Design Justification File against the ECSS-E-ST-10C Annex K Document Requirements Definition: validate each justification record's method and review status, confirm every record cites the document its evidence lives in, resolve each requirement to justified, open, rejected-evidence or no-evidence under a severity ordering, surface a requirement whose accepted argument rests on similarity alone, and decide whether the file supports the design. Trigger: ecss, e-st-10-system-scope, design-justification-file, djf, annex-k-drd, justification-evidence, similarity-heritage, evidence-traceability."
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
  tags: [ecss, e-st-10-system-scope, design-justification-file, annex-k-drd, justification-evidence, evidence-traceability]
  version: 0.1.0
  author: Aero Agent Skills
---

# ECSS System Engineering — Design Justification File DRD (space-systems/ecss/e10-djf-drd)

Use when the task is to assemble or review the Design Justification File
of ECSS-E-ST-10C Annex K -- the record that shows, requirement by
requirement, why the design is believed to meet its Technical
Specification, and what evidence carries that belief.

## Domain quick reference

- A justification record has three parts, and all three are graded: the
  method that produced the evidence (analysis, test, similarity,
  inspection, review of design), the document the evidence lives in,
  and the review status the evidence reached.
- The document reference is not metadata. The DJF is an index into the
  evidence, so a record citing nothing has not filed evidence at all --
  it is flagged whatever its status, accepted included.
- Requirement status is severity-ordered and the order matters: a
  rejected record dominates, because rejected evidence must be
  dispositioned rather than out-voted by an accepted record beside it.
  Only then does an accepted record justify the requirement; draft-only
  evidence leaves it open.
- A requirement with no record at all is its own outcome, distinct from
  one whose evidence exists but is unfinished. The first is a planning
  gap, the second an execution backlog, and they are closed by
  different work.
- Similarity is a legitimate Annex K method, but a requirement whose
  entire accepted argument is similarity carries no evidence about
  *this* design. That is surfaced rather than passed -- it is a
  judgement for a reviewer, not a defect the file can resolve itself.
- Method and status are validated before anything is graded. An
  unrecognized value cannot be placed in the severity order at all, so
  it stops the review instead of landing in a bucket.
- The file is complete only when the open, rejected and no-evidence
  lists and the finding list are all empty.

## Workflow

1. Validate the method and review status of every justification record.
2. Confirm each record cites the document holding its evidence; record
   a traceability finding for any that does not.
3. Resolve each requirement's status from its records under the
   severity ordering: rejected, then justified, then open, then no
   evidence.
4. For each requirement whose accepted records are all similarity,
   record a finding for the reviewer.
5. Partition every requirement into exactly one status bucket,
   rejecting a duplicate requirement identifier.
6. The DJF supports the design only when nothing is open, rejected or
   unevidenced and no finding stands.

## Pitfalls

- Letting an accepted record cancel a rejected one on the same
  requirement. The rejection is the finding; it closes through an
  explicit disposition, not by being outnumbered.
- Accepting a record because the analysis was done, without a document
  reference. An unlocatable analysis cannot be reviewed, which is the
  whole function of the file.
- Filing a requirement with no evidence under "open". That buries a
  planning gap inside an execution backlog.
- Treating similarity as equivalent to analysis or test when it is the
  sole accepted method. Heritage says the previous design worked, not
  that this one does.
- Reporting a percentage of requirements justified as the DJF verdict.
  Annex K completeness is all-or-nothing across the specification.
- Grading a record whose method or status is unrecognized by guessing
  the nearest known value; the review must stop and have the record
  corrected.

## Behavior contract (gate 3)

The method/status validation, record traceability, severity-ordered
requirement status, method-diversity, similarity-only and partition
logic is exercised by the gate 3 contract test:
scripts/test_e10_djf_drd.py against scripts/e10_djf_drd_logic.py
(stdlib unittest, offline). Run:
python3 scripts/test_e10_djf_drd.py

## Compliance

- ECSS standards are freely downloadable (ESA); cite the source and
  paraphrase per standards-map.yaml.
- compliance: STANDARDS-REF, gated: false.
