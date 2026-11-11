---
name: sas-validate
description: Reconcile either approved public SAS workflow's behavioral controls with frozen cases and original evidence. Use to explain expected defects, unverified semantics, and the correctness evidence still needed by candidate architectures. Also use for an explicitly supplied public ML-2/MOD-2 modeling evidence package.
---

## Public ML-2/MOD-2 modeling package

Use this path when the request supplies the public ML-2 source review (EVIDENCE.json, or ML2_EVIDENCE.json in a review bundle) and its matching MOD-2 package. Confirm the manifest and plan refer to the same source and review identity before drawing conclusions. Use only the supplied artifacts. A canonical graph, legacy fixture reports and SAS tie-out are not prerequisites for this path. Report missing or mismatched evidence without filling gaps from another fixture.

1. Inspect MANIFEST.json, VALIDATION.json, DESIGN.json, SCORES.json and the mapping and coefficients. Reconcile each public case's audit keys, expected and observed scores, and the reported tolerance. Distinguish a recorded check from a check you performed.
2. Return a verification plan separating declaration checks, public engineering checks, independent SAS comparison and human acceptance. Name missing SAS descriptors, response profile, CLASS columns, fitted outputs and attributable scored rows. Preserve fitting, convergence, ODS production and reference execution as NOT_RUN.

Label every material claim **SOURCE_DECLARED**, **CANDIDATE_ENGINEERING**, **INFERRED** or **UNRESOLVED**. Cite its supplied filename and JSON pointer or source location, including original byte ranges when available. Report the review actions actually performed separately from skill discovery, loads or file reads. Keep the result DRAFT, behavioral evidence UNAVAILABLE, semantic verification UNVERIFIABLE, acceptance BLOCKED, reference and benchmark execution NOT_RUN, and historical provenance UNBOUND. Return notes without editing artifacts or executing SAS.

## Original synthetic fixture workflows

Review evidence availability in MANIFEST.json before opening [TIEOUT.json](../../examples/offline-review/TIEOUT.json) from one existing [manifest-bound package](../../examples/offline-review/MANIFEST.json) or a requested fresh output of [review_workflow.py](../../scripts/review_workflow.py). Existing-package inspection requires no execution receipt. Read every package document from that chosen directory. Links here locate the checked-in example. The existing [tie-out script](../../scripts/mvp3_tieout.py) owns behavioral computation. Inspection can use its recorded results without rerunning it.

1. Verify the selected package hashes and subject. If behavioral_evidence is UNAVAILABLE, confirm that tie-out and decision reports are absent, explain the missing oracle, and review the source-based obligations and hand-authored expectations. The stateful fixture's [public declarations](../../tests/p2a_expectations.py) are reference material, without observed behavioral verdicts. Return notes with UNVERIFIABLE verification and BLOCKED acceptance. For legacy MVP-2, manifest-listed reports identify available evidence. Continue the following case checks only for that fixture, binding the report's `reference` to the manifest's graph, source and fixture identities. Check the SHA-256 of the [frozen case table](../../tests/mvp3_cases.py) against both `reference.specification_sha256` and `subject.case_table_sha256`. Inspect its literal `CASES` and `FIXTURES` declarations. Extra behavioral vectors have their own case/input identities within that table. The graph digest identifies the original MVP-2 subject.
2. For MVP-2, reconcile all 17 unique case IDs with the frozen definitions. Check input ID, probe, expected verdict, expected rows and first-discrepancy stage against the table. Compare observed verdict with expected verdict, require `matches_specification` to be true, and inspect observed rows, discrepancy details and modeled scope. Use the existing [comparison rules and explanations](../../docs/MVP3_VALIDATION.md#reference-and-comparison-rules), including permitted tie permutations. The 7 PASS, 8 deliberate FAIL and 2 UNVERIFIABLE totals are a consistency check after individual reconciliation.
3. For available behavioral evidence, explain passing controls, expected defect detection and UNVERIFIABLE cases using the selected [decision-review matrix](../../examples/offline-review/DECISION_REVIEW.md). An injected negative-control FAIL is its expected outcome. A mismatched expected/observed outcome, incorrect discrepancy or missing case blocks using that report. UNVERIFIABLE cases retain their reasons and unassessed outputs. B17 covers O1–O3 while O4's include effects remain UNKNOWN and full-workflow acceptance BLOCKED.
4. Trace each material discrepancy or remaining obligation into [EVIDENCE.md](../../examples/offline-review/EVIDENCE.md) using the original operation/edge/fact, module and source span. Identify the independent SAS reference outputs, numerical ranges and tolerances, missing-value evidence, state-boundary proof and authorized include evidence still required. Public development controls establish only their modeled subset. Independent SAS semantic acceptance requires its separate gate.

Return concise notes in chat or a separate review document with case IDs, expected and observed outcomes, discrepancy meaning, source references and the next required evidence. Identify recorded-result inspection versus a replay actually executed. Report file-guided use, Codex discovery, typed loading and completed model execution only as individually observed.

Stop on altered bindings, missing declared available evidence or frozen definitions, duplicate cases or unexplained disagreements. UNAVAILABLE evidence requires missing-proof notes and keeps the review usable. It must carry no invented PASS outcomes or borrowed case IDs. A declared unresolved dependency stays an explicit blocker during review. Keep architecture selection BLOCKED. Do not execute SAS, submitted programs or distributed runtimes, invent a new oracle or benchmark, or treat this report as protected evaluation gold. Native Windows evidence I/O remains BLOCKED. The [downstream pin](../../docs/COMPATIBILITY.md) is read-only.

```text
artifact_authority: DRAFT
semantic_verification: UNVERIFIABLE
semantic_acceptance: BLOCKED
benchmark_execution: NOT_RUN
```
