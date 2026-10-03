---
name: human-intent-audit
description: Enforce traceability from natural-language intent to machine predicates, final observables, evidence, and owner-readable acceptance. Use when conducting any audit, review, QA pass, parity or compliance check, security assessment, code or architecture review, visual or behavioral comparison, data validation, system verification, completion gate, or claim that an implementation satisfies a human request.
---

# Human Intent Audit

## Role

Own the translation from human goals to machine-verifiable evidence. Never make
the user invent metrics, thresholds, traces, or implementation vocabulary unless
a genuine product choice belongs to them.

`[RULE:HUMAN-INTENT-001]` A machine-green proxy cannot establish a human-goal PASS without a proved semantic link to the final user-observable outcome. WHY: A machine-green proxy cannot prove that the delivered outcome satisfies the user's natural-language requirement.

## Input Contract

Collect the user's natural-language requirements, authoritative references,
available artifacts, execution context, and any explicit non-goals. Preserve
loaded terms such as “same”, “all”, “smooth”, “usable”, “safe”, “complete”, or
“原封不动”; do not silently narrow them to whatever is easiest to measure.

## Workflow

1. Record each material human requirement and the interpreted intent.
2. Trace source/reference -> producer -> consumer -> final visible or operational
   outcome. Mark every missing edge.
3. Select final observables. Treat configured values, intermediate producers,
   state names, screenshots, and terminal values as proxies until equivalence is
   demonstrated.
4. Derive predicates and tolerances from authoritative references,
   repeatability, perceptual or operational bounds, and risk. Never choose a
   tolerance merely because current output passes it.
5. Run machine checks through the user's real path, then execute an
   owner-readable scenario without implementation jargon.
6. Run a negative fixture reproducing the prior false-positive pattern.
7. Audit both implementation-vs-predicate and predicate-vs-human-intent.

Perform the scenario before asking the owner to test. The owner is final
authority, not the first QA worker or detector author.

## Output Contract

For every requirement, record:

- `human_requirement` and `interpreted_intent`;
- `final_observables` and `machine_predicates`;
- `threshold_basis`;
- `proxy_risks` and unresolved semantic gaps;
- machine `evidence`;
- `owner_acceptance_scenario`;
- status: `pass`, `partial`, `open`, `blocked`, or `fail`.

Return top-level `pass` only when all material requirements pass both audits.
Otherwise name the exact semantic or evidence gap.

## Enforcement Hooks

For durable JSON, use schema `human-intent-audit.v1` and run:

```powershell
python scripts/validate_intent_traceability.py <record.json> --json
```

The script checks traceability structure and rejects a top-level pass when a
requirement or semantic review remains open. Keep domain-specific detectors;
this gate supplements rather than replaces them.

## Positive Example

User intent: “导出的 CSV 不能少任何一行，也不能改字段值。” Compare decoded
input/output row counts and canonical row multisets with exact equality, execute
a fresh export/open scenario, and record both machine and owner-readable proof.

## Negative Example

User intent: “操作手感要和参考程序一样。” A configured speed equals one captured
request value, but final animation, collision, Transform, and camera behavior
remain unmeasured. Reject PASS even though the configuration detector is green.

## Final Check

Before any audit or completion claim, confirm all of the following:

1. Every material human requirement appears in the intent ledger.
2. Each predicate measures a final outcome or has a proved proxy equivalence.
3. Thresholds have an independent basis.
4. Evidence uses the real user path.
5. Positive and negative fixtures behave as expected.
6. The agent executed the owner-readable scenario.
7. No machine-green result is summarized beyond its proved semantic scope.
