---
name: ak-orchestrate
description: "Run staged or parallel jobs as resumable sessions of this runtime, or opted-in live-verified runtimes and Pi, with worktrees, fallback, safety gates, a final arbiter."
when_to_use: "Invoke to route split work by capability, risk and quota, or to onboard Pi."
category: workflow
keywords: [orchestrate, headless, multi-agent, sessions, session-first, cross-runtime, quota, fallback, pi, pi-sessions, onboarding, live-routing, model-routing, capability, risk, worktree, resume, parallel, arbiter]
argument-hint: "<job-spec.yaml | task description | --resume <run-dir>> [--yes] [--cross-runtime] [--internal (deprecated)]"
license: Proprietary
metadata:
  author: agentkit
  version: "2.0.0"
---

# Orchestrate

Coordinate independent sessions and headless coding-agent jobs through a
staged, captured, resumable workflow. The skill owns routing and judgment;
`ak orchestrate` owns deterministic plan state, process supervision and
observable evidence. No service or dashboard is required.

Runtime and model catalogs drift. Resolve every route from live evidence;
never treat a runtime, provider, model, flag, or agent seen in this file or an
older report as currently available.

## Inputs

Accepted forms:

```bash
/ak-orchestrate "research three implementation options and compare them"
/ak-orchestrate "run the three scouts as pi sessions, then one arbiter"
/ak-orchestrate plans/orchestrate-jobs.yaml [--yes] [--cross-runtime]
/ak-orchestrate --resume plans/reports/orchestrate-<timestamp>
```

Use a YAML job spec for repeatable runs; for a free-form request, write one
to `plans/reports/orchestrate-<timestamp>/jobs.yaml` before dispatch.

## Session-First Dispatch

Every orchestrated worker runs outside the coordinator's turn: a
current-runtime or Pi session with its own native handle, context, model and
lifecycle, or a supervised headless process. A current-runtime session is
`runtime: internal` in a job spec, defined in
[session-routing.md](references/session-routing.md). Nested in-harness
subagents are not workers; the one exception is the permission fallback
below.

- **Scope defaults to the current runtime.** Candidates are sessions of the
  runtime you are running in and its own supervised headless CLI.
- **`--cross-runtime` opts in other installed runtimes** that pass live
  probes, auth, controls, quota and cost checks. A job's `runtime:` pin or
  `fallback_runtime` chain, or a runtime the user names ("as pi sessions"),
  is an equivalent explicit opt-in for that runtime. A named runtime that is
  missing or not authenticated runs its onboarding as a visible setup step.
- **Unavailable is visible.** When the current runtime cannot start a
  qualifying session and no opted-in candidate qualifies, report the job
  `blocked` with the probe evidence. Never widen scope silently.
- **Permission fallback.** When the runtime refuses to start a session because
  the coordinator lacks permission, the job may run as a nested agent under the
  conditions in
  [session-routing.md](references/session-routing.md#permission-fallback),
  disclosed in the report. Quota, budget, resource, missing-runtime and crash
  failures never fall back to a subagent.
- **`--internal` is deprecated.** Accept it as "prefer current-runtime
  sessions" (already the default) and print one line telling the user to drop
  it. It never selects a nested agent.

Never override an explicit runtime, model or role-profile pin silently.

## Authority Map

Keep durable facts in one place:

- [model-routing.md](references/model-routing.md) is the **sole route-selection
  authority**: runtime scope gate, capability tiers, risk tiers, task
  defaults, session selection, strongest judgment model, fallback
  qualification, and model-family independence.
- [runtime-matrix.md](references/runtime-matrix.md): live candidate discovery,
  probing, command verification, OS evidence, `<run-dir>/runtimes.json`.
- [harness-profiles.md](references/harness-profiles.md): evidence schema for
  permissions, isolation, capture, budgets, and enablement.
- [session-routing.md](references/session-routing.md): session qualification,
  role profiles, dispatch, permission fallback, capture, timeout, and resume.
- [failure-modes.md](references/failure-modes.md): failure classes and the
  bounded fallback ladder.
- [concurrency-admission.md](references/concurrency-admission.md): sizing
  parallelism from usage windows and host headroom instead of a fixed count.
- [pi-sessions.md](references/pi-sessions.md): Pi probing, session handles,
  dispatch shape, capture, and intervention limits.
- [pi-onboarding.md](references/pi-onboarding.md): installing, profiling,
  authenticating, and verifying a Pi runtime that a job requires.
- [job-spec.md](references/job-spec.md): the executable YAML and acceptance
  contract; Go types and validation own exact machine fields.
- [observation.md](references/observation.md): observation, intervention,
  diagnosis and evidence-based improvement.

When references disagree, stop and report the contract mismatch.

## Platform Support

Orchestrate is not macOS-only. Plan state and current-runtime session jobs
work on every host; only supervised CLI and Pi processes and executable
`verification:` checks are Darwin-gated. Check the host before refusing a
request and follow [platform-support.md](references/platform-support.md).

## Pipeline

### 1. Brainstorm and intake

- Clarify the desired outcome, constraints, non-goals, and acceptance evidence.
- Read the request or job spec; identify the workspace root, dependencies,
  destructive or external intent, expected outputs, and runtime constraints.
- Refuse any plan that would place secrets, credentials, private keys, dotenv
  values, or unrelated private data in prompts or capture.
- Prefer a direct single-session workflow when orchestration adds no useful
  parallelism, staged dependency, runtime diversity, or arbiter value.

### 2. Build the job graph

- Convert the accepted outcome into jobs with explicit `task`, `cwd`, timeout,
  expected output, and file ownership.
- Use `depends_on` to form stages; run same-stage jobs concurrently only when
  ownership and outputs do not overlap, and only as many as
  [concurrency-admission.md](references/concurrency-admission.md) admits.
- Mark public-contract, security-sensitive, cross-module, or hard-to-revert
  implementation as `importance: high`; set `isolation: worktree` for parallel
  writers, untrusted write prompts, and harnesses with a weak write boundary.
- Name the skill, role profile or instructions each job must load; a fresh
  session or one-shot process cannot rely on automatic skill discovery.

### 3. Discover, profile, route, and onboard when required

- Reuse discovery evidence only while runtime binary/version, account, host,
  permissions, requested controls and model catalog remain unchanged;
  invalidate on change or probe failure. Resume reconciles existing attempts
  before dispatch.
- Apply the runtime scope gate in
  [model-routing.md](references/model-routing.md#runtime-scope-gate) first:
  current runtime by default, other runtimes only with an explicit opt-in.
- Build a live inventory per [runtime-matrix.md](references/runtime-matrix.md)
  and profile each candidate per
  [harness-profiles.md](references/harness-profiles.md); Pi candidates add
  the evidence in [pi-sessions.md](references/pi-sessions.md).
- When a pinned, fallback, or user-named candidate is missing or
  unauthenticated, run its onboarding as a visible setup step (Pi:
  [pi-onboarding.md](references/pi-onboarding.md)) and probe again. Discovery
  itself never installs or logs in, because a probe must not mutate the host.
- Pass the live evidence and job classification to
  [model-routing.md](references/model-routing.md); record the selected
  runtime, model or agent, capability tier, risk tier, controls, evidence
  source, and fallback reason. Do not restate or override its task defaults,
  tier floors, ranking, or fallback rules elsewhere.
- A missing, unauthenticated, unverified, or under-controlled candidate cannot
  satisfy a route. Re-profile fallbacks and rebuild their commands; never
  carry model names or flags between runtimes.
- Mark the job `blocked` when no candidate meets both capability and risk
  floors; never budget-route judgment or silently weaken safety.

### 4. Apply the safety gate

- Confirm every job's cwd, allowed files, writable roots, and expected side
  effects. Use least-privilege permission and tool controls verified on the
  live runtime, with every permission-bypass mode off by default.
- Record existing user authorization and its exact scope in `authority`.
  Request approval only for an action outside that scope; prior authorization
  stays valid without repeating `--yes`. A reference records the decision; it
  cannot grant authority by itself.
- Treat inherently auto-approved headless modes as constrained: read/report
  work or R2-isolated writes, never shared-tree destructive work. A worktree
  prevents edit collisions but is not an OS sandbox.
- Give every CLI process an external timeout; session timeouts are
  accounting-only unless the runtime proves cancellation.

### 5. Dispatch, observe and verify

- Create required worktrees, resolve input handoffs, pin each cwd, and build
  each CLI invocation from the live profile with argument arrays and scoped
  tools. Prepare with `ak orchestrate prepare <jobs.yaml> <run-dir>`; advance
  with `ak orchestrate advance <run-dir> --json`.
- Persisted attempts and intended supervisor IDs precede launch. Advance
  reconciles existing work before dispatch; never bypass an uncertain attempt
  by calling start manually. Follow [job-spec.md](references/job-spec.md).
- Start each returned internal job as a current-runtime session, preserving
  its attempt ID. Store the session handle and capture per
  [session-routing.md](references/session-routing.md); accept only a settled
  attempt with verified artifacts and checks, never a session's report alone.
- Give Pi jobs a run-scoped session directory and store each session id as
  the resume handle; dependents continue or fork it per
  [pi-sessions.md](references/pi-sessions.md).
- Read `status`, `events --after <cursor>` and `output --offset <bytes>` per
  supervisor run, each with its own cursor; poll until `all_settled`, not
  merely an aggregate failed status.
- Supervisor deadlines and bounded redacted capture survive the client exit
  on Darwin. Elsewhere, follow [Platform Support](#platform-support): keep
  dispatching qualified session jobs through the same `prepare`/`advance`/
  `accept` loop and block only the jobs that need supervision.
- Apply the observation and intervention contract in
  [observation.md](references/observation.md): a quiet process is not proof
  of a stall, and a cancelled request is not proof of a stopped writer.
- Classify each failure and climb the bounded ladder in
  [failure-modes.md](references/failure-modes.md) and report the mapped
  `error_class` in the `accept` receipt: reattach, retry through the job's
  `retry:` policy, then a new run directory that adapts within the current
  runtime or, when opted in, crosses runtimes; else pause, replan or block. A
  prepared run never re-routes a job. Unknown flags/models need fresh discovery;
  permission or external-effect failures need a scope-aware decision.

### 6. Run an arbiter review

- Wait for all runnable jobs to settle, then run the arbiter in a fresh,
  separate session on a C3 route. Resolve its model with the strongest
  judgment model rule in
  [model-routing.md](references/model-routing.md#strongest-judgment-model):
  honour pins and model policy, use only models the live runtime can select,
  fall back in a deterministic order, and disclose the runtime and model that
  actually served it.
- Prefer independently configured or different-family review when live
  evidence proves it; disclose a same-family fallback. A Pi arbiter counts as
  independent only when its resolved model family differs.
- Compare each result with `expected_output` and the original intent, run the
  checks listed in the spec, and flag contradictions, unsupported claims,
  missing artifacts, safety gaps, timeouts, and failed checks. Do not
  summarize unverified work as complete.

### 7. Report

- Write `plans/reports/orchestrate-<timestamp>/report.md`.
- Include per-job status, capability/risk tier, resolved runtime, session
  handle, role profile and model, how each runtime was admitted, failure
  classes and fallback steps taken (including any permission fallback),
  artifacts, errors, arbiter verdict with its actual runtime and model,
  checks, reproduction commands, worktree diffs awaiting integration, Pi
  session handles and exports, onboarding actions taken, and unresolved
  questions.
- Record effective model/effort, startup/fork/communication time and cache
  telemetry when exposed, alongside retries and cost. Unknown cache cost is
  not zero. Metrics never lower capability/risk floors, override explicit
  pins, or silently rewrite routing policy; keep per-attempt metrics in the
  run and aggregate comparable records without changing their evidence.

## Pi Sessions

Pi is orchestrable because every run is a resumable session file. The
coordinator keeps those files under the run directory, records each job's
session id as its handle, and chains dependent jobs by continuing or forking
the upstream session instead of re-sending its output. Headless Pi has no
sandbox and no per-operation approval, so its writes belong in a
coordinator-created worktree and it starts offline so a job cannot install
packages mid-run. Probe budgets, flags, capture and the RPC intervention
channel are in [pi-sessions.md](references/pi-sessions.md); install, profile,
authentication and AgentKit projection are in
[pi-onboarding.md](references/pi-onboarding.md).

## Worktree Isolation

- Create one worktree per isolated job from the accepted base ref, on a
  unique branch under the run namespace, and set the job's cwd to it. Never
  share a worktree across jobs or reuse a failed attempt without an explicit
  recovery decision.
- Sequence jobs that must edit the same generated artifact, lockfile,
  migration sequence, or shared configuration. Separate worktrees defer those
  conflicts; they do not resolve them.
- Integration is coordinator-owned and follows the arbiter pass: summarize
  diffs first; merging or cherry-picking is a separate reviewed step.
- Remove only integrated or explicitly discarded worktrees; preserve failed
  ones for diagnosis and list them in the report.

## Job Spec

Schema, examples and acceptance rules: [job-spec.md](references/job-spec.md).
Runtime and model fields hold placeholders until live discovery resolves them;
`runtime: internal` marks a current-runtime session job.

## Safety Defaults

- Every job has an explicit cwd, timeout, expected output, and ownership;
  capture stays under `plans/reports/orchestrate-<timestamp>/` with secrets
  redacted from prompts, commands, logs, and reports.
- Start with read-only or scoped-write behavior.
- Permission bypasses stay off unless the user approved the exact action and
  a stronger external boundary contains the residual risk.
- Parallel writers use separate worktrees and disjoint ownership; failed
  output is preserved for diagnosis, never hidden or relabeled.
- Keep destructive and credentialed external actions off prompt-only
  isolation. Onboarding installs are visible and reversible; profile
  overwrites are snapshotted first; credentials are entered only by the user.

## On-demand References

- `references/output-layout.md`: run-directory and supervisor capture tree,
  plus the rules on exporting private graphs or job specs.
- `references/arbiter-checklist.md`: load at step 6; the final report is
  blocked until every question in it is answered.
- `references/failure-modes.md`: load when a job fails, times out, requests
  permission, is interrupted, or ownership or references disagree.
- `references/metrics-and-self-improvement.md`: load when comparing run
  outcomes or considering a routing-policy change.

## Limitations

- Jobs share no implicit memory; pass artifacts through explicit dependencies.
  A continued Pi session carries context, not accepted proof.
- Session jobs may lack force cancellation, per-job sandboxing, or model
  selection; each is probed per run. A permission-fallback subagent lacks
  independent resume and shares the coordinator's quota and permissions.
- CLI commands, models, authentication, and safety behavior drift; every run
  revalidates them. Worktrees need a git repository and disk headroom and do
  not provide process isolation.
- Metrics are advisory and cannot authorize an automatic route-policy change.
- Orchestrate coordinates existing runtimes; it adds no daemon, dashboard,
  account pool, message broker, or provider adapter. Quota and resource
  admission are coordinator judgment over observed evidence, not an enforced
  reservation. Onboarding installs a runtime the user
  asked for and stops at the credentials only the user can supply.
- `ak orchestrate` supervises external CLI and Pi processes only on Darwin.
  Plan state and current-runtime session dispatch work on every platform; see
  [Platform Support](#platform-support). Record host and harness limits per
  route.

## Completion Report

End with:

```markdown
**Orchestrate Result**
- Spec: <path or inline request>
- Report: <plans/reports/orchestrate-.../report.md>
- Jobs: <success>/<failed>/<blocked>
- Arbiter: pass|fail|blocked
- Checks: <commands or none>

Unresolved questions:
- None
```
