---
name: leeway-bootstrap-authority
description: Root startup authority for LeeWay-governed agents. On the first substantive interaction of a session/runtime, verifies canonical skill authority, establishes a session receipt, records Formula evaluator exposure honestly, discovers authorized Tool Gateway/Conversation Vault capabilities when available, and hands verified state into Continuity, Context, Formula, and the Universal Capability Kernel.
license: MIT
metadata:
  authority: Creator/Human Authority > LeeWay Standards
  mode: always-on-bootstrap
  stage: pre-continuity
  repository: 4citeB4U/LeeWay-Agent-Skills
  formula-evaluator-contract: config/leeway-formula-evaluator-contract.yaml
  compatibility: Agent Skills / GitHub Copilot / Codex / MCP / OpenCode / Hermes
---

# LeeWay Bootstrap Authority

## Root law
A new chat is a new window, not a new identity.

Before substantive LeeWay work, establish whether the current runtime has valid live LeeWay skill authority. Do not confuse remembered knowledge about LeeWay with a verified read of the current canonical package.

Canonical authority: `4citeB4U/LeeWay-Agent-Skills`.

## Startup contract
On first substantive interaction:

1. Check for a current `LEEWAY_SKILL_SESSION_RECEIPT`.
2. If absent/invalid, retrieve or verify the canonical package when authorized host access exists.
3. Verify `AGENTS.md` and the always-on core named there.
4. Preserve repository identity, ref/commit/hash evidence when available, verification time, and core-skill availability.
5. Establish Formula evaluator state from `config/leeway-formula-evaluator-contract.yaml`.
6. If no evaluator or authorized adapter is proven, set:
   - `FORMULA_EVALUATOR_STATE = UNEXPOSED`
   - `FORMULA_EXECUTION_STATE = NOT_EXECUTED`
7. Discover authorized Tool Gateway and Conversation Vault capabilities when the runtime exposes them.
8. Hand verified state to Continuity Authority.
9. Continue through Message Ingress, Context Engineering, Formula Governance, Universal Capability Kernel, and focal task execution.

## Session receipt
Preserve when available:
- `repository`
- `authorityRef`
- `authorityCommit`
- `rootContractHash`
- `coreSkills`
- `verifiedAt`
- `runtimeIdentity`
- `continuityState`
- `formulaEvaluatorState`
- `formulaAuthorityState`
- `formulaExecutionState`
- `capabilityKernelState`
- `toolGatewayState`
- `conversationVaultState`
- `status`: READY/PARTIAL/BLOCKED

Never fabricate missing commits, hashes, timestamps, runtime IDs, evaluator identities, authorization states, or availability states.

## Evaluator boundary
`FORMULA_EVALUATOR_STATE = UNEXPOSED` is a valid bootstrap result.

It means the Formula governance law is loaded but the actual canonical evaluator/authorized adapter has not been proven in this runtime. Continue governed work, but do not claim Formula execution.

## Host boundary
This repository governs only a runtime that actually loads or can access the LeeWay contract. A `SKILL.md` cannot force an unrelated host to execute before the host reads it.

If live skill authority is required but unavailable: `LEEWAY_SKILL_AUTHORITY = BLOCKED`.

If Formula evaluator access is unavailable: preserve `UNEXPOSED` or `BLOCKED` as appropriate; do not fabricate execution.

## Handoff
`Bootstrap → Continuity → Message Ingress → Context/Phi-C64 → Formula/Phi-D → Universal Capability Kernel → Tool Gateway when available → task capability weave → focal execution → Veritas → receipt → Conversation Vault when available → LeeWay delivery`

Bootstrap proves the governing package is present. It does not prove the Formula executed, a task runtime executed, or Veritas passed.
