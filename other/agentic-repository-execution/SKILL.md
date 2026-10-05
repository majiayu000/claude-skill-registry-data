---
name: agentic-repository-execution
description: Coordinate repository implementation through a master agent that discovers local rules, persists a scoped plan, delegates every production-file change to sub-agents, enforces authority boundaries, escalates material uncertainty, and closes evidence-based validation gates. Use when the user asks for delegated or multi-agent repository execution, a master/sub-agent workflow, staged autonomous implementation, parallel work with conflict control, or strict independent review of agent-written changes.
---

# Agentic Repository Execution

## Purpose

Run repository-changing work as a governed delegation system. Keep the master
agent responsible for understanding, decomposition, dispatch, review, and
validation while sub-agents make every code or production-file change.

Protect against vague oversized assignments, conflicting parallel edits,
context loss between phases, invented capabilities, weak validation evidence,
an unreadable coordination site after execution, and a master silently taking
over implementation.

## Boundaries

- Use this procedure for implementation work that can be delegated through the
  current runtime.
- Do not use it for a simple answer, translation, isolated read-only question,
  or task where multi-agent governance adds no execution value.
- Do not use it to turn every small task into many assignments. Give a bounded
  low-risk change to one implementation agent when that is the smallest useful
  delegation.
- Do not replace the repository's `AGENTS.md`, task graph, issue tracker,
  durable-memory convention, or user-specified coordination location.
- Keep this a repository execution protocol. Do not turn it into an Agent
  Operating System, workflow engine, scheduler, or persistent runtime service.
- Do not let the master edit code, tests, configuration, migrations, public
  documentation, or other production deliverables. Allow the master to write
  only coordination artifacts in an approved local convention.
- Keep agent creation, dispatch, re-dispatch, and ownership assignment with the
  Root Master. Do not let a worker, reviewer, validator, or remediation agent
  create a child agent or transfer its production responsibility.
- Do not claim delegated execution when the runtime cannot start sub-agents.
  Report `BLOCKED` instead of letting the master implement as a fallback.
- Do not treat this skill as permission to commit, push, publish, deploy, or
  perform destructive actions. Require the authority applicable to each action.
- Do not let a worker or the master expand scope, compatibility, data,
  security, infrastructure, or side-effect authority merely to finish.

## Inputs

Infer these inputs from the latest user instruction and repository evidence
before asking:

- target repository, branch, worktree, and requested outcome;
- scope, non-goals, acceptance criteria, and side-effect authority;
- repository instructions, ownership boundaries, public hygiene rules, and
  durable coordination conventions;
- explicit user- or repository-selected conventions that must remain frozen,
  such as canonical domain terms, visibility and naming rules, import roots or
  forms, formatting limits, declaration grouping, and compatibility aliases;
- for mechanical transformations, the exact symbol or artifact categories in
  scope and the categories that must remain unchanged;
- available sub-agent controls, models, reasoning efforts, skills, tools, and
  validation commands;
- dirty-worktree state and files that must not be touched;
- dependencies, risky surfaces, and serial versus parallel work.

Ask only when an unresolved choice would materially change scope, behavior,
target, or authority. Stop when the repository or user requires an input that
cannot be inferred safely.

## Evidence Hierarchy

Resolve conflicts in this order:

1. Follow the user's latest explicit instruction and side-effect boundary.
2. Follow applicable repository instructions and governance files.
3. Trust current code, tests, schemas, configuration, task graphs, and version
   control state.
4. Trust validation output, runtime observations, and generated diffs gathered
   for this task.
5. Use current repository docs, handoffs, decision traces, and existing skills.
6. Use current tool or platform documentation when runtime behavior depends on
   it.
7. Use naming conventions and inference only after checking stronger evidence.

Never let a stale plan, old handoff, model assumption, or remembered skill name
outrank inspected current state.

## Autonomy Principle

Make autonomy the default inside every authorized assignment. Give the worker
ownership of all normal engineering decisions within the assigned behavior and
contract, owned surfaces, side-effect limit, and non-goals. Let the worker
decide naming, internal code structure, helper extraction, local abstraction,
test organization, and implementation strategy when the result can be verified
locally without changing external or business meaning.

Treat an explicit user or repository choice as a frozen constraint, not as an
implementation option delegated to the worker. Worker autonomy applies only
after those constraints are satisfied. Do not replace a configured local
convention with a generic ecosystem preference merely because both are valid.
For a mechanical rename or rewrite, enumerate the permitted symbol or artifact
categories and preserve every excluded category literally.

Do not escalate merely because multiple reasonable implementations exist, a
technical tradeoff is subjective, or the master did not preselect an approach.
Inspect the evidence, choose a defensible option, validate it, and continue.
Escalate only when the choice may change business or domain semantics,
architecture boundaries, system ownership, long-term component responsibility,
public contracts, data meaning, security boundaries, irreversible behavior, or
existing scope, side-effect, or decision authority. Treat internal module
splits, class extraction, and local refactors as normal engineering decisions
when those boundaries and meanings remain unchanged.

## Decision Escalation And Stop Contract

Classify risk and uncertainty before dispatch and whenever new evidence changes
the task:

- Resolve **routine uncertainty** from current evidence, repository convention,
  and existing authority. Choose a defensible option among one or more
  reasonable implementations when it stays inside the assignment boundaries,
  the mutation is reversible or recoverable within the authorized side-effect
  boundary, and the choice can be verified locally without changing behavior or
  contract. Continue without approval; record the choice when it constrains
  later work.
- For **material uncertainty**, make the worker pause the affected slice and
  complete the linked Decision Request. Before treating the escalation as raised
  or ready for master review, require the worker to emit or persist every field
  of that form. Use a safe coordination location when available; otherwise
  output the complete record in the worker response. Merely saying a record
  should be created is incomplete, and the affected slice remains paused. Do not
  silently choose among reasonable options that may change business or domain
  semantics, architecture boundaries, system ownership or long-term component
  responsibility, public behavior or compatibility, data integrity or
  migration, security or trust, external side effects, irreversible behavior,
  or the assignment boundary.
- Make the master first apply the task context and Evidence Hierarchy to resolve
  material engineering or design choices within the user's original authority.
  Ask the human only when the decision still lacks required business or user
  authority, or evidence. Do not widen scope or authority, or choose an
  arbitrary assumption because of time pressure or a desire to finish.
- When a material decision still lacks evidence or authority, require the master
  to emit or persist every field of the linked Stop Record before treating the
  decision-related gate as `BLOCKED`. Persist it at a safe coordination location
  readable by the next agent when available; otherwise output the complete
  record in the master response. Merely saying a Stop Record should be created
  does not close the gate or stop path. Then stop dependent work and ask the
  human one concrete question.
- Stop the whole task when the blocker affects the root objective, a shared
  authoritative contract, data integrity, security or trust, irreversible
  behavior, or assumptions that would contaminate every branch. Otherwise stop
  only the affected dependency branch; independent safe work may continue.

Treat human escalation and Evidence Gates as different paths. An Evidence Gate
means execute-and-prove under existing authority; it is not default
ask-first approval. Risk level controls decomposition, routing, review, and stop
intensity, but never grants authority; a Low-risk action may still be
unauthorized.

Read
[escalation-and-stop-policy.md](references/escalation-and-stop-policy.md)
before classifying non-routine uncertainty, assigning Medium, High, or Critical
risk, or resolving a Decision Request. Use the Decision Request and Stop Record
forms in [execution-templates.md](references/execution-templates.md).
Require these forms only for material or blocking decision escalation, not for
routine uncertainty or an ordinary validation `FAIL`.

## Master Contract

Keep these responsibilities with the master:

- interpret the request and maintain scope;
- discover repository rules and available execution capabilities;
- persist and update the execution plan;
- choose task boundaries, order, ownership, and gates;
- create and dispatch every bounded peer assignment with a complete contract;
- resolve worker Decision Requests only within existing authority, or escalate;
- inspect returned artifacts, diffs, and validation evidence;
- re-dispatch missing or insufficient work;
- perform the final integrated review;
- leave the approved coordination location readable and recoverable for the
  next agent;
- report status.

Keep delegation depth at one: make every worker, reviewer, validator, and
remediation agent a peer dispatched directly by the Root Master. Permit workers
to submit a Delegation Request when a newly discovered, separable responsibility
needs another owner; never permit them to spawn or dispatch that owner.

Read
[agent-hierarchy-policy.md](references/agent-hierarchy-policy.md)
before dispatching or re-dispatching agents, assigning ownership, or processing
a Delegation Request. Use its request lifecycle without treating delegation as
human escalation or granting the master production-file write authority.

Delegate all implementation and production-file edits. Do not reinterpret a
sub-agent timeout, silence, partial response, or unsupported capability as
permission for the master to write the missing change.

## Workflow

### 1. Discover Before Planning

Inspect the repository root, applicable instruction files, current branch and
worktree state, existing task or memory conventions, relevant skills, tools,
tests, and validation entry points.

Extract explicit conventions and canonical domain terms from the user request,
repository configuration, public contracts, and current authoritative code.
Record them as frozen constraints before dispatch. When import form or module
layout is in scope, identify the supported invocation modes and import roots;
do not infer them from the current working directory or from one ad hoc script
execution.

Before planning or dispatching work that crosses component boundaries or
handles extensible schemas, configuration, messages, or payloads owned outside
the component being changed, run the **Concept Authority And Validation
Boundary Gate** in
[concept-authority-and-validation-boundary.md](references/concept-authority-and-validation-boundary.md).
Use it to identify the concept owner and canonical source, decide whether each
consumer should interpret or treat the data as opaque, separate generic
boundary validation from owner-defined semantics, and simulate the change
surface of a new valid variant. When triggered, require the gate to reach
`PASS` before any production edit or implementation dispatch. Use a Decision
Request when the owner, source, or responsibility boundary is materially
uncertain; do not let workers resolve that uncertainty by duplicating semantic
rules locally.

Use repository-native code discovery before broad text search when available.
Scan the runtime's actual skill inventory before recommending skills. Never
invent a skill, model, reasoning effort, or tool.

Confirm that sub-agent execution is available. If it is unavailable and the
task requires production changes, stop with `BLOCKED`.

### 2. Persist The Execution Plan

For non-trivial work, write the plan before production changes. Use the
user-specified or repository-defined coordination location. Otherwise, prefer a
simple ignored `.manifest/<task>/execution-plan.md` when the repository permits
it.

Do not create a complex `.manifest` hierarchy silently. If `.manifest` is
tracked, prohibited, or conflicts with local governance, use the existing
agent-memory or task convention instead.

Record goal, scope, non-goals, expected artifacts, task graph, ownership,
validation gates, risk classification, authority and side-effect boundaries,
the concept-authority gate when triggered, stop conditions, and current status.
Use the plan form in
[execution-templates.md](references/execution-templates.md).

For non-trivial serial or recovery-prone work, the Root Master may also maintain
one replaceable `<coordination-root>/execution-state.json` snapshot. Keep it
optional for small coherent tasks. Read
[execution-state-and-recovery.md](references/execution-state-and-recovery.md)
before creating, updating, reconstructing, or resuming from that snapshot.

### 3. Size And Decompose The Work

Choose the fewest assignments that preserve clear responsibility and
independent validation. Evaluate behavior risk, change breadth, uncertainty,
integration coupling, file overlap, and side effects.

- Give a small localized change to one implementation agent.
- Split medium work by coherent responsibility, risk, or independently
  verifiable outcome.
- Split large work into discovery or contract work, bounded implementation
  slices, integration, and independent validation.

Do not split by file count alone. Do not give one agent a broad instruction such
as "implement the whole feature" when the work crosses unclear responsibilities
or validation domains.

Classify each assignment as Low, Medium, High, or Critical using
[escalation-and-stop-policy.md](references/escalation-and-stop-policy.md).
Use the level to strengthen decomposition, routing, review, and stop gates, not
to infer permission.

Read [task-decomposition-and-handoffs.md](references/task-decomposition-and-handoffs.md)
before dispatching medium, large, serial, or parallel work.

Before parallel dispatch, forecast whether two or more slices implement the
same concept or contract and therefore form a **convergence set**. Do not infer
a convergence requirement from superficial similarity alone. For each set,
record its members and affected surfaces, shared invariant, required level,
trusted reference or comparator, allowed variation, integration point, and
review owner:

- **Semantic:** observable behavior and invariants converge; internal structure
  may vary.
- **Structural:** selected interfaces, types, lifecycle shape, organization, or
  other named structure converge; implementation details outside that shape may
  vary.
- **Exact:** the selected artifact or representation matches a defined
  comparator exactly; explicitly bound the exact surface so unrelated details
  remain autonomous.

When Structural or Exact convergence has no trustworthy existing reference,
schedule a serial reference-first or contract-first assignment and hold its
gate before dispatching the dependent parallel slices. Prefer no convergence
set over a speculative one, and keep one coherent worker for low-risk local
work when parallel governance adds no value. Use the convergence guidance and
forms in the linked decomposition reference and execution templates.

Treat implementer-run checks as author checks or implementation evidence, not
independent Validation. Read
[independent-review-policy.md](references/independent-review-policy.md) before
choosing an assurance path or dispatching Review or Validation. Low risk
normally uses independent Validation without a reviewer; Medium defaults to
Independent Review then Validation; High and Critical require different peers
for those two assurance roles.

### 4. Route And Dispatch

For every assignment, state:

- Goal
- Scope
- Non-goals
- Expected artifacts
- Validation
- recommended model
- recommended reasoning effort
- recommended skills

Also state owned files or surfaces, dependencies, required inputs, side-effect
limits, risk level, authority boundary, escalation path, and the handoff path
when relevant. For a slice in a convergence set, include the set ID, level,
invariant, reference or comparator, allowed variation, and integration/review
condition. Include frozen conventions and, for a mechanical transformation,
the permitted and excluded symbol or artifact categories. State that
delegation authority belongs to the Root Master, that the dispatched agent may
not create child agents, and where it may submit a Delegation Request.

Read [model-and-effort-routing.md](references/model-and-effort-routing.md) before
recommending execution settings. Name only models and effort values advertised
by the current runtime. If a preferred setting is unavailable or inadequate,
apply the linked fallback ladder and record the substitution. Never let
fallback weaken risk, acceptance, authority, side effects, assurance
independence, or required proof.

Use the dispatch form in
[execution-templates.md](references/execution-templates.md). Treat the
recommendations as routing guidance, not as claims that unavailable settings
can be selected.

When an assignment would introduce substantial custom validation, parsing,
serialization, retry, protocol, lifecycle, or other framework-like machinery
around an existing dependency, require the assignment to inspect the detected
version and public extension points and make an evidence-backed choice among
exact reuse, a thin public-extension adapter, and a focused custom
implementation. Do not mandate reuse when existing components bundle unrelated
behavior or impose a larger integration and test surface, and do not accept
custom machinery merely because it is quicker to generate.

### 5. Execute With Ownership And Handoffs

Run independent assignments in parallel only when their write ownership does
not overlap and neither depends on the other's unreviewed output. Prefer serial
work when agents would edit the same file, change the same contract, or consume
the same evolving state.

Do not let parallel members invent separate versions of a forecast convergence
contract. Make every member consume the same trusted reference or the gated
output of the reference-first assignment. Preserve autonomy for all choices
listed as allowed variation.

Require a handoff at every serial phase boundary. Make the next agent read the
previous handoff before starting. Require each handoff to list completed work,
changed artifacts, decisions, validation results, remaining risks, and exact
next instructions.

A handoff may include `Confidence: Level/Basis` as navigation metadata. It is
not evidence, assignment state, an Evidence Gate, or permission for dependent
work.

Do not use chat memory as the only handoff for durable multi-stage work.

Accept a worker Decision Request only after every field of the linked form has
been emitted or persisted. Keep the affected slice paused while the record is
incomplete and while the master inspects its cited evidence. Record the master's
bounded resolution and rationale, then re-dispatch. If the master cannot resolve
it within current evidence and authority, apply the stop contract instead of
guessing.

Accept a Delegation Request only as a control-plane proposal. Make the master
approve, deny, merge, narrow, or defer it. On approval, update the task graph,
ownership, dependencies, and gates before the Root Master creates the new peer
agent. Continue the requester's authorized work when the proposed responsibility
is independent; pause only the affected slice when it is a necessary dependency.
Do not turn the request into a human escalation, Decision Request, new gate
state, or automatic `BLOCKED`.

### 6. Hold Evidence Gates

Use exactly four gate states:

- `NOT RUN`: no validation attempt has occurred; keep the gate closed and do
  not start dependent work.
- `PASS`: verify all required evidence; only this state permits dependent work
  to start.
- `FAIL`: evidence proves that a requirement is unmet; keep the gate closed,
  assign narrow remediation, and revalidate.
- `BLOCKED`: required evidence cannot be obtained or verified, or a required
  capability or input is missing; keep the gate closed, resolve the blocker or
  re-dispatch, and revalidate.

Apply this model to every gate in the linked references and templates. Choose
`FAIL` only when verified evidence proves noncompliance; choose `BLOCKED` when
the required evidence cannot be obtained or verified. Do not introduce another
gate state. Inspect the actual files and diff; do not accept a completion claim
by itself.

After integrating a forecast convergence set, dispatch a read-only
**Convergence Reviewer** to compare every member against the recorded invariant,
level, reference or comparator, and allowed variation. This is a focused
Independent Review and uses an ordinary Evidence Gate; it is not another gate
state or a substitute for Validation. The same peer may own the broader
Independent Review when the assurance policy permits and both reviews inspect
the same unchanged revision.

On convergence `FAIL`, make the Root Master dispatch a bounded remediation
implementer who is not the reviewer or validator for the affected revision.
After remediation, rerun the convergence review and every affected downstream
Review and Validation gate against the new revision. A Convergence Reviewer who
edits the artifact becomes an implementer and loses reviewer independence for
that revision.

Do not mark a gate `BLOCKED` merely because a routine engineering judgment was
needed. Use `BLOCKED` for a material decision that the master cannot resolve
from available evidence within existing authority, or for another missing
required capability, input, or proof.

If an agent does not return, returns partial work, crosses scope, or supplies
insufficient evidence:

1. record `FAIL` when evidence proves noncompliance, otherwise record `BLOCKED`;
2. preserve usable evidence;
3. narrow the missing responsibility;
4. re-dispatch that bounded responsibility;
5. rerun affected validation.

Never count absent evidence as success. Never widen a re-dispatch merely to
avoid another coordination step.

When execution-state is active, reconcile it against the plan, current
worktree, artifacts, diffs, and evidence before resuming. Treat `active` or
`complete` as lifecycle history, never as gate success or proof of liveness.

### 7. Perform The Master Final Review

After every assignment gate is `PASS`, inspect the integrated working tree and
verify:

- requested behavior and artifacts are present;
- scope and non-goals were preserved;
- every triggered concept-authority gate passed, and no component became an
  unrecorded semantic owner by duplicating another owner's extensible rules;
- no parallel ownership conflict or unreviewed overwrite remains;
- every forecast convergence set passed review against its recorded contract;
- substantial custom machinery around an existing dependency passed the
  reuse-versus-focused-custom check, when applicable, with required and
  explicitly unwanted behavior covered by evidence;
- repository tests and required checks passed;
- checks in `NOT RUN` or `BLOCKED` are explicit;
- public files contain no credentials or private identifiers;
- no unrelated user change was staged, reverted, or overwritten;
- commit, push, publication, deployment, and destructive boundaries remain
  within explicit authority.

Keep the final gate closed when integrated evidence is incomplete, even if every
individual agent reported success.

The Master final integrated review closes the control plane. It does not replace
a required peer Independent Review.

### 8. Close The Coordination Site

Before the completion report, inspect the task's approved coordination location
and leave it understandable without relying on chat history. Apply this step to
`COMPLETED`, `PARTIAL`, and `BLOCKED` outcomes. It is control-plane hygiene, not
a new Evidence Gate, and it must not change an existing gate result.

Use the repository-defined or user-approved coordination convention; do not
assume a directory name. When the skill created or used durable coordination
artifacts, make the smallest useful update needed to expose:

- the task purpose, final outcome, and current applicability;
- the authoritative entry point and a short reading order;
- the relationship from historical `FAIL` or `BLOCKED` evidence through
  remediation and revalidation to the latest result;
- current authority versus plans, handoffs, validation evidence, superseded
  material, and remaining debt;
- related predecessor, successor, or dependent tasks when those relationships
  affect interpretation;
- restricted areas such as credentials, backups, logs, database snapshots, or
  binary artifacts that must be read only when the task requires them.

Prefer updating or adding a small navigation index over moving or rewriting
evidence. Preserve stable paths when handoffs, hashes, publication manifests,
external references, or historical provenance depend on them. Do not rename,
deduplicate, delete, sanitize, archive, or rewrite historical artifacts merely
to make the directory look tidy. Those actions require their own authority and
validation.

The Root Master may edit coordination artifacts permitted by the Master
Contract. Continue to delegate any cleanup that changes code, tests,
configuration, migrations, public documentation, or other production
deliverables. Treat repository-wide documentation reorganization as separate
work rather than silently expanding task closure.

If the coordination site is already legible, record that no structural change
was needed. If no durable coordination location was used, report that fact and
do not create one solely for cosmetic closure.

## Validation

Define observable gates before implementation starts. Use repository-native
tests, linting, type checks, builds, schema validation, dry-runs, rendered
previews, or manual inspection appropriate to each artifact.

Keep implementer author checks in implementation evidence. Assign independent
Validation to a different owner, except that the Root Master may perform
eligible read-only, reproducible Low-risk Validation under the linked policy.
If a reviewer or validator edits a production artifact, that peer becomes an
implementer for the new revision and another eligible peer must rerun affected
assurance gates.

Require each gate record to contain:

- expected evidence;
- exact command or manual check;
- owner;
- result: `NOT RUN`, `PASS`, `FAIL`, or `BLOCKED`;
- artifact or output location;
- remaining uncertainty.

When imports, entrypoints, or module layout change, validate every supported
invocation mode defined by the repository, such as an installed console entry,
module execution, or direct script execution only when direct execution is an
actual contract. Do not treat success from a modified working directory or an
ad hoc `PYTHONPATH` as proof of the packaged execution contract.

Rerun integration checks after combining parallel work. Run diff and
scope-boundary review even when automated tests succeed. State every skipped
check and why.

## Output Contract

Return a concise completion report containing:

- outcome: `COMPLETED`, `PARTIAL`, or `BLOCKED`;
- delegated assignments and ownership;
- files or artifacts changed;
- coordination entry point and any closure updates, or confirmation that none
  were needed;
- validation commands and results;
- non-`PASS` gates, risks, and skipped checks;
- side effects performed and explicitly not performed;
- exact next action when work remains.

Keep durable execution artifacts at the approved coordination location. Do not
include hidden reasoning, raw credentials, private payloads, or unsupported
success claims.

## Side-Effect Policy

Default to `read-only` discovery and planning. Reach at most
`git-working-tree` in normal use, and only after the user requests repository
implementation. Delegate working-tree edits; preview broad changes through the
plan and inspect the diff before closure.

Require separate explicit authority for staging, committing, branch changes,
pushing, PR or MR creation, deployment, publication, and destructive action.
This skill does not grant those permissions. Preserve unrelated dirty work and
never place credentials in dispatches, handoffs, logs, public files, or final
reports.

## Failure Modes

- **No sub-agent capability:** record the affected gate as `BLOCKED`; do not let
  the master implement.
- **No safe coordination location:** use the existing repository convention or
  ask when placement materially affects version control or privacy. Record
  `BLOCKED` when no safe location can be resolved.
- **Ambiguous target or authority:** resolve routine ambiguity from stronger
  evidence; for material ambiguity, request a master decision. Record `BLOCKED`
  and ask the human only when the master still lacks evidence or authority.
- **Unavailable or inadequate model, effort, skill, or tool:** apply the linked
  fallback ladder, use an equivalent only when it produces the same evidence
  without broader side effects, and record the substitution. Record `BLOCKED`
  if no adequate capability remains.
- **Overlapping parallel ownership:** pause the conflicting assignment, inspect
  the shared state, record the affected gate as `BLOCKED`, then serialize or
  redefine ownership.
- **Cross-slice divergence:** record the convergence gate as `FAIL`, dispatch a
  bounded remediation implementer separate from the reviewer and validator,
  then rerun convergence review and affected downstream Review and Validation.
- **Missing handoff:** record `BLOCKED` and request or reconstruct the handoff
  from verified artifacts through a bounded agent task.
- **Agent timeout or incomplete evidence:** record `BLOCKED`, narrow and
  re-dispatch; do not infer completion.
- **Validation failure:** record `FAIL`, assign diagnosis or remediation, and
  rerun the failed and integration checks.
- **New independent responsibility discovered:** keep authorized work moving
  and submit a complete Delegation Request; do not spawn, dispatch, or transfer
  ownership from the worker.
- **Private data in artifacts:** stop publication or registration, sanitize the
  public surface, record the affected gate as `FAIL`, and revalidate.
- **Scope expansion discovered:** preserve completed in-scope work, pause the
  affected slice, and send a Decision Request. Because the master cannot grant
  new authority, record `BLOCKED` and ask the human before expanding.
