---
name: adaptive-workflow-router
description: Select, compose, and run evidence-gated application workflows while using adaptive-model-router as the exclusive model and reasoning-tier authority. Use when the user explicitly requests the harness or work is materially multi-phase, dependently multi-agent, long-running or resumable, recurring or monitored, needs cross-system coordination or judgment, consequential or high-risk, or evidence-heavy/conflict-bearing. Do not use for low-risk work clearly bounded to the current turn when one agent—or only a small independent read-only fan-out—can complete it without cross-system coordination or judgment.
---

# Adaptive Workflow Router

Use a deterministic application graph for known work and spend model reasoning only inside cognitive phases. Resolve every active cognitive phase through `adaptive-model-router`; never put a model, provider, tier, effort, or fallback in a workflow source.

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

## Start here

1. Read `../adaptive-model-router/SKILL.md` completely. It owns T0-T4, active assignments, risk floors, escalation, model discovery, experiments, promotion, and rollback.
2. Validate and inspect the installed workflows. Resolve `scripts/` relative to this skill directory; the examples assume that directory is the current working directory:

```text
python3 scripts/workflow_plan.py validate
python3 scripts/workflow_plan.py list
python3 scripts/test_workflow_plan.py
python3 scripts/test_workflow_dispatch.py
python3 scripts/test_agent_governance.py
python3 scripts/workflow_dispatch.py check
```

3. Select one root application. Compose additional workflows only when the request genuinely crosses applications.
4. Generate the route-bound plan before dispatching substantial work:

```text
python3 scripts/workflow_plan.py plan \
  --application coding \
  --objective "Implement the scoped change and prepare a PR" \
  --enable-condition delivery_requested
```

Use repeated `--application` values for mixed work; they compose sequentially in the requested order and wait for each run's active completion frontier, including an enabled delivery/publication branch. Useful floors include `--ambiguity novel`, `--risk-level high`, `--risk-tag security`, `--visual-required`, and `--current-info-required`. Enable only input conditions listed by the selected workflow; runtime conditions activate from evidence during execution.

## Choose the application

| Application | Workflow | Default shape |
| --- | --- | --- |
| Coding | `coding.change` | frame -> inspect -> design -> implement -> exact verification -> review -> optional delivery |
| Research | `research.synthesis` | frame -> decompose -> parallel retrieval -> synthesis -> conflict and citation gates |
| Planning | `planning.decision` | objective -> constraints -> alternatives -> tradeoffs -> selection -> stress test -> sequence |
| Debugging | `debugging.incident` | observe -> reproduce -> hypotheses -> discriminating tests -> diagnosis -> optional fix -> verify |
| Review | `review.audit` | freeze rubric -> mechanical checks and inspection -> adversarial probes -> validate -> adjudicate |
| Data | `data.analysis` | define metric -> inventory -> validate -> transform -> analyze -> robustness -> visualize -> report |
| Writing | `writing.document` | brief -> sources -> outline -> draft -> critique/revise -> fact check -> optional publication |
| Operations | `operations.release` | preflight -> plan -> read-only dry-run -> authorize -> single mutation lane -> poll -> verify -> close |

Use `research` before `planning` when a decision depends on current external evidence. Use `research` before `coding` when implementation depends on current APIs or standards. Use `review` after `coding` only when its independent rubric adds value beyond the coding workflow's built-in review.

## Execute the plan

The planner emits phase dependencies, activation mode, artifacts, exit gates, route requests, active-policy bindings, and requested route identities. It does not execute tools or confer authority.

Once an adaptive workflow is active, every T1-T3 phase must run through the headless `claude -p` dispatcher when this local harness is available. T4 (`fable`/`max`) is **not** headless-dispatchable — `claude --effort` accepts only `low|medium|high` — so this dispatcher fails closed as `T4_HEADLESS_UNSUPPORTED`, never silently downgrading to `high`. The recovery pivot is explicit for every grounded cognitive failure: a complete, internally consistent immutable evidence bundle selects `t4_consult`; incomplete or contradictory evidence selects `t4_diagnose`; `authority_required` selects `ask_user` and never dispatches T4. This Claude CLI driver does not claim to enforce either T4 mode: an in-session runner must reject the packet unless it can enforce the mode's exact repository/path scope, read-only filesystem, disabled network, no mutation tools, and all bound limits. A T4 result is direction only; a mutation requires a freshly planned and bound T3-or-lower packet that consumes and revalidates that bounded direction contract.

```text
python3 scripts/workflow_plan.py bind \
  --plan PLAN.json \
  --phase-key WORKFLOW:PHASE \
  --prompt-file PHASE.md \
  --cwd /absolute/workspace/path \
  --sandbox read-only \
  --tool-mode default \
  --wall-time-seconds 900 \
  --output PHASE.dispatch.json

python3 scripts/workflow_dispatch.py run \
  --plan PLAN.json \
  --phase-key WORKFLOW:PHASE \
  --dispatch-packet PHASE.dispatch.json \
  --prompt-file PHASE.md \
  --sandbox read-only
```

`run` takes cwd from the bound packet; passing `--cwd` is rejected.

Before dispatch, record a fresh `skill-read` receipt for every applicable skill and bind the resulting self-hashed required-skills contract with `workflow_plan.py bind --required-skills-file`. Dispatch re-reads every listed skill, checks its hash and bounded read age, and fails closed when a required skill is absent, changed, stale, or never read. Completed workflow receipts retain `required_skills`, `skill_hashes`, `source_commit`, `exit_gate`, `files_changed`, and `verification`.

All execution inside an activated adaptive workflow belongs to the bounded governance ledger. There is no arbitrary global agent-count ceiling. The coordinator decomposes the task first into an exact branch DAG with route identity, dependencies, mutation scopes, model-specific cost/quota weights, and separate token, model-cycle, tool-cycle, and wall-time ceilings. `workflow_dispatch.py capacity-plan` ignores caller-authored capacity and the governance authority deterministically derives a time-bounded weighted snapshot from the installed execution policy and current host resources, then packs the branch DAG into conflict-free waves and self-hashes the result. Every branch's weights must exactly match the installed model policy. `open-tree` derives descendant tokens from that contract; callers cannot type an unbound fan-out count. At child admission, the locked ledger conserves active resource weight across all trees, so multiple valid plans cannot each consume the full envelope. Every child must use a verified workflow plan and exact planner packet, name one unused branch and coordinator lease, start in a clean task-bound worktree, and match the branch's route, packet hash, permissions, resource envelope, and exclusive hierarchical mutation scopes. Both committed and uncommitted writes outside those scopes, and any source-commit drift including an empty commit, block acceptance. A planned branch can reach `COMPLETED` only with its matching execution receipt in the harness's validated hash-chained registry; generic terminal calls cannot complete planned branches or coordinators. A later wave cannot start until every prior-wave branch completed with that evidence. `close-tree` cannot claim success with active, failed, or unfinished branches. `close-tree --status` accepts exactly `COMPLETED|ABORTED|BLOCKED` (uppercase, required); `EXPIRED` is reachable only by lease decay, never by request. Every terminal, expired, or stale lease emits an immediate receipt. Single-phase one-off harness dispatches get a one-child ephemeral tree, consume the conservative maximum model weight, and cannot spawn descendants.

The operational sequence is `capacity-plan -> open-tree -> run each ready wave -> close-tree`. Run independent branches concurrently with ordinary process orchestration; do not hold a model turn open while waiting. Poll branch processes with T0, then dispatch a model only for terminal audit or failure diagnosis. A capacity contract may describe more than nine branches. Its finite count is derived from the actual task DAG, not a product-wide cap.

Retain the `bind` command's JSON output as `PHASE.dispatch.json`; it cryptographically binds the selected planned phase to the exact prompt, one ordered precomputed context bundle, cwd, sandbox, network, tool mode, mutation authority, requested token/model-cycle/tool-cycle limits, budget-contract hashes, and wall-time contract. Each model phase carries a structured `token_budget.declared_token_cap`; use `plan --phase-token-cap PHASE_KEY=CAP` to lower one explicitly and `bind --token-cap-contract-output PATH` to emit the coupled self-hashed fixed-cap/evidence pair. A headless model invocation requires that exact contract via `run --token-cap-contract PATH`; prose never authorizes a cap. Dispatch rejects any changed input, contract, or permission. Prefer this planner-bound fixed bundle over model-led file discovery whenever the required evidence can be assembled deterministically.

**There is no resumption lane on the Claude surface.** The Claude CLI exposes
`--resume`/`--session-id` but no analog of the App Server `turn/steer` +
`turn/interrupt` pair against a live turn, so the explicit
checkpoint-restart protocol cannot be honored and is not implemented. There is
no `resume` command, no `smoke` canary, and no resumption policy asset. An
interrupted phase is `ABORTED_NO_RESUMABLE_CHECKPOINT`: the partial run is
recorded as an aborted execution receipt and the phase is re-planned and
re-dispatched from its bound packet. When the abort is triggered by
`--wall-time-seconds`, the dispatcher retains the partial stream at
`runs/<id>/claude-cli.0001.jsonl`, appends a receipt with `status:
"ABORTED_WALL_TIME"`, `wall_time_seconds`, and `execution_identity:
"ABORTED_NO_RESUMABLE_CHECKPOINT"` (`observed_models` and `runtime_metadata`
are absent — no terminal event exists), and raises a `DispatchError` naming the
retained stream path and receipt hash. Such receipts are ordinary provenance
only: they are never learning-loop or model-promotion evidence and do not train
budget envelopes. `workflow_plan.py bind --resumable` fails
closed with that same code rather than minting an unenforceable contract. Do not
describe, promise, or design around Claude resumption until the CLI gains a
steer/interrupt surface.

A `runtime_condition` is intentionally non-executable until its declared upstream evidence exists. First retain a self-hashed `adaptive-workflow.phase-result` record bound to the prior plan ID, exact dependency phase contract, declared produced artifacts, triggered condition, separate execution record, and canonical paths/hashes. Then create a self-hashed `adaptive-workflow.runtime-condition` contract that references that phase-result record and is bound to the prior plan ID plus exact target phase/condition. Run:

```text
python3 scripts/workflow_plan.py activate-runtime \
  --plan PLAN.json \
  --phase-key WORKFLOW:CONDITIONAL_PHASE \
  --evidence-contract CONDITION.json \
  --output PLAN.activated.json
```

Bind and dispatch only from the new activated plan. The prior plan remains immutable evidence. An arbitrary condition flag, local file, or detached hash is not activation authority.

Use `--sandbox workspace-write --mutation-authorized` only after the parent has authorized the exact reversible mutation. Worker dispatch never permits unrestricted host access; externally visible or irreversible actions remain parent-only. Such a lane — and only such a lane — additionally receives `--allowedTools` carrying the dispatcher's frozen verification vocabulary (`WORKSPACE_VERIFICATION_ALLOWED_TOOLS`: test, typecheck, lint, and build runners plus `git status`/`git diff`), so a phase that changes code can run its own checks in its own cwd instead of handing verification back to the parent. It is a vocabulary, not a shell: there is no bare `Bash`, no raw interpreter, nothing that installs, publishes, escalates, or mutates version control, and a caller cannot extend it — widening it is a reviewed source change covered by the frozen release binding. A workspace-write lane the packet did not mark `mutation_authorized`, and every read-only or `tool_mode none` lane, receives no execution grant at all. Every headless dispatch is one unique single-turn `claude -p` process: the dispatcher assembles `--model <slug> --effort <low|medium|high> --output-format stream-json --max-budget-usd <cap> --permission-mode <sandbox mapping>` plus `--disallowedTools` derived from the bound tool mode and network access, spawns it with the packet's exact prompt and cwd, retains raw stdout verbatim as `runs/<id>/claude-cli.0001.jsonl`, and accepts the phase only when the stream ends in a non-error terminal `result` event. Session id, duration, cost, and per-model usage are extracted from that event as runtime metadata. Every accepted turn receives a crash-safe private hash-chained execution receipt in `~/.claude/adaptive-workflow-router/execution-registry.jsonl` binding the assembled command, permission mode, disallowed tools, allowed tools, budget cap, packet/phase/prompt hashes, source commit, requested route, observed models, retained stream path and hash, elapsed time, and the extracted runtime metadata.

Execution has four independently enforced resource limits—total tokens, harness-started turn cycles, tool-call cycles, and wall time. The dispatcher also records every strictly advancing cumulative usage update as `model_api_call_updates`; this is observed accounting telemetry, not a reliable provider-call boundary and not an additional ordinary-runtime stop. One headless turn can emit several usage-bearing stream events before or after tools, including reasoning continuations. For tool-enabled cold starts, immutable prompt/context and built-in context reserve are conservatively sized for `tool_cycle_cap + 4` usage-bearing responses, and bounded replay growth uses the same estimate. Actual cumulative tokens remain the hard spend limit. Tool mode `none` remains a strict one-response, zero-tool phase. The legacy `model_api_call_allowance` field is retained as the cold-start accounting estimate, and `--model-cycle-cap` remains a compatibility spelling for the harness-turn cap. Never make a model hold a streaming wait command open: unchanged CI, scheduler, and deployment waits are T0 deterministic polling, and a routed model wakes only for a terminal audit or failure diagnosis.

Cold-start envelopes are derived from the fixed phase contract. Once the exact workflow/version/phase/model/effort/tool-mode group has enough accepted executions, future limits use the configured successful-use percentile plus bounded headroom from `assets/execution-budget-policy.json`. An execution enters that distribution only when it has at least one registered quality receipt and every registered quality receipt accepts it; `COMPLETED` transport status alone is not task acceptance. Before learning, the harness re-reads the retained quality artifact, recomputes its verdict, re-runs a pinned deterministic grader or revalidates the registered blind-grader execution, and rejects any contradictory, missing, stale, or malformed provenance. Model-specific cost/quota weights reduce discretionary headroom for expensive or scarce routes; they never lower a cap beneath the measured successful percentile, even if a later cold-start formula is smaller. Failed, blocked, foreign-version, foreign-route, stale, ungraded, or quality-rejected records do not train the envelope. Retained failures may be used only as non-learning regression evidence when they demonstrate a deterministic invalidity in cold-start accounting. A caller may always request lower token, turn, tool, or wall limits; lowering the tool cap also lowers the cold-start usage-response estimate. A larger legitimate hard envelope requires a task-bound `adaptive-workflow.execution-budget-increase` contract, retained measured evidence, and a trusted completed `review.audit` execution receipt whose exact output approves the canonical proposal hash. The contract and requested limits are bound into the dispatch packet; an unrelated review or arbitrary rationale is not approval. Parallelism remains a task-plan decision: add a branch only when its measured benefit exceeds its weighted resource envelope and it does not overlap another mutation owner.

Planned execution additionally uses `verify-plan` to regenerate the full plan from the installed trusted catalog/current router, replay any evidence-bound runtime activations, and reject a self-rehashed forged phase before checking its dispatch packet. The selected phase must be explicitly `active`; a merely runtime-conditional phase cannot execute until evidence-gated activation produces a new plan. Tool-enabled cold-start derivation uses the bounded-tool-loop profile and assumes a short evidence-first loop. Before dispatch, inspect all four limits: ordinary T1/T2 work above 110,000 cold-start tokens or an unusually large cycle envelope is a partitioning failure unless measured evidence and independent review justify it. Split the work, switch immutable analysis to no-tools, or move deterministic edits/checks to T0. Use `--token-cap-contract` for a fixed, task-bound evaluation cap; use `--budget-increase-contract` for any increase above the measured envelope. A no-tools route permits only bound-thread passive user, reasoning, and agent-message items; every other or unknown bound item type is interrupted and rejected, while foreign thread/turn events are ignored. A provider/model/effort/service-tier mismatch, reroute, safety buffering, missing evidence, cap breach, malformed invocation/event, or setup failure fails closed and remains an explicit artifact. Never retry such a failure through generic spawn or an inherited parent model.

Dispatcher health admission uses the router's explicit active-routing fields (`routing_status=HEALTHY` and `workflow_routing_ready=true`). A visible `CATALOG_STALE` maintenance state, evaluation-only degradation, or prepromotion candidate problem must not disable healthy active routes; active policy/profile faults still fail closed.

For read-only synthesis or review, prefer repeated `--context-file` inputs at bind time with `--tool-mode none`. The planner turns the ordered inputs into one immutable, self-hashed context-bundle record; the dispatcher verifies the bundle and embeds it once. This mode is valid only with a read-only sandbox and network disabled, derives a one-model-cycle budget from actual bytes, and rejects any attempted tool use. Direct hashed context remains available for bounded smoke/diagnostic work, but planned cognitive work should use the precomputed bundle.

For each ready phase:

1. Invoke any applicable domain skill before work begins.
2. Dispatch the route with `workflow_dispatch.py`; generic collaboration spawn does not expose enforceable model/effort selection and is not a route implementation.
3. Give a worker only the declared objective, inputs, outputs, evidence standard, and exit gate.
4. Fan out only independent work. Gather results through one synthesizing phase; do not let parallel workers mutate the same state.
5. Record exact commands, source links, artifact paths, checks, uncertainty, and failures before advancing. A tool-enabled phase must observe the local `node_repl` bridge reach `ready` before its model turn starts; missing readiness fails closed without spending a model call.
6. Treat `REQUESTED_PENDING_RUNTIME_METADATA` as a requested route, not proof of the model that ran. Only a completed dispatcher record and its registry receipt supply observed runtime identity. Ordinary dispatcher records are explicitly ineligible for model promotion; scored experiments must separately satisfy the router's grader/run/import contract. A scored workflow result additionally needs a registered quality receipt from the pinned deterministic grader or a receipt-bound independent blind grader; a caller-authored quality file is not evidence. These receipts are first-party observed harness provenance, not provider-signed proof. The legacy `REQUESTED_NOT_ATTESTED` identity remains valid only with its external-verifier contract.
7. Stop when the exit gate passes. A transient tool or network error gets one same-route retry. Every grounded cognitive failure pivots deterministically to `t4_consult` for complete, internally consistent evidence or `t4_diagnose` for incomplete or contradictory evidence; `authority_required` is `ask_user`, never T4.

Within an activated adaptive workflow, T0 is reserved for exact checks, bounded polling, and predefined deterministic execution. Source selection, interpretation, diagnosis, synthesis, approval, and risk decisions are cognitive phases even when their output is short.

## Preserve authority boundaries

- `parent_gate` pauses for authority already present in the user's request or for an explicit parent/user decision.
- `parent_action` is executed only by the parent through the exact prepared action packet. A worker's route never grants permission.
- An operations release dry-run is read-only evidence collection. It validates the exact action packet without mutating the workspace or production; the authorized `parent_action` remains the single release mutation lane.
- Keep merge, deploy, rollback, publication, payment, destructive data operations, and other externally visible or irreversible actions outside worker autonomy.
- During incidents, use one mutation owner. Parallel agents may collect or analyze evidence but must not concurrently change production.
- Polling success is evidence, not merge or release authority.

## Handle conditions and loops

- Input conditions such as `delivery_requested`, `fix_requested`, `consequential_plan`, and `publication_requested` are enabled explicitly with `--enable-condition`.
- Runtime conditions such as a failed verification or material source conflict activate only when recorded evidence satisfies them.
- Evaluator-optimizer and agent loops have hard iteration bounds in the catalog. When the bound is reached, report the unresolved state; do not silently continue.
- Use a fixed rubric for evaluator loops. Self-critique alone is not independent proof.

## Improve without confounding

Use the Karpathy-style loop as controlled hill climbing: freeze the harness, make one change, measure, keep only evidence-backed improvements, and revert the rest.

- To test a model route, freeze `workflow_hashes`, inputs, tools, budgets, graders, and source corpus. Let `adaptive-model-router` run paired incumbent/challenger trials and own promotion or rollback.
- To test a workflow, freeze `router_policy_id` and change one workflow graph, prompt contract, gate, or parallelization choice. Compare identical task sets across multiple trials.
- Grade outcomes with deterministic checks first, blind rubrics or calibrated humans for subjective quality, and safety vetoes. Read failed transcripts; do not optimize only an aggregate score.
- Use held-out tasks and post-promotion canaries. Keep ties and inconclusive results on the incumbent.
- Run mutating workflow trials in a sandbox or dry-run environment. Never compare variants by duplicating real PRs, emails, deployments, payments, or production writes.
- For research comparisons, capture one source bundle and give both arms the same evidence; separate live searches confound the comparison.
- Record workflow version/hash, phase, active policy, runtime attestation, input and artifact hashes, gate results, quality, latency, tokens, cost, retries, and user corrections.
- Platform ports drift silently where behavior is contract-level (status vocabularies, CLI flags, receipt semantics); prefer a single core-vendored module (as `usage_projection.py` and `deterministic_quality_grader.py` are) over parallel hand-maintained copies, and let `sync_core.py --check` be the gate.

New coding models require no workflow rewrite: every plan resolves phases against the model router's current active policy. Its catalog monitor stages new candidates and promotes only through paired evals.

Persistent cross-cycle policy learning (`scripts/learning_loop.py`) is ported to
this platform. It aggregates workflow-policy evidence, owns the exact-byte
workflow activation transaction, and reads only first-party bytes: the
hash-chained execution/quality receipts this dispatcher wrote plus the raw
`runs/<id>/claude-cli.NNNN.jsonl` stream it retained. Every such receipt is
`evidence_grade: "declared"` from source `claude-code-headless-stream` /
`claude-code-headless-metadata`. It is first-party observed CLI output, not a
server-issued receipt chain, so it can never satisfy an incumbent/challenger or
top-tier model-evidence gate. Scored model-lane experiments stay
`BLOCKED_MODEL_ENFORCEMENT` until `router_lab.py configure-attestation` pins an
external verifier (the learner accepts only `execution_evidence_mode:
external-verifier` for model observations), and `router_lab.py` remains the
exclusive model candidate, promotion, canary, and rollback authority.

Because Claude Code exposes no versioned model families, the learner's routable
"family" is the curated catalog slug set (`haiku`/`sonnet`/`opus`/`fable`) that
`router_lab.py` baselines from `adaptive-model-router/assets/claude-catalog.json`;
a live global `catalog.json` that no longer matches those curated bytes fails
closed. T4 is exactly the `fable`/`max` read-only route.

**Usage projection (analytics, not evidence).** `scripts/usage_projection.py` (a `core/` file, byte-identical across all platforms, stdlib-only) provides a normalized read-only view over both platforms' native execution registries without altering either receipt schema. Commands:

```text
python3 scripts/usage_projection.py report [--platform all|codex|claude] [--since ISO8601|epoch] [--until ...] [--json]
python3 scripts/usage_projection.py project --platform codex|claude --receipt-file PATH
```

`report` aggregates by platform / tier / model / status and prints "routed output share by tier" — the share of output tokens spent through receipted dispatch, by tier. Two honest limitations: (1) Codex receipts currently record model/effort/service_tier but no T0–T4 route tier, so Codex rows report tier `?` until the Codex receipt writer records `route_tier`; (2) this projection is analytics, not evidence — it confers no execution identity, quality, governance, or learning authority and must never be cited as proof of what model ran.

Read [references/workflow-contract.md](references/workflow-contract.md) before changing workflow definitions or evaluation rules. Read [references/learning-loop-contract.md](references/learning-loop-contract.md) before changing persistent learning, evidence reuse, SERENDIPITY, activation, or recovery. Read [references/research-basis.md](references/research-basis.md) before changing the pattern taxonomy or application graphs.

## In-session dispatch (T4 and inherited surfaces)

Two lanes exist and they are not interchangeable.

* **Headless (`scripts/workflow_dispatch.py run`)** — T1-T3 only, evidence-bearing,
  receipts written. This is the lane for every phase whose effort is
  `low|medium|high`.
* **In-session (Agent tool / Workflow tool)** — a possible T4 lane only when
  that runner enforces the canonical T4 packet. For every grounded cognitive
  failure, complete and internally consistent evidence selects `t4_consult`:
  its evidence bundle is immutable and precomputed, `tool_mode: none`, the
  scope is offline/read-only, it has exactly one model cycle and zero tool
  cycles, and it observes strict structured token and wall caps. Incomplete or
  contradictory evidence selects `t4_diagnose`: it is offline with a
  repository read-only filesystem, exact repository/path scope, no mutation
  tools, only bounded read-only tools, and strict token, tool-cycle,
  model-cycle, and wall-time caps. Neither mode may mutate. If the in-session
  runner cannot prove those controls, it must reject the packet rather than
  execute a weaker T4 route. `authority_required` is `ask_user`, not a T4
  request. T4 output is direction only; a mutation requires a freshly planned
  and bound T3-or-lower packet that consumes and revalidates the bounded
  direction contract. In-session execution produces **no** execution receipt: its
  identity stays `REQUESTED_PENDING_RUNTIME_METADATA` and it is never
  model-promotion evidence; that requested identity is not proof of a runtime.

Never satisfy a T4 phase by running the headless dispatcher at `high`. The
refusal is deliberate: a silently weaker route would make the plan's own
evidence false.
