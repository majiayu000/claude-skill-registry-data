---
name: omp-moe-dispatch
description: Route substantial YURI/MURE work through the OMP TaskTool using allowlisted `compileOmpSpawn` payloads and explicit configured agent IDs with model overrides. Use for multi-step work, parallel research, implementation, architecture, verification, adjudication, or any request where Sol should orchestrate OMP-native workers. Never substitute CLI `task` subprocesses, Codex `spawn_agent`, or a runtime-bypass adapter for this workflow.
---

# OMP MoE Dispatch

Use Sol/Yuri as the parent control plane. Delegate worker leaves through the OMP `task` tool, dispatching the exact `compileOmpSpawn(...)` arguments produced by `_SYSTEM/mure/sol-moe-native-dispatch.mjs`.

## Build the route

1. Preserve the user's goal spine in the parent session.
2. Decompose substantial work into independent subtasks. `compileOmpSpawn` compiles exactly one manifest entry and always emits exactly one `tasks[0]`; every dispatched unit therefore uses a separate TaskTool call, even when consecutive units use the same agent. Independent calls may run concurrently under the parent.
3. Build the governed manifest with `_SYSTEM/mure/sol-moe-company.mjs` and `_SYSTEM/config/sol-moe-routing-policy.json`.
4. Compile each ready manifest entry with `compileOmpSpawn(entry, context)` from `_SYSTEM/mure/sol-moe-native-dispatch.mjs`. The compiled action has no top-level `agent`; the dispatched card lives at `tasks[0].agent` and `tasks[]` contains exactly one dispatched unit. Execute only the returned whitelist-only payload — never hand-write TaskTool arguments.
5. Apply runtime availability masks before spawning. Treat a provider quota/timeout/auth failure as unavailable for the current run.
6. Keep hard policy above learned ranking:
   - R0 may use cheap semantic producers.
   - R1 uses a frontier producer by default.
   - R2 requires an independent frontier verifier.
   - R3 requires Opus 4.8 verification and never uses Opus as its own producer.

## Spawn native children via OMP TaskTool

For every immediate producer or selected evidence entry the reducer emits a `compileOmpSpawn` payload of the exact shape `_SYSTEM/mure/sol-moe-native-dispatch.mjs` produces — currently:

```js
{
  i: `MURE ${purpose} ${taskId}`,           // human-readable intent header
  context: '# Goal\nExecute one MURE <purpose> task.\n# Constraints\n...', // OMP context block
  tasks: [                                 // exactly one dispatched unit
    {
      task: '<built task prompt>',         // full task prompt (string)
      name: '<deterministicOmpTaskId>',    // CamelCase ≤32 chars, emitted as OMP task id
      agent: '<manifest agentId>',         // card id; TaskTool binds this card
    },
  ],
}
```

The compiled action has NO top-level `agent` (the focused test at `_SYSTEM/mure/sol-moe-native-dispatch.test.mjs` asserts the absence). The dispatched card lives at `tasks[0].agent`. Every `compileOmpSpawn` payload contains one task and produces one TaskTool call. Separate calls are required for all additional units, whether they target the same or different named agents; the parent may still dispatch independent calls concurrently. Never hand-write TaskTool arguments: the legacy shape `{id, assignment, description, role}` is not what `compileOmpSpawn` emits and is rejected by the focused test.

Track the `{jobId, agent}` receipt returned by the OMP `task` tool. Job/transcript correlation is always by `jobId` plus task/agent/model evidence (`tasks[0].name`, `tasks[0].agent`, transcript `model_change.model`), never by guessed status.

Nested orchestration is bounded by `.omp/config.yml` `task.maxRecursionDepth: 2`. At depth 2, workers are leaves and must not spawn further children; OMP has no `maxChildrenPerAgent` setting in this contract.

Before native admission, replace `shadow` with `mirrorOmpSpawnAction(shadow, action)`, then call `admitOmpSpawn(state, shadow, action, rawReceipt)` from `_SYSTEM/mure/sol-moe-parent-adapter.mjs` with the reducer's `omp-task-spawn` action and the OMP receipt. `admitOmpSpawn` calls `recordNativeSpawnAccepted` (reducer) and `observeNativeAdmission` (shadow) in lockstep — there is no path where one is admitted and the other is not. The reducer fails the task loud (`MODEL_MISMATCH`) if the resolved model from the transcript `model_change` line does not match the requested model; admission itself only records the requested model. Feed only pushed `<task-result>` blocks (plus the path-confined JSONL transcript under `artifactsDir/<jobId>.jsonl`) into `applyOmpCompletion` (or `applyOmpCompletionFromDisk`). The parent OMP session owns execution and I/O — no subprocesses, no Codex `spawn_agent`, no runtime-bypass adapters.

Do not use:

Use case 1 — the OMP CLI / subprocess runtime pretending to be the TaskTool path is forbidden. Use case 2 — Codex `spawn_agent` is forbidden for MURE model/role dispatch. Use case 3 — a model override without an `agent` whose card id appears in `WORKER_BINDINGS` (`_SYSTEM/mure/sol-moe-native-dispatch.mjs`) is forbidden. Use case 4 — hand-written TaskTool arguments when a `compileOmpSpawn` payload is available are forbidden. Use case 5 — any selector that matches `FORBIDDEN_SELECTOR_PREFIXES` (`_SYSTEM/mure/omp-model-resolver.mjs`: `openai/`, `minimax-portal/`, `cline-pass/`, `cursor-cli/`, `ollama/`) is forbidden and must never be emitted; `resolveOmpModel` rejects them in the Step 4 forbidden-prefix gate (after the Step 2 registry gate at lines 602–656 and after Step 3 selector normalization). Use case 6 — any registry route whose status is not `canary-proven` (or the narrow `catalog-candidate` + `canary-bootstrap` exception) is forbidden; `blocked-schema`, `quota-blocked`, `unresolved`, `owner-excluded`, and any future unknown status all fail closed at the Step 2 registry gate before the forbidden-prefix gate runs. Use case 7 — legacy surfaces are forbidden: Fable (registry card `fable-synth-bootstrap` is marked `owner-excluded` on 2026-07-17 and must never be admitted as a worker; its registry row is retained only as historical provenance), OpenClaw, `context-router`, and `yuri-control-plane` (no longer present in `provider-route-registry.json`); any reference in user input must be rejected rather than silently routed. Use case 8 — the Cline provider (`cline-pass/*`) is forbidden; it is categorically unavailable in OMP (`FAIL_CLASSES.CLINE_UNAVAILABLE`) with no fallback or substitute. Use case 9 — local Ollama producer bindings are forbidden; they fail closed via the `ollama/` `FORBIDDEN_SELECTOR_PREFIXES` gate, and only `ollama-cloud/*` routes are eligible when canary-proven in the registry.

## Model roles

| Work | Native child |
|---|---|
| Parent orchestration and final synthesis | Parent seat is registry-resolved (`provider-route-registry.json:roleTopology.orchestrator`: owner `sol`, `allowedModels: ["openai/gpt-5.6-sol"]`, `mayExecuteWorkerTasks: false`, `maySpawn: true`). The `mure-yuri` card family is parent-only and never compiled as a worker; the `mure-yuri-sol` variant sits at `disabled/mure-route-unavailable` and is excluded from worker inheritance. The earlier `mure-yuri · anthropic/claude-opus-4-8` row is a card-only entry for the parent front-end persona and is not the runtime orchestrator selector — runtime Opus rebind is out of scope without direct owner authorization. |
| Delegated orchestration and frontier-volume production | `mure-synthesist-m3` · `minimax-code/MiniMax-M3` · thinking `adaptive` (registry canary-proven; bootstrap variants tombstoned). The legacy alias `minimax-portal/MiniMax-M3` must never be emitted in user/lane code or in newly written manifests — `normalizeSelector` at `_SYSTEM/mure/omp-model-resolver.mjs:378-386` translates it to the canonical `minimax-code/MiniMax-M3`, and the forbidden-prefix gate at line 661 tests the normalized selector, so the legacy alias is accepted only through canonical normalization rather than fail-closed; the canonical selector remains `minimax-code/MiniMax-M3`. |
| Implementation and refactor | deterministic 85% `mure-synthesist-m3` · `minimax-code/MiniMax-M3`; 15% specialist sample / escalation `mure-engineer` · `openai/gpt-5.6-terra` — currently `quota-blocked` in the registry; route fails closed in `resolveOmpModel` (`FAIL_CLASSES.REGISTRY_BLOCKED`) until a fresh live canary lifts the block |
| Adjudication and red-team | deterministic 65% `mure-synthesist-m3` · `minimax-code/MiniMax-M3`; 35% cross-provider specialist `mure-adjudicator-luna` · `openai-codex/gpt-5.6-luna` (note: the legacy `mure-adjudicator` card bound to `openai/gpt-5.6-luna` is a different route; the `mure-adjudicator-luna` card is reserved for the `openai-codex/gpt-5.6-luna` source selector) |
| Deterministic R2 gate | `mure-calibrator-sonnet5` · `anthropic/claude-sonnet-5` |
| Security/governance R3 gate | `mure-sentinel` · `anthropic/claude-opus-4-8` (R3 requires Opus 4.8 verification; Opus never acts as its own producer) |
| Mechanical breadth | Four distinct values to keep separate: source input key `deepseek-v4-flash:direct` (no provider prefix); normalized OMP selector `deepseek/deepseek-v4-flash`; canary-evidence registry card `deepseek-flash-bootstrap` on the proven route `ollama-cloud/deepseek-v4-flash` (evidence-only, never a producer/verifier/fallback/escalation); executable card `deepseek-flash` per `WORKER_BINDINGS` for the `deepseek-v4-flash:direct` source key. The direct `deepseek/deepseek-v4-flash` route is `catalog-candidate` and not yet executable; the bootstrap identity is the evidence carrier, not the executable card — call this a documented evidence-ID drift between the canary registry row and the executable binding. |
| Cheap overflow/evidence | `mure-artificer` · `opencode-go/mimo-v2.5`, only after a completed OMP canary; mimo family is in `CHEAP_PROVIDER_FAMILIES` so it may only run R0 evidence, never R1+ semantic work |
| Long-context architecture | `mure-architect` · `zai/glm-5.2` (compile binding `WORKER_BINDINGS["zai/glm-5.2"] = "mure-architect"`; the canary-evidence identity `mure-architect-glm52` in the registry is a documented evidence-ID drift — the executable card stays `mure-architect` until WORKER_BINDINGS is updated; selector remains in `AVAILABILITY_MASKED_MODELS` until a fresh OMP child completes) |

Worker allocation excludes the Sol parent seat and is measured first by accepted OMP TaskTool dispatch count; token share is observed separately. While GLM (`zai/glm-5.2`) is runtime-masked in the compiler (`AVAILABILITY_MASKED_MODELS` in `_SYSTEM/mure/sol-moe-native-dispatch.mjs`), target a 50-task rolling mix of 40–60% MiniMax, 20–35% Anthropic (including verification), 12–25% DeepSeek, and no more than 12% OpenAI workers. MiMo (`opencode-go/mimo-v2.5`) is `canary-proven` in the registry and is NOT in `AVAILABILITY_MASKED_MODELS`; the `availabilityDefaults.opencode-go/mimo-v2.5: true` value in `_SYSTEM/config/sol-moe-routing-policy.json` is a planning-layer note that `_SYSTEM/mure/sol-moe-native-dispatch.mjs` does not read as an enforcement gate — `sol-moe-native-dispatch.mjs` does not import or consult that config file, so it is policy guidance, not a dispatch gate. The compiler's `plan.availabilityEvidence` gate at `_SYSTEM/mure/sol-moe-native-dispatch.mjs:524-527` fires only for models in `AVAILABILITY_MASKED_MODELS` (GLM only), so it is NOT a MiMo availability requirement — MiMo's availability gate is the resolver's `canary-proven` status (already satisfied). MiMo's admission is NOT generally eligible: the compiler also enforces other gates — `WORKER_BINDINGS` membership and entry validation, `CHEAP_PROVIDER_FAMILIES` semantics (`workerSafetyViolation` at `_SYSTEM/mure/sol-moe-native-dispatch.mjs:529-535`) which forbid verifier purpose (`CHEAP_VERIFIER_FORBIDDEN`) and forbid non-evidence R1+ work for any purpose (`CHEAP_SEMANTIC_WORK_FORBIDDEN`: producer, availability-fallback, and quality-escalation are all blocked at risk ≥ R1, while evidence-purpose bypasses the risk check and is separately policy-governed), plus R3 Anthropic reservation and `R3_OPUS_VERIFIER_REQUIRED`, and the provider-calibration ceiling — so MiMo is compiler-eligible for R0 non-verifier work (R0 producer, R0 availability-fallback, R0 quality-escalation, and evidence-purpose are all permitted; verifier purpose is forbidden). OpenAI worker models are selective specialists and quality escalations, not the volume default. When GLM recovers (live OMP canary), shift 10–20% to Z.ai without weakening the R2/R3 floors. MiMo widening is constrained by the cheap-family semantics above: R0 non-verifier work passes the compiler predicate; only the policy and routing-policy layer may further restrict it, and they are advisory for the compiler.

The native reducer records every accepted child admission, including evidence, producer, availability fallback, quality escalation, and verifier attempts. Feed its prior `providerCalibration.history` into the next `createNativeDispatchState(..., { providerHistory })` call to preserve the rolling window. When a selected OpenAI worker would exceed the 12% ceiling, the reducer emits an eligible non-OpenAI peer with route kind `calibration-rebalance`; if none remains, it fails loud (`PROVIDER_CALIBRATION_CEILING`). Sol itself is never a worker candidate (`SOL_PARENT_WORKER_FORBIDDEN`).

## Process completions

1. Treat child output as advisory until verified.
2. On transport, quota, timeout, or auth failure, spawn only the task's next availability fallback.
3. On producer success for R2/R3, the reducer itself spawns the declared verifier after the producer finishes. The verifier contract is strict: return exactly `{"verdict":"pass"}` or `{"verdict":"reject"}`, no markdown or prose.
4. On verifier rejection, the reducer spawns only the quality-escalation candidate, then re-runs the verifier.
5. On verifier transport/auth/timeout failure, fail loud (`VERIFIER_EXECUTION_FAILURE`); changing the producer cannot repair a dead verifier.
6. Fail loud when compliant candidates are exhausted. Never drop to a cheap semantic worker (`PRODUCER_MISSING` / `AVAILABILITY_FALLBACK_EXHAUSTED` / `QUALITY_ESCALATION_EXHAUSTED`).
7. Keep final acceptance, owner gates, and user-facing synthesis in the Sol parent.

## Current availability override

When Marcel or a live failure establishes that GLM 5.2 is unavailable, mask `zai/glm-5.2` for the run and begin its declared fallback chain at MiniMax M3. Do not probe GLM repeatedly. Remove the mask only after a successful bounded OMP canary or explicit availability evidence.

Apply the same fail-closed rule to any child provider whose profile was just seeded but is not visible to the running runtime. Keep it masked until a fresh OMP child completes; admission alone is not sufficient.

A boolean availability override cannot unmask a default-masked model. Supply proof sourced from the OMP transcript for that exact model with `source: 'omp-task-result'`, `status: 'completed-omp-canary'`, `ok: true`, an exact `model_change.model`, plus its `jobId`; otherwise the router keeps it unavailable (`MODEL_AVAILABILITY_UNPROVEN`).

## Evidence contract

Record for each child: task ID, role, agent ID, requested model, resolved model (`model_change.model` from transcript), `jobId`, route kind, result status, verifier verdict, and whether fallback or escalation was used. Admission (`recordNativeSpawnAccepted` succeeded) is not execution proof; require a `<task-result>` completion event from the resolved child model and a transcript whose `model_change.model` matches the requested entry.
