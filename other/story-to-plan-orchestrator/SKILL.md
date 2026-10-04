---
name: story-to-plan-orchestrator
description: Coordinate multi-stage story-to-plan preparation across story-clarifier, story-repo-scout, and story-implementation-planner. Use for complete implementation-ready handoffs, two or more missing stages, split-slice selection, partial-packet resumption, consistency validation, or stale-stage recovery before coding; use a component skill for one requested artifact and implementation guidance for code changes.
---

# Story-To-Plan Orchestrator

Coordinate the path from product intent to an evidence-backed implementation
plan. Let each component skill own its artifact; this skill owns routing,
invalidation, resumption, and packet assembly.

This is a process overlay and multi-stage entry point. The component skills
remain independently usable.

For a review-only request, assess packet coherence and readiness and return
findings without rebuilding artifacts. Resume or repair stages when requested.
Return artifacts in the conversation unless file output was requested; pipeline
preparation does not authorize product implementation or external publication.

## When To Use

- produce a complete Story Card, Repo Context, and Implementation Plan handoff
- run or repair two or more preparation stages
- select and materialize one slice from a Split Story Set before scouting
- resume or validate a partial packet whose next valid stage is unclear
- reconcile stale or contradictory stage outputs before coding

## Not For

- one requested artifact; use its owning component skill
- direct code implementation after preparation
- broad product strategy, architecture review, test strategy, or security review

## Ownership

| Owner | Artifact | Decisions it owns |
|---|---|---|
| `story-clarifier` | Story Card or Split Story Set | behavior, scope, acceptance, and story readiness |
| `story-repo-scout` | Repo Context | repository evidence, proposed-path basis, and repo-context readiness |
| `story-implementation-planner` | Implementation Plan | executor fit, task shape, validation, and plan readiness |
| this skill | Preparation Packet | packet status, stage routing, invalidation, slice selection, resumption, and coherence |

Treat each component's artifact schema and stage-specific readiness evidence as
authoritative. The shared three-field protocol below is the family-level rule.
Do not copy a component's full schema, anti-pattern list, or executor rules into
this skill.

## Shared Stage Protocol

This section is the normative story-family definition of the three-field
protocol. Component skills restate it so they remain independently usable, but
own only the stage-specific evidence needed to justify readiness.

Every stage artifact and Preparation Packet declares `Artifact Type`, one
status, and `Reason` (`None` when ready; a concise cause otherwise):

- `Ready`: the next stage can proceed without material guessing.
- `Needs Input`: a named answer, evidence-gathering action, or rescope can make
  the artifact ready.
- `Blocked`: required external authority, dependency, or evidence is
  unavailable; stop the dependent pipeline.

Keep artifact shape separate from status. A Split Story Set can be `Ready` even
though one slice still needs to be selected for downstream work.

Derive Preparation Packet status from the earliest required stage that cannot
proceed:

- `Ready` only when the active Story Card, Repo Context, and Implementation
  Plan are ready, current, and mutually coherent;
- `Needs Input` when that stage is `Needs Input` and no earlier dependency is
  blocked;
- `Blocked` when that stage is `Blocked`.

Do not translate a component's `Needs Input` into packet-level `Blocked`.

## Route By Desired Output

Route from what the user asked to receive, not merely from whichever inputs are
missing:

- story artifact only -> `story-clarifier`
- repository evidence only -> `story-repo-scout`
- implementation plan only, with a ready active Story Card and sufficient Repo
  Context -> `story-implementation-planner`
- complete handoff, two or more stages, packet validation, or uncertain
  resumption -> this skill

If a single-stage request lacks prerequisites, let that component return
`Needs Input` and name the upstream owner. Do not silently broaden the request
into a complete pipeline.

## Pipeline

1. **Inspect.** Identify the desired output, available artifacts, source or
   revision, status, evidence basis, and possible staleness. Read complete
   authorized referenced inputs and material linked decisions when accessible;
   otherwise preserve the access gap instead of reconstructing missing context.
2. **Clarify.** Run `story-clarifier` when no ready story artifact exists.
3. **Select.** For a ready Split Story Set, select the first ready slice in the
   current unblocked dependency frontier by default unless the user names
   another slice. Derive that frontier from declared blockers plus current
   completion or prerequisite evidence; never infer satisfaction from artifact
   readiness. A named blocked slice retains its prerequisites and cannot yield
   a `Ready` plan or packet until they are satisfied. Scout and draft the
   supported portions of its non-ready plan only when the user explicitly wants
   future-slice preparation. Keep exactly one active slice per Preparation
   Packet. If the user requests several slices, produce separate packets in
   dependency order rather than merging their evidence and plans.
4. **Materialize.** Preserve every selected Story Card field, its order, and
   slice-specific content. Resolve `inherited from parent Split Story Set` to
   the parent's exact concrete source list, then merge only applicable shared
   constraints, dependencies, assumptions, open questions, Out of Scope, and
   Validation Notes without overwriting slice-specific content. Map blocking
   slices and external prerequisites into its Dependencies. Keep original slice
   order, dependency edges, shared Out of Scope, Deferred Work, and unselected
   cards with the deferred packet content.
5. **Scout.** Run `story-repo-scout` against the active Story Card when Repo
   Context is missing, insufficient, or stale. When a bounded external fact is
   planning-critical, network access is authorized, and the host supports safe
   parallel work, gather its owning primary source concurrently with independent
   repository scouting. Merge only cited claim-level evidence into Repo Context;
   concurrency does not create another stage or artifact owner.
6. **Plan.** Run `story-implementation-planner` when the Story Card and Repo
   Context are ready and the plan is missing or stale.
7. **Review.** Apply the semantic quality gate below.
8. **Handoff.** Return the packet and stop before implementation.

Skip a stage only when its artifact is both `Ready` and not invalidated by a
newer upstream fact. Preserve incomplete artifacts as evidence, not as approved
downstream inputs.

## Invalidation And Resumption

Use the smallest safe invalidation:

| Change | Outputs to revalidate or rebuild |
|---|---|
| wording-only story edit with unchanged behavior | Story Card; check downstream coherence without automatically rerunning stages |
| behavior, acceptance, scope, assumptions, material constraints or dependencies, the answer to a material open question, or selected slice changed | Story Card, Repo Context, and Implementation Plan |
| validation notes changed without changing behavior | Story Card and Implementation Plan; also Repo Context when the validation surface, command, path, or convention changed |
| relevant repo paths, instructions, conventions, or evidence changed | Repo Context and Implementation Plan |
| material external source, applicable version, or contract changed | Repo Context and Implementation Plan; also Story Card when intended behavior or acceptance changed |
| target executor or executor constraints changed | Implementation Plan |
| plan formatting changed without semantic change | Implementation Plan only |

When available, preserve the story source or revision, the scout's scope and
search record, and target-executor constraints in the packet. Never invent
provenance. Treat unknown freshness as a risk only when the affected evidence
could change the plan.

When a downstream stage contradicts an upstream artifact:

1. return to the earliest owner that can resolve the contradiction;
2. mark dependent outputs stale;
3. preserve still-useful evidence, clearly labeled as unvalidated;
4. stop with the exact pending-stage status when another pass would repeat the
   same unresolved condition without new evidence.

Preserve settled facts and decisions during resumption. Reopen one only when
its source, prerequisite, authority, applicable version, or governing scope
changed, then recompute and invalidate only its dependents.

## Question Handling

- Route `[Fact]` gaps to the stage or authorized primary source that can resolve
  them. Ask the user only when they are the source, authority, or access owner.
- Keep `[Decision]` gaps with the authorized decision owner. An evidence-backed
  recommendation is not a resolution unless decision authority was explicitly
  delegated.
- Ask at most three high-impact questions from the current frontier whose
  prerequisites are settled. Never ask a dependent question in the same batch
  as its prerequisite; recompute after each answer or evidence result.
- Keep material `[Not yet specifiable]` areas in scope and non-ready until their
  prerequisites expose a sharp question. Do not fabricate downstream stories
  or plan steps from them.
- Use labeled assumptions only when they do not materially change behavior,
  scope, acceptance, authoritative boundaries, or validation feasibility.
- Never promote `Needs Input` or `Blocked` to `Ready` merely to finish a packet.

## Semantic Quality Gate

Reject or repair the packet when any of these is true:

- any embedded component artifact fails its owning skill's current readiness
  and quality gate;
- packet status does not follow the shared protocol, or active-slice blockers
  and their satisfaction evidence do not support that status;
- a planned existing or proposed path cannot be traced to its required Repo
  Context evidence, or a Story Card acceptance criterion is absent from the
  plan;
- a planning-critical external claim lacks either a current, applicable
  `EXT-*` primary-evidence row in Repo Context or the matching `EXT-*` ID under
  the plan's Inputs;
- a downstream artifact is older than a material upstream change;
- story language, dependency state, and repository evidence conflict without
  explicit resolution.

Surface non-blocking risks without inventing numeric step or file limits. The
three-question batch ceiling above is a coordination rule, not a complexity
metric. Complexity is a reason to split only when the work contains independent
goals, exceeds the executor's real constraints, or lacks a safe checkpoint.

## Final Output

Use this shape for a complete packet:

```markdown
Artifact Type: Preparation Packet
Status: Ready
Reason: None

## Slice Selection
- Active slice: <slice ID and title, when selected from a split set>
- Declared blockers: <blocking slices and external prerequisites, or None>
- Satisfaction evidence: <source for every satisfied blocker, or None required>

## Story Card
The ready active story.

## Deferred Stories
Original slice order, dependency graph, shared Out of Scope, Deferred Work, and
unselected Story Cards when a Split Story Set was materialized.

## Repo Context
Evidence-backed current context.

## Implementation Plan
The ready executor-aware plan.
```

Omit `Slice Selection` and `Deferred Stories` only when the source was not a
Split Story Set. A packet for a user-named slice with an unsatisfied declared
blocker uses `Status: Blocked`; its plan preserves supported preparation but
lists the blocker rather than claiming immediate executability.

When embedding a component artifact, preserve its field names, section order,
and content while shifting internal Markdown heading levels only as needed to
keep the packet hierarchy legible. Heading-level shifts do not change the
component schema.

If work stops early, return completed artifacts plus:

```markdown
Artifact Type: Preparation Packet
Status: <Needs Input | Blocked>
Reason: <the earliest pending stage and concise cause>

## Pending Stage
- Owner: <component skill>
- Artifact Type: <pending artifact>
- Status: <the component's exact Needs Input or Blocked status>
- Reason: <the component's reason>
- Smallest Next Action: <answer, evidence-gathering action, rescope, or external authority>
```

Do not implement code or automatically invoke downstream implementation skills.
Name the handoff target only when it helps the user continue.

## Resources

Read [references/story-to-plan-packet-example.md](references/story-to-plan-packet-example.md)
when a concrete packet shape would resolve ambiguity.

## Examples

- `Clarify this rough ticket, find the relevant files, and make an implementation plan.`
  -> run all missing stages.
- `This packet may be stale; validate it and resume from the earliest invalid stage.`
  -> inspect provenance and apply the invalidation table.
- `I have a ready active Story Card and Repo Context; make the implementation
  plan.` -> use `story-implementation-planner`, not this skill.
- `Implement this plan.` -> use implementation guidance, not this skill.
