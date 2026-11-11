---
name: sas-analyze
description: Review dependency constraints and conditional optimization ideas for either approved public synthetic SAS workflow. Use to trace sequential boundaries, question independence claims, and identify missing parallelism proof. Also use for an explicitly supplied public ML-2/MOD-2 modeling evidence package.
---

## Public ML-2/MOD-2 modeling package

Use this path when the request supplies the public ML-2 source review (EVIDENCE.json, or ML2_EVIDENCE.json in a review bundle) and its matching MOD-2 package. Confirm the manifest and plan refer to the same source and review identity before drawing conclusions. Use only the supplied artifacts. A canonical graph, legacy fixture reports and SAS tie-out are not prerequisites for this path. Report missing or mismatched evidence without filling gaps from another fixture.

1. Compare the declared modeling input and outputs with the candidate's gate and pre-sort handoff in PLAN.json. Identify which dependency is source-declared and which belongs to the Python implementation.
2. Return the execution-boundary assessment. Identify global category and fitting dependencies, and any conditional per-row scoring opportunity as an inference with proof obligations. Report absent partition, workload and benchmark evidence; make no claim of demonstrated independence.

Label every material claim **SOURCE_DECLARED**, **CANDIDATE_ENGINEERING**, **INFERRED** or **UNRESOLVED**. Cite its supplied filename and JSON pointer or source location, including original byte ranges when available. Report the review actions actually performed separately from skill discovery, loads or file reads. Keep the result DRAFT, behavioral evidence UNAVAILABLE, semantic verification UNVERIFIABLE, acceptance BLOCKED, reference and benchmark execution NOT_RUN, and historical provenance UNBOUND. Return notes without editing artifacts or executing SAS.

## Original synthetic fixture workflows

Inspect one existing [manifest-bound package](../../examples/offline-review/MANIFEST.json), including the [checked-in example](../../examples/offline-review/README.md), or a requested fresh output of [review_workflow.py](../../scripts/review_workflow.py). Existing-package inspection requires no execution receipt. Read every package document from that chosen directory. Links here locate the checked-in example.

1. Verify the manifest's payload hashes and consistent subject across [ARCHITECTURE.md](../../examples/offline-review/ARCHITECTURE.md) and [EVIDENCE.md](../../examples/offline-review/EVIDENCE.md). Keep the graph digest, workspace/run/attempt, source fingerprint, canonical operation/edge IDs, module ownership and original source spans in the trace.
2. Interpret the rendered results of the existing [P3-A1 diagnostic](../../src/sas_re/_dependency_diagnostics.py) using its [reading key](../../docs/P3_A1_DESIGN.md#reading-the-result). DATA represents producer/consumer relationships, ORDER represents ordering constraints, and STATE records state requirements requiring separate value-lineage review. RESOURCE annotations concern shared resources separately from semantic precedence. Identify the edge types and LOG/LST observations actually present in the chosen graph. Keep missing measurements explicit.
3. Identify represented sequential constraints, independence claims needing proof and conditional optimization boundaries. MVP-2 examples include E4/E2 across modules, E1 into SQL and E3 BY state separate from current-row arithmetic. In the stateful graph, trace the actual accumulation, retained state and explicit reset. Derive IDs and module relationships from the selected package. A missing edge or path leaves independence unproved. Require effect completeness, physical dataset versions, order, state continuity, cardinality and numerical proof before treating a boundary as independent or safe to split. Carry any declared unresolved dependency as an explicit blocker.
4. When behavioral evidence is available and the report is listed in the selected manifest, use [DECISION_REVIEW.md](../../examples/offline-review/DECISION_REVIEW.md) for the Python/Spark comparison and case limits. Otherwise use its ADRs and proof obligations, explicitly carrying behavioral_evidence UNAVAILABLE without borrowing cases from another fixture. Discuss local Python processing or distribution through Spark, Ray or Dask only when relevant to a cited boundary and workload question. Label each approach as a hypothesis. Ray and Dask have no evaluated design or runtime result in this package. Keep absent capacity, movement, cost and timing evidence UNKNOWN.

Return concise notes in chat or a separate review document giving each proposed optimization, its original operation/edge/fact or source span, represented constraint, missing proof and next test or owner decision. Preserve the graph's original classifications. Report file-guided use, Codex discovery, typed loading and completed model execution only as individually observed.

Stop on mismatched subjects, digests or broken required references. Declared unresolved dependencies remain reviewable blockers. Keep production selection and operational parallelism BLOCKED. Do not invent schedules, speedups or measurements, run SAS or distributed runtimes, or expand source intake. Native Windows evidence I/O remains BLOCKED. The [downstream pin](../../docs/COMPATIBILITY.md) is read-only.

```text
artifact_authority: DRAFT
semantic_verification: UNVERIFIABLE
semantic_acceptance: BLOCKED
benchmark_execution: NOT_RUN
```
