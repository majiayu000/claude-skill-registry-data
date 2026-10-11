---
name: adaptive-model-router
description: Route harness-eligible Codex work to the smallest proven OpenAI coding model and reasoning tier for each phase, with measured promotion and exact rollback. Use when the user explicitly requests adaptive routing or work needs model or effort selection, dependent multi-agent coordination, multiple material phases, resumption or recurrence, cross-system coordination or judgment, consequential action, or evidence-heavy adjudication. Do not use for low-risk work clearly bounded to the current turn when one agent—or only a small independent read-only fan-out—can complete it without cross-system coordination or judgment.
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
- Treat `$CODEX_HOME/adaptive-model-router/active-policy.json` as model authority. Treat this skill's tier descriptions as role authority.
- Keep active-routing health independent from catalog experiments. A missing evidence runner, blocked challenger, prepromotion provider mismatch, or candidate-profile problem must be surfaced as evaluation degradation but must not prevent `resolve-phase` from using a healthy active policy and active profiles.
- Treat `CATALOG_STALE` as visible maintenance, not a workflow outage. Dispatcher admission must use `routing_status` plus `workflow_routing_ready`, never the aggregate doctor label.
- Preserve the parent agent as coordinator unless the user requests a separate task or thread.
- Never claim that a model changed unless runtime metadata proves the selected model and effort.
- Restrict automatic routing to locally available OpenAI models. Never substitute Anthropic or another provider.
- Treat Daybreak only as an explicitly staged, evaluation-only T3 security candidate. Never discover, stage, select, fall back to, promote, or describe it as an automatic general-purpose route.
- Enforce a non-regressing current-family rule: derive the newest visible OpenAI text family from the canonical live normalized router catalog and combine it with the active policy's no-downgrade family window. A caller declaration, profile, prompt, or substitute catalog cannot select the family. Every model-bearing route, fallback, and scored harness arm must use that family. Compare variants and reasoning efforts only within it. A catalog disappearance never moves the family backward; fail visibly instead of downgrading. T0 remains model-free.
- Within the current family, use the active policy's qualified role/effort assignment for each tier. T4's qualified deepest-effort route is a hard requirement; if it is unavailable, fail visibly instead of assigning a weaker variant.
- T4 is a read-only strategic lane. A phase that directly mutates state may be planned or adjudicated at T4, but its separately bound execution route is capped at the highest write-capable lane, T3. A T4 response is direction only: it cannot contain a patch, mutation grant, deployment instruction, or external-action authorization. Every `grounded_cognitive_failure` selects `t4_consult` when immutable evidence is complete and non-contradictory: offline, no tools, read-only, one model cycle, and the packet's strict cap. Incomplete or contradictory evidence selects `t4_diagnose`: exact repository/path scope, network disabled, strict token/tool/model-cycle/wall caps, and bounded read-only tools only. Any resulting mutation must re-enter through a newly planned and bound T3-or-lower route. Its fresh T3 packet must consume and revalidate an `adaptive-workflow.t4-direction-to-t3-mutation` contract bound to the T4 pivot, evidence bundle, source commit, repository/path, phase, and limits.
- Size token budgets from the phase requirements and measured runner context, not from one universal workflow ceiling. Keep identical explicit caps for paired experiment arms, but derive each case cap from its manifest.
- Require a quality-preserving top-tier counterfactual before qualifying a T1-T3 candidate. The counterfactual uses an evaluation-only copy of the candidate tier's exact role template, tools, and permissions while changing only provider/model/effort to the active T4 route. It never becomes an active profile and T4 candidates are exempt because T4 is the reference.
- Treat ordinary ungraded workflow telemetry as operational telemetry only. It cannot satisfy incumbent/challenger or top-tier model-evidence gates, even when its observed route and usage are valid.
- An exact `instruction_hash`-only catalog change on a still-eligible active route is an evidence-preserving instruction-contract rebaseline. A second narrow continuity class applies when every active model slug uniformly changes exactly `instruction_hash` plus `supports_reasoning_summaries`, all active routes remain eligible and byte-identical, and current-family/T4 invariants still hold. Record old/new field values and revision hashes, stale dependent experiment evidence, and count no model evidence or promotion. Any partial, nonuniform, additional, absent, or unclassified semantic field follows the normal fallback/fail-closed path.
- Honor an explicit user model choice over the adaptive policy.

## Load the active route

After activation, run `python3 scripts/router_lab.py status` before the first adaptive model-routing or dispatch decision. Run `python3 scripts/router_lab.py refresh --stage-new` when the catalog baseline is absent or stale. Do not load router state merely to classify direct work.

Use the four active assignments returned by the lab:

| Tier | Role and effort | Use for | Avoid |
| --- | --- | --- | --- |
| T0 deterministic | No model | Waiting, exact CI or PR status reads, scripted checks, formatter execution, file existence checks | Interpretation, diagnosis, or decisions |
| T1 fast operator | `fast_operator`, active policy model at `low` | Read-heavy scans, log filtering, status summaries, exact commands, mechanical PR creation with supplied inputs | Visual inputs, architecture, ambiguous debugging, sensitive edits, merge or deploy decisions |
| T2 standard worker | `standard_worker`, active policy model at `medium` | Contained implementation, ordinary tests, localized debugging, straightforward documentation and review | Cross-system ambiguity or high-consequence judgment |
| T3 high solver | `high_solver`, active policy model at `high` | Cross-file diagnosis, nuanced implementation, edge cases, difficult review, conflicting evidence, auth or release analysis; highest write-capable execution lane | Passive waiting and repetitive polling |
| T4 ultra planner | `ultra_planner`, active policy model at its qualified deepest effort | Hard architecture, novel multi-system planning, migrations, adversarial or security reasoning, adjudication | Direct mutation, routine coding, known execution steps, status checks, idle waiting |

Require exact `ultra` support for a new T4 challenger. A text-only coding model may serve T1 only when the phase has no image or visual-inspection requirement; keep it out of T2-T4.

The active tier mapping is role policy, not an experiment suggestion: use the policy-rendered assignment and required effort for each tier. Same-family experiments may compare alternatives, but promotion may not violate an active-variant requirement.

## Route the work

1. Decompose the request into discovery, planning, implementation, verification, polling, and release phases.
2. Remove phases that need no model. Prefer a deterministic tool, script, wait primitive, or automation.
3. Assign the smallest tier that can satisfy the phase.
4. Raise the tier to meet the risk floor.
5. Delegate only bounded work with clear inputs, outputs, and stopping conditions. Pass minimum useful context.
6. Reassess after evidence. De-escalate when ambiguity resolves; escalate after a grounded cognitive failure. Consume the workflow dispatcher's validated typed pivot rather than inferring recovery from logs.

For application workflows, let `adaptive-workflow-router` own phase order, dependencies, artifacts, and completion gates. Keep this skill as the sole authority for tiers, models, effort, escalation, promotion, and rollback. Resolve a machine-readable phase request with:

```text
router_lab.py resolve-phase --request REQUEST.json
cat REQUEST.json | router_lab.py resolve-phase --request -
```

The response binds the route to the active policy and profile hash. `REQUESTED_PENDING_SERVER_METADATA` means the route is selected but is not yet eligible evidence. Eligibility requires a completed first-party Codex App Server turn with matching observed model, effort, and service tier, thread and turn IDs, completed agent-message IDs, usage, a raw-transcript hash, and no reroute or safety-buffer event. The workflow dispatcher additionally issues a private hash-chained execution receipt for accepted turns; persistent workflow learning requires that receipt and a trusted quality receipt bound to the exact evaluated executions. These are observed first-party harness records, not provider-signed or cryptographic proof that the provider executed the requested model.

For activated work on this machine, execute the selected route through `../adaptive-workflow-router/scripts/workflow_dispatch.py`; run its `check` command before substantial dispatch. A planned phase also requires the exact prompt/context/runtime packet generated by `workflow_plan.py bind`; a selected route without that packet is not executable. The public generic-spawn interface does not expose enforceable model and effort selection, so it is inherited-model execution and must not stand in for T1-T4 routing. If the dispatcher reports a mismatch, reroute, safety buffering, missing evidence, or cap breach, surface the incident and stop that phase rather than falling back to the parent model.

## Apply risk floors

- Require at least T2 for changes affecting runtime behavior, data shape, public interfaces, security posture, dependencies, or builds. Allow T1 for an exact reversible typo or formatter-only edit.
- Require at least T3 for authentication, authorization, secrets, billing, security, destructive data changes, schema migrations, production deploys, merge decisions, or rollback design.
- Apply sensitive-domain floors to causal interpretation, design, decisions, and mutations. Allow tightly scoped T1 evidence collection that exposes no secret values and makes no sensitive judgment.
- Use T4 for read-only planning or adjudication when T3-level risk combines with substantial ambiguity, novelty, interacting systems, weak observability, or repeated grounded failures. Hand the resulting bounded mutation to a newly planned and bound T3 route; no T4 route may mutate.
- Keep final authority for irreversible or externally visible actions with the parent agent.
- Judge reasoning and consequence, not output length.

## Optimize execution

- Plan once at the necessary tier, then hand bounded execution to T2 or T1.
- Send large read-only discovery work to T1 and return distilled evidence to T3 or T4.
- Use T0 for polling. Use T1 for summaries; use T2 or T3 for failure diagnosis.
- Open a PR at T1 only from an already prepared branch with supplied title and body. Use T3 for merge, release, deploy, or rollback decisions.
- Do not duplicate agent work unless independent validation is worth the cost.
- Stop agents after their phase. Never spend a reasoning model on idle waiting.
- Preserve evidence paths, commands, test results, and uncertainty in handoffs.

## Escalate and recover

Run `workflow_dispatch.py pivot-from-receipt` on a validated terminal control-return. It is deterministic and idempotent: it produces the next route request or exact question packet, but cannot select a model directly, grant authority, mutate, or enlarge a budget.

- Repair a `deterministic_setup_failure` at T0 and permit one corrected retry. A repeated identical failure is a harness incident returned to the parent, not a T4 consultation.
- Retry a `transient_failure` once at the same route; a repeated transient failure is a blocker.
- Every `grounded_cognitive_failure` selects bounded read-only T4 direction through this router: `t4_consult` for complete immutable evidence and `t4_diagnose` for incomplete or contradictory evidence. Never repeat an identical failed cognitive prompt at the same tier. An `exit_gate_failure` returns to the model router for reassessment under its ordinary risk floor.
- Return `authority_required` as an exact user/parent question without dispatching another worker; authority never routes to T4.
- Partition `budget_or_context_exhaustion` before considering architectural consultation; a pivot never authorizes a budget increase.
- Return `harness_unavailable` as a bounded read-only break-glass consultation packet. Any mutation prompted by it must re-enter the governed graph as a fresh T3-or-lower plan.
- De-escalate after the plan, invariant, or exact command is established.

## Reoptimize the policy

Before catalog maintenance, experiments, promotion, or rollback, read [references/self-improvement-protocol.md](references/self-improvement-protocol.md) completely.

The workflow router's persistent `learning_loop.py` is a coordination and total-resource ledger, not a parallel model policy. It derives family authority from this router's canonical live catalog and active policy, requires receipt-bound execution and quality provenance, and maps every measured invocation to a predeclared budget call. Model-lane cycles must reference eligible `router_lab.py` observation and candidate identities and may only mirror states read from the live router authority. Never consume a locally asserted model recommendation, novelty score, or workflow-ledger label as an active route. SERENDIPITY model mutations remain current-family, single-variable, evidence-gated candidates under this router's normal qualification, promotion, canary, and rollback rules.

- Discover candidates from the local Codex catalog using semantic capability hashes. Do not treat a refetch timestamp, display priority, or marketing description as evidence of improvement.
- Stage newly available compatible models as challengers; never replace an incumbent from catalog metadata alone.
- Change one tier assignment per experiment. Compare incumbent and challenger on identical cryptographically bound inputs and budgets.
- Count only runs accepted by the configured execution-evidence mode. The default `server-metadata` mode pins the official Codex App Server executable and accepts completed response metadata with exact requested provider, model, effort, profile, input manifest, grader identity, and safety signals. The optional `external-verifier` mode retains the stronger signed-receipt contract.
- Bind server-metadata evidence to the retained raw JSONL transcript. Derive observed identity, usage, completion, message IDs, reroutes, and safety buffering only from events matching the experiment's exact thread and turn; ignore unrelated concurrent workflow events.
- Pass `--input-manifest-file` on every scored `record` import. The lab hashes and parses that file, requires its case, service tier, token cap, and wall-time cap to match the run, and rejects an arm whose measured tokens or transcript turn duration exceed those inclusive bounds.
- Use the bound transcript's `turn/completed.turn.durationMs` as the sole latency authority in server-metadata mode. Driver wall clock and caller-supplied timing are not model evidence; any supplied latency value must agree with the transcript-derived value.
- For a T1-T3 candidate, collect five exact candidate-versus-top-tier comparisons spanning at least three task families and one holdout. Both arms use the same input-manifest file, independent grader identity, service tier, retry rule, and caps. Reuse a top-tier control only when every execution and evidence binding matches and the observation remains within the configured freshness window.
- The top-tier gate requires no more than a 0.02 quality drop, at least 10% median token improvement, at least 10% median transcript-derived latency improvement, and a strict resource improvement on at least four of the five cases for each resource. Missing coverage remains `COLLECTING`; a complete gate failure is `REJECTED`. These requirements are additive to the incumbent comparison, not a substitute for it.
- Grade with deterministic tests, objective checks, blind rubrics, or user acceptance. Never let a challenger grade itself.
- Keep ties and inconclusive results on the incumbent.
- Promote only after a fresh evaluation still returns exact qualification under the current catalog and incumbent bindings and all quality, safety, holdout, family-diversity, and efficiency gates pass. A stale `QUALIFIED` label is not promotion authority.
- Snapshot the full policy and all four profiles before activation. Keep the activation journal until policy and candidate state both commit. Roll back exact bytes on activation failure or a qualified regression.
- Retain the incumbent as a canary control after promotion. `monitor` derives identity, quality, safety, regressions, and complete-window counts from imported paired canary evidence; it does not accept caller verdicts. Require the configured complete windows before validation and automatically restore the candidate-bound snapshot on regression.
- If the current surface cannot explicitly select the route and emit acceptable server metadata or a verified receipt, record `BLOCKED_MODEL_ENFORCEMENT`; run no scored experiment and permit no promotion.
- A prepromotion provider/model/effort/service-tier mismatch, reroute, or safety-buffer event is an enforcement incident, not model-quality evidence: preserve an abort artifact, import nothing, quarantine the candidate with `block`, verify active routing still resolves, and report the incident. The equivalent verified mismatch on a promoted active canary remains rollback evidence.

Use the lab commands:

```text
router_lab.py refresh --stage-new
router_lab.py enforce-version-window
router_lab.py adopt-current-family
router_lab.py stage --model MODEL --tier TIER
router_lab.py restart --candidate-id ID --reason REASON
router_lab.py configure-server-metadata --runner PATH --sha256 HASH
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

Prefer `ultra_planner`, `high_solver`, `standard_worker`, and `fast_operator` when the surface supports explicit custom-agent selection. The active policy renders their model and effort fields.

Candidate profiles use `router_candidate_*` names. Use them only inside a controlled paired experiment. If the spawn surface exposes no custom role or model selector, treat all spawned work as inherited-model work: do not score it and do not count it as successful adaptive workflow routing. Use the verified workflow dispatcher for active-policy phases instead.

For installation on another machine, run `python3 scripts/install_agent_profiles.py` only when the user requests installation. Use `python3 scripts/router_lab.py sync-agents` to render the active adaptive policy.

## Report routing briefly

Expose a route manifest only when requested, when cost or latency matters, or when a tier changes:

```text
phase -> tier / active model / effort: reason; exit condition
```

Report catalog experiments as `STAGED`, `COLLECTING`, `BLOCKED_MODEL_ENFORCEMENT`, `QUALIFIED`, `REJECTED`, `PROMOTED`, `VALIDATED`, or `ROLLED_BACK`. Lead with task progress.
