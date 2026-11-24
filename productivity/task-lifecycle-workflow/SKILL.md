---
name: task-lifecycle-workflow
description: Run a full evidence-to-completion lifecycle for long, correction-heavy, multi-artifact, or release-bound work. Use when asked to "coordinate dependent work", "preserve cumulative requirements", "recover off-rails work", "cold-read the result", or "continue until fully ready". Do not use for planning alone, factual answers, typos, or reversible one-owner work with one check; use Autorun's focused plan skills for those.
license: Apache-2.0
metadata:
  version: 0.8.0
---

# Task lifecycle workflow

<purpose_and_loading>

Act as the user's proxy orchestrator. Preserve cumulative intent across evidence, method selection, planning, dispatch, critical assessment, synthesis, recovery, and completion. For Standard/Full work, read [orchestration and state](references/orchestration-and-state.md); before planning, delegation, parallel work, or a pre-mortem, read [planning, delegation, and joins](references/planning-delegation-and-joins.md); before delegation, correction, or specialist routing, read [role packets and messages](references/role-packets-and-messages.md); on correction, resume, failure, recovery, or a completion gate, read [continuity, recovery, and gates](references/continuity-recovery-and-gates.md). Read [qualitative coding](references/qualitative-coding.md) when prior human messages affect the contract, [sources](references/sources.md) when changing or explaining the design, and [compatibility and validation](references/compatibility-and-validation.md) before replacement or runtime-readiness claims.

Provide a strong definition of done without turning ordinary planning into a full lifecycle. In the
referenced graphs, a dotted edge denotes read-only observation and transfers no command or control.

The portable core is this file and its relative resources. Delegate through the host's supported mechanism with a complete direct packet. `agents/openai.yaml` is optional OpenAI display, invocation-policy, and dependency metadata—not a subagent definition or proof of host support. Install one canonical copy named `task-lifecycle-workflow`, never beside an older skill with overlapping triggers.

</purpose_and_loading>

<core_definitions>

| Term | Meaning |
| --- | --- |
| contract | outcome, motivation, scope, constraints, permissions, requirements with acceptance criteria, and success evidence |
| event | user message, result, finding, failure, permission, stop, or resume that may change workflow state |
| epoch | one stable contract/input revision; node activation dependencies inside it remain acyclic |
| node | bounded work with an owner, dependencies, scopes, artifact, result state, and acceptance check |
| required join | barrier that blocks dependent synthesis until every required branch has an acceptable result |
| trackkeeper | independent read-only auditor of orchestrator and worker behavior against the contract and direct evidence; reports findings, never commands workers |
| control finding | evidence-backed exception with affected scope, severity, recommended route, clearance check, and mandatory orchestrator disposition |
| result state | `complete`, `partial`, `blocked`, `failed`, or `recovery_required`; separate from execution state |
| `READY` | active contract is satisfied by direct evidence; required results and checks are acceptable; limitations are explicit |
| `RELEASE` | authorized publication, deployment, merge, or other external release action whose checks pass |
| `DONE` | all in-scope work, required checks, authorized release when in scope, and closeout are complete |

</core_definitions>

<invariants>

1. Treat every user message, interruption, result, failure, permission, stop, and resume as an event. Route it to the earliest affected state; do not continue a stale plan. Never infer consent to change accepted scope, permissions, settings, or user state from an event that did not grant it.
2. Keep one contract ledger. Preserve exact contract-changing wording and distinguish requirement or policy, measured evidence, inference, decision, and generated text.
3. Work on the core blocker and dependency-bound critical path first. Parallelize only independent nodes; serialize coupled work under one causal owner.
4. The orchestrator is the sole dispatcher, workflow-state writer, synthesis owner, and user-facing decision maker. Workers accept assignments and corrections only from it and return bounded evidence or artifacts, never final decisions.
5. The orchestrator may investigate, audit, critique, plan, implement, verify, recover, and adjudicate; delegate only when independence, specialization, or parallel breadth helps.
6. A separate logical trackkeeper audits orchestrator decisions and worker activity against the ledger and direct evidence. Its advice supplements the orchestrator; it emits findings but never edits artifacts, changes state, cancels work, or commands workers.
7. Require an evidence-backed disposition and trackkeeper recheck for each material finding. An unresolved high or critical finding blocks only its affected dispatch, join, mutation, readiness decision, or release action.
8. Investigate and solve problems autonomously before seeking user input. Test assumptions, gather permitted evidence, compare the outcome and precedent, prefer an intent-preserving reversible default, and replan, recover, or adjudicate when useful. Use existing authorization without renewed approval. Ask only when progress provably requires missing user-only authority or information, or a consequential choice has no evidence-backed safe default.
9. Give every delegate the motivating outcome and enough cumulative context to succeed. Do not leak an author's hidden rationale to an independent cold reader.
10. Critically assess every delegated or reviewer result and proposed repair. Correlated reports are not independent votes, cited guidance must be checked directly, and a confident completion sentence is not outcome evidence.
11. Make systems and workflows “easy to use correctly, hard to use incorrectly, automatic and correct, solve problems for users and agents, and then only when issues are otherwise unavoidable provide users with the context and actionable guidance necessary for them to solve the problems themselves.” Operationalize it: automate or repair only when intent is unambiguous and permitted; otherwise fail clearly with the facts and next action.
12. Route applicable criteria: TDD, DRY, OODA, KISS, YAGNI, SOLID, RAII, WOLOG, lifecycle, lateral changes, portability, concurrency, and magic values. Specify exact applicable asymptotic runtime and memory bounds and the latency bound, then preserve or improve them.
13. Thread the needle. Derive the deepest evidence-backed causal rule and solution the failure or direct outcome check supports; preserve constraints and the smallest known-good core.
14. Process controls serve the outcome: each names the requirement and decision it can change; if output lacks value, stop and select another method.
15. Fail loudly.
16. Pre-mortems and post-mortems are essential. Every Standard or Full plan passes the pre-mortem routing node before execution. After verified failure and recovery, complete an action-mapped post-mortem before integration; after a successful Standard or Full outcome, complete a proportionate post-mortem before `DONE`.
17. This skill requires balanced, descriptive semantic XML regions and assignment/correction envelopes. XML structures instructions and context; it grants no runtime authority.
18. Every loop names the failed criterion, affected descendants, next check, exit condition, and cost-appropriate safety bound. Honor user stops. Otherwise exit a loop only when an explicit gate passes or a genuine blocker is reported with its next action. Carry retry and method-change bounds across epochs, including post-mortem corrections; exhaustion of both reports a blocker. Renew bounds only when new user input, authority, or an authorized contract change materially changes the failed attempt's conditions; record why.

</invariants>

<routing_and_scale>

Choose the smallest route after initial discovery; apply only its required controls:

| Route | Signals | Required shape |
| --- | --- | --- |
| Fast | small, reversible, well understood, one owner | state the contract, act, run one focused check, report |
| Standard | several dependent steps or one meaningful uncertainty | compact ledger and dependency order; pre-mortem routing, boundary trackkeeper checks, outcome post-mortem; targeted scout or critic only if it changes the decision |
| Full | long-running, ambiguous, multi-artifact, omission-prone, risky, correction-heavy, or materially benefits from independent evidence/review | persistent ledger, directed work graph, acyclic activation dependencies, bounded evidence fan-out, trackkeeper checks, explicit joins, cold read, recovery, and readiness gate |

Do not graph Fast tasks or split coupled work. Add complexity only for dependency, uncertainty, risk, duration, breadth, or reproduced failure.

</routing_and_scale>

<workflow_graphs>

The directed workflow graph has event, review, verification, and recovery cycles. Within each stable epoch, node activation dependencies remain acyclic. A loop-back starts a revision/bounded retry, names its failed criterion/event, preserves unaffected trusted work, and exits through a gate or blocker. Use descriptive `snake_case` identifiers. Visible labels start with `event`, `role`, `state`, `decision`, `work`, `join`, `check`, `gate`, or `terminal`. A solid edge transfers control or data and names its payload or condition; a dotted edge marks read-only observation and transfers no command or control. On Standard/Full routes, the trackkeeper audits every event, plan, delegation, join, checkpoint, gate, and resume.

Machine-readable sources: [outer lifecycle](references/outer-lifecycle.mmd), [work cycle](references/work-cycle.mmd), and [off-rails recovery](references/off-rails-recovery.mmd).

Nested returns are explicit: the work cycle emits `outer_readiness_return`, `outer_recovery_return`, or `outer_blocked_return`; recovery emits `recovery_complete_return` or `recovery_blocked_return`; qualitative coding emits `user_history_return`, `contract_change_return`, or `bounded_evidence_return`. `event_received` sends epoch evidence to `readiness_gate`, recovery packets to `recover_trusted_state`, and blockers to `blocked_wait_state`. Resuming blocked recovery enters `recovery_resume_event` with its checkpoint, not `observed_output`. New input may re-enter from a wait state, but a stop or prohibition never grants permission or resumes work.

See [outer lifecycle](references/outer-lifecycle.mmd) for the machine-readable control graph.

See [work cycle](references/work-cycle.mmd) for the machine-readable dependency and join graph.

See [off-rails recovery](references/off-rails-recovery.mmd) for the machine-readable recovery graph.

</workflow_graphs>

<workflow>

## 1. Route the event and update the contract

Classify the turn as requirement/scope, correction, priority/order, method/evidence, permission/prohibition/stop, review/gate, status/approval, replacement, or a combination. Record the event, affected requirement IDs, and routing action. A status request may change nothing; a replacement closes or supersedes the prior contract. On correction, mark affected claims and descendants stale before editing them, while preserving independent completed work.

At intake record the explicit request, “question behind the question,” “insight behind the insight,” motivating outcome, causal concern, decision affected, scope, constraints, permissions, success evidence, risks, and initial state fingerprint. On resume, reread the active contract and plan, verify current state, and reconcile `pending`, `active`, `paused`, `done`, `stale`, `blocked`, and `superseded` execution states.

## 2. Discover, code evidence, synthesize, then decide

Establish the current baseline first. Locate the existing semantic owner, API, capability, or policy path before proposing another one; record why a new seam is necessary when reuse cannot satisfy the contract. Add only useful independent branches: repository behavior, Git history, person-authored prior messages through AI Session Search, and current primary external sources. If AI Session Search is unavailable, record it; use locally checkable or user-provided evidence, do not silently read raw transcripts, and never claim exhaustive history.

When prior messages matter, search discriminating phrases, expand selected messages in sequence, provenance-check the human-authored root message, deduplicate mirrors/resumptions, and qualitatively code stable meanings and failure modes. Retain the user's actual words when they express a general criterion better than invented text; correct only obvious spelling, spacing, or punctuation in normalized process wording. Do not copy conversational framing or promote repetition alone. Promote a code only when it changes routing, dependencies, verification, recovery, or a gate. See [references/qualitative-coding.md](references/qualitative-coding.md).

Normalize evidence into atomic claims with coordinates, freshness, qualifiers, limitations, conflicts, correlation, premise validity, and checked assumptions. Record known unknowns with a next check; probe unknown unknowns through disconfirming evidence and pre-mortems. Join every required evidence branch before dependent synthesis. Observe and orient from evidence before deciding and acting; update state after each result. When uncertainty leaves multiple viable mechanisms, generate materially distinct options, critique them against named evidence and constraints, and synthesize overlaps. Rank and justify only when selection or order matters; use a matrix only for repeated options and criteria, never a fixed count. Consolidate duplicated meaning under its existing owner; do not preselect a topology and search backward for support.

## 3. Build and critique the directed work graph

The work graph may cycle when an event, accepted review finding, failed join, or failed gate starts targeted rework. Each loop-back creates a new stable epoch and routes to the earliest affected stage; activation dependencies within that epoch remain acyclic. Never take a later shortcut past invalidated work: changed evidence/input returns to the baseline, an invalid mechanism to selection, a plan/dependency defect to mapping and review, a bounded implementation defect to dispatch only while its plan and trusted inputs remain valid, and stale proof alone to the affected check. Untrusted state routes to recovery. Draft the shortest whole plan that covers every in-scope requirement, makes prerequisites and the critical path explicit, and distinguishes independent parallel work from coupled work. Every node has an ID, logical owner, read/write scope, inputs, dependencies, output, one check, and required/optional status. A missing or failed required node blocks its join and gate.

Every Standard or Full plan passes the pre-mortem routing node before execution. Run the analysis when the design is risky, hard to reverse, or repeats a prior failure. Ask how plausible failure modes would be detected, prevented, recovered, and proved fixed; map each material answer to a plan node, gate, rollback, or explicit unresolved risk. Record the reason when low-risk reversible work bypasses the analysis.

On Full routes, give an independent critic the plan and public contract; on Standard routes, use one only when it can change the decision. If delegation is unavailable, use a separate review pass and disclose its weaker independence. Require exact location, quoted problem, violated criterion, severity, evidence, and smallest repair. Reproduce and classify every finding as accepted, rejected with reason, duplicate, stale, or unresolved; independently check any cited specification or example, and assess whether the proposed repair is necessary, sufficient, and smaller than the defect. Reject preferences without a violated criterion and replace defective steps rather than appending contradictory patches. If repeated review misses expose a defective rubric, prompt, or evidence request, repair the review method before adding another reviewer.

## 4. Delegate, execute, join, and track

Each assignment uses the [canonical packet](references/planning-delegation-and-joins.md) plus applicable [role text](references/role-packets-and-messages.md). It names outcome, motivation, revisions, requirements, context/evidence, node/dependency/peer IDs, scopes, joins, deliverable/result contracts, acceptance, limits, stop, and return conditions. Copy the canonical `result_contract` unchanged; reject packets with missing fields or altered contract text. Recovery adds checkpoint, trusted/quarantined/forbidden state, and restoration proof. Tell workers to preserve others' work and report peer output conflicting with the contract, direct evidence, or owned boundary. Send specialists the packet and relevant reference directly; never make them reconstruct it.

For concrete code proposals, repairs, forensic findings, reviews, or handoffs, require revision-verified `file:symbol:minline-maxline` coordinates, before/after blocks or insertion points, and rationale when needed for implementation or audit. Otherwise state why omitted.

Every node returns `result_state`: `complete` includes the assigned artifact, passing acceptance check results, and evidence, pending orchestrator acceptance; `partial` includes a safe subset, omitted scope, limit, and next action but cannot satisfy a complete requirement; `blocked` or `failed` includes the failed check, condition, affected requirements, and recovery; `recovery_required` quarantines untrusted output. Prefer bounded recovery; never disguise empty or incomplete output as complete.

Before activating a node or allowing its side effects, require every dependency to have `execution_state=done`, orchestrator acceptance of the current contract/input/output revisions, and an acceptable `result_state`: `complete`, or `partial` only when the active contract explicitly permits that bounded result. Otherwise do not start the dependent node; return `blocked` with the failed dependency IDs, `failure_reason`, and `recovery_action`.

Launch parallel nodes only when no dependency path connects them, shared inputs are stable, resolved write targets and side effects are disjoint, and their checks can succeed independently. If the host cannot isolate or verify write ownership, serialize the nodes under one causal owner. If concurrency is unavailable, run the same nodes sequentially without changing ownership or joins. Join all required branches before integration; the synthesis preparer normalizes completeness, provenance, conflicts, and limits, while the orchestrator performs and accepts the final synthesis.

On Standard/Full routes, run the trackkeeper check at each event, plan adoption, delegation, join, checkpoint, gate, and resume. Record the checked boundary, reviewer, revision, evidence, and finding or no-finding result in the existing ledger. The orchestrator may run the same checks anytime; trackkeeping supplies independence, not an exclusive capability. On Full routes with delegation, assign a dedicated read-only trackkeeper to audit orchestrator and worker behavior against the ledger and direct evidence. It neither corrects workers nor implements. Otherwise run a distinct ledger pass, record its weaker independence, and keep the finding contract.

A material control finding names `finding_id`, `actor_under_review`, `observed_contract_revision`, affected requirement and node IDs, the violated criterion, direct evidence, severity, affected side effects, recommended route, clearance check, and gate scope. The orchestrator records `accepted`, `rejected_with_evidence`, `duplicate`, `stale`, or `unresolved`; the trackkeeper returns recheck evidence and a clearance recommendation, which the orchestrator records and routes. For an accepted finding, update the contract or graph first, then have the orchestrator send affected workers a revisioned correction packet naming the superseded instruction, stale-output handling, next check, and required acknowledgement. An unresolved high or critical finding blocks only the affected action; a critical safety, permission, integrity, or destructive-side-effect finding pauses that side effect before execution.

Before requesting user input, reproduce the problem from direct evidence, test the blocking assumptions, and gather permitted local or current external information. Apply Project Manager (PM) reasoning: restate the outcome and motivation, inspect requirements and precedent, distinguish decisions required now from deferrable ones, prefer a conventional reversible default that preserves intent, and test whether one option dominates for the accepted workflow. Then use the smallest safe resolution: clarify from evidence, run a targeted experiment, replan, recover, restart a faulty worker, or use a one-shot evidence-based adjudicator with no implementation authority. Incomplete analysis, low confidence, or agent disagreement triggers these checks again; it does not create a user decision. Ask only after evidence shows that progress requires user-only authority or information, or a consequential choice has no intent-preserving safe default.

Checkpoint before risky transitions and at strong progress points when persistence is warranted. Before replacing a durable plan or note, preserve a recoverable prior state, cross-reference changed and removed factual claims or requirements, and restore verified current information lost by the edit. If Git commits are authorized, commit only a coherent, checked join owned by this work; a commit is a recoverable checkpoint, not proof of readiness.

## 5. Verify, cold read, and gate

Use the cheapest falsifiable domain-native oracle for every affected requirement: focused tests, direct live interaction, render/screenshot, protocol trace, data invariant, benchmark, or recorded artifact. Verify the real user/runtime surface; “visual” evidence may be literal for GUIs, TUIs, or documents and analogous direct observability for protocols, data flows, or resource behavior. Dogfood the current supported build through every applicable interface path with real parameters before turning observed defects into TDD cases, then keep the fixes on the causal critical path.

At affected gates, check assumptions and for regressions; route lifecycle/cleanup, threading/multiprocess, exact performance bounds, portability/platforms, cross-surface parity, academic integrity, docs, newcomer use, and release. For portable outcomes, record the target matrix, prefer a common path, isolate demonstrated adapters, verify parity, and never infer support from one surface. When streamlining prose or workflows, preserve a recovery point and atomic fact index; afterward restore against the index and conversation, reread the whole file, inspect every removed diff segment, and repeat after fixes. Then run AI-tell, newcomer, and applicable accessibility checks. Cold-read costly-to-misunderstand artifacts. Treat reviewers as evidence; adjudicate and rerun only affected gates.

Before `DONE`, complete a proportionate post-mortem for every successful Standard or Full outcome. Record the outcome against the contract, surprises, evidence gaps, and reusable lessons; complete required corrective work; map follow-up actions to a new epoch or record their explicit disposition. Required corrective work satisfies an in-scope requirement or repairs a defect in in-scope agent-owned output; treat it as a failed readiness criterion. Other lessons require follow-up disposition, not automatic scope expansion. This does not replace the action-mapped failure post-mortem in recovery.

`READY` means every in-scope requirement except release execution and post-release checks has direct proof and disposition; required checks pass; no critical/high finding is unresolved; conflicts, limitations, recovery state, newcomer behavior, and agent-owned changes are explicit. A required partial result blocks full readiness unless the active contract explicitly defines that bounded partial result as success. `RELEASE` is a separate authorized action and gate. If release is out of scope, complete closeout and finish at `DONE`. Every `RELEASE` action requires explicit user permission covering the action, artifact, and target; reuse prior permission while its scope covers the current release. Reuse verified release evidence for the same artifact and target instead of releasing it again. If permission is missing, remain `READY` and report the authorization needed. Preparing until ready does not authorize release.

## 6. Recover when work goes off the rails

On contradiction with source evidence, repeated drift, unsafe mutation, corrupted state, or increasingly unreliable claims: stop or pause the affected branch; checkpoint trusted state; quarantine its output as untrusted; determine the earliest unsupported finding, decision, or edit and stale its descendants; restore or reconstruct affected shared state from the last trusted artifact and verify its fingerprint or invariant; then preserve unaffected nodes. If trusted restoration is unavailable, stop with the missing recovery input. Choose repair-in-place only when the fault is bounded and state is trustworthy; otherwise use a fresh worker with a smaller recovery packet and independent check. If the orchestrator is the drifting actor, route the trackkeeper finding through disposition, the affected-action gate, and autonomous adjudication; do not let the orchestrator silently self-clear it. After a verified failure and recovery, record a proportionate post-mortem with the timeline, root cause, contributing factors, detection and recovery gaps, direct proof, and recurrence controls. Map each action to a requirement, plan node, check, or recovery instruction, or record why it is closed. If the host cannot cancel work, ignore its later output and mark it stale. Never expand permissions merely to recover.

</workflow>

<output_contract>

Fast returns the artifact, focused check, and material limitations. Standard/Full add the requirement-evidence-check trace; routing changes; dependencies, ownership, joins; finding dispositions/rechecks; results; risks; recovery; terminal gate; and initial-versus-agent-owned state. Keep notes actionable—what advances the outcome, not an activity log. If user input is required, report assumptions tested, evidence inspected, remedies attempted, safe default, residual decision, and why acting would change scope or risk user state.

For external material retain title, author/organization, direct URL, access date, supported claim, and limitations. Distinguish quotation, paraphrase, inference, and generated text; follow applicable citation, attribution, licensing, disclosure, and academic-integrity rules; never fabricate sources or present generated work as original human research. Before public output, redact personal names, local paths, provider/session identifiers, secrets, and unrelated transcript content. Keep exact user wording in private evidence notes unless quoting it is authorized and safe.

Package or runtime validation reports measured instruction size, references read, and relevant tool/runtime cost; label unknowns. Claim host support only after testing discovery, activation, reload, reference loading, behavior, and duplicate handling there.

</output_contract>

<examples>

## Examples

- Fast: “Fix this spelling mistake.” One owner, one edit, one focused check; no ledger file, agents, or cold read.
- Full: “Research the mechanisms, plan and refine, coordinate independent agents, preserve my corrections, cold-read the result, and continue until the evidence gates pass.” Use the directed lifecycle and work cycle; keep each epoch's activation dependencies acyclic.
- Correction: “Wait—do not touch that file; the supported platforms include mobile and desktop.” Pause affected nodes, update scope/permissions, stale descendants, preserve independent work, and replan from the earliest affected state.

</examples>
