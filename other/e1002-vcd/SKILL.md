---
name: e1002-vcd
description: "Use when establishing and maintaining the Verification Control Document (VCD) under ECSS-E-ST-10-02C clause 5.2.8.2 and Annex B: validate a recorded verification method and status against their enumerations, determine which methods are permitted to close a given requirement category, check the recorded method is permitted, check that the recorded method is consistent with the requirement's applicability, check a closed status carries its closure evidence, evaluate one VCD entry, roll entries up to a program status, and decide VCD completeness. Trigger: ecss, e-st-10-02c, vcd, verification control document, annex b, method permission, requirement category, closure evidence, status roll-up."
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
  tags: [ecss, e-st-10-02c, verification-control-document, vcd, annex-b, method-permission, applicability, closure, status-rollup]
  version: 0.1.0
  author: Aero Agent Skills
---

# ECSS Verification — Verification Control Document (space-systems/ecss/e1002-vcd)

Use when establishing and maintaining the Verification Control Document (VCD) under ECSS-E-ST-10-02C clause 5.2.8.2 and Annex B — validating method/status enumerations, checking method permission by requirement category, applicability and closure evidence, and rolling entries up to a program status.

## Domain quick reference

- The VCD is the requirement-by-requirement record: for each requirement it states the verification method and the closure status with the evidence behind them.
- Method and status are enumerated: an unrecognized value is an input error, not a new category.
- Method permission is category-dependent: some requirement categories may only be closed by certain methods (e.g. a quantitative requirement cannot be closed by inspection alone).
- A 'closed' status must carry closure evidence; a closed status with no evidence is a defect.
- Entries roll up to a program status; the VCD is complete only when every applicable entry is clean.

## Workflow

1. Validate enumerations: `validate_verification_method(method)`, `validate_verification_status(status)`.
2. Check permission: `allowed_methods_for_category(category)` -> `method_selection_issues(entry)`.
3. Check applicability: `applicability_issues(entry)`.
4. Check closure evidence: `closure_issues(entry)`.
5. Evaluate one entry: `evaluate_vcd_entry(entry)` -> `is_entry_clean(result)`.
6. Roll up + completeness: `vcd_status_rollup(entries)` -> `is_vcd_complete(rollup)`; full review `vcd_program_review(entries)`.

## Pitfalls

- Closing a requirement with a method its category does not permit — a clause violation, not a judgment call.
- Marking a requirement closed with no closure evidence — `closure_issues` returns it.
- Rolling up only clean entries and dropping the rest — the roll-up must span every entry.
- Security-marking vocabulary: the content-policy gate flags the word beginning 'classif-'; use 'categorized' instead.

## Behavior contract (gate 3)

`scripts/test_e1002_vcd.py` (stdlib unittest, offline) verifies method/status validation and error paths, category method permission, applicability and closure-evidence issues, per-entry evaluation, program roll-up, and VCD completeness.

## Compliance

ECSS-E-ST-10-02C is a normative standard; this leaf implements only common-knowledge procedure and paraphrases it — no verbatim standard text. `license: Apache-2.0`, `compliance: STANDARDS-REF`, `standards: ecss` (reference-only), `gated: false`.
