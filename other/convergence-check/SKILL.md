---
name: convergence-check
description: Evaluate whether a hypothesis newly entered the current top-k set and update the convergence counter deterministically.
---

# convergence-check

Goal:

- Evaluate whether a hypothesis newly entered the current top-k set and update the convergence counter deterministically.

Inputs:

- `hypothesis_id`
- `previous_top_k_ids`
- `current_top_k_ids`
- current convergence count
- caller-owned `state/EVOLUTION_STATE.json`

Outputs:

- `ConvergenceCheckResult`
- updated convergence count
- when consumed by the evolution loop, updated `state/EVOLUTION_STATE.json`

Context Loading:

- Open `skills/shared-references/schema-index.md`.
- Read `packages/agent_contracts/pipeline_control.py` and confirm the exact `EvolutionStateContract` shape before writing `state/EVOLUTION_STATE.json`.
- Treat the top-k sets as caller-supplied frontier inputs. This skill only evaluates the rule and updates the counter.

Execution Contract:

- This skill is deterministic and must not call an LLM.
- Use `from tools import evaluate_convergence` as the stable invocation surface.
- The exported helper is implemented in `packages/agent_mechanics/convergence_check.py`.
- The helper signature is `evaluate_convergence(hypothesis_id, previous_top_k_ids, current_top_k_ids, current_convergence_count) -> ConvergenceCheckResult`.

Execution Steps:

1. Open `skills/shared-references/schema-index.md`, then read `packages/agent_contracts/pipeline_control.py` before writing `state/EVOLUTION_STATE.json`.
2. Read the candidate `hypothesis_id`, the previous and current top-k sets, and the current convergence count.
3. Call `tools.evaluate_convergence(hypothesis_id, previous_top_k_ids, current_top_k_ids, current_convergence_count)`.
4. Return the `ConvergenceCheckResult` to the caller.
5. When used by the evolution loop, persist the returned `entered_top_k` and `convergenceCount` values into `state/EVOLUTION_STATE.json`.
6. Validate any updated `state/EVOLUTION_STATE.json` artifact before declaring completion.

Artifact Rules:

- The convergence rule is fixed: entering the top-k frontier resets the counter to zero; otherwise the counter increments by one.
- Do not fold additional stopping logic into this skill. Stop decisions belong to evolution state management and completion verification.

Completion Rule:

- This skill is complete only when the deterministic result has been produced and any caller-owned `state/EVOLUTION_STATE.json` update matches that result exactly.
