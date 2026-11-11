---
name: sas-specify
description: Review the draft PRD and module specifications for either approved synthetic SAS workflow. Use to trace requirements to source evidence, find unsupported business claims, and identify questions for an owner. Also use for an explicitly supplied public ML-2/MOD-2 modeling evidence package.
---

## Public ML-2/MOD-2 modeling package

Use this path when the request supplies the public ML-2 source review (EVIDENCE.json, or ML2_EVIDENCE.json in a review bundle) and its matching MOD-2 package. Confirm the manifest and plan refer to the same source and review identity before drawing conclusions. Use only the supplied artifacts. A canonical graph, legacy fixture reports and SAS tie-out are not prerequisites for this path. Report missing or mismatched evidence without filling gaps from another fixture.

1. Trace the response, predictor order, CLASS references, scores and declared ODS targets from the source records. Use PLAN.json for the candidate event, encoding and eligibility rules.
2. Return a modeling PRD with testable acceptance criteria, owner questions and a traceable requirement for each boundary. Record which source and candidate records support the requirements.

Label every material claim **SOURCE_DECLARED**, **CANDIDATE_ENGINEERING**, **INFERRED** or **UNRESOLVED**. Cite its supplied filename and JSON pointer or source location, including original byte ranges when available. Report the review actions actually performed separately from skill discovery, loads or file reads. Keep the result DRAFT, behavioral evidence UNAVAILABLE, semantic verification UNVERIFIABLE, acceptance BLOCKED, reference and benchmark execution NOT_RUN, and historical provenance UNBOUND. Return notes without editing artifacts or executing SAS.

## Original synthetic fixture workflows

Work from one output of [review_workflow.py](../../scripts/review_workflow.py) or the [checked-in example](../../examples/offline-review/README.md). Use the [manifest](../../examples/offline-review/MANIFEST.json) to identify the subject and files. The engine's [generate_preview](../../src/sas_re/_draft_preview.py) already produces the drafts. Make review notes separately.

For a fresh run, read every named document from that output directory. Links below locate the checked-in example.

1. Read [EVIDENCE.md](../../examples/offline-review/EVIDENCE.md), then [PRD.md](../../examples/offline-review/PRD.md) and [MODULES.md](../../examples/offline-review/MODULES.md). Follow each material requirement back to its operation or edge, canonical ID, module owner, fact index where available, and original file/line/byte span. State what a candidate could be tested against.
2. Classify each claim. **OBSERVATION** describes what the supplied graph records. **INFERENCE** interprets a represented relationship and retains the record's original classification. **ASSUMPTION** names something an owner or independent reference must confirm. **HYPOTHESIS** proposes a requirement or design to test. Reserve **MEASUREMENT** for attributable execution evidence.
3. Challenge requirements against the selected facts and input order. In MVP-2, O3 projects `batch, adjusted` and orders only by batch. In the stateful fixture, distinguish RETAIN initialization, FIRST.group reset, accumulation from retained state and LAST.subkey usage. Keep these fixture-specific examples separate from general review rules. Ask the owner about the business purpose, accepted population, duplicate and tie policies, and numerical tolerance. Keep unanswered questions open.
4. Return findings with the disputed wording, classification, cited evidence, and proposed correction or owner question. For architecture review, identify the invariant both alternatives must preserve and the evidence still needed. Report file-guided use, Codex discovery, typed skill loading and completed model execution only as individually observed.

Stop the package review on a mixed subject. For a broken or mismatched citation, stop using the affected claim, report the citation defect and continue only with independently traceable claims. Mark a claimed source behavior without a supporting span or record as unsupported. Use the manifest's actual reconstruction status and evidence availability. Missing behavioral references require proof obligations without invented passing results. An explicitly recorded unresolved dependency such as MVP-2's O4 include is a valid finding. Continue reviewing the represented scope while carrying that dependency as an explicit blocker, with complete semantics UNVERIFIABLE and acceptance BLOCKED. Keep proposed requirements labeled as hypotheses and owner questions open. Do not infer approved business intent, rewrite sealed evidence, run private inputs or send findings [downstream](../../docs/COMPATIBILITY.md). Native Windows evidence I/O remains BLOCKED.

```text
artifact_authority: DRAFT
semantic_verification: UNVERIFIABLE
semantic_acceptance: BLOCKED
benchmark_execution: NOT_RUN
```
