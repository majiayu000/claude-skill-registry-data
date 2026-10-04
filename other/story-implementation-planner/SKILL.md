---
name: story-implementation-planner
description: Create a constraint-aware implementation plan from a Ready Story Card and sufficiently evidenced Repo Context. Use when the requested artifact is the plan itself; use story-to-plan-orchestrator for multi-stage preparation, packet completion, resumption, or validation. Avoid story drafting, repo scouting, and direct implementation.
---

# Story Implementation Planner

Own the `Implementation Plan` artifact. Turn an implementation-ready story and
repo evidence into an executable plan for a named or described executor without
clarifying the story, scouting the repository, assembling a packet, or editing
code.

## Activation Contract

Use this skill only when all of these are true:

- the requested output is an implementation plan;
- the input is one materialized active Story Card, not a Split Story Set, with
  `Artifact Type: Story Card`, `Status: Ready`, observable acceptance criteria,
  and a settled implementation boundary;
- Repo Context contains enough evidence to locate the existing implementation,
  validation surface, and any convention needed for proposed files;
- every planning-critical external claim, when present, has current and
  applicable primary-source support in Repo Context `External Evidence`; and
- executor constraints are known or can be stated conservatively without
  changing the required behavior or safety policy.

Use `story-to-plan-orchestrator` when the request spans clarification, scouting,
planning, packet assembly, readiness validation, or resumption. Use
`story-clarifier` for unresolved product behavior and `story-repo-scout` for
missing, weak, or stale repository evidence. Do not perform those stages here.
A ready Split Story Set still requires slice selection and materialization by
the orchestrator before it becomes valid planning input.

If this skill is invoked with inadequate inputs, return the supported portions
of the artifact with a non-ready status and route the missing work to its owner.
Do not fill gaps by guessing.

## Status Contract

Every output starts with:

```markdown
## Implementation Plan

Artifact Type: Implementation Plan
Status: Ready | Needs Input | Blocked
Reason: None | <concise readiness reason>
```

Use the statuses operationally:

- `Ready`: the plan is executable as written and has no unresolved blocking
  input; write `Reason: None`.
- `Needs Input`: a specific answer, upstream revision, or re-scout can make the
  plan executable. Name each missing input, its owner, and the next action; do
  not write unsupported downstream steps.
- `Blocked`: a hard dependency or constraint prevents an honest plan and the
  required input cannot currently be obtained through the preparation
  workflow. Name the evidence, unblock condition, and safe stopping point.

Risks are uncertainties the ready plan can manage. Blocking inputs prevent the
plan from being ready; never combine them in one list.

Return the plan in the conversation unless a file output was requested. A plan
request does not authorize implementation or mutating verification commands.

## Core Workflow

1. Read the complete active Story Card and Repo Context. Confirm that the story
   artifact is one materialized `Story Card`, not a `Split Story Set`, and
   preserve its source, acceptance-criterion identifiers, Out of Scope,
   authoritative constraints, dependencies, assumptions, open questions, and
   Validation Notes.
2. Check readiness before planning. Treat behavior-changing ambiguity,
   conflicting upstream evidence, stale critical paths, missing validation or
   file-convention evidence, and missing, conflicting, or version-mismatched
   material external evidence as inputs to resolve, not planning latitude.
3. Record the target executor and the constraints that affect plan shape:
   autonomy, context capacity, tool access, parallelism, and checkpoint needs.
4. Define the evidence and file boundary from Repo Context. Apply the detailed
   path, external-evidence, and authoritative-boundary trace rules below.
5. Describe the scope and risk drivers: behavior surfaces, subsystem breadth,
   state or contract changes, integration points, evidence strength, blast
   radius, reversibility, and external coordination.
6. Decompose work into narrow end-to-end outcomes that are demoable or
   independently verifiable where practical; apply the vertical and enabling
   outcome rules below rather than forcing layer-only tasks.
7. Build and validate the outcome dependency graph as specified below. Make
   ownership, blockers, joins, and shared invariants explicit before claiming
   parallel work.
8. Choose delivery and recovery measures according to affected surfaces and
   risk. Apply the wide-change rule below when needed; do not add migration or
   rollout boilerplate automatically.
9. Map every acceptance criterion to validation using the smallest-sufficient
   observable-seam rules below.
10. Review the plan for unsupported paths or commands, placeholder work,
    dependency order, criterion coverage, unmanaged risk, and status accuracy.

## Executor Constraints

Describe capabilities, not model stereotypes:

- **Autonomy:** decisions the executor may make versus checkpoints requiring a
  person or upstream owner.
- **Context capacity:** how much cross-file state can be carried reliably and
  where re-entry summaries or smaller outcome batches are useful.
- **Tool access:** repository, build, test, network, deployment, or other tools
  available and unavailable.
- **Parallelism:** whether independent tracks can run concurrently and how they
  rejoin.
- **Checkpoint needs:** review, stop-and-report, or validation points required
  before risky or irreversible actions.

A named model or agent may be recorded as the executor label, but it supplies
no capability facts by itself. Use only constraints the user supplied or the
environment demonstrated. Unknown constraints do not justify weaker safety,
completeness, validation, or recovery. State neutral assumptions or request
input only when the missing constraint would materially change the plan.

Adapt presentation to the constraints: use narrower outcome batches and an
optional `First Action` for limited context or autonomy; include tool
preconditions or alternatives for limited access; and use parallel tracks only
when the executor can coordinate them safely. Do not impose arbitrary file or
step counts, and do not invent human time estimates.

## Output Contract

After the common header, use this structure:

```markdown
### Target Executor and Constraints
- Executor:
- Autonomy:
- Context capacity:
- Tool access:
- Parallelism:
- Checkpoint needs:

### Goal
The behavior and boundary this plan will deliver.

### Inputs
- Story Card:
- Repo Context:
- External primary evidence: None, or `EXT-*` - planning use.
- Accepted assumptions or decisions:
- Non-blocking open questions:

### Scope and Risk Drivers
- Scope drivers:
- Risk drivers:

### Files
- Existing Change: path - purpose; matching Repo Context evidence.
- Existing Read: path - decision or invariant; matching Repo Context evidence.
- Existing Validate: path - behavior or oracle; matching Repo Context evidence.
- Proposed Create: path - purpose; matching Proposed Paths entry and convention basis.
- Authoritative Do Not Edit: path or scope - source and basis.

### First Action
- Open:
- Do:
- Check:
- Stop if:

### Steps
1. `P1 - Stable outcome title` - deliver a narrow end-to-end, demoable or independently verifiable outcome.
   - Blocked by: None, or direct step IDs.
   - Ordered substeps when the outcome crosses layers or surfaces.
   - Checkpoint or observable result.

### Dependencies and Parallel Work
- Starting frontier: step IDs with no unsatisfied blockers.
- External prerequisites, safe parallel tracks, shared invariants, and join points.

### Risks
- Non-blocking uncertainty - mitigation, signal to watch, and contingency.

### Blocking Inputs
- Missing input - owner, next action, and unblock condition.

### Acceptance Criteria and Validation
| Acceptance Criterion | Planned Outcome | Validation Seam | Validation Evidence |
|---|---|---|---|
| AC-1 | Step ID or behavior | Existing observable seam | Supported command, probe, assertion, or oracle |

### Delivery and Recovery
- Delivery approach and why the affected surface and risk warrant it.
- Backout, rollback, restore, or forward-fix approach when needed.

### Handoff
- Starting context, decision checkpoints, and completion evidence to return.
```

Always include `Target Executor and Constraints`, `Goal`, `Inputs`, `Files`,
`Steps`, and `Acceptance Criteria and Validation` in a ready plan. Include
`First Action` only when it materially reduces ambiguity for a constrained
executor. Include `Blocking Inputs` only for `Needs Input` or `Blocked`; a
`Ready` plan cannot contain unresolved items there. Omit other empty optional
sections.

Preserve non-blocking questions from Ready upstream artifacts under Inputs;
also map one to Risks when its uncertainty needs a mitigation or contingency.
Any question that can change behavior, path selection, an authoritative
boundary, validation feasibility, or plan executability is a Blocking Input and
requires a non-ready plan instead.

Reference every planning-critical external claim under Inputs by its stable
Repo Context `EXT-*` ID and state only its planning use. Keep the owning source,
section, and applicable version in `External Evidence`. Missing support,
conflicting primary sources, or a material version or applicability mismatch
makes the plan non-ready and routes the gap to `story-repo-scout`; do not
silently resolve it in the plan.

List each path under its intended use and make its Repo Context trace explicit.
Every `Existing Read`, `Existing Change`, and `Existing Validate` path must map
to inspected `Existing Evidence`. Every `Proposed Create` path must map to a
scout-supplied `Proposed Paths` entry whose basis is an inspected parent,
sibling convention, manifest, registration point, or documented rule. A test
that must change belongs under `Existing Change`; it may also appear as
validation evidence. If a required path lacks that upstream evidence, make the
plan non-ready and route the gap to `story-repo-scout` instead of inventing it.
Use `Authoritative Do Not Edit` only for a boundary backed by the user,
repository instructions, ownership, generated or vendored-source policy, or
another explicit authority. Do not promote a scout's nearby non-target into a
hard prohibition.

Keep one stable, unique ID and title for each outcome while its identity is
unchanged. `Blocked by` names immediate plan-step IDs only; put external
prerequisites in `Dependencies and Parallel Work`. The starting frontier is
exactly the steps whose direct blockers and external prerequisites are
satisfied. A ready plan has no duplicate or unknown IDs, cycles, or hidden
blocking edges.

Prefer vertical outcomes. An enabling outcome must cite the evidence for the
coupling, required seam, or safety constraint it resolves and must itself have
an observable completion condition. For an evidence-backed wide mechanical
change that cannot land green vertically, model expand, migrate batches, and
contract as explicit outcomes with direct blockers and validation; add an
integration join and final verification when a batch cannot stand alone.

Treat discovery as a plan step only when its decision branches and exit evidence
are known. An unresolved material decision cannot be hidden in a step or
checkpoint unless the inputs explicitly delegate it to the executor and bound
the available choices, authority, and exit criteria. Otherwise make it a
blocking input. A known unsatisfied execution prerequisite, including an
unfinished blocking slice, is also a Blocking Input: the supported plan may be
drafted, but it and its packet cannot be `Ready`. If discovery would materially
rewrite later steps, make it a blocking input instead. When Story Card and Repo
Context conflict, stop at the earliest affected upstream stage rather than
silently reinterpreting either.

For validation, start from the documented observable seam that can detect the
criterion's failure. Reuse an existing test when it protects the same contract;
add lower-level checks only for meaningful uncovered branches or diagnostics.
Introduce a new seam only with an evidence-backed need and an explicit file
disposition. Do not substitute mocked internals for a required integration
contract or repeat checks that cannot add relevant evidence.

## Final Quality Gate

Before returning the artifact, verify:

- every read, change, and validation path maps to Repo Context `Existing
  Evidence`, and every create path maps to a convention-backed `Proposed Paths`
  entry;
- every planning-critical external claim maps to a current, applicable
  primary-source Repo Context `External Evidence` entry;
- every symbol, command, and proposed-file convention has upstream evidence;
- step IDs and titles are stable and unique, direct blockers form an acyclic
graph with a truthful starting frontier, and steps are coherent outcomes with
  observable checkpoints, not
  placeholders such as `refactor`, `handle edge cases`, `add tests`, or
  `polish`;
- every acceptance criterion maps to the smallest sufficient set of stable
  observable seams, with lower or new seams justified;
- enabling outcomes and wide-refactor sequencing have the required evidence,
  blocker edges, and independent or final integration validation;
- `Ready` has no blocking input, and risks have mitigations or contingencies;
- delivery and recovery match the affected surface instead of automatic
  migration, flag, backfill, or rollback boilerplate; and
- executor identity did not introduce a fabricated estimate, numeric limit, or
  weaker completeness, safety, validation, or recovery policy.

## Composition Boundaries

- `story-clarifier` owns the Story Card, `story-repo-scout` owns Repo Context,
  and this skill is the source of truth for the Implementation Plan schema and
  stage-specific readiness evidence.
- `story-to-plan-orchestrator` owns stage selection, invalidation, resumption,
  and preparation-packet assembly. It may validate this artifact but must not
  redefine its contract.
- The named executor consumes a ready plan. Select any language, domain,
  project, testing, or security guidance needed for implementation at handoff;
  this skill does not maintain that downstream inventory.
- A request to edit code is implementation, not planning.

## Examples

- `Create an implementation plan from this Ready Story Card and Repo Context
  for an executor with no network access.` -> use this skill and record the tool
  constraint.
- `Turn this rough ticket into a coding-ready preparation packet.` -> use
  `story-to-plan-orchestrator`.
- `Scour the repo and append relevant file paths.` -> use `story-repo-scout`.
- `Implement this accepted plan.` -> hand off to implementation guidance.
