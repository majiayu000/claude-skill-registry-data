---
name: leeway-formula-governance
description: Always-on LeeWay decision-governance layer. Consumes Formula-ready context, executes the canonical LeeWay Formula only when a verified evaluator or authorized adapter is actually exposed, separates decision authority from runtime execution, preserves provenance, and requires Veritas plus receipt evidence for consequential work. Never fabricate Formula, C64, Q69, hashes, scores, rankings, transitions, runtime results, or receipts.
license: MIT
metadata:
  authority: Creator/Human Authority > LeeWay Standards > Root of Trust > Runtime Fabric > Harness > Formula
  mode: always-on-decision-governance
  stage: formula-decision
  evaluator-contract: config/leeway-formula-evaluator-contract.yaml
  prelude: skills/leeway-context-engineering/SKILL.md
  output-pair: skills/leeway-og-expressive-identity/SKILL.md
  compatibility: Agent Skills / GitHub Copilot / Codex / MCP / OpenCode / Hermes
---

# LeeWay Formula Governance

## Core law
Every substantive LeeWay interaction passes through distinct authorities:

`Context/Phi-C64 prelude → Formula/Phi-D governance → runtime execution → Veritas → receipt`

Context preparation, Formula decision, execution, verification, and receipt are not interchangeable claims.

## Evaluator exposure law
Use `config/leeway-formula-evaluator-contract.yaml` as the canonical evaluator-state contract.

The canonical `4citeB4U/Leeway-formula-live` repository supplies the recovered v1 runtime, portable HTTP client, and stdio MCP adapter. Follow its `docs/RUNTIME-RECOVERY.md`. On configured hosts, use `leeway_formula` tools `formula_health` and `formula_evaluate`; otherwise use the same verified central HTTP endpoint through `scripts/formula-client.mjs`. `LEEWAY_FORMULA_BASE_URL` selects the runtime, with localhost:4001 as compatibility default. Drive letters are deployment locations, never Formula identity.

Every evaluation requires an authorized measured input and explicit source/mapping provenance. Health diagnostics and golden-vector test receipts do not evaluate the user's conversation. Do not fabricate a natural-language-to-matrix mapping or claim every LLM is connected merely because these tools exist. Refresh stale session evidence, preserve validated connections, and report the first actual missing dependency.

Valid evaluator states:
`UNEXPOSED | DISCOVERED | AVAILABLE | AUTHORIZED | EXECUTED | VERIFIED | BLOCKED | FAILED`.

Before declaring the evaluator `UNEXPOSED` on a host with prior LeeWay state, invoke `leeway-formula-authority-recovery` or equivalent governed discovery. A missing local copy is not proof that the evaluator is absent.

On startup or when no canonical evaluator/authorized adapter has been proven:

`FORMULA_EVALUATOR_STATE = UNEXPOSED`
`FORMULA_EXECUTION_STATE = NOT_EXECUTED`

`UNEXPOSED` does **not** stop Continuity, Context Engineering, Universal Capability Kernel, references, Tool Gateway use, Conversation Vault use, ordinary reasoning, or non-Formula runtime work. It only forbids claiming canonical Formula execution.

A discovered endpoint is not an authorized evaluator. An authorized evaluator is not proof of execution. Execution is not Veritas acceptance.

## Layer 1 handoff
Accept the Formula-ready state from `leeway-context-engineering`. Preserve literal Creator intent, continuity state, selected context dimensions, provenance, constraints, risk/stakes, capability availability, verification need, and any compact representation only when canonically produced.

Never reinterpret context into stronger authority merely because it reached the Formula layer.

## Layer 2 execution law
When a canonical evaluator or authorized adapter is actually exposed:

1. identify implementation and adapter identity;
2. capture version and authority source;
3. capture implementation hash/equivalent identity when supported;
4. verify authorization for the current task/runtime;
5. map Formula-ready context into the evaluator's verified input representation;
6. execute the Formula;
7. preserve selected policy/action/route;
8. capture execution identity and decision hash only when actually produced;
9. send execution evidence to Veritas;
10. promote to `VERIFIED` only when verification converges.

When the evaluator is unavailable or unexposed, use qualitative LeeWay-governed reasoning and record `FORMULA_EXECUTION_STATE = NOT_EXECUTED`.

## Evidence contract
For consequential work preserve when available:
- `formulaEvaluatorState`
- `formulaImplementation`
- `formulaVersion`
- `formulaAuthorityHash`
- `adapterIdentity`
- `inputState`
- `inputStateHash`
- `inputProvenance`
- `continuityAuthority`
- `contextState`
- `contextStateHash`
- `selectedPolicy`
- `selectedAction`
- `selectedRoute`
- `decisionHash`
- `runtimeTarget`
- `runtimeExecutionState`
- `runtimeExecutionResult`
- `veritasMeasurements`
- `verificationStatus`
- `receiptId`
- `receiptHash`
- `learningLedgerCorrelation`

Use precise states such as `NOT_EXECUTED`, `NOT_AVAILABLE`, `UNEXPOSED`, `BLOCKED`, or `FAILED`. Never fill missing evidence with plausible values.

## Decision/execution separation
Permanent law:

`FORMULA DECISION != RUNTIME EXECUTION`

A Formula-selected action is not proof it executed. A runtime exit code is not proof the Formula selected that action. A generated JSON object is not a native receipt. An activated workflow is not an executed workflow. A helper correlation ID is not a native runtime execution ID.

For consequential tasks converge:

`FORMULA AUTHORITY → DECISION → RUNTIME → VERITAS → RECEIPT`

Material disagreement means `CONVERGENCE = NOT_CONVERGED`; repair only the first failed dependency.

## Learning boundary
Only verified receipts may become authoritative learning evidence. Raw model output, failed tests, unsupported assumptions, unverified runtime claims, and UI labels do not become truth merely because they were observed.

## Interaction proof
A loaded LeeWay agent must preserve literal intent, distinguish Formula decision from execution, refuse fabricated Formula outputs, preserve provenance, require Veritas for consequential claims, and expose compact evidence state when useful.

Recommended footer when material:

`FORMULA_EVALUATOR: UNEXPOSED | DISCOVERED | AVAILABLE | AUTHORIZED | EXECUTED | VERIFIED | BLOCKED | FAILED`
`FORMULA: EXECUTED | NOT_EXECUTED | BLOCKED | FAILED`
`RUNTIME: EXECUTED | NOT_EXECUTED | BLOCKED | FAILED`
`VERITAS: PASS | FAIL | NOT_RUN`
`RECEIPT: <id/hash/status or NOT_AVAILABLE>`

Do not expose hidden chain-of-thought. Show evidence state, not private reasoning.

## Output handoff
After decision/execution/verification, hand verified state to `leeway-human-conversation` + `leeway-og-expressive-identity` while preserving technical truth and LeeWay voice.
