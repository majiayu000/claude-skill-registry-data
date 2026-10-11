---
name: adaptive-model-router
description: Route harness-eligible Cursor working-agent phases to the smallest proven model and reasoning tier. Use when the user explicitly requests adaptive routing or work needs model or effort selection, dependent multi-agent coordination, multiple material phases, resumption or recurrence, cross-system coordination or judgment, consequential action, or evidence-heavy adjudication. Do not use for low-risk work clearly bounded to the current turn when one agent—or only a small independent read-only fan-out—can complete it without cross-system coordination or judgment.
---

# Adaptive Model Router (Cursor)

Spend reasoning on the phases that need it. This is the Cursor port of the
adaptive routing harness (`github.com/Gladys-Toper/adaptive-codex-harness`).
It shares the Codex reference's T0-T4 tier model and phase-routing heuristic,
but is honestly scoped down to what Cursor's surfaces can actually verify:
**no scored experiments, no promotion pipeline, no scripted headless
dispatcher in pass 1.** See `references/self-improvement-protocol.md` for why.

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
  in this skill and `adaptive-workflow-router` are mandatory. Direct work is
  outside T0-T4 and creates no harness plan, receipt, governance ledger entry,
  or adaptive-routing claim.

## Operating contract

- Route each phase independently; do not label the whole request with one tier.
- Use the smallest tier that clears both the reasoning need and the risk floor.
- Treat `~/.cursor/adaptive-model-router/active-policy.json` as model authority.
  Treat this skill's tier table as role authority.
- Restrict automatic routing to Cursor's own model catalog. Never auto-select
  an Anthropic slug as a default route (`anthropic_default_allowed: false`,
  standing founder rule) — Anthropic models remain in the catalog and are
  available for an explicit user choice, never for adaptive auto-routing.
- Never claim a model changed unless the surface you dispatched through
  actually reports it; see `references/dispatch-contract.md` for exactly what
  each surface honestly proves. Every model-bearing route is
  `REQUESTED_NOT_ATTESTED` in pass 1 — say so, don't imply otherwise.
- Preserve the parent agent as coordinator unless the user requests a
  separate task or thread.
- Scope guard: this governs Cursor's own working agents only, never
  user-facing or product model selection, and never the separate
  `liberai-*-router` skill stack or its state.

## Load the active route

After activation, run `python3 scripts/router_lab.py status` before the first
adaptive model-routing decision. Do not load router state merely to classify
direct work.
Run `python3 scripts/router_lab.py refresh` when the catalog is stale or
absent (first run seeds `~/.cursor/adaptive-model-router/`, backing up any
prior stub instead of clobbering it).

| Tier | Role and effort | Use for | Avoid |
| --- | --- | --- | --- |
| T0 deterministic | No model | Waiting, exact CI/PR status reads, scripted checks, formatter runs | Interpretation, diagnosis, decisions |
| T1 fast operator | `fast_operator`, active policy model, default effort | Read-heavy scans, log filtering, status summaries, mechanical PR creation with supplied inputs | Visual inputs, architecture, ambiguous debugging, sensitive edits |
| T2 standard worker | `standard_worker`, active policy model at `medium` | Contained implementation, ordinary tests, localized debugging, straightforward docs/review | Cross-system ambiguity or high-consequence judgment |
| T3 high solver | `high_solver`, active policy model at `high` | Cross-file diagnosis, nuanced implementation, edge cases, difficult review, auth/release analysis | Passive waiting, repetitive polling |
| T4 ultra planner | `ultra_planner`, active policy model at its deepest seeded effort | Hard architecture, novel multi-system planning, migrations, adversarial/security reasoning, adjudication | Direct mutation, routine coding, known execution steps |

For every grounded cognitive failure, the shared pure T4 contract selects
`t4_consult` only when its retained evidence packet is complete and internally
consistent; its immutable precomputed bundle is offline/read-only,
`tool_mode: none`, one model cycle, zero tool cycles, and strictly token- and
wall-capped. It otherwise selects `t4_diagnose` when evidence is incomplete or
contradictory; that mode is offline with repository-read-only filesystem and
exact repository/path scope, only bounded read-only tools, no mutation tools,
and strict tool-cycle, token, model-cycle, and wall-time caps. An authority
blocker is `ask_user` immediately, never T4. T4 never authorizes or performs
a mutation, deployment, external action, or other state change; its result is
direction only, and an actual mutation must re-enter through a freshly planned
and bound T3-or-lower packet that consumes and revalidates the direction
contract.

## Route the work

1. Decompose the request into discovery, planning, implementation,
   verification, polling, and release phases.
2. Remove phases that need no model. Prefer a deterministic tool or check.
3. Assign the smallest tier that can satisfy the phase; raise it to meet the
   risk floor (auth, secrets, billing, security, destructive data changes,
   schema migrations, production deploys, merge/rollback decisions require at
   least T3; runtime behavior, data shape, public interfaces, dependencies,
   or builds require at least T2).
4. Delegate only bounded work with clear inputs, outputs, and stopping
   conditions.
5. Reassess after evidence: de-escalate when ambiguity resolves, escalate
   after a grounded cognitive failure (never repeat the same failed prompt
   more than once at one tier).

Resolve a machine-readable phase request with:

```text
router_lab.py resolve-phase --request REQUEST.json
cat REQUEST.json | router_lab.py resolve-phase --request -
```

For application workflows, let `adaptive-workflow-router` own phase order,
dependencies, and completion gates; this skill remains the sole authority for
tiers, models, and effort. `workflow_plan.py plan`/`bind` calls
`resolve-phase` for every routed phase automatically.

## Dispatch

See `references/dispatch-contract.md` for the two documented dispatch
surfaces (in-session Task tool; headless `cursor-agent -p --model <slug>`).
There is no scripted dispatcher, terminal receipt store, or pivot CLI in this
skill in pass 1. Planner packets are not runtime enforcement evidence. If the
surface you use cannot honor the resolved model and effort exactly, treat the
phase as inherited-model execution: do not claim adaptive routing occurred.
Unsupported runtime repair, resumption, enforcement, or pivot requests fail
closed rather than being inferred from the planner. This includes T4
consultation/diagnosis: Cursor can resolve and plan the pure contract, but
cannot claim it ran, enforced its no-tools/read-only boundary, or authorized a
mutation without a dispatcher and retained runtime evidence.

## Reoptimize the catalog

Before catalog maintenance, read
[references/self-improvement-protocol.md](references/self-improvement-protocol.md).

```text
router_lab.py refresh              # re-probe cursor-agent models, verify seeded slugs, write policy+catalog
router_lab.py status               # active policy + catalog freshness
router_lab.py doctor               # routing health used to gate resolve-phase
router_lab.py resolve-phase --request REQUEST.json
```

Changing a seeded tier slug is a reviewed edit to `assets/default-policy.json`
followed by `refresh` to confirm it is live — see the protocol doc for why
there is no automated promotion path.

## Report routing briefly

Expose a route manifest only when requested, when cost or latency matters, or
when a tier changes:

```text
phase -> tier / active model / effort: reason; exit condition
```
