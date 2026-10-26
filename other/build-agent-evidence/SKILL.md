---
name: build-agent-evidence
description: "Build a reproducible evidence packet and bounded autonomous coding test workflow for a proposed agent behavior or change. Use when defining cases, fixtures, evaluators, heldout comparisons, test artifacts, or release-facing evidence; do not use to define a missing contract, grant access, approve risk, deploy, or invent results."
metadata:
  version: "0.1.0"
  playbook_version: "0.5.0-draft.2"
  source_commit: "151fca01fbc609c5550c563c902946db540c2f4c"
---

# Build Agent Evidence

## Purpose and boundary

Build attributable, reproducible evidence for a bounded candidate and its claims.
Produce an evidence packet and test workflow; do **not** certify readiness, approve a release,
grant data or tool access, deploy, or turn a planned fixture into an observed result.

Use this skill directly after a candidate, intended behavior, and approved coding workspace exist.
Use it for a first candidate or a behavior-affecting change. It supports direct invocation;
it does not assume that any sibling package has activated.

## Read first

1. Read [the Part 4 owner map](references/owner-map.md) for the exact requirement owners.
2. Read [the packet contract](references/packet-contract.md) before creating a packet or run record.
3. Read [the examples](references/examples.md) only when shaping a case register, emitted artifacts,
   comparison ledger, or bounded repair record.
4. Treat [evaluation cases](assets/evaluation-cases.json) as planned selection fixtures, not behavioral evidence.
5. Copy [the packet template](assets/packet-template.json) into the approved workspace and replace its
   draft values only with attributable information.

## Preflight and direct-load predicates

Confirm all of the following before planning an execution:

- A named candidate, behavior-affecting scope, accountable evaluation owner, and approved isolated workspace exist.
- The candidate contract names user-visible outcomes, prohibited outcomes, boundaries, stop conditions,
  configuration, and material risks or records why one is not applicable.
- A baseline identity is available, or a documented first-release comparison rationale exists.
- The allowed workspace, fixtures, test data, effects, budgets, and authority boundaries are explicit.
- Artifact retention can use normalized relative paths within the approved workspace and content digests.

At each missing-input boundary, check whether the named leaf is available for **direct** loading:

| Missing input or next phase | Directly load if available | If unavailable |
| --- | --- | --- |
| Intended use, risk, or material-change scope | `plan-agent-use` | Request the versioned scope record; block evidence design. |
| Contract, outcomes, interface, or stop conditions | `specify-agent-contract` | Request the contract artifact; do not infer it. |
| Capability, source, effect, or trust boundary | `design-trust-boundaries` | Request the boundary record; block affected claims. |
| Approved implementation approach is absent | `draft-agent-implementation` | Request the approved implementation plan; do not write code. |
| Evidence is complete and a readiness decision is requested | `review-agent-readiness` | Hand off the packet without claiming readiness. |

Do not fetch a substitute dependency. Missing material is a `needs_information` or `blocked` result,
not a reason to invent a claim, evaluator, fixture, or authorization.

## Build the evidence design

1. **Bind the subject.** Record candidate source and configuration identity, route and fallback identity,
   baseline or first-release rationale, accountable owner, scope, and resolution time. Bind semantic identity
   too: the claimed behavior, case purpose, allowed variation, and fixture meaning—not only file names.
2. **Map claims before tests.** Map each acceptance criterion, prohibited outcome, and material risk to a
   claim family, case, fixture, test level, evaluator or authoritative observation, coverage profile, stage,
   rerun trigger, decision role, and owner. Use all applicable `CASE`, `BEHAVIOR`, `EVALUATOR`,
   `COVERAGE`, and `RELEASE-EVIDENCE` groups in the owner map. State an objective absent-trigger rationale
   for each profile marked not applicable.
3. **Predeclare the decision.** Before inspecting candidate results, record hard gates, required coverage and
   slices, pass predicates, denominators, status treatment, operating constraints, repair rule, decision
   authority, and the treatment of missing, invalid, and inconclusive evidence. Keep control gates, task
   metrics, and diagnostics separate.
4. **Design controlled cases.** Give each case a stable ID, versioned input, origin, tags, suite purpose,
   expected terminal result, observable invariants, and permitted variation. Include normal, allowed-counterpart,
   boundary, missing or malformed dependency, denied, exhaustion, and untrusted-input cases when triggered.
   Pair uncertainty or refusal with an answerable allowed case so over-refusal is visible.
5. **Protect independence.** Keep development and regression cases separate from an independently authored
   holdout task and fixture. Do not tune the candidate, checker, rubric, or threshold from the holdout it reports.
   A fixture is a controlled starting world and planned test input; it is never execution evidence by itself.
6. **Control the fixture.** Version initialization, per-run isolation, permitted live boundary, reset method,
   reset verification, authoritative observation, and data minimization. Give every test its own fixture copy;
   never use mutable shared state as proof that trials began alike.

## Choose test levels and evaluators

Use the narrowest check that can establish each claim, then add the level required by the crossed boundary:

- **Unit:** deterministic rules, transformations, limits, and local failure handling.
- **Contract:** typed interfaces, schemas, permission decisions, and component boundary invariants.
- **Integration:** interactions that cross components or controlled dependencies.
- **End-to-end:** the user-visible terminal result plus required observable trajectory and boundary effects.
- **Adversarial:** injected or untrusted content in its actual channel, malformed or unavailable inputs,
  denial, stale or conflicting evidence, exhaustion, and applicable abuse or bypass attempts.

Define observable end-state verifiers for every case. Prefer a deterministic checker or authoritative state
observation for deterministic claims. Record outcome and trajectory judgments separately; accept safe
invariant-compliant alternatives rather than exact command traces unless a contract or protocol requires one.

For every evaluator, record its bounded claim, allowed evidence, rule, identity, version, statuses, purpose,
and limits. Supply known-pass and known-relevant-failure self-tests. Use qualified independent review for
material ambiguity or specialized interpretation. Introduce a model judge only when an objective or qualified
method cannot establish the qualitative claim; keep it diagnostic-only until its exact configuration has a
predeclared, independently human-reviewed heldout calibration. Never use it as the only check for an
enforceable boundary, authorization, isolation, approval, schema, or effect.

## Run an autonomous coding cycle

Modify only the user-approved isolated workspace. Autonomy to change that workspace does not authorize live
effects, access changes, deployment, or risk acceptance.

1. Emit **planned** evidence records for the approved claims, cases, fixtures, evaluators, baseline, bounds,
   and repair budget before execution. Snapshot candidate, checker, configuration, and fixture identities.
2. Start each trial in a fresh session and a freshly initialized, verified workspace. Record the reset result,
   runtime conditions, source identities, selected configuration, attempted actions, and terminal status.
3. Run unit, contract, integration, end-to-end, and applicable adversarial cases. Run the baseline and candidate
   under the same applicable cases, fixture rules, reset, sources, trial policy, and comparison unit.
4. Emit an immutable per-attempt record and artifact digest immediately after each trial. Include the command or
   procedure, stdout or structured event log, checker result, end-state observation, timing or resource data,
   and distinct `pass`, `fail`, `invalid`, or `inconclusive` status.
5. Do **not** retry a failing candidate trial until it becomes green. Preserve it as a failure. A timeout is not a
   silent retry. Count physical attempts separately from any declared final-policy result.
6. Repair only under the predeclared bounded rule. Retain the original record; log diagnosis, repair identity,
   counter, non-bias rationale, and changed files. Keep the candidate's semantic case purpose, fixture meaning,
   input scope, gates, and thresholds fixed. Rerun every affected paired case after repair. Stop when the repair
   budget is exhausted or a required dependency or authority is absent.
7. After the required end-to-end test passes under its declared rule, clean generated trial state as the fixture
   requires, run the full applicable suite again from clean state, verify retained artifacts, then package the
   evidence. Never package before this **end-to-end → cleanup → full retest → package** order completes.

## Compare, retain, and hand off

Keep the complete attempt ledger, including candidate and baseline paired flips. When variability, selection,
retry, fallback, or inference matters, state the trial unit, fixed and varying sources, uncertainty assumptions,
and separately label first-attempt, any multi-attempt measure, and final-policy success. Do not treat repeats
within one case as independent population observations without a justified design.

Retain invalid and inconclusive records with their reason. A harness or evaluator repair can add replacement
evidence only under the declared rule; it never erases attributable candidate failure or relaxes the claim.
Keep observed artifacts confined to the approved workspace and attach lowercase content digests.

Return the completed packet, coverage map, case and fixture register, evaluator records, trial ledger,
candidate-baseline comparison, repair record if any, and a decision-ready evidence summary. The packet may
recommend `go`, `conditional_go`, or `no_go` only under its declared policy; its `authorized` field remains
`false`. Missing required evidence, an unmet non-waivable gate, absent coverage, or an inconclusive required
result requires `no_go`, not an average-based exception.

## Stop and verify

Stop and surface a blocker when the contract, baseline rationale, controlled fixture, fresh-session reset,
authoritative observation, evaluator fitness, required holdout, workspace approval, or repair authority is absent.
Do not call a simulated trace, a fixture, a planned check, a favorable judge opinion, or a selected transcript
observed evidence.

Before handoff, verify that all observed artifacts exist under the approved workspace, hashes match, each `met`
applicability entry cites observed passing evidence, every status is visible, candidate and baseline identities
are comparable, holdout independence remains intact, and no decision is presented as deployment authorization.
