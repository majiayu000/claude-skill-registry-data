---
name: run-policy-router
description: Interpret the user's high-level research intent into `RUN_POLICY.yaml` and `state/POLICY_DECISION.json`.
---

# run-policy-router

Goal:

- Interpret the user's high-level research intent into `RUN_POLICY.yaml` and `state/POLICY_DECISION.json`.

Inputs:

- one run directory root
- run-local `input.md`
- optional `RUN_POLICY.yaml`
- research brief and operator constraints

Outputs:

- updated `RUN_POLICY.yaml`
- updated `state/POLICY_DECISION.json`

Context Loading:

- Open `skills/shared-references/schema-index.md`.
- Read `packages/agent_contracts/policy.py` and confirm the exact `RunPolicyContract` plus `PolicyDecisionContract` shapes before writing `RUN_POLICY.yaml` or `state/POLICY_DECISION.json`.
- Read `input.md` plus any operator constraints that should influence the high-level routing axes.

Execution Contract:

- The router must stay at the high-level policy layer and must not invent raw numeric mechanics values directly.
- Allowed routing axes are documented in `../shared-references/policy-contract.md`.
- Downstream numeric settings are resolved separately into `state/RESOLVED_RUN_CONFIG.json`.
- This skill owns canonical policy artifact emission only:
  - `RUN_POLICY.yaml`
  - `state/POLICY_DECISION.json`
- This skill does not own numeric mechanics resolution, direct strategy routing, or downstream evolution-state writes.

Execution Steps:

1. Open `skills/shared-references/schema-index.md`, then read `packages/agent_contracts/policy.py` before writing `RUN_POLICY.yaml` or `state/POLICY_DECISION.json`.
2. Interpret the research brief into the allowed policy axes only.
3. Write canonical `RUN_POLICY.yaml` and `state/POLICY_DECISION.json`.
4. Do not invent raw numeric mechanics values that belong in `state/RESOLVED_RUN_CONFIG.json`.
5. Validate the emitted policy artifacts.

Completion Rule:

- This skill is complete only when `RUN_POLICY.yaml` and `state/POLICY_DECISION.json` have been written in canonical form and remain consistent with the selected high-level policy axes.
