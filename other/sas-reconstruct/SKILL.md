---
name: sas-reconstruct
description: Reconstruct or trace either approved public synthetic SAS workflow with the existing offline Python engine. Use for source identity, module ownership, data flow, dependency edges, and unresolved evidence. Also use for an explicitly supplied public ML-2/MOD-2 modeling evidence package.
---

## Public ML-2/MOD-2 modeling package

Use this path when the request supplies the public ML-2 source review (EVIDENCE.json, or ML2_EVIDENCE.json in a review bundle) and its matching MOD-2 package. Confirm the manifest and plan refer to the same source and review identity before drawing conclusions. Use only the supplied artifacts. A canonical graph, legacy fixture reports and SAS tie-out are not prerequisites for this path. Report missing or mismatched evidence without filling gaps from another fixture.

1. Resolve the MODEL input, output and score columns in the evidence. Cite their original spans and identify the prepared dataset as the declared input. Keep the sorted CSV separate if described in the guide. Treat pre-sort row-end eligibility in PLAN.json as candidate engineering.
2. Return a short dependency and uncertainty review. Record the evidence pointers and byte anchors you resolved. Mark historical dataset continuity, execution order and step-check effects unresolved.

Label every material claim **SOURCE_DECLARED**, **CANDIDATE_ENGINEERING**, **INFERRED** or **UNRESOLVED**. Cite its supplied filename and JSON pointer or source location, including original byte ranges when available. Report the review actions actually performed separately from skill discovery, loads or file reads. Keep the result DRAFT, behavioral evidence UNAVAILABLE, semantic verification UNVERIFIABLE, acceptance BLOCKED, reference and benchmark execution NOT_RUN, and historical provenance UNBOUND. Return notes without editing artifacts or executing SAS.

## Original synthetic fixture workflows

Inspect an existing manifest-bound package for `mvp2` or `by-retain-and-sum`, including the [checked-in example](../../examples/offline-review/README.md), or generate a fresh package when requested. For fresh reconstruction, run from this checkout with the prepared Python 3.12 environment active on a supported POSIX development host. Choose an unused destination and preserve any existing directory.

```bash
python3.12 -IB scripts/review_workflow.py --destination /tmp/sas-re-review-sk1
```

For explicit fixture selection, supply `--fixture mvp2` or `--fixture by-retain-and-sum` to the same entry script. The command without that option preserves the legacy MVP-2 package.

The [entry script](../../scripts/review_workflow.py) owns the inputs. P1 inventories original bytes and hashes. P2A reconstructs one canonical v2 graph and checks its source consistency. MVP-2 exercises SORT, current-row DATA/SET, SQL and an unresolved include. The stateful fixture exercises RETAIN, FIRST.group reset, retained accumulation and LAST.subkey under declared input ordering. Use the [P2A subset](../../docs/P2A_DESIGN.md#closed-source-profile) to distinguish supported forms from unknown effects. P3-A1's [diagnostics](../../src/sas_re/_dependency_diagnostics.py) check the supplied graph and identify represented paths, cycles, conflicts and missing proof. Leave parsing, hashing and diagnostics to Python.

1. Open the chosen package's README and [MANIFEST.json](../../examples/offline-review/MANIFEST.json). Check the selected fixture, subject, graph binding, payload names and digests against the command's approved fixture declarations. Read the actual reconstruction status and behavioral evidence availability. Legacy MVP-2 lists its behavioral reports in the manifest files map. Require a successful command receipt and compare its manifest digest only when a fresh command was actually run. Existing-package inspection needs the package's manifest and payload checks. Identify which package you inspected and whether you generated it in this task. Read all named documents from that package. Links here locate the checked-in example.
2. Trace the requested boundary in [EVIDENCE.md](../../examples/offline-review/EVIDENCE.md). For MVP-2, E4 DATA and E2 ORDER connect prepare to enrich. For the stateful package, trace the actual retained-state, reset and value-lineage facts. Local O/E labels belong to the selected graph. Preserve the canonical IDs behind those local labels, the fact index, source file, line numbers and half-open byte span. A missing path leaves independence unproved.
3. Return a short trace with the subject, producing and consuming modules, cited transformations, unresolved effects and the stage gate. Hand the evidence references to requirements review without editing the generated files. Report file-guided use, Codex discovery, typed skill loading and completed model execution only as individually observed.

Stop on a refused command, mismatched digest or missing required package evidence. In MVP-2, O4 records unresolved `postcheck.sas`, making reconstruction PARTIAL. The stateful package can record COMPLETE reconstruction within the supported profile while behavioral evidence is UNAVAILABLE. Keep full-workflow semantic acceptance BLOCKED in both cases. Keep unsupported syntax unresolved. Never search for an include, accept private paths or execute SAS to fill a gap. Native Windows evidence I/O remains BLOCKED. The [downstream pin](../../docs/COMPATIBILITY.md) is read-only.

```text
artifact_authority: DRAFT
semantic_verification: UNVERIFIABLE
semantic_acceptance: BLOCKED
benchmark_execution: NOT_RUN
```
