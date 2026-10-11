---
name: adaptive-workflow-router
description: Compose deterministic application workflow graphs and resolve every active cognitive phase through the Cursor adaptive model router. Use when the user explicitly requests the harness or work is materially multi-phase, dependently multi-agent, long-running or resumable, recurring or monitored, needs cross-system coordination or judgment, consequential or high-risk, or evidence-heavy/conflict-bearing. Do not use for low-risk work clearly bounded to the current turn when one agent—or only a small independent read-only fan-out—can complete it without cross-system coordination or judgment.
---

# Adaptive Workflow Router (Cursor)

## Activation boundary

- Keep work direct only when it is low-risk and clearly bounded to the current
  turn, needs no cross-system coordination or judgment, and either one agent
  can finish it or a small fan-out is limited to independent, bounded read-only
  scans or reviews. A short inspection, local edit, focused test, exact status
  read, or mechanical PR creation from prepared inputs can remain direct.
- Activate this harness when the user explicitly requests it or when work is
  materially multi-phase, needs dependent multi-agent coordination, is
  long-running or resumable, is recurring or monitored, needs cross-system
  coordination or judgment, is consequential or high-risk, or depends on
  evidence-heavy/conflict-bearing judgment.
- Risk overrides apparent simplicity. Merge or deploy decisions and actions,
  destructive operations, security or authorization judgments or changes,
  billing changes, and schema or data migrations always activate the harness,
  even when the immediate command is short.
- Once activated, all routing, dispatch, evidence, budget, and authority rules
  are mandatory. Direct work is outside T0-T4 and creates no harness plan,
  receipt, governance ledger entry, or adaptive-routing claim.

Once activated, own phase order, dependencies, artifacts, and completion gates
for multi-phase application work. `adaptive-model-router` remains the sole
authority for tiers, models, effort, and evidence grade — this skill never
declares a model, provider, tier, agent, or effort inside a workflow
definition (enforced by `workflow_plan.py`'s catalog validator).

`scripts/workflow_plan.py` shares the core planner schema: the same
route-request and structured token-cap contracts, runtime-condition and
phase-result names, and dispatch-packet/plan-identity hashing.
`assets/workflows.json` and `assets/resumption-policy.json` are vendored
byte-identical from `core/workflow/`. See
[references/workflow-contract.md](references/workflow-contract.md) for
exactly what is and is not Cursor-specific. Cursor has **no dispatcher, pivot
CLI, retained terminal receipt, or runtime cap-enforcement evidence** in pass
1. `plan` and `bind` only produce and validate immutable planner contracts;
they must never be presented as proof that a phase ran or that its cap was
enforced. Every model-bearing route is `REQUESTED_NOT_ATTESTED`.

## Compose and validate

```text
workflow_plan.py validate                                   # validate the installed catalog
workflow_plan.py list                                        # list installed application workflows
```

## Plan

```text
workflow_plan.py plan \
  --application COMMA_OR_REPEATED_APPLICATION_NAMES \
  --objective "what this plan accomplishes" \
  [--enable-condition NAME]... \
  [--scope|--ambiguity|--mutation|--risk-level|--risk-scope overrides] \
  [--risk-tag TAG]... [--visual-required] [--current-info-required] [--external-action] \
  [--output PLAN.json]
```

Every phase with `execution: route` resolves against the live Cursor router
(`../adaptive-model-router/scripts/router_lab.py resolve-phase`); the plan
fails closed if routing health is not `HEALTHY`. A phase whose resolved route
requires consequential mutation and lacks an ancestor `parent_gate` gets one
inserted automatically — the parent agent must explicitly authorize it.

## Shared T4 consultation boundary

For every grounded cognitive failure, the shared pure planner contract
deterministically distinguishes `t4_consult` from `t4_diagnose`. Complete,
internally consistent retained evidence selects `t4_consult`: an immutable
precomputed evidence bundle, offline/read-only scope, `tool_mode: none`, one
model cycle, zero tool cycles, and strict token and wall caps. Incomplete or
contradictory evidence selects `t4_diagnose`: network disabled,
repository-read-only filesystem, exact repository/path scope, only bounded
read-only tools and no mutation tools, plus strict tool-cycle, token,
model-cycle, and wall-time caps. `authority_required` is not a T4 job:
produce `ask_user` immediately.

T4 never authorizes or performs a repository mutation, deployment, external
action, or other state change. Its result is direction only. Any resulting
mutation must use a freshly planned and bound T3-or-lower packet that consumes
and revalidates the bounded direction contract. Cursor has no dispatcher or
retained runtime enforcement, so it can plan and validate this contract but
must fail closed rather than claim either T4 mode executed or enforced its
tool boundary.

## Bind one phase to exact dispatch inputs

```text
workflow_plan.py bind --plan PLAN.json --phase-key KEY \
  --prompt-file PROMPT.txt [--context-file FILE]... --cwd DIR \
  --sandbox read-only|workspace-write --tool-mode default|none \
  [--mutation-authorized] --wall-time-seconds N \
  [--output PACKET.json]
```

The resulting packet hashes the prompt, context files, structured cap contract,
and runtime contract, and requires a Git-backed source commit
(`require_authoritative_source_commit`) — an unversioned working tree fails
closed. Cursor has no `workflow_dispatch.py`, `pivot-from-receipt`, receipt
validator, or runtime action command. A request for any of those operations is
unsupported and must fail closed; a bound packet is not execution authority.

## Runtime-conditioned phases and plan authority

```text
workflow_plan.py activate-runtime --plan PLAN.json --phase-key KEY \
  --evidence-contract CONTRACT.json --output ACTIVATED.json
workflow_plan.py verify-plan --plan PLAN.json
```

These work exactly as documented for Codex/Claude: pure verification over
retained planner evidence, no dispatch surface involved. They cannot validate
an unretained Cursor execution receipt or repair/pivot a terminal runtime
failure.

## Scope guard

Routes and composes Cursor's own working-agent phases only — never
user-facing or product model selection — and is fully independent of the
`liberai-*-router` skill stack.
