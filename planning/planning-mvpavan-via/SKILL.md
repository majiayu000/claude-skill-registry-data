---
name: planning
description: Use when settled work needs a durable implementation plan, dependency graph, or workstream decomposition. Skip planning ceremonies for clear bounded tasks.
---

# Planning

Turn settled scope into executable work at the smallest useful scale.

## Route

| Situation | Path |
|---|---|
| Material behavior unresolved | Brainstorming for those decisions |
| Clear bounded task | Brief local sequence if useful; continue execution without a plan document |
| Durable implementation plan requested or needed for handoff | Elaborate |
| Approved spec needs phase/stage decomposition | Decompose |
| Standard phase with sufficient roadmap acceptance | Execute from its roadmap row |

Reuse recorded approvals. Ask only about material scope, dependency or authority
choices that remain open. Planning-only requests authorize planning artifacts,
not implementation; when implementation is already authorized, continue to it.

## Decompose

Read the governing spec and only relevant project constraints and current Beads
state. Confirm approval evidence; if missing, record the settled decision in the
spec rather than treating a draft as approved.

Use `references/decompose.md` for layout, join keys and seeding commands. Reuse an
obvious named workstream; ask when the choice is consequential or unclear. Split
into demoable phases with checkable exits, flat stages with acceptance, and real
dependency edges. Independent subsystems need separate ownership, not necessarily
separate specs or an additional interview.

Present consequential structural choices for approval if not already authorized.
Then seed epics/stages and render tracking. A single-phase spec may use one epic
and an Elaborate plan without creating a workstream. Write later phase plans
just in time against the code those phases will encounter.

## Elaborate

Use `references/plan-format.md` for a durable plan. Read the origin, relevant
code and tests, and stage acceptance for phase work. Identify ownership boundaries,
interfaces, verification and dependencies. List known files; permit implementers
to discover internal details within that ownership. Do not invent exact symbols
or freeze a file map without evidence.

Every phase plan task names an existing `Stage: <epic>.N`; every stage has covering
tasks. Preserve this mapping because execution uses it to close stages. Mark
risky changes test-first or characterization-first as appropriate.

Check requirement coverage, compatibility, unresolved decisions and integration
risks. Use independent critique when required by the task or justified by risk,
following `AGENTS.md`; do not require a critic for every plan.

Save phase plans under `docs/workstreams/<name>/plans/`, standalone plans under
`docs/plans/`, or the supplied path. Put `plan: <path>` in Beads notes. An epic's
`--spec-id` holds its spec and `--design` its roadmap, never its plan. Attribute
Beads writes with `--actor` and reuse existing records.

## Slicing

Prefer independently verifiable vertical slices. For broad refactors, use
expand → migrate → contract with genuine dependencies. If intermediate tasks
cannot remain green, name one integration boundary or atomic group explicitly.
A plan is ready when an implementer can identify acceptance, ownership and the
next ready unit; unresolved material decisions remain visible blockers.
