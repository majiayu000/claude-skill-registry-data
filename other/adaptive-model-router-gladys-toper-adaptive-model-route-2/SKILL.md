---
name: adaptive-model-router
description: Route harness-eligible Claude Code work to the smallest proven model and reasoning effort for each phase, with measured promotion and exact rollback. Use when the user explicitly requests adaptive routing or work needs model or effort selection, dependent multi-agent coordination, multiple material phases, resumption or recurrence, cross-system coordination or judgment, consequential action, or evidence-heavy adjudication. Do not use for low-risk work clearly bounded to the current turn when one agent—or only a small independent read-only fan-out—can complete it without cross-system coordination or judgment.
---

# Adaptive Model Router

Spend reasoning on the phases that need it. Keep model selection adaptive, evidence-backed, and reversible.

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
- Treat `~/.claude/adaptive-model-router/active-policy.json` (under `$CLAUDE_CONFIG_DIR` when set) as model authority. Treat this skill's tier descriptions as role authority.
- Preserve the parent agent as coordinator unless the user requests a separate task or thread.
- Never claim that a model changed unless runtime metadata proves the selected model and effort.
- Restrict automatic routing to locally available Claude models in this harness; never substitute another provider.
- Scope guard: this policy governs routing of Claude Code's own working agents only. Model selection for products, experiments, teacher or judge roles, or anything user-facing stays with the user and the `model-recommender` skill, and an explicit user model choice always overrides the adaptive policy.

## Load the active route

After activation, load the route once per session, not once per decision: run `python3 scripts/router_lab.py status` at the first adaptive routing decision, then reuse its assignments until a route fails, the policy changes, or the session is told otherwise. Do not load router state merely to classify direct work. Fast path: for one or two dispatches, route directly from the table below; invoke the scripts only for multi-phase work, machine-readable phase requests, or after a routing failure. Run `python3 scripts/router_lab.py refresh --stage-new` only when the catalog baseline is absent or `assets/claude-catalog.json` was edited.

Use the four active assignments returned by the lab:

| Tier | Role and effort | Use for | Avoid |
| --- | --- | --- | --- |
| T0 deterministic | No model | Waiting, exact CI or PR status reads, scripted checks, formatter execution, file existence checks | Interpretation, diagnosis, or decisions |
| T1 fast operator | `fast-operator`, active policy model at `low` (baseline `haiku`) | Read-heavy scans, log filtering, status summaries, exact commands, mechanical PR creation with supplied inputs | Visual inputs, architecture, ambiguous debugging, sensitive edits, merge or deploy decisions |
| T2 standard worker | `standard-worker`, active policy model at `medium` (baseline `sonnet`) | Contained implementation, ordinary tests, localized debugging, straightforward documentation and review | Cross-system ambiguity or high-consequence judgment |
| T3 high solver | `high-solver`, active policy model at `high` (baseline `opus`) | Cross-file diagnosis, nuanced implementation, edge cases, difficult review, conflicting evidence, auth or release analysis | Passive waiting and repetitive polling |
| T4 ultra planner | `ultra-planner`, active policy model at its qualified deepest effort (baseline `fable` at `max`) | Hard architecture, novel multi-system planning, migrations, adversarial or security reasoning, adjudication | Routine coding, known execution steps, status checks, idle waiting |

Require exact `max` support for a new T4 challenger. A model without image input may serve T1 only when the phase has no image or visual-inspection requirement; keep it out of T2-T4. All currently cataloged Claude models accept image input, so this floor is presently inactive; retain it for future catalog entries.

T4 is the per-agent equivalent of the session effort slider's Ultracode position: `max` is the deepest effort expressible in agent frontmatter and Workflow calls. Ultracode itself is a session posture (deepest effort plus a standing multi-agent orchestration opt-in), not a routable effort value. T4 is direction-only: it is read-only and cannot carry a patch, mutation grant, deployment instruction, or external-action authorization. A grounded cognitive failure deterministically selects `t4_consult` when its retained evidence is complete and internally consistent, or `t4_diagnose` when that evidence is incomplete or contradictory. `authority_required` selects `ask_user`; it never dispatches T4. Any resulting write must use a freshly planned and bound T3-or-lower packet that consumes and revalidates the bounded T4 direction contract. Under Ultracode, this policy is what keeps exhaustive from meaning extravagant: scale coverage with more T1 and T2 workers, not top-tier models on mechanical work.

## Route the work

1. Decompose the request into discovery, planning, implementation, verification, polling, and release phases.
2. Remove phases that need no model. Prefer a deterministic tool, script, wait primitive, or automation.
3. Assign the smallest tier that can satisfy the phase.
4. Raise the tier to meet the risk floor.
5. Delegate only bounded work with clear inputs, outputs, and stopping conditions. Pass minimum useful context.
6. Reassess after evidence. De-escalate when ambiguity resolves; escalate after a grounded cognitive failure.

Dispatch routed phases on Claude Code surfaces:

- T1-T4 via the Agent tool with `subagent_type` set to `fast-operator`, `standard-worker`, `high-solver`, or `ultra-planner` once profiles are installed. The profile carries both model and effort; the Agent tool itself exposes a `model` parameter but no effort parameter, so prefer the installed profile for effort-exact routing.
- T1-T4 via the Workflow tool with `agent(prompt, {model, effort})` or `{agentType: "<profile>"}`, bound from `resolve-phase` output.
- T0 via deterministic Bash, scripts, Monitor, or background-task notifications — never a reasoning model idle-waiting or poll-looping. Prefer event-driven reads over watch loops.

For application workflows, let `adaptive-workflow-router` own phase order, dependencies, artifacts, and completion gates. Keep this skill as the sole authority for tiers, models, effort, escalation, promotion, and rollback. Resolve a machine-readable phase request with:

```text
router_lab.py resolve-phase --request REQUEST.json
cat REQUEST.json | router_lab.py resolve-phase --request -
```

The response binds the route to the active policy and profile hash. `REQUESTED_PENDING_RUNTIME_METADATA` means the route is selected but the actual runtime model still requires retained dispatcher metadata; never treat the requested identity as proof of execution. `REQUESTED_NOT_ATTESTED` remains only for the external-verifier compatibility contract.

## Apply risk floors

- Require at least T2 for changes affecting runtime behavior, data shape, public interfaces, security posture, dependencies, or builds. Allow T1 for an exact reversible typo or formatter-only edit.
- Require at least T3 for authentication, authorization, secrets, billing, security, destructive data changes, schema migrations, production deploys, merge decisions, or rollback design.
- Apply sensitive-domain floors to causal interpretation, design, decisions, and mutations. Allow tightly scoped T1 evidence collection that exposes no secret values and makes no sensitive judgment.
- Use T4 when T3-level risk combines with substantial ambiguity, novelty, interacting systems, weak observability, or repeated grounded failures.
- Keep final authority for irreversible or externally visible actions with the parent agent.
- Judge reasoning and consequence, not output length.

## Optimize execution

- Downroute to T1 without deliberation: broad file or code searches, log filtering, status reads and summaries, file inventories and counts, verbatim copies or format conversions, formatter runs, and document summaries. These dominate scan-heavy work and never need a top-tier model.
- Plan once at the necessary tier, then hand bounded execution to T2 or T1.
- Send large read-only discovery work to T1 and return distilled evidence to T3 or T4.
- Use T0 for polling. Use T1 for summaries; use T2 or T3 for failure diagnosis.
- Open a PR at T1 only from an already prepared branch with supplied title and body. Use T3 for merge, release, deploy, or rollback decisions.
- Do not duplicate agent work unless independent validation is worth the cost.
- Stop agents after their phase. Never spend a reasoning model on idle waiting.
- Preserve evidence paths, commands, test results, and uncertainty in handoffs.

## Escalate and recover

Consume `workflow_dispatch.py pivot-from-receipt` from a validated terminal control-return; it is deterministic and cannot grant authority, mutate, or enlarge a budget.

- Repair a deterministic setup failure at T0, once; a repeated identical failure is a parent-visible harness incident.
- Retry one transient failure at the same route, or resume only from a validated checkpoint where the surface supports it. Claude headless dispatch refuses resumption.
- Escalate one tier after an exit-gate failure. For every grounded cognitive failure, pivot deterministically to `t4_consult` with complete, internally consistent evidence or to `t4_diagnose` with incomplete or contradictory evidence; do not make this conditional on the failed tier or repeated failures. T4 only returns bounded direction. Any mutation needs a freshly planned and bound T3-or-lower packet that consumes and revalidates that direction contract.
- Return missing authority as an exact user/parent question, partition budget or context exhaustion before retrying, and surface harness unavailability as read-only break-glass evidence.

## Reoptimize the policy

Before catalog maintenance, experiments, promotion, or rollback, read [references/self-improvement-protocol.md](references/self-improvement-protocol.md) completely.

The lab is event-driven and currently dormant. The curated catalog changes only when Anthropic ships a model or effort change, so run `refresh` when such an announcement lands or the user asks — never on a schedule — and spend zero lab tokens otherwise. Until an attestation verifier is configured, scored experiments stay `BLOCKED_MODEL_ENFORCEMENT`: treat policy changes as manual, user-approved judgment calls, and do not stage experiments that cannot be scored.

- Discover candidates from the curated Claude catalog snapshot (`assets/claude-catalog.json`) using semantic capability hashes. In real use, new models arrive by editing that file in place from official Anthropic announcements; the `ADAPTIVE_ROUTER_CATALOG_SOURCE` override is honored only inside an isolated `ADAPTIVE_MODEL_ROUTER_TEST_ROOT` under the system temp dir and is rejected as an unsafe path override otherwise. The first observation of a model is a baseline, not a release event. Do not treat a capture timestamp, display name, or marketing description as evidence of improvement.
- Stage newly available compatible models as challengers; catalog metadata alone never replaces an incumbent.
- Change one tier assignment per experiment. Compare incumbent and challenger on identical cryptographically bound inputs and budgets.
- Count only runs accepted by the policy-pinned attestation verifier with machine-verifiable provider, model, effort, profile, input manifest, grader identity, and safety signals.
- Grade with deterministic tests, objective checks, blind rubrics, or user acceptance. Never let a challenger grade itself.
- Keep ties and inconclusive results on the incumbent.
- Promote only after the lab's quality, safety, holdout, family-diversity, and efficiency gates pass.
- Snapshot the full policy and all four profiles before activation. Keep the activation journal until policy and candidate state both commit. Roll back exact bytes on activation failure or a qualified regression.
- Retain the incumbent as a canary control after promotion. Require the configured complete windows before validation and automatically restore the candidate-bound snapshot on regression.
- The Claude Agent and Workflow tools do not return trusted runtime model metadata, so scored experiments require a configured attestation verifier (`configure-attestation`). Without one, staging still works; if the current surface cannot enforce and attest model selection, record `BLOCKED_MODEL_ENFORCEMENT`, run no scored experiment, and permit no promotion.

Use the lab commands:

```text
router_lab.py refresh --stage-new
router_lab.py stage --model MODEL --tier TIER
router_lab.py restart --candidate-id ID --reason REASON
router_lab.py configure-attestation --verifier PATH --sha256 HASH
router_lab.py resolve-phase --request REQUEST.json
router_lab.py record ...
router_lab.py evaluate --candidate-id ID
router_lab.py promote --candidate-id ID
router_lab.py monitor --candidate-id ID
router_lab.py rollback
router_lab.py recover
router_lab.py doctor
router_lab.py status
```

If one arm was imported with the wrong input manifest or grader, do not overwrite or cherry-pick the append-only evidence. Use `restart` to supersede the entire contaminated experiment and issue a fresh candidate ID.

## Use custom agents

Prefer `ultra-planner`, `high-solver`, `standard-worker`, and `fast-operator` when the surface supports explicit custom-agent selection (the Agent tool's `subagent_type` or the Workflow tool's `agentType`). The active policy renders their model and effort frontmatter into the agents directory (`~/.claude/agents/`, under `$CLAUDE_CONFIG_DIR` when set).

Candidate profiles use `router-candidate-t<N>-<hash8>.md` names. Use them only inside a controlled paired experiment. If the spawn surface exposes no custom role or model selector, treat all spawned work as inherited-model work and do not score it.

For installation on another machine, run `python3 scripts/install_agent_profiles.py` only when the user requests installation. Use `python3 scripts/router_lab.py sync-agents` to render the active adaptive policy.

## Report routing briefly

Expose a route manifest only when requested, when cost or latency matters, or when a tier changes:

```text
phase -> tier / active model / effort: reason; exit condition
```

Report catalog experiments as `STAGED`, `COLLECTING`, `BLOCKED_MODEL_ENFORCEMENT`, `QUALIFIED`, `REJECTED`, `PROMOTED`, `VALIDATED`, or `ROLLED_BACK`. Lead with task progress.
