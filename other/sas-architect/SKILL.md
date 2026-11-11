---
name: sas-architect
description: Compare the draft native Python and Spark designs for either approved public SAS workflow. Use to connect dependency constraints and behavioral controls to conditional design choices and missing proof. Also use for an explicitly supplied public ML-2/MOD-2 modeling evidence package.
---

## Public ML-2/MOD-2 modeling package

Use this path when the request supplies the public ML-2 source review (EVIDENCE.json, or ML2_EVIDENCE.json in a review bundle) and its matching MOD-2 package. Confirm the manifest and plan refer to the same source and review identity before drawing conclusions. Use only the supplied artifacts. A canonical graph, legacy fixture reports and SAS tie-out are not prerequisites for this path. Report missing or mismatched evidence without filling gaps from another fixture.

1. Use the supplied PLAN.json, VALIDATION.json and the earlier modeling-review findings, if available, to compare fixed scoring with fitting. Compare native and distributed options against the same evidence and verification obligations.
2. Return a draft ADR and one bounded next implementation with acceptance criteria. Check what MOD-2 already implements before proposing work. Explain what could justify distribution and keep production selection open without scale, benchmark or independent behavioral evidence.

Label every material claim **SOURCE_DECLARED**, **CANDIDATE_ENGINEERING**, **INFERRED** or **UNRESOLVED**. Cite its supplied filename and JSON pointer or source location, including original byte ranges when available. Report the review actions actually performed separately from skill discovery, loads or file reads. Keep the result DRAFT, behavioral evidence UNAVAILABLE, semantic verification UNVERIFIABLE, acceptance BLOCKED, reference and benchmark execution NOT_RUN, and historical provenance UNBOUND. Return notes without editing artifacts or executing SAS.

## Original synthetic fixture workflows

Review one existing [manifest-bound package](../../examples/offline-review/MANIFEST.json) or a requested fresh output of [review_workflow.py](../../scripts/review_workflow.py). Read [ARCHITECTURE.md](../../examples/offline-review/ARCHITECTURE.md), [ADR_NATIVE.md](../../examples/offline-review/ADR_NATIVE.md), [ADR_SPARK.md](../../examples/offline-review/ADR_SPARK.md) and, when manifest-listed, [DECISION_REVIEW.md](../../examples/offline-review/DECISION_REVIEW.md). Follow their links into [EVIDENCE.md](../../examples/offline-review/EVIDENCE.md) and any manifest-listed [TIEOUT.json](../../examples/offline-review/TIEOUT.json).

For a fresh run, read every named document from that output directory. Links above locate the checked-in example.

1. Trace the selected subject, graph, source spans and module ownership. Interpret its actual DATA, ORDER, STATE and RESOURCE records. MVP-2 E3 is conservative BY state with current-row division. The stateful fixture represents retained accumulation and explicit resets. Assess value lineage alongside state effects before proposing any split.
2. Inspect evidence availability first. The stateful manifest declares behavioral_evidence UNAVAILABLE and omits tie-out and decision reports. Continue a draft review using source evidence, ADRs and explicit missing-reference obligations. The legacy MVP-2 manifest identifies available reports in its files map. Only that fixture uses the 17 MVP-3 cases, including B04/B12/B17. Reconcile expected and observed verdicts, matches_specification, discrepancies and scope before citing controls. Expected negative-control FAIL is deliberate defect detection.
3. Use the selected ADR matrix and any available decision review to compare both candidates against the same correctness obligations. Hand-authored expectations without an approved behavioral report remain reference material requiring a future tie-out. For Python, assess workstation memory and local order preservation. For Spark, assess order, state and multiplicity across exchanges and retries. Retain the matrix's open numerical, missing-value and performance obligations.
4. Return a short decision note giving the obligation, original operation/edge/fact or source span, case ID and verdict, implication for each candidate, then the next test or human decision. Notes may be returned directly in chat or separately from the generated package. Report file-guided use, Codex discovery, typed skill loading and completed model execution only as individually observed. Use [downstream compatibility](../../docs/COMPATIBILITY.md) only as a read-only reference.

Stop if required evidence or declared available cases are missing, duplicated, mismatched or disagree with the bound package. Reject unavailable evidence accompanied by purported passing results. Keep production selection BLOCKED. Do not produce a schedule, speedup estimate, benchmark, SAS/Spark execution or downstream handoff. Native Windows evidence I/O remains BLOCKED.

```text
artifact_authority: DRAFT
semantic_verification: UNVERIFIABLE
semantic_acceptance: BLOCKED
benchmark_execution: NOT_RUN
```
